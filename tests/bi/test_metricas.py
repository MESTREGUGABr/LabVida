"""Camada semantica — o que antes eram 11 SQLs inline nas paginas, sem teste.

O foco aqui e o que o professor pediu: **periodo**. Cada indicador tem que
respeitar a janela, e nao ha como verificar isso com SQL escrito dentro de uma
tela do Streamlit.
"""

from datetime import date
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.atendimento.ordem_servico.models import OsItem
from src.bi import metricas
from src.bi.etl import executar_etl
from src.bi.metricas import FiltroDimensoes, Periodo
from src.bi.models import DimConvenio, DimProcedimento, DimUnidade
from src.financeiro.movimento_caixa.models import MovimentoCaixa
from src.financeiro.titulo_pagar.models import TituloPagar
from tests.bi._helpers import (
    coletar,
    criar_os,
    faturar,
    glosar,
    liberar_laudos,
    montar_cadastros,
    receber_em_caixa,
    titulo_receber,
    transportar,
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


def test_taxa_cancelamento_itens(session: Session) -> None:
    cenario = montar_cadastros(session)
    ordem = criar_os(
        session, cenario, aberta_em=utc(2026, 1, 10),
        procedimentos=[cenario.procedimento_bioquimica, cenario.procedimento_hematologia],
    )
    itens = session.scalars(select(OsItem).where(OsItem.ordem_servico_id == ordem.id)).all()
    itens[0].status = "CANCELADO"
    session.commit()

    executar_etl()

    assert metricas.taxa_cancelamento_itens(session, JANEIRO) == 50.0


def test_taxa_cancelamento_itens_sem_dados_e_zero(session: Session) -> None:
    assert metricas.taxa_cancelamento_itens(session, JANEIRO) == 0.0


def test_tempo_coleta_recebimento_medio(session: Session) -> None:
    cenario = montar_cadastros(session)
    ordem = criar_os(session, cenario, aberta_em=utc(2026, 1, 10))
    amostra = coletar(session, cenario, ordem, coletada_em=utc(2026, 1, 10, 8))
    transportar(
        session, cenario, amostra,
        despachado_em=utc(2026, 1, 10, 12), recebido_em=utc(2026, 1, 10, 20),
    )

    executar_etl()

    assert metricas.tempo_coleta_recebimento_medio(session, JANEIRO) == 12.0


def test_tempo_coleta_recebimento_medio_sem_dados_e_zero(session: Session) -> None:
    assert metricas.tempo_coleta_recebimento_medio(session, JANEIRO) == 0.0


def _sk_unidade(session: Session, unidade_id) -> int:
    return session.scalar(select(DimUnidade.sk_unidade).where(DimUnidade.id_origem == unidade_id))


def _sk_convenio(session: Session, convenio_id) -> int:
    return session.scalar(select(DimConvenio.sk_convenio).where(DimConvenio.id_origem == convenio_id))


def test_filtro_por_unidade_restringe_kpis_e_grafico(session: Session) -> None:
    cenario = montar_cadastros(session)
    ordem_a = criar_os(session, cenario, aberta_em=utc(2026, 1, 10))
    coletar(session, cenario, ordem_a, coletada_em=utc(2026, 1, 10, 8))

    ordem_b = criar_os(session, cenario, aberta_em=utc(2026, 1, 12))
    ordem_b.unidade_id = cenario.unidade_central
    session.commit()
    coletar(session, cenario, ordem_b, coletada_em=utc(2026, 1, 12, 8))

    executar_etl()

    sk_a = _sk_unidade(session, cenario.unidade_coleta)
    filtro = FiltroDimensoes(unidades=[sk_a])

    assert metricas.kpis(session, JANEIRO)["exames"] == 2
    assert metricas.kpis(session, JANEIRO, filtro)["exames"] == 1

    por_unidade = metricas.exames_por_unidade(session, JANEIRO, filtro)
    assert len(por_unidade) == 1
    assert por_unidade.iloc[0]["exames"] == 1


def test_filtro_convenio_particular_e_or_nao_exclusao(session: Session) -> None:
    cenario = montar_cadastros(session)
    ordem_convenio = criar_os(session, cenario, aberta_em=utc(2026, 1, 10))
    coletar(session, cenario, ordem_convenio, coletada_em=utc(2026, 1, 10, 8))

    ordem_particular = criar_os(session, cenario, aberta_em=utc(2026, 1, 12), convenio_id=None)
    coletar(session, cenario, ordem_particular, coletada_em=utc(2026, 1, 12, 8))

    executar_etl()

    sk_convenio = _sk_convenio(session, cenario.convenio)

    so_convenio = FiltroDimensoes(convenios=[sk_convenio], incluir_particular=False)
    assert metricas.kpis(session, JANEIRO, so_convenio)["exames"] == 1

    convenio_e_particular = FiltroDimensoes(convenios=[sk_convenio], incluir_particular=True)
    assert metricas.kpis(session, JANEIRO, convenio_e_particular)["exames"] == 2


def test_filtro_nao_quebra_calendario_denso(session: Session) -> None:
    """Regressao: um WHERE direto sobre o lado do LEFT JOIN faria o mes sem
    dado QUE CASA com o filtro desaparecer da serie, em vez de aparecer com
    zero — quebrando o "mes sem movimento entra com zero" quando ha filtro
    de dimensao ativo."""
    cenario = montar_cadastros(session)
    ordem_a = criar_os(session, cenario, aberta_em=utc(2026, 1, 10))
    coletar(session, cenario, ordem_a, coletada_em=utc(2026, 1, 10, 8))

    ordem_b = criar_os(session, cenario, aberta_em=utc(2026, 2, 10))
    ordem_b.unidade_id = cenario.unidade_central
    session.commit()
    coletar(session, cenario, ordem_b, coletada_em=utc(2026, 2, 10, 8))

    executar_etl()

    sk_a = _sk_unidade(session, cenario.unidade_coleta)
    trimestre = Periodo(date(2026, 1, 1), date(2026, 3, 31), "1o trimestre")
    df = metricas.exames_por_mes(session, trimestre, FiltroDimensoes(unidades=[sk_a]))

    meses = dict(zip(df["mes"], df["exames"]))
    assert meses.get("2026-01") == 1
    # Fevereiro tem exame, mas so de outra unidade (filtrada) — tem que
    # continuar aparecendo com zero, nao desaparecer da serie.
    assert meses.get("2026-02") == 0
    assert meses.get("2026-03") == 0


def test_filtro_procedimento_nao_afeta_tat_nem_cancelamento(session: Session) -> None:
    """Limitacao documentada: `FatoOrdemServico` nao tem `sk_procedimento` —
    o filtro de Exame nao pode restringir TAT/Taxa de cancelamento
    (indicadores do grao da OS, nao do exame)."""
    cenario = montar_cadastros(session)
    ordem = criar_os(
        session, cenario, aberta_em=utc(2026, 1, 10),
        procedimentos=[cenario.procedimento_bioquimica, cenario.procedimento_hematologia],
    )
    itens = session.scalars(select(OsItem).where(OsItem.ordem_servico_id == ordem.id)).all()
    itens[0].status = "CANCELADO"
    session.commit()

    executar_etl()

    sk_procedimento = session.scalar(
        select(DimProcedimento.sk_procedimento).where(
            DimProcedimento.id_origem == cenario.procedimento_bioquimica
        )
    )
    filtro = FiltroDimensoes(procedimentos=[sk_procedimento])

    sem_filtro = metricas.taxa_cancelamento_itens(session, JANEIRO)
    com_filtro = metricas.taxa_cancelamento_itens(session, JANEIRO, filtro)
    assert sem_filtro == com_filtro == 50.0


def test_filtro_procedimento_nao_afeta_recebido_caixa(session: Session) -> None:
    """Limitacao documentada: `FatoFinanceiro` nao tem `sk_procedimento` —
    o filtro de Exame nao pode restringir 'Recebido (caixa)' nem o fluxo de
    caixa (regime de caixa nao carrega essa dimensao)."""
    cenario = montar_cadastros(session)
    ordem = criar_os(session, cenario, aberta_em=utc(2026, 1, 10), valor=Decimal("100.00"))
    coletar(session, cenario, ordem, coletada_em=utc(2026, 1, 10, 8))
    laudos = liberar_laudos(session, ordem, liberado_em=utc(2026, 1, 11))
    lote = faturar(session, cenario, laudos, fechado_em=utc(2026, 1, 12), valor=Decimal("100.00"))
    titulo = titulo_receber(session, lote, valor=Decimal("100.00"), vencimento=date(2026, 2, 11))
    receber_em_caixa(session, titulo, valor=Decimal("100.00"), ocorrido_em=utc(2026, 1, 15))

    executar_etl()

    sk_procedimento = session.scalar(
        select(DimProcedimento.sk_procedimento).where(
            DimProcedimento.id_origem == cenario.procedimento_bioquimica
        )
    )
    filtro = FiltroDimensoes(procedimentos=[sk_procedimento])

    sem_filtro = metricas.kpis(session, JANEIRO)["recebido"]
    com_filtro = metricas.kpis(session, JANEIRO, filtro)["recebido"]
    assert sem_filtro == com_filtro == 100.0


def test_filtro_unidade_de_coleta_zera_recebido_caixa(session: Session) -> None:
    """`FatoFinanceiro.sk_unidade` aponta pra unidade CENTRAL (caixa
    consolidado do laboratorio) — nao pra unidade de coleta da OS que gerou o
    faturamento, ja que um lote pode reunir OSs de varias unidades. Filtrar
    por uma unidade de COLETA tem que zerar 'Recebido (caixa)'/'Resultado
    (DRE)' (o valor pertence ao consolidado, nao aquela unidade); filtrar
    pela unidade CENTRAL devolve o valor cheio."""
    cenario = montar_cadastros(session)
    ordem = criar_os(session, cenario, aberta_em=utc(2026, 1, 10), valor=Decimal("100.00"))
    coletar(session, cenario, ordem, coletada_em=utc(2026, 1, 10, 8))
    laudos = liberar_laudos(session, ordem, liberado_em=utc(2026, 1, 11))
    lote = faturar(session, cenario, laudos, fechado_em=utc(2026, 1, 12), valor=Decimal("100.00"))
    titulo = titulo_receber(session, lote, valor=Decimal("100.00"), vencimento=date(2026, 2, 11))
    receber_em_caixa(session, titulo, valor=Decimal("100.00"), ocorrido_em=utc(2026, 1, 15))

    executar_etl()

    sk_coleta = _sk_unidade(session, cenario.unidade_coleta)
    sk_central = _sk_unidade(session, cenario.unidade_central)

    assert metricas.kpis(session, JANEIRO)["recebido"] == 100.0
    assert metricas.kpis(session, JANEIRO, FiltroDimensoes(unidades=[sk_coleta]))["recebido"] == 0.0
    assert metricas.kpis(session, JANEIRO, FiltroDimensoes(unidades=[sk_central]))["recebido"] == 100.0

    dre_coleta = metricas.dre_simplificado(session, JANEIRO, FiltroDimensoes(unidades=[sk_coleta]))
    assert float(dre_coleta[dre_coleta["linha"] == "Receita recebida"]["valor"].iloc[0]) == 0.0


def test_filtro_particular_nao_infla_despesas_como_receita(session: Session) -> None:
    """Despesa (`TituloPagar`/`MovimentoCaixa` SAIDA) nunca tem convenio — o
    ETL grava `sk_convenio=None` pra toda saida, sempre, porque aluguel/
    fornecedor nao tem essa dimensao. Selecionar "Particular" no filtro de
    Convenio (que vira `sk_convenio IS NULL`) casava com TODA despesa, fazendo
    o DRE mostrar um resultado bem negativo mesmo sem nenhum paciente
    particular real na base — bug de regra de negocio, nao falta de dado."""
    cenario = montar_cadastros(session)
    ordem = criar_os(session, cenario, aberta_em=utc(2026, 1, 5))
    laudos = liberar_laudos(session, ordem, liberado_em=utc(2026, 1, 6))
    lote = faturar(session, cenario, laudos, fechado_em=utc(2026, 1, 20), valor=Decimal("100.00"))
    titulo = titulo_receber(session, lote, valor=Decimal("100.00"), vencimento=date(2026, 1, 28))
    receber_em_caixa(session, titulo, valor=Decimal("100.00"), ocorrido_em=utc(2026, 1, 15))

    pagar = TituloPagar(valor=Decimal("500.00"), vencimento=date(2026, 1, 10), status="PAGO")
    session.add(pagar)
    session.flush()
    session.add(
        MovimentoCaixa(
            titulo_pagar_id=pagar.id, tipo="SAIDA",
            valor=Decimal("500.00"), ocorrido_em=utc(2026, 1, 12),
        )
    )
    session.commit()

    executar_etl()

    particular = FiltroDimensoes(incluir_particular=True)
    dre = metricas.dre_simplificado(session, JANEIRO, particular)

    assert float(dre[dre["linha"] == "Receita recebida"]["valor"].iloc[0]) == 0.0
    assert float(dre[dre["linha"] == "Despesas pagas"]["valor"].iloc[0]) == -500.0

    caixa = metricas.fluxo_caixa_mensal(session, JANEIRO, particular)
    assert float(caixa[caixa["mes"] == "2026-01"]["saidas"].iloc[0]) == 500.0
    assert float(caixa[caixa["mes"] == "2026-01"]["entradas"].iloc[0]) == 0.0
