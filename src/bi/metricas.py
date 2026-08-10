"""Camada semantica do BI — um indicador por funcao.

Antes havia 11 queries SQL em string, escritas inline dentro das paginas. Nada
era testavel sem subir o Streamlit, cada uma decidia sozinha se filtrava por
data (so 2 das 11 filtravam), e o mesmo indicador reescrito em duas telas
divergia. Aqui cada indicador e uma funcao tipada que recebe o mesmo `Periodo` e
devolve um DataFrame pronto para grafico, tabela ou export.

Medidas derivadas (ticket medio, taxa de glosa, rentabilidade) sao calculadas
AQUI, sobre as medidas aditivas dos fatos, e nao guardadas em coluna: razao
pre-calculada nao reagrega — a media das medias nao e a media (ADR 0009).
"""

from dataclasses import dataclass
from datetime import date, timedelta

import pandas as pd
from sqlalchemy import Select, and_, case, func, select
from sqlalchemy.orm import Session

from src.bi.models import (
    DimConvenio,
    DimFaixaEtaria,
    DimMotivoGlosa,
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

_PARTICULAR = "Particular"


@dataclass(frozen=True)
class Periodo:
    """Janela de analise. Unica forma de filtrar data em todo o BI."""

    inicio: date
    fim: date
    rotulo: str = ""

    @property
    def dias(self) -> int:
        return (self.fim - self.inicio).days + 1

    def anterior(self) -> "Periodo":
        """Janela imediatamente anterior, de mesmo tamanho — base do delta."""
        duracao = timedelta(days=self.dias)
        return Periodo(self.inicio - duracao, self.inicio - timedelta(days=1), "Periodo anterior")


def _no_periodo(consulta: Select, fato, periodo: Periodo) -> Select:
    return consulta.join(DimTempo, DimTempo.sk_tempo == fato.sk_tempo).where(
        and_(DimTempo.data >= periodo.inicio, DimTempo.data <= periodo.fim)
    )


def _df(session: Session, consulta: Select) -> pd.DataFrame:
    resultado = session.execute(consulta)
    return pd.DataFrame(resultado.mappings().all())


def _nome_convenio():
    """`NULL` em convenio significa particular — nunca 'sem nome'."""
    return func.coalesce(DimConvenio.nome, _PARTICULAR)


# ---------------------------------------------------------------------------
# Produtividade
# ---------------------------------------------------------------------------


def exames_por_unidade(session: Session, periodo: Periodo) -> pd.DataFrame:
    consulta = (
        select(DimUnidade.nome.label("unidade"), func.sum(FatoAtendimento.qtd_exames).label("exames"))
        .select_from(FatoAtendimento)
        .join(DimUnidade, DimUnidade.sk_unidade == FatoAtendimento.sk_unidade)
        .where(FatoAtendimento.cancelado.is_(False))
        .group_by(DimUnidade.nome)
        .order_by(func.sum(FatoAtendimento.qtd_exames).desc())
    )
    return _df(session, _no_periodo(consulta, FatoAtendimento, periodo))


def exames_por_mes(session: Session, periodo: Periodo) -> pd.DataFrame:
    """Serie mensal. O calendario e denso, entao mes sem exame vem com zero."""
    exames = (
        select(
            DimTempo.ano_mes.label("mes"),
            func.count(FatoAtendimento.sk_fato).label("exames"),
        )
        .select_from(DimTempo)
        .join(
            FatoAtendimento,
            and_(
                FatoAtendimento.sk_tempo == DimTempo.sk_tempo,
                FatoAtendimento.cancelado.is_(False),
            ),
            isouter=True,
        )
        .where(and_(DimTempo.data >= periodo.inicio, DimTempo.data <= periodo.fim))
        .group_by(DimTempo.ano_mes)
        .order_by(DimTempo.ano_mes)
    )
    return _df(session, exames)


def exames_por_convenio(session: Session, periodo: Periodo) -> pd.DataFrame:
    consulta = (
        select(_nome_convenio().label("convenio"), func.sum(FatoAtendimento.qtd_exames).label("exames"))
        .select_from(FatoAtendimento)
        .join(DimConvenio, DimConvenio.sk_convenio == FatoAtendimento.sk_convenio, isouter=True)
        .where(FatoAtendimento.cancelado.is_(False))
        # Agrupa pela coluna crua, nao pelo COALESCE: o SQLAlchemy emitiria dois
        # bind params distintos para o literal e o Postgres trataria as duas
        # expressoes como diferentes ("must appear in the GROUP BY clause").
        # NULL cai num grupo unico, que o COALESCE do SELECT rotula "Particular".
        .group_by(DimConvenio.nome)
        .order_by(func.sum(FatoAtendimento.qtd_exames).desc())
    )
    return _df(session, _no_periodo(consulta, FatoAtendimento, periodo))


def exames_por_faixa_etaria(session: Session, periodo: Periodo) -> pd.DataFrame:
    consulta = (
        select(
            DimFaixaEtaria.descricao.label("faixa_etaria"),
            func.sum(FatoAtendimento.qtd_exames).label("exames"),
        )
        .select_from(FatoAtendimento)
        .join(DimFaixaEtaria, DimFaixaEtaria.sk_faixa_etaria == FatoAtendimento.sk_faixa_etaria)
        .where(FatoAtendimento.cancelado.is_(False))
        .group_by(DimFaixaEtaria.descricao, DimFaixaEtaria.ordem)
        .order_by(DimFaixaEtaria.ordem)
    )
    return _df(session, _no_periodo(consulta, FatoAtendimento, periodo))


def exames_por_setor(session: Session, periodo: Periodo) -> pd.DataFrame:
    """Destravado pela correcao de B4 — `DimProcedimento.setor` era sempre NULL."""
    consulta = (
        select(DimSetor.nome.label("setor"), func.sum(FatoAtendimento.qtd_exames).label("exames"))
        .select_from(FatoAtendimento)
        .join(DimSetor, DimSetor.sk_setor == FatoAtendimento.sk_setor)
        .where(FatoAtendimento.cancelado.is_(False))
        .group_by(DimSetor.nome)
        .order_by(func.sum(FatoAtendimento.qtd_exames).desc())
    )
    return _df(session, _no_periodo(consulta, FatoAtendimento, periodo))


def sazonalidade_por_dia_da_semana(session: Session, periodo: Periodo) -> pd.DataFrame:
    """`dia_semana` existia na dimensao desde o inicio e nunca foi usado."""
    consulta = (
        select(
            DimTempo.dia_semana.label("dia_semana"),
            DimTempo.dia_semana_num.label("ordem"),
            func.sum(FatoAtendimento.qtd_exames).label("exames"),
        )
        .select_from(FatoAtendimento)
        .join(DimTempo, DimTempo.sk_tempo == FatoAtendimento.sk_tempo)
        .where(
            and_(
                DimTempo.data >= periodo.inicio,
                DimTempo.data <= periodo.fim,
                FatoAtendimento.cancelado.is_(False),
            )
        )
        .group_by(DimTempo.dia_semana, DimTempo.dia_semana_num)
        .order_by(DimTempo.dia_semana_num)
    )
    return _df(session, consulta)


# ---------------------------------------------------------------------------
# Tempo de atendimento (TAT)
# ---------------------------------------------------------------------------


def tat_por_mes(session: Session, periodo: Periodo) -> pd.DataFrame:
    """Tempo medio coleta -> laudo, no grao correto (uma linha por OS)."""
    consulta = (
        select(
            DimTempo.ano_mes.label("mes"),
            func.round(func.avg(FatoOrdemServico.tempo_ciclo_horas), 2).label("horas"),
            func.count(FatoOrdemServico.sk_fato).label("ordens"),
        )
        .select_from(FatoOrdemServico)
        .join(DimTempo, DimTempo.sk_tempo == FatoOrdemServico.sk_tempo)
        .where(
            and_(
                DimTempo.data >= periodo.inicio,
                DimTempo.data <= periodo.fim,
                FatoOrdemServico.tempo_ciclo_horas.is_not(None),
            )
        )
        .group_by(DimTempo.ano_mes)
        .order_by(DimTempo.ano_mes)
    )
    return _df(session, consulta)


def tat_por_setor(session: Session, periodo: Periodo) -> pd.DataFrame:
    """Media por OS dentro de cada setor.

    A OS e contada uma vez por setor em que tem exame — nao uma vez por exame,
    que era o erro de grao do modelo anterior.
    """
    ordens_por_setor = (
        select(
            DimSetor.nome.label("setor"),
            FatoOrdemServico.ordem_servico_id.label("ordem"),
            func.max(FatoOrdemServico.tempo_ciclo_horas).label("horas"),
        )
        .select_from(FatoAtendimento)
        .join(DimSetor, DimSetor.sk_setor == FatoAtendimento.sk_setor)
        .join(
            FatoOrdemServico,
            FatoOrdemServico.sk_paciente == FatoAtendimento.sk_paciente,
        )
        .join(DimTempo, DimTempo.sk_tempo == FatoAtendimento.sk_tempo)
        .where(
            and_(
                DimTempo.data >= periodo.inicio,
                DimTempo.data <= periodo.fim,
                FatoOrdemServico.tempo_ciclo_horas.is_not(None),
            )
        )
        .group_by(DimSetor.nome, FatoOrdemServico.ordem_servico_id)
        .subquery()
    )

    consulta = (
        select(
            ordens_por_setor.c.setor,
            func.round(func.avg(ordens_por_setor.c.horas), 2).label("horas"),
            func.count().label("ordens"),
        )
        .group_by(ordens_por_setor.c.setor)
        .order_by(func.avg(ordens_por_setor.c.horas).desc())
    )
    return _df(session, consulta)


# ---------------------------------------------------------------------------
# Logistica
# ---------------------------------------------------------------------------


def amostras_por_unidade(session: Session, periodo: Periodo) -> pd.DataFrame:
    consulta = (
        select(
            DimUnidade.nome.label("unidade"),
            func.sum(FatoLogistica.qtd_amostras).label("amostras"),
            func.sum(case((FatoLogistica.rejeitada.is_(True), 1), else_=0)).label("rejeitadas"),
        )
        .select_from(FatoLogistica)
        .join(DimUnidade, DimUnidade.sk_unidade == FatoLogistica.sk_unidade)
        .group_by(DimUnidade.nome)
        .order_by(func.sum(FatoLogistica.qtd_amostras).desc())
    )
    return _df(session, _no_periodo(consulta, FatoLogistica, periodo))


def amostras_por_mes(session: Session, periodo: Periodo) -> pd.DataFrame:
    """Serie que antes era uma barra unica em 'hoje' (bug B1)."""
    consulta = (
        select(
            DimTempo.ano_mes.label("mes"),
            func.count(FatoLogistica.sk_fato).label("amostras"),
        )
        .select_from(DimTempo)
        .join(FatoLogistica, FatoLogistica.sk_tempo == DimTempo.sk_tempo, isouter=True)
        .where(and_(DimTempo.data >= periodo.inicio, DimTempo.data <= periodo.fim))
        .group_by(DimTempo.ano_mes)
        .order_by(DimTempo.ano_mes)
    )
    return _df(session, consulta)


def tempo_transito_por_unidade(session: Session, periodo: Periodo) -> pd.DataFrame:
    """Indicador novo: a coluna existia no modelo e nunca havia sido populada."""
    consulta = (
        select(
            DimUnidade.nome.label("unidade"),
            func.round(func.avg(FatoLogistica.tempo_transito_horas), 2).label("horas"),
            func.count().label("amostras"),
        )
        .select_from(FatoLogistica)
        .join(DimUnidade, DimUnidade.sk_unidade == FatoLogistica.sk_unidade)
        .where(FatoLogistica.tempo_transito_horas.is_not(None))
        .group_by(DimUnidade.nome)
        .order_by(func.avg(FatoLogistica.tempo_transito_horas).desc())
    )
    return _df(session, _no_periodo(consulta, FatoLogistica, periodo))


def status_das_amostras(session: Session, periodo: Periodo) -> pd.DataFrame:
    """Vem do fato, nao da tabela operacional `amostras` — que a pagina de
    logistica consultava direto, furando o modelo dimensional."""
    consulta = (
        select(
            FatoLogistica.status_atual.label("status"),
            func.count().label("quantidade"),
        )
        .select_from(FatoLogistica)
        .group_by(FatoLogistica.status_atual)
        .order_by(func.count().desc())
    )
    return _df(session, _no_periodo(consulta, FatoLogistica, periodo))


# ---------------------------------------------------------------------------
# Faturamento e receita
# ---------------------------------------------------------------------------


def receita_por_convenio(session: Session, periodo: Periodo) -> pd.DataFrame:
    consulta = (
        select(
            _nome_convenio().label("convenio"),
            func.sum(FatoFaturamento.valor_faturado).label("faturado"),
            func.sum(FatoFaturamento.valor_glosado).label("glosado"),
            func.sum(FatoFaturamento.valor_liberado).label("liberado"),
        )
        .select_from(FatoFaturamento)
        .join(DimConvenio, DimConvenio.sk_convenio == FatoFaturamento.sk_convenio, isouter=True)
        # Agrupa pela coluna crua, nao pelo COALESCE: o SQLAlchemy emitiria dois
        # bind params distintos para o literal e o Postgres trataria as duas
        # expressoes como diferentes ("must appear in the GROUP BY clause").
        # NULL cai num grupo unico, que o COALESCE do SELECT rotula "Particular".
        .group_by(DimConvenio.nome)
        .order_by(func.sum(FatoFaturamento.valor_faturado).desc())
    )
    return _df(session, _no_periodo(consulta, FatoFaturamento, periodo))


def receita_por_mes(session: Session, periodo: Periodo) -> pd.DataFrame:
    consulta = (
        select(
            DimTempo.ano_mes.label("mes"),
            func.coalesce(func.sum(FatoFaturamento.valor_faturado), 0).label("faturado"),
            func.coalesce(func.sum(FatoFaturamento.valor_glosado), 0).label("glosado"),
        )
        .select_from(DimTempo)
        .join(FatoFaturamento, FatoFaturamento.sk_tempo == DimTempo.sk_tempo, isouter=True)
        .where(and_(DimTempo.data >= periodo.inicio, DimTempo.data <= periodo.fim))
        .group_by(DimTempo.ano_mes)
        .order_by(DimTempo.ano_mes)
    )
    return _df(session, consulta)


def ticket_medio_por_convenio(session: Session, periodo: Periodo) -> pd.DataFrame:
    """Calculado sobre os aditivos — nao lido de uma coluna `ticket_medio`.

    Guardar a razao no fato impede reagregacao: o ticket medio de dois convenios
    nao e a media dos dois tickets.
    """
    consulta = (
        select(
            _nome_convenio().label("convenio"),
            func.sum(FatoFaturamento.valor_faturado).label("faturado"),
            func.sum(FatoFaturamento.qtd_itens).label("exames"),
            func.round(
                func.sum(FatoFaturamento.valor_faturado)
                / func.nullif(func.sum(FatoFaturamento.qtd_itens), 0),
                2,
            ).label("ticket_medio"),
        )
        .select_from(FatoFaturamento)
        .join(DimConvenio, DimConvenio.sk_convenio == FatoFaturamento.sk_convenio, isouter=True)
        # Agrupa pela coluna crua, nao pelo COALESCE: o SQLAlchemy emitiria dois
        # bind params distintos para o literal e o Postgres trataria as duas
        # expressoes como diferentes ("must appear in the GROUP BY clause").
        # NULL cai num grupo unico, que o COALESCE do SELECT rotula "Particular".
        .group_by(DimConvenio.nome)
        .order_by(func.sum(FatoFaturamento.valor_faturado).desc())
    )
    return _df(session, _no_periodo(consulta, FatoFaturamento, periodo))


def curva_abc_procedimentos(session: Session, periodo: Periodo, limite: int = 15) -> pd.DataFrame:
    """Receita por procedimento com participacao acumulada (classificacao ABC)."""
    consulta = (
        select(
            DimProcedimento.nome.label("procedimento"),
            func.sum(FatoFaturamento.valor_faturado).label("faturado"),
            func.sum(FatoFaturamento.qtd_itens).label("exames"),
        )
        .select_from(FatoFaturamento)
        .join(DimProcedimento, DimProcedimento.sk_procedimento == FatoFaturamento.sk_procedimento)
        .group_by(DimProcedimento.nome)
        .order_by(func.sum(FatoFaturamento.valor_faturado).desc())
    )
    df = _df(session, _no_periodo(consulta, FatoFaturamento, periodo))
    if df.empty:
        return df

    df["faturado"] = df["faturado"].astype(float)
    total = df["faturado"].sum()
    df["participacao"] = df["faturado"] / total * 100 if total else 0
    df["acumulado"] = df["participacao"].cumsum()

    # Regra de classe: pelo acumulado ANTES do item (onde ele "abre"), nao pelo
    # acumulado depois. Um item ocupa uma faixa do acumulado, e classificar pelo
    # fim joga para B o procedimento que sozinho representa 90% da receita —
    # justamente o mais classe A da lista. Pelo inicio, o primeiro item e sempre
    # A, que e a leitura que interessa a quem olha uma curva ABC.
    acumulado_anterior = df["acumulado"] - df["participacao"]
    df["classe"] = pd.cut(
        acumulado_anterior, bins=[-0.01, 80, 95, 100.01], labels=["A", "B", "C"]
    )
    return df.head(limite)


def ticket_medio_por_procedimento(session: Session, periodo: Periodo, limite: int = 10) -> pd.DataFrame:
    consulta = (
        select(
            DimProcedimento.nome.label("procedimento"),
            func.round(
                func.sum(FatoFaturamento.valor_faturado)
                / func.nullif(func.sum(FatoFaturamento.qtd_itens), 0),
                2,
            ).label("ticket_medio"),
            func.sum(FatoFaturamento.qtd_itens).label("exames"),
        )
        .select_from(FatoFaturamento)
        .join(DimProcedimento, DimProcedimento.sk_procedimento == FatoFaturamento.sk_procedimento)
        .group_by(DimProcedimento.nome)
        .order_by(
            (
                func.sum(FatoFaturamento.valor_faturado)
                / func.nullif(func.sum(FatoFaturamento.qtd_itens), 0)
            ).desc()
        )
        .limit(limite)
    )
    return _df(session, _no_periodo(consulta, FatoFaturamento, periodo))


# ---------------------------------------------------------------------------
# Glosa
# ---------------------------------------------------------------------------


def glosa_por_motivo(session: Session, periodo: Periodo) -> pd.DataFrame:
    """Indicador novo — exige `bi_fato_glosa`, que nao existia."""
    consulta = (
        select(
            DimMotivoGlosa.descricao.label("motivo"),
            func.sum(FatoGlosa.valor_glosado).label("glosado"),
            func.sum(FatoGlosa.qtd_glosas).label("ocorrencias"),
        )
        .select_from(FatoGlosa)
        .join(DimMotivoGlosa, DimMotivoGlosa.sk_motivo_glosa == FatoGlosa.sk_motivo_glosa)
        .group_by(DimMotivoGlosa.descricao)
        .order_by(func.sum(FatoGlosa.valor_glosado).desc())
    )
    return _df(session, _no_periodo(consulta, FatoGlosa, periodo))


def taxa_glosa_por_convenio(session: Session, periodo: Periodo) -> pd.DataFrame:
    consulta = (
        select(
            _nome_convenio().label("convenio"),
            func.sum(FatoFaturamento.valor_faturado).label("faturado"),
            func.sum(FatoFaturamento.valor_glosado).label("glosado"),
            func.round(
                func.sum(FatoFaturamento.valor_glosado)
                * 100
                / func.nullif(func.sum(FatoFaturamento.valor_faturado), 0),
                2,
            ).label("taxa_glosa"),
        )
        .select_from(FatoFaturamento)
        .join(DimConvenio, DimConvenio.sk_convenio == FatoFaturamento.sk_convenio, isouter=True)
        # Agrupa pela coluna crua, nao pelo COALESCE: o SQLAlchemy emitiria dois
        # bind params distintos para o literal e o Postgres trataria as duas
        # expressoes como diferentes ("must appear in the GROUP BY clause").
        # NULL cai num grupo unico, que o COALESCE do SELECT rotula "Particular".
        .group_by(DimConvenio.nome)
        .order_by(
            (
                func.sum(FatoFaturamento.valor_glosado)
                / func.nullif(func.sum(FatoFaturamento.valor_faturado), 0)
            ).desc()
        )
    )
    return _df(session, _no_periodo(consulta, FatoFaturamento, periodo))


# ---------------------------------------------------------------------------
# Financeiro
# ---------------------------------------------------------------------------


def fluxo_caixa_mensal(session: Session, periodo: Periodo) -> pd.DataFrame:
    """Regime de CAIXA: dinheiro que de fato entrou e saiu.

    Antes o painel rotulado "Fluxo de Caixa" plotava cronograma de vencimentos e
    contava titulo nao pago como receita.
    """
    consulta = (
        select(
            DimTempo.ano_mes.label("mes"),
            func.coalesce(
                func.sum(case((FatoFinanceiro.fluxo == "ENTRADA", FatoFinanceiro.valor_realizado), else_=0)),
                0,
            ).label("entradas"),
            func.coalesce(
                func.sum(case((FatoFinanceiro.fluxo == "SAIDA", FatoFinanceiro.valor_realizado), else_=0)),
                0,
            ).label("saidas"),
        )
        .select_from(DimTempo)
        .join(
            FatoFinanceiro,
            and_(
                FatoFinanceiro.sk_tempo == DimTempo.sk_tempo,
                FatoFinanceiro.regime == "CAIXA",
            ),
            isouter=True,
        )
        .where(and_(DimTempo.data >= periodo.inicio, DimTempo.data <= periodo.fim))
        .group_by(DimTempo.ano_mes)
        .order_by(DimTempo.ano_mes)
    )
    df = _df(session, consulta)
    if not df.empty:
        df["saldo"] = df["entradas"].astype(float) - df["saidas"].astype(float)
    return df


def previsto_x_realizado(session: Session, periodo: Periodo) -> pd.DataFrame:
    consulta = (
        select(
            DimTempo.ano_mes.label("mes"),
            func.coalesce(
                func.sum(
                    case(
                        (
                            and_(FatoFinanceiro.regime == "PREVISTO", FatoFinanceiro.fluxo == "ENTRADA"),
                            FatoFinanceiro.valor_previsto,
                        ),
                        else_=0,
                    )
                ),
                0,
            ).label("previsto"),
            func.coalesce(
                func.sum(
                    case(
                        (
                            and_(FatoFinanceiro.regime == "CAIXA", FatoFinanceiro.fluxo == "ENTRADA"),
                            FatoFinanceiro.valor_realizado,
                        ),
                        else_=0,
                    )
                ),
                0,
            ).label("realizado"),
        )
        .select_from(DimTempo)
        .join(FatoFinanceiro, FatoFinanceiro.sk_tempo == DimTempo.sk_tempo, isouter=True)
        .where(and_(DimTempo.data >= periodo.inicio, DimTempo.data <= periodo.fim))
        .group_by(DimTempo.ano_mes)
        .order_by(DimTempo.ano_mes)
    )
    return _df(session, consulta)


def aging_carteira(session: Session, referencia: date) -> pd.DataFrame:
    """Titulos a receber em aberto, por faixa de atraso. Indicador novo.

    As faixas sao comparacoes de DATA, nao aritmetica de dias: em Postgres
    `date - date` devolve integer (nao interval), entao `date_part('day', ...)`
    nao existe para essa assinatura. Comparar contra limites calculados em
    Python e mais simples e nao depende do dialeto.
    """
    limite_30 = referencia - timedelta(days=30)
    limite_60 = referencia - timedelta(days=60)
    limite_90 = referencia - timedelta(days=90)

    faixa = case(
        (DimTempo.data > referencia, "A vencer"),
        (DimTempo.data >= limite_30, "1-30 dias"),
        (DimTempo.data >= limite_60, "31-60 dias"),
        (DimTempo.data >= limite_90, "61-90 dias"),
        else_="90+ dias",
    )
    ordem = case(
        (DimTempo.data > referencia, 0),
        (DimTempo.data >= limite_30, 1),
        (DimTempo.data >= limite_60, 2),
        (DimTempo.data >= limite_90, 3),
        else_=4,
    )

    consulta = (
        select(
            faixa.label("faixa"),
            func.sum(FatoFinanceiro.valor_previsto).label("valor"),
            func.count().label("titulos"),
        )
        .select_from(FatoFinanceiro)
        .join(DimTempo, DimTempo.sk_tempo == FatoFinanceiro.sk_tempo)
        .where(
            and_(
                FatoFinanceiro.regime == "PREVISTO",
                FatoFinanceiro.fluxo == "ENTRADA",
                FatoFinanceiro.liquidado.is_(False),
            )
        )
        .group_by(faixa, ordem)
        .order_by(ordem)
    )
    return _df(session, consulta)


def dre_simplificado(session: Session, periodo: Periodo) -> pd.DataFrame:
    """DRE gerencial em regime de caixa — F13 do relatorio de revisao."""
    entradas = session.scalar(
        _no_periodo(
            select(
                func.coalesce(
                    func.sum(
                        case((FatoFinanceiro.fluxo == "ENTRADA", FatoFinanceiro.valor_realizado), else_=0)
                    ),
                    0,
                )
            ).select_from(FatoFinanceiro).where(FatoFinanceiro.regime == "CAIXA"),
            FatoFinanceiro,
            periodo,
        )
    ) or 0
    saidas = session.scalar(
        _no_periodo(
            select(
                func.coalesce(
                    func.sum(
                        case((FatoFinanceiro.fluxo == "SAIDA", FatoFinanceiro.valor_realizado), else_=0)
                    ),
                    0,
                )
            ).select_from(FatoFinanceiro).where(FatoFinanceiro.regime == "CAIXA"),
            FatoFinanceiro,
            periodo,
        )
    ) or 0
    glosado = session.scalar(
        _no_periodo(
            select(func.coalesce(func.sum(FatoFaturamento.valor_glosado), 0)).select_from(FatoFaturamento),
            FatoFaturamento,
            periodo,
        )
    ) or 0

    entradas, saidas, glosado = float(entradas), float(saidas), float(glosado)
    return pd.DataFrame(
        [
            {"linha": "Receita recebida", "valor": entradas, "tipo": "positivo"},
            {"linha": "Glosas do periodo", "valor": -glosado, "tipo": "negativo"},
            {"linha": "Despesas pagas", "valor": -saidas, "tipo": "negativo"},
            {"linha": "Resultado", "valor": entradas - saidas, "tipo": "resultado"},
        ]
    )


# ---------------------------------------------------------------------------
# KPIs consolidados
# ---------------------------------------------------------------------------


def kpis(session: Session, periodo: Periodo) -> dict[str, float]:
    """Numeros de topo, todos derivados de medidas aditivas."""
    exames = session.scalar(
        _no_periodo(
            select(func.coalesce(func.sum(FatoAtendimento.qtd_exames), 0))
            .select_from(FatoAtendimento)
            .where(FatoAtendimento.cancelado.is_(False)),
            FatoAtendimento,
            periodo,
        )
    ) or 0

    faturado, glosado = session.execute(
        _no_periodo(
            select(
                func.coalesce(func.sum(FatoFaturamento.valor_faturado), 0),
                func.coalesce(func.sum(FatoFaturamento.valor_glosado), 0),
            ).select_from(FatoFaturamento),
            FatoFaturamento,
            periodo,
        )
    ).one()

    recebido = session.scalar(
        _no_periodo(
            select(
                func.coalesce(
                    func.sum(
                        case((FatoFinanceiro.fluxo == "ENTRADA", FatoFinanceiro.valor_realizado), else_=0)
                    ),
                    0,
                )
            )
            .select_from(FatoFinanceiro)
            .where(FatoFinanceiro.regime == "CAIXA"),
            FatoFinanceiro,
            periodo,
        )
    ) or 0

    tat = session.scalar(
        _no_periodo(
            select(func.avg(FatoOrdemServico.tempo_ciclo_horas))
            .select_from(FatoOrdemServico)
            .where(FatoOrdemServico.tempo_ciclo_horas.is_not(None)),
            FatoOrdemServico,
            periodo,
        )
    )

    amostras, rejeitadas = session.execute(
        _no_periodo(
            select(
                func.coalesce(func.sum(FatoLogistica.qtd_amostras), 0),
                func.coalesce(
                    func.sum(case((FatoLogistica.rejeitada.is_(True), 1), else_=0)), 0
                ),
            ).select_from(FatoLogistica),
            FatoLogistica,
            periodo,
        )
    ).one()

    faturado, glosado, recebido = float(faturado), float(glosado), float(recebido)
    amostras, rejeitadas = int(amostras), int(rejeitadas)

    return {
        "exames": int(exames),
        "faturado": faturado,
        "glosado": glosado,
        "liberado": faturado - glosado,
        "recebido": recebido,
        "taxa_glosa": (glosado / faturado * 100) if faturado else 0.0,
        "ticket_medio": (faturado / exames) if exames else 0.0,
        "tat_horas": float(tat) if tat is not None else 0.0,
        "amostras": amostras,
        "taxa_rejeicao": (rejeitadas / amostras * 100) if amostras else 0.0,
    }
