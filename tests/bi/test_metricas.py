"""Camada semantica — o que antes eram 11 SQLs inline nas paginas, sem teste.

O foco aqui e o que o professor pediu: **periodo**. Cada indicador tem que
respeitar a janela, e nao ha como verificar isso com SQL escrito dentro de uma
tela do Streamlit.
"""

from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session

from src.bi import metricas
from src.bi.etl import executar_etl
from src.bi.metricas import Periodo
from tests.bi._helpers import (
    coletar,
    criar_os,
    faturar,
    glosar,
    liberar_laudos,
    montar_cadastros,
    receber_em_caixa,
    titulo_receber,
    utc,
)

JANEIRO = Periodo(date(2026, 1, 1), date(2026, 1, 31), "Janeiro")
FEVEREIRO = Periodo(date(2026, 2, 1), date(2026, 2, 28), "Fevereiro")
PRIMEIRO_TRIMESTRE = Periodo(date(2026, 1, 1), date(2026, 3, 31), "1o trimestre")


def _dois_meses(session: Session):
    """Uma OS em janeiro e duas em fevereiro — base dos testes de periodo."""
    cenario = montar_cadastros(session)

    janeiro = criar_os(session, cenario, aberta_em=utc(2026, 1, 10), valor=Decimal("100.00"))
    coletar(session, cenario, janeiro, coletada_em=utc(2026, 1, 10, 8))
    liberar_laudos(session, janeiro, liberado_em=utc(2026, 1, 11, 8))

    for dia in (5, 6):
        ordem = criar_os(session, cenario, aberta_em=utc(2026, 2, dia), valor=Decimal("100.00"))
        coletar(session, cenario, ordem, coletada_em=utc(2026, 2, dia, 8))
        liberar_laudos(session, ordem, liberado_em=utc(2026, 2, dia + 1, 8))

    return cenario


def test_periodo_filtra_de_verdade(session: Session) -> None:
    """O apontamento do professor: antes todo agregado era 'desde o inicio dos
    tempos' e apenas 2 das 11 consultas tocavam a dimensao de tempo."""
    _dois_meses(session)
    executar_etl()

    janeiro = metricas.exames_por_unidade(session, JANEIRO)
    fevereiro = metricas.exames_por_unidade(session, FEVEREIRO)
    trimestre = metricas.exames_por_unidade(session, PRIMEIRO_TRIMESTRE)

    assert int(janeiro["exames"].sum()) == 1
    assert int(fevereiro["exames"].sum()) == 2
    assert int(trimestre["exames"].sum()) == 3


def test_agrupamentos_por_convenio_rotulam_particular(session: Session) -> None:
    """OS sem convenio precisa aparecer como 'Particular', nao sumir nem virar
    linha sem nome. Exercita as quatro metricas que agrupam por convenio."""
    cenario = montar_cadastros(session)

    com_convenio = criar_os(session, cenario, aberta_em=utc(2026, 1, 5))
    laudos_convenio = liberar_laudos(session, com_convenio, liberado_em=utc(2026, 1, 6))
    faturar(session, cenario, laudos_convenio, fechado_em=utc(2026, 1, 20), valor=Decimal("100.00"))

    particular = criar_os(session, cenario, aberta_em=utc(2026, 1, 7), convenio_id=None)
    laudos_particular = liberar_laudos(session, particular, liberado_em=utc(2026, 1, 8))
    faturar(
        session, cenario, laudos_particular,
        fechado_em=utc(2026, 1, 21), convenio_id=None, valor=Decimal("60.00"),
    )

    executar_etl()

    for consulta in (
        metricas.exames_por_convenio,
        metricas.receita_por_convenio,
        metricas.ticket_medio_por_convenio,
        metricas.taxa_glosa_por_convenio,
    ):
        resultado = consulta(session, JANEIRO)
        assert "Particular" in set(resultado["convenio"]), consulta.__name__
        assert resultado["convenio"].isna().sum() == 0, consulta.__name__


def test_serie_mensal_mostra_mes_vazio_como_zero(session: Session) -> None:
    """Com o calendario denso, mes sem movimento aparece com zero em vez de
    sumir do eixo (bug B8)."""
    cenario = montar_cadastros(session)
    criar_os(session, cenario, aberta_em=utc(2026, 1, 10))
    criar_os(session, cenario, aberta_em=utc(2026, 3, 10))
    executar_etl()

    serie = metricas.exames_por_mes(session, PRIMEIRO_TRIMESTRE)

    assert list(serie["mes"]) == ["2026-01", "2026-02", "2026-03"]
    assert int(serie[serie["mes"] == "2026-02"]["exames"].iloc[0]) == 0


def test_ticket_medio_e_calculado_sobre_os_aditivos(session: Session) -> None:
    """ADR 0009: guardar a razao no fato impede reagregacao.

    Dois itens de R$ 100 e um de R$ 40 dao ticket de R$ 80 — nao a media dos
    tickets de cada linha.
    """
    cenario = montar_cadastros(session)
    ordem = criar_os(
        session,
        cenario,
        aberta_em=utc(2026, 1, 5),
        procedimentos=[cenario.procedimento_bioquimica, cenario.procedimento_hematologia],
    )
    laudos = liberar_laudos(session, ordem, liberado_em=utc(2026, 1, 6))
    faturar(session, cenario, laudos, fechado_em=utc(2026, 1, 20), valor=Decimal("100.00"))

    outra = criar_os(session, cenario, aberta_em=utc(2026, 1, 7))
    laudos_outra = liberar_laudos(session, outra, liberado_em=utc(2026, 1, 8))
    faturar(session, cenario, laudos_outra, fechado_em=utc(2026, 1, 21), valor=Decimal("40.00"))

    executar_etl()

    resultado = metricas.ticket_medio_por_convenio(session, JANEIRO)

    assert len(resultado) == 1
    assert float(resultado["faturado"].iloc[0]) == 240.0
    assert int(resultado["exames"].iloc[0]) == 3
    assert float(resultado["ticket_medio"].iloc[0]) == 80.0


def test_kpis_separam_faturado_de_recebido(session: Session) -> None:
    cenario = montar_cadastros(session)
    ordem = criar_os(session, cenario, aberta_em=utc(2026, 1, 5))
    laudos = liberar_laudos(session, ordem, liberado_em=utc(2026, 1, 6))
    lote = faturar(session, cenario, laudos, fechado_em=utc(2026, 1, 20), valor=Decimal("200.00"))
    glosar(session, cenario, lote, valor=Decimal("50.00"), motivo="Sem senha", criado_em=utc(2026, 1, 25))
    titulo = titulo_receber(session, lote, valor=Decimal("200.00"), vencimento=date(2026, 1, 28))
    receber_em_caixa(session, titulo, valor=Decimal("150.00"), ocorrido_em=utc(2026, 1, 30))

    executar_etl()

    indicadores = metricas.kpis(session, JANEIRO)

    assert indicadores["faturado"] == 200.0
    assert indicadores["glosado"] == 50.0
    assert indicadores["liberado"] == 150.0
    assert indicadores["recebido"] == 150.0
    assert indicadores["taxa_glosa"] == 25.0


def test_fluxo_de_caixa_usa_o_realizado(session: Session) -> None:
    """B2: o painel rotulado "Fluxo de Caixa" plotava cronograma de vencimentos
    e contava titulo nao pago como receita."""
    cenario = montar_cadastros(session)
    ordem = criar_os(session, cenario, aberta_em=utc(2026, 1, 5))
    laudos = liberar_laudos(session, ordem, liberado_em=utc(2026, 1, 6))
    lote = faturar(session, cenario, laudos, fechado_em=utc(2026, 1, 20))

    pago = titulo_receber(session, lote, valor=Decimal("300.00"), vencimento=date(2026, 1, 25))
    receber_em_caixa(session, pago, valor=Decimal("300.00"), ocorrido_em=utc(2026, 2, 3))
    # Este nunca foi pago: nao pode aparecer no fluxo de caixa.
    titulo_receber(session, lote, valor=Decimal("999.00"), vencimento=date(2026, 2, 10))

    executar_etl()

    caixa = metricas.fluxo_caixa_mensal(session, PRIMEIRO_TRIMESTRE)
    fevereiro = caixa[caixa["mes"] == "2026-02"].iloc[0]

    assert float(fevereiro["entradas"]) == 300.0
    assert float(caixa["entradas"].sum()) == 300.0


def test_previsto_x_realizado_sao_series_distintas(session: Session) -> None:
    cenario = montar_cadastros(session)
    ordem = criar_os(session, cenario, aberta_em=utc(2026, 1, 5))
    laudos = liberar_laudos(session, ordem, liberado_em=utc(2026, 1, 6))
    lote = faturar(session, cenario, laudos, fechado_em=utc(2026, 1, 20))
    titulo = titulo_receber(session, lote, valor=Decimal("500.00"), vencimento=date(2026, 1, 28))
    receber_em_caixa(session, titulo, valor=Decimal("400.00"), ocorrido_em=utc(2026, 1, 30))

    executar_etl()

    resultado = metricas.previsto_x_realizado(session, JANEIRO)
    janeiro = resultado[resultado["mes"] == "2026-01"].iloc[0]

    assert float(janeiro["previsto"]) == 500.0
    assert float(janeiro["realizado"]) == 400.0


def test_curva_abc_classifica_pelo_acumulado_de_abertura(session: Session) -> None:
    """A classe sai do acumulado ANTES do item.

    Com 90/10, o primeiro procedimento abre em 0% (classe A) e o segundo abre em
    90% (classe B). Classificar pelo acumulado de FECHAMENTO daria classe B ao
    procedimento que sozinho e 90% da receita — o mais classe A da lista.
    """
    cenario = montar_cadastros(session)
    caro = criar_os(session, cenario, aberta_em=utc(2026, 1, 5))
    laudos_caro = liberar_laudos(session, caro, liberado_em=utc(2026, 1, 6))
    faturar(session, cenario, laudos_caro, fechado_em=utc(2026, 1, 20), valor=Decimal("900.00"))

    barato = criar_os(
        session, cenario, aberta_em=utc(2026, 1, 7),
        procedimentos=[cenario.procedimento_hematologia],
    )
    laudos_barato = liberar_laudos(session, barato, liberado_em=utc(2026, 1, 8))
    faturar(session, cenario, laudos_barato, fechado_em=utc(2026, 1, 21), valor=Decimal("100.00"))

    executar_etl()

    abc = metricas.curva_abc_procedimentos(session, JANEIRO)

    assert list(abc["classe"].astype(str)) == ["A", "B"]
    assert float(abc["participacao"].iloc[0]) == 90.0
    assert float(abc["acumulado"].iloc[-1]) == 100.0


def test_glosa_por_motivo_agrupa_normalizado(session: Session) -> None:
    cenario = montar_cadastros(session)
    ordem = criar_os(session, cenario, aberta_em=utc(2026, 1, 5))
    laudos = liberar_laudos(session, ordem, liberado_em=utc(2026, 1, 6))
    lote = faturar(session, cenario, laudos, fechado_em=utc(2026, 1, 20), valor=Decimal("100.00"))
    glosar(session, cenario, lote, valor=Decimal("30.00"), motivo="Sem senha", criado_em=utc(2026, 1, 25))
    glosar(session, cenario, lote, valor=Decimal("20.00"), motivo="SEM SENHA", criado_em=utc(2026, 1, 26))

    executar_etl()

    resultado = metricas.glosa_por_motivo(session, JANEIRO)

    assert len(resultado) == 1
    assert float(resultado["glosado"].iloc[0]) == 50.0
    assert int(resultado["ocorrencias"].iloc[0]) == 2


def test_dre_fecha_com_entradas_menos_saidas(session: Session) -> None:
    cenario = montar_cadastros(session)
    ordem = criar_os(session, cenario, aberta_em=utc(2026, 1, 5))
    laudos = liberar_laudos(session, ordem, liberado_em=utc(2026, 1, 6))
    lote = faturar(session, cenario, laudos, fechado_em=utc(2026, 1, 20))
    titulo = titulo_receber(session, lote, valor=Decimal("500.00"), vencimento=date(2026, 1, 28))
    receber_em_caixa(session, titulo, valor=Decimal("500.00"), ocorrido_em=utc(2026, 1, 30))

    executar_etl()

    dre = metricas.dre_simplificado(session, JANEIRO)
    resultado = dre[dre["linha"] == "Resultado"]["valor"].iloc[0]

    assert float(dre[dre["linha"] == "Receita recebida"]["valor"].iloc[0]) == 500.0
    assert float(resultado) == 500.0


def test_aging_separa_a_vencer_de_atrasado(session: Session) -> None:
    """Faixas de atraso da carteira, com o titulo liquidado fora da conta."""
    cenario = montar_cadastros(session)
    ordem = criar_os(session, cenario, aberta_em=utc(2026, 1, 5))
    laudos = liberar_laudos(session, ordem, liberado_em=utc(2026, 1, 6))
    lote = faturar(session, cenario, laudos, fechado_em=utc(2026, 1, 20))

    referencia = date(2026, 3, 1)
    titulo_receber(session, lote, valor=Decimal("100.00"), vencimento=date(2026, 3, 20))  # a vencer
    titulo_receber(session, lote, valor=Decimal("200.00"), vencimento=date(2026, 2, 20))  # 1-30
    titulo_receber(session, lote, valor=Decimal("300.00"), vencimento=date(2026, 1, 10))  # 31-60
    # Liquidado: sai da carteira em aberto.
    pago = titulo_receber(session, lote, valor=Decimal("900.00"), vencimento=date(2026, 2, 1))
    receber_em_caixa(session, pago, valor=Decimal("900.00"), ocorrido_em=utc(2026, 2, 2))

    executar_etl()

    aging = metricas.aging_carteira(session, referencia)
    por_faixa = dict(zip(aging["faixa"], aging["valor"].astype(float)))

    assert por_faixa["A vencer"] == 100.0
    assert por_faixa["1-30 dias"] == 200.0
    assert por_faixa["31-60 dias"] == 300.0
    assert float(aging["valor"].sum()) == 600.0  # o liquidado nao entra


def test_periodo_anterior_tem_o_mesmo_tamanho(session: Session) -> None:
    """Base do delta percentual mostrado nos KPIs."""
    anterior = JANEIRO.anterior()

    assert anterior.fim == date(2025, 12, 31)
    assert anterior.dias == JANEIRO.dias


def test_status_das_amostras_vem_do_fato(session: Session) -> None:
    """A pagina de logistica consultava a tabela operacional `amostras` direto,
    furando o modelo dimensional (regra #35 da revisao)."""
    cenario = montar_cadastros(session)
    ordem = criar_os(session, cenario, aberta_em=utc(2026, 1, 10))
    coletar(session, cenario, ordem, coletada_em=utc(2026, 1, 10, 8))

    executar_etl()

    status = metricas.status_das_amostras(session, JANEIRO)

    assert int(status["quantidade"].sum()) == 1
    assert status["status"].iloc[0] == "COLETADA"
