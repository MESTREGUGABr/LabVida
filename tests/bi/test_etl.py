"""Cobertura da carga de fatos — que antes nao tinha um unico teste.

Cada teste marcado com o codigo do bug (B1..B8, G1, G2) guarda uma regressao
catalogada em `docs/plano-bi.md` secao 1.
"""

from datetime import date
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.bi.etl import executar_etl, ultima_execucao
from src.bi.models import (
    DimFaixaEtaria,
    DimMotivoGlosa,
    DimPacienteAnon,
    DimProcedimento,
    DimSetor,
    DimTempo,
    DimUnidade,
    FatoAtendimento,
    FatoFaturamento,
    FatoFinanceiro,
    FatoGlosa,
    FatoLogistica,
    FatoOrdemServico,
)
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

_FATOS = (
    FatoOrdemServico,
    FatoAtendimento,
    FatoFaturamento,
    FatoFinanceiro,
    FatoLogistica,
    FatoGlosa,
)


def _cenario_completo(session: Session):
    """OS coletada em janeiro, faturada em fevereiro, glosada e recebida em marco."""
    cenario = montar_cadastros(session)

    ordem = criar_os(
        session,
        cenario,
        aberta_em=utc(2026, 1, 12),
        procedimentos=[cenario.procedimento_bioquimica, cenario.procedimento_hematologia],
        valor=Decimal("50.00"),
    )
    amostra = coletar(session, cenario, ordem, coletada_em=utc(2026, 1, 12, 9))
    transportar(
        session,
        cenario,
        amostra,
        despachado_em=utc(2026, 1, 12, 14),
        recebido_em=utc(2026, 1, 12, 17, 30),
    )
    laudos = liberar_laudos(session, ordem, liberado_em=utc(2026, 1, 13, 9))
    lote = faturar(session, cenario, laudos, fechado_em=utc(2026, 2, 5), valor=Decimal("50.00"))
    glosar(
        session,
        cenario,
        lote,
        valor=Decimal("20.00"),
        motivo="Falta de autorizacao",
        criado_em=utc(2026, 2, 20),
    )
    titulo = titulo_receber(session, lote, valor=Decimal("100.00"), vencimento=date(2026, 3, 7))
    receber_em_caixa(session, titulo, valor=Decimal("80.00"), ocorrido_em=utc(2026, 3, 10))
    return cenario, ordem, lote, titulo


# ---------------------------------------------------------------- idempotencia


def test_etl_e_idempotente(session: Session) -> None:
    """Rodar duas vezes sobre a mesma origem produz exatamente as mesmas linhas.

    O ETL anterior tinha `date.today()` em quatro pontos de `_carga_fatos`: os
    numeros mudavam conforme o dia da execucao.
    """
    _cenario_completo(session)

    def fotografia() -> dict:
        instantaneo = {
            fato.__name__: session.scalar(select(func.count()).select_from(fato)) for fato in _FATOS
        }
        instantaneo["soma_faturado"] = session.scalar(
            select(func.coalesce(func.sum(FatoFaturamento.valor_faturado), 0))
        )
        instantaneo["soma_glosado"] = session.scalar(
            select(func.coalesce(func.sum(FatoGlosa.valor_glosado), 0))
        )
        instantaneo["soma_realizado"] = session.scalar(
            select(func.coalesce(func.sum(FatoFinanceiro.valor_realizado), 0))
        )
        return instantaneo

    primeira = executar_etl()
    antes = fotografia()

    segunda = executar_etl()
    depois = fotografia()

    assert primeira == segunda
    assert antes == depois


def test_execucao_e_registrada(session: Session) -> None:
    _cenario_completo(session)
    executar_etl()

    registro = ultima_execucao(session)

    assert registro is not None
    assert registro.status == "SUCESSO"
    assert registro.finalizado_em is not None
    assert registro.linhas["fato_atendimento"] == 2


# ------------------------------------------------------------------------ grao


def test_nenhuma_chave_natural_duplicada(session: Session) -> None:
    """G2: sem chave natural nao havia como detectar duplicacao de fato."""
    _cenario_completo(session)
    executar_etl()

    chaves = (
        (FatoOrdemServico, FatoOrdemServico.ordem_servico_id),
        (FatoAtendimento, FatoAtendimento.os_item_id),
        (FatoFaturamento, FatoFaturamento.guia_item_id),
        (FatoLogistica, FatoLogistica.amostra_id),
        (FatoGlosa, FatoGlosa.glosa_id),
    )
    for modelo, coluna in chaves:
        total = session.scalar(select(func.count()).select_from(modelo))
        distintas = session.scalar(select(func.count(func.distinct(coluna))).select_from(modelo))
        assert total == distintas, f"{modelo.__name__} tem chave natural duplicada"


def test_tempo_de_ciclo_vive_no_grao_da_os(session: Session) -> None:
    """G1: o tempo de ciclo era repetido em cada item, e o AVG ponderava a OS
    pelo numero de exames — uma OS com 2 exames pesava o dobro de uma com 1."""
    _cenario_completo(session)
    executar_etl()

    assert session.scalar(select(func.count()).select_from(FatoOrdemServico)) == 1
    assert session.scalar(select(func.count()).select_from(FatoAtendimento)) == 2

    fato = session.scalar(select(FatoOrdemServico))
    # coleta 12/01 09:00 -> laudo 13/01 09:00 = 24h exatas
    assert fato.tempo_ciclo_horas == Decimal("24.00")
    # coleta 09:00 -> recebimento 17:30 = 8.5h
    assert fato.tempo_coleta_recebimento_horas == Decimal("8.50")
    assert fato.qtd_itens == 2
    assert fato.concluida is True

    assert not hasattr(FatoAtendimento, "tempo_ciclo_os_horas")


# ---------------------------------------------------------------- bugs de data


def test_b1_logistica_datada_pela_coleta(session: Session) -> None:
    """B1: `_sk_tempo(date.today())` dentro do loop colapsava toda a serie
    temporal de logistica numa barra unica em 'hoje'."""
    cenario = montar_cadastros(session)

    janeiro = criar_os(session, cenario, aberta_em=utc(2026, 1, 10))
    coletar(session, cenario, janeiro, coletada_em=utc(2026, 1, 10, 8))
    marco = criar_os(session, cenario, aberta_em=utc(2026, 3, 10))
    coletar(session, cenario, marco, coletada_em=utc(2026, 3, 10, 8))

    executar_etl()

    datas = session.execute(
        select(DimTempo.data).join(FatoLogistica, FatoLogistica.sk_tempo == DimTempo.sk_tempo)
    ).scalars().all()

    assert sorted(datas) == [date(2026, 1, 10), date(2026, 3, 10)]


def test_b1_tempo_de_transito_e_populado(session: Session) -> None:
    """`tempo_transito_horas` nunca havia sido populado, embora
    `malotes.despachado_em` e `protocolos_recebimento.recebido_em` existissem."""
    _cenario_completo(session)
    executar_etl()

    fato = session.scalar(select(FatoLogistica))
    # despacho 14:00 -> recebimento 17:30 = 3.5h
    assert fato.tempo_transito_horas == Decimal("3.50")


def test_b2_titulo_em_aberto_nao_conta_como_recebido(session: Session) -> None:
    """B2: o ETL somava `titulo.valor` de TODO titulo em `valor_recebido`.

    Um titulo ABERTO de R$ 10.000 aparecia como R$ 10.000 recebidos, e o painel
    chamava isso de "Fluxo de Caixa".
    """
    cenario = montar_cadastros(session)
    ordem = criar_os(session, cenario, aberta_em=utc(2026, 1, 5))
    laudos = liberar_laudos(session, ordem, liberado_em=utc(2026, 1, 6))
    lote = faturar(session, cenario, laudos, fechado_em=utc(2026, 1, 20))
    titulo_receber(session, lote, valor=Decimal("10000.00"), vencimento=date(2026, 2, 20))

    executar_etl()

    previsto = session.scalar(
        select(func.coalesce(func.sum(FatoFinanceiro.valor_previsto), 0)).where(
            FatoFinanceiro.regime == "PREVISTO"
        )
    )
    realizado = session.scalar(
        select(func.coalesce(func.sum(FatoFinanceiro.valor_realizado), 0)).where(
            FatoFinanceiro.regime == "CAIXA"
        )
    )

    assert previsto == Decimal("10000.00")
    assert realizado == Decimal("0")


def test_b2_regime_de_caixa_vem_do_movimento(session: Session) -> None:
    _cenario_completo(session)
    executar_etl()

    caixa = session.scalar(select(FatoFinanceiro).where(FatoFinanceiro.regime == "CAIXA"))

    assert caixa is not None
    assert caixa.valor_realizado == Decimal("80.00")
    assert caixa.fluxo == "ENTRADA"
    # Datado pelo `ocorrido_em` do movimento, nao pelo vencimento do titulo.
    assert session.get(DimTempo, caixa.sk_tempo).data == date(2026, 3, 10)


def test_b3_lote_aberto_nao_entra_no_faturamento(session: Session) -> None:
    """B3: item de lote aberto caia em `date.today()` e migrava de bucket
    temporal a cada execucao do ETL."""
    cenario = montar_cadastros(session)
    ordem = criar_os(session, cenario, aberta_em=utc(2026, 1, 5))
    laudos = liberar_laudos(session, ordem, liberado_em=utc(2026, 1, 6))
    faturar(session, cenario, laudos, fechado_em=None)  # lote ABERTO

    executar_etl()

    assert session.scalar(select(func.count()).select_from(FatoFaturamento)) == 0


# ---------------------------------------------------------- bugs dimensionais


def test_b4_setor_do_procedimento_e_preenchido(session: Session) -> None:
    """B4: a carga passava `setor=None` explicitamente, entao analise por setor
    era impossivel — embora `procedimentos.setor` existisse."""
    _cenario_completo(session)
    executar_etl()

    setores = session.execute(
        select(DimProcedimento.nome, DimProcedimento.setor).order_by(DimProcedimento.nome)
    ).all()

    assert dict(setores) == {"Glicose": "Bioquimica", "Hemograma": "Hematologia"}
    assert session.scalar(select(func.count()).select_from(DimSetor)) >= 2

    sem_setor = session.scalar(
        select(func.count()).select_from(FatoAtendimento).where(FatoAtendimento.sk_setor.is_(None))
    )
    assert sem_setor == 0


def test_b5_faturamento_tem_unidade_real(session: Session) -> None:
    """B5: todo fato de faturamento apontava para a unidade fake 'consolidado'."""
    cenario, _ordem, _lote, _titulo = _cenario_completo(session)
    executar_etl()

    unidades = session.execute(
        select(DimUnidade.id_origem)
        .join(FatoFaturamento, FatoFaturamento.sk_unidade == DimUnidade.sk_unidade)
        .distinct()
    ).scalars().all()

    assert unidades == [cenario.unidade_coleta]


def test_b6_financeiro_tem_convenio(session: Session) -> None:
    """B6: `sk_convenio` era `None` hardcoded, embora a FK existisse no modelo."""
    _cenario_completo(session)
    executar_etl()

    com_convenio = session.scalar(
        select(func.count())
        .select_from(FatoFinanceiro)
        .where(FatoFinanceiro.sk_convenio.is_not(None))
    )

    assert com_convenio > 0


def test_b7_dimensao_reflete_alteracao_na_origem(session: Session) -> None:
    """B7: as dimensoes so eram criadas, nunca atualizadas — convenio renomeado
    nunca propagava ao BI."""
    cenario = montar_cadastros(session)
    criar_os(session, cenario, aberta_em=utc(2026, 1, 5))
    executar_etl()

    from src.cadastro.procedimento.models import Procedimento

    procedimento = session.get(Procedimento, cenario.procedimento_bioquimica)
    procedimento.nome = "Glicose em jejum"
    procedimento.setor = "Bioquimica Clinica"
    session.commit()

    executar_etl()

    dim = session.scalar(
        select(DimProcedimento).where(DimProcedimento.id_origem == cenario.procedimento_bioquimica)
    )
    session.refresh(dim)
    assert dim.nome == "Glicose em jejum"
    assert dim.setor == "Bioquimica Clinica"


def test_b8_calendario_e_denso(session: Session) -> None:
    """B8: `bi_dim_tempo` nascia sob demanda, entao mes sem fato nao existia e a
    serie temporal PULAVA o mes em vez de mostrar zero."""
    cenario = montar_cadastros(session)
    criar_os(session, cenario, aberta_em=utc(2026, 1, 15))
    criar_os(session, cenario, aberta_em=utc(2026, 4, 15))

    executar_etl()

    meses = session.execute(
        select(DimTempo.ano_mes).distinct().order_by(DimTempo.ano_mes)
    ).scalars().all()

    assert "2026-02" in meses, "mes sem movimento sumiu do calendario"
    assert "2026-03" in meses

    limites = session.execute(select(func.min(DimTempo.data), func.max(DimTempo.data))).one()
    esperado = (limites[1] - limites[0]).days + 1
    assert session.scalar(select(func.count()).select_from(DimTempo)) == esperado


def test_faixa_etaria_congelada_na_data_do_fato(session: Session) -> None:
    """ADR 0009: a faixa e a vigente na data do fato gerador.

    Recalcular na dimensao faria o paciente que faz 19 anos sumir
    retroativamente da faixa '13-18' em todo relatorio historico.
    """
    cenario = montar_cadastros(session)
    from src.cadastro.models import Paciente

    paciente = session.get(Paciente, cenario.pacientes[0])
    paciente.data_nascimento = date(2007, 6, 15)  # faz 19 anos em 15/06/2026
    session.commit()

    criar_os(session, cenario, aberta_em=utc(2026, 1, 10))  # ainda 18
    criar_os(session, cenario, aberta_em=utc(2026, 12, 10))  # ja 19

    executar_etl()

    faixas = session.execute(
        select(DimFaixaEtaria.chave_natural, func.count())
        .join(FatoAtendimento, FatoAtendimento.sk_faixa_etaria == DimFaixaEtaria.sk_faixa_etaria)
        .group_by(DimFaixaEtaria.chave_natural)
    ).all()

    assert dict(faixas) == {"13-18": 1, "19-30": 1}


# --------------------------------------------------------------- reconciliacao


def test_faturamento_reconcilia_com_o_oltp(session: Session) -> None:
    _cenario_completo(session)
    executar_etl()

    from src.faturamento.lote_faturamento.models import GuiaItem, GuiaTiss, LoteFaturamento

    origem = session.scalar(
        select(func.coalesce(func.sum(GuiaItem.valor_faturado), 0))
        .select_from(GuiaItem)
        .join(GuiaTiss, GuiaTiss.id == GuiaItem.guia_tiss_id)
        .join(LoteFaturamento, LoteFaturamento.id == GuiaTiss.lote_faturamento_id)
        .where(LoteFaturamento.fechado_em.is_not(None))
    )
    olap = session.scalar(select(func.coalesce(func.sum(FatoFaturamento.valor_faturado), 0)))

    assert origem == olap


def test_glosa_reconcilia_e_abate_o_liberado(session: Session) -> None:
    _cenario_completo(session)
    executar_etl()

    from src.faturamento.glosa.models import Glosa

    origem = session.scalar(select(func.coalesce(func.sum(Glosa.valor_glosado), 0)))
    olap = session.scalar(select(func.coalesce(func.sum(FatoGlosa.valor_glosado), 0)))
    assert origem == olap

    faturado, glosado, liberado = session.execute(
        select(
            func.sum(FatoFaturamento.valor_faturado),
            func.sum(FatoFaturamento.valor_glosado),
            func.sum(FatoFaturamento.valor_liberado),
        )
    ).one()
    assert liberado == faturado - glosado


def test_motivo_de_glosa_e_normalizado(session: Session) -> None:
    """`glosas.motivo` e texto livre: variacao de caixa e espaco viravam
    motivos distintos no agrupamento."""
    cenario = montar_cadastros(session)
    ordem = criar_os(session, cenario, aberta_em=utc(2026, 1, 5))
    laudos = liberar_laudos(session, ordem, liberado_em=utc(2026, 1, 6))
    lote = faturar(session, cenario, laudos, fechado_em=utc(2026, 1, 20))

    glosar(session, cenario, lote, valor=Decimal("10.00"),
           motivo="Falta de autorizacao", criado_em=utc(2026, 2, 1))
    glosar(session, cenario, lote, valor=Decimal("5.00"),
           motivo="  falta de   autorizacao  ", criado_em=utc(2026, 2, 2))

    executar_etl()

    motivos_usados = session.scalar(select(func.count(func.distinct(FatoGlosa.sk_motivo_glosa))))
    assert motivos_usados == 1
    assert session.scalar(select(func.count()).select_from(FatoGlosa)) == 2


def test_poda_remove_fato_cuja_origem_sumiu(session: Session) -> None:
    """A carga precisa refletir remocao na origem, nao so insercao."""
    from src.atendimento.ordem_servico.models import OrdemServico, OsItem

    cenario = montar_cadastros(session)
    primeira = criar_os(session, cenario, aberta_em=utc(2026, 1, 5))
    criar_os(session, cenario, aberta_em=utc(2026, 1, 6))
    executar_etl()
    assert session.scalar(select(func.count()).select_from(FatoOrdemServico)) == 2

    session.query(OsItem).filter(OsItem.ordem_servico_id == primeira.id).delete()
    session.query(OrdemServico).filter(OrdemServico.id == primeira.id).delete()
    session.commit()

    executar_etl()

    assert session.scalar(select(func.count()).select_from(FatoOrdemServico)) == 1


def test_dimensoes_basicas_populadas(session: Session) -> None:
    _cenario_completo(session)
    executar_etl()

    assert session.scalar(select(func.count()).select_from(DimFaixaEtaria)) == 7
    assert session.scalar(select(func.count()).select_from(DimMotivoGlosa)) >= 2


def test_paciente_permanece_anonimizado(session: Session) -> None:
    """LGPD: `id_origem` e hash SHA-256, nunca o UUID do paciente."""
    cenario, _ordem, _lote, _titulo = _cenario_completo(session)
    executar_etl()

    dim = session.scalar(select(DimPacienteAnon))
    assert len(dim.id_origem) == 64
    assert dim.id_origem not in {str(pid) for pid in cenario.pacientes}
    assert not hasattr(dim, "faixa_etaria")
