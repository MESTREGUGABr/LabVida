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

import uuid
from dataclasses import dataclass
from datetime import date, timedelta

import pandas as pd
from sqlalchemy import Select, and_, case, func, or_, select
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
from src.auditoria.models import AuditoriaLog
from src.compras.insumo.models import EstoqueMovimento, InsumoMaterial
from src.usuario.models import Usuario

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


@dataclass(frozen=True)
class FiltroDimensoes:
    """Filtro composto, combinado com `Periodo`. `None` num campo = sem
    restricao naquela dimensao (todas passam) — retrocompatibilidade: cada
    funcao abaixo so aplica a dimensao que o fato de origem tem de fato
    (`hasattr`), entao passar um filtro nao quebra fatos sem aquela FK
    (ex: `FatoLogistica` nao tem convenio nem procedimento)."""

    unidades: list[int] | None = None
    convenios: list[int] | None = None
    incluir_particular: bool = False
    procedimentos: list[int] | None = None


def _no_periodo(consulta: Select, fato, periodo: Periodo) -> Select:
    return consulta.join(DimTempo, DimTempo.sk_tempo == fato.sk_tempo).where(
        and_(DimTempo.data >= periodo.inicio, DimTempo.data <= periodo.fim)
    )


def _condicoes_dimensoes(fato, filtro: "FiltroDimensoes | None") -> list:
    """Condicoes de Unidade/Convenio/Procedimento, so na dimensao que o fato
    tem (`hasattr`) — e o que garante "cada pagina so oferece o filtro que
    faz sentido pros seus dados" sem precisar de `if` especial por funcao.

    Devolve uma LISTA de condicoes, nao uma query pronta: series mensais com
    calendario denso (`isouter=True` direto contra `DimTempo`) precisam
    destas condicoes dentro do ON do LEFT JOIN, nao num WHERE — um WHERE
    sobre coluna do lado direito de um LEFT JOIN vira INNER JOIN de fato e
    faz o mes sem movimento (linha toda NULL) desaparecer, quebrando o
    "mes sem dado entra com zero" (ver `exames_por_mes`/`receita_por_mes`).
    """
    if filtro is None:
        return []
    condicoes = []
    if filtro.unidades and hasattr(fato, "sk_unidade"):
        condicoes.append(fato.sk_unidade.in_(filtro.unidades))
    if hasattr(fato, "sk_convenio"):
        sub = []
        if filtro.convenios:
            sub.append(fato.sk_convenio.in_(filtro.convenios))
        if filtro.incluir_particular:
            sub.append(fato.sk_convenio.is_(None))
        if sub:
            condicoes.append(or_(*sub))
    if filtro.procedimentos and hasattr(fato, "sk_procedimento"):
        condicoes.append(fato.sk_procedimento.in_(filtro.procedimentos))
    return condicoes


def _com_dimensoes(consulta: Select, fato, filtro: "FiltroDimensoes | None") -> Select:
    """Para JOIN comum (INNER) ou agregado sem quebra por mes: aplica via
    WHERE. NAO use em series mensais de calendario denso — ver
    `_condicoes_dimensoes`."""
    condicoes = _condicoes_dimensoes(fato, filtro)
    return consulta.where(and_(*condicoes)) if condicoes else consulta


def _sem_convenio(filtro: "FiltroDimensoes | None") -> "FiltroDimensoes | None":
    """Despesa (`FatoFinanceiro.fluxo == "SAIDA"`) nunca tem convenio — nao e
    "particular", e simplesmente uma dimensao que nao existe pra aluguel,
    fornecedor etc (o ETL grava `sk_convenio=None` pra TODA saida, sempre).
    Selecionar "Particular" no filtro de Convenio (que vira `sk_convenio IS
    NULL`) casava com TODAS as despesas, inflando o lado "Despesas pagas" do
    DRE como se fossem receita de paciente particular. Usado so na consulta
    de saidas — entradas (que tem convenio real, via o titulo/lote) continuam
    respeitando o filtro normalmente."""
    if filtro is None or (filtro.convenios is None and not filtro.incluir_particular):
        return filtro
    return FiltroDimensoes(
        unidades=filtro.unidades,
        convenios=None,
        incluir_particular=False,
        procedimentos=filtro.procedimentos,
    )


def _df(session: Session, consulta: Select) -> pd.DataFrame:
    resultado = session.execute(consulta)
    return pd.DataFrame(resultado.mappings().all())


def _nome_convenio():
    """`NULL` em convenio significa particular — nunca 'sem nome'."""
    return func.coalesce(DimConvenio.nome, _PARTICULAR)


def _humanizar(texto: str) -> str:
    """"CRIAR_PACIENTE" -> "Criar paciente"; "ordem_servico" -> "Ordem servico".

    `acao`/`entidade` de `AuditoriaLog` sao gravados em MAIUSCULO_COM_UNDERSCORE
    ou minusculo_com_underscore pelo codigo (ver chamadas de `registrar_auditoria`),
    nao tem cadastro proprio com nome de exibicao como convenio/setor/unidade.
    "os" fica maiusculo (sigla de Ordem de Servico) — o resto do sistema trata
    OS como sigla, nao palavra comum (`atendimento_os.py`, `laboratorio_bancada.py`).
    """
    palavras = [p.upper() if p == "os" else p for p in texto.lower().split("_")]
    rotulo = " ".join(palavras)
    return rotulo[:1].upper() + rotulo[1:] if rotulo else rotulo


# ---------------------------------------------------------------------------
# Produtividade
# ---------------------------------------------------------------------------


def exames_por_unidade(
    session: Session, periodo: Periodo, filtro: FiltroDimensoes | None = None
) -> pd.DataFrame:
    consulta = (
        select(DimUnidade.nome.label("unidade"), func.sum(FatoAtendimento.qtd_exames).label("exames"))
        .select_from(FatoAtendimento)
        .join(DimUnidade, DimUnidade.sk_unidade == FatoAtendimento.sk_unidade)
        .where(FatoAtendimento.cancelado.is_(False))
        .group_by(DimUnidade.nome)
        .order_by(func.sum(FatoAtendimento.qtd_exames).desc())
    )
    return _df(session, _com_dimensoes(_no_periodo(consulta, FatoAtendimento, periodo), FatoAtendimento, filtro))


def exames_por_mes(
    session: Session, periodo: Periodo, filtro: FiltroDimensoes | None = None
) -> pd.DataFrame:
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
                *_condicoes_dimensoes(FatoAtendimento, filtro),
            ),
            isouter=True,
        )
        .where(and_(DimTempo.data >= periodo.inicio, DimTempo.data <= periodo.fim))
        .group_by(DimTempo.ano_mes)
        .order_by(DimTempo.ano_mes)
    )
    return _df(session, exames)


def exames_por_convenio(
    session: Session, periodo: Periodo, filtro: FiltroDimensoes | None = None
) -> pd.DataFrame:
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
    return _df(session, _com_dimensoes(_no_periodo(consulta, FatoAtendimento, periodo), FatoAtendimento, filtro))


def exames_por_faixa_etaria(
    session: Session, periodo: Periodo, filtro: FiltroDimensoes | None = None
) -> pd.DataFrame:
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
    return _df(session, _com_dimensoes(_no_periodo(consulta, FatoAtendimento, periodo), FatoAtendimento, filtro))


def exames_por_setor(
    session: Session, periodo: Periodo, filtro: FiltroDimensoes | None = None
) -> pd.DataFrame:
    """Destravado pela correcao de B4 — `DimProcedimento.setor` era sempre NULL."""
    consulta = (
        select(DimSetor.nome.label("setor"), func.sum(FatoAtendimento.qtd_exames).label("exames"))
        .select_from(FatoAtendimento)
        .join(DimSetor, DimSetor.sk_setor == FatoAtendimento.sk_setor)
        .where(FatoAtendimento.cancelado.is_(False))
        .group_by(DimSetor.nome)
        .order_by(func.sum(FatoAtendimento.qtd_exames).desc())
    )
    return _df(session, _com_dimensoes(_no_periodo(consulta, FatoAtendimento, periodo), FatoAtendimento, filtro))


def sazonalidade_por_dia_da_semana(
    session: Session, periodo: Periodo, filtro: FiltroDimensoes | None = None
) -> pd.DataFrame:
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
    return _df(session, _com_dimensoes(consulta, FatoAtendimento, filtro))


# ---------------------------------------------------------------------------
# Tempo de atendimento (TAT)
# ---------------------------------------------------------------------------


def tat_por_mes(
    session: Session, periodo: Periodo, filtro: FiltroDimensoes | None = None
) -> pd.DataFrame:
    """Tempo medio coleta -> laudo, no grao correto (uma linha por OS).

    `FatoOrdemServico` nao tem `sk_procedimento` (grao e a OS, nao o exame) —
    um filtro de Exame nao se aplica aqui, so Unidade/Convenio (ver
    `_condicoes_dimensoes`, que ja ignora `filtro.procedimentos` neste fato)."""
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
    return _df(session, _com_dimensoes(consulta, FatoOrdemServico, filtro))


def tat_por_setor(
    session: Session, periodo: Periodo, filtro: FiltroDimensoes | None = None
) -> pd.DataFrame:
    """Media por OS dentro de cada setor.

    A OS e contada uma vez por setor em que tem exame — nao uma vez por exame,
    que era o erro de grao do modelo anterior.

    So Unidade/Convenio filtram aqui (nao Exame): a hora e do grao da OS
    (`FatoOrdemServico`), nao do exame individual — filtrar por um exame
    especifico so restringiria QUAIS setores aparecem, sem mudar a hora
    exibida (que continua sendo da OS inteira). Pra manter o mesmo
    comportamento documentado de `tat_por_mes`, o filtro de procedimento e
    ignorado aqui de proposito, mesmo `FatoAtendimento` tendo essa coluna.
    """
    filtro_sem_exame = (
        FiltroDimensoes(
            unidades=filtro.unidades,
            convenios=filtro.convenios,
            incluir_particular=filtro.incluir_particular,
        )
        if filtro is not None
        else None
    )
    consulta_ordens = (
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
    )
    ordens_por_setor = _com_dimensoes(consulta_ordens, FatoAtendimento, filtro_sem_exame).subquery()

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


def amostras_por_unidade(
    session: Session, periodo: Periodo, filtro: FiltroDimensoes | None = None
) -> pd.DataFrame:
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
    return _df(session, _com_dimensoes(_no_periodo(consulta, FatoLogistica, periodo), FatoLogistica, filtro))


def amostras_por_mes(
    session: Session, periodo: Periodo, filtro: FiltroDimensoes | None = None
) -> pd.DataFrame:
    """Serie que antes era uma barra unica em 'hoje' (bug B1)."""
    condicao_join = and_(
        FatoLogistica.sk_tempo == DimTempo.sk_tempo,
        *_condicoes_dimensoes(FatoLogistica, filtro),
    )
    consulta = (
        select(
            DimTempo.ano_mes.label("mes"),
            func.count(FatoLogistica.sk_fato).label("amostras"),
        )
        .select_from(DimTempo)
        .join(FatoLogistica, condicao_join, isouter=True)
        .where(and_(DimTempo.data >= periodo.inicio, DimTempo.data <= periodo.fim))
        .group_by(DimTempo.ano_mes)
        .order_by(DimTempo.ano_mes)
    )
    return _df(session, consulta)


def tempo_transito_por_unidade(
    session: Session, periodo: Periodo, filtro: FiltroDimensoes | None = None
) -> pd.DataFrame:
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
    return _df(session, _com_dimensoes(_no_periodo(consulta, FatoLogistica, periodo), FatoLogistica, filtro))


def status_das_amostras(
    session: Session, periodo: Periodo, filtro: FiltroDimensoes | None = None
) -> pd.DataFrame:
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
    return _df(session, _com_dimensoes(_no_periodo(consulta, FatoLogistica, periodo), FatoLogistica, filtro))


# ---------------------------------------------------------------------------
# Faturamento e receita
# ---------------------------------------------------------------------------


def receita_por_convenio(
    session: Session, periodo: Periodo, filtro: FiltroDimensoes | None = None
) -> pd.DataFrame:
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
    return _df(session, _com_dimensoes(_no_periodo(consulta, FatoFaturamento, periodo), FatoFaturamento, filtro))


def receita_por_mes(
    session: Session, periodo: Periodo, filtro: FiltroDimensoes | None = None
) -> pd.DataFrame:
    condicao_join = and_(
        FatoFaturamento.sk_tempo == DimTempo.sk_tempo,
        *_condicoes_dimensoes(FatoFaturamento, filtro),
    )
    consulta = (
        select(
            DimTempo.ano_mes.label("mes"),
            func.coalesce(func.sum(FatoFaturamento.valor_faturado), 0).label("faturado"),
            func.coalesce(func.sum(FatoFaturamento.valor_glosado), 0).label("glosado"),
        )
        .select_from(DimTempo)
        .join(FatoFaturamento, condicao_join, isouter=True)
        .where(and_(DimTempo.data >= periodo.inicio, DimTempo.data <= periodo.fim))
        .group_by(DimTempo.ano_mes)
        .order_by(DimTempo.ano_mes)
    )
    return _df(session, consulta)


def ticket_medio_por_convenio(
    session: Session, periodo: Periodo, filtro: FiltroDimensoes | None = None
) -> pd.DataFrame:
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
    return _df(session, _com_dimensoes(_no_periodo(consulta, FatoFaturamento, periodo), FatoFaturamento, filtro))


def curva_abc_procedimentos(
    session: Session, periodo: Periodo, filtro: FiltroDimensoes | None = None, limite: int = 15
) -> pd.DataFrame:
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
    df = _df(session, _com_dimensoes(_no_periodo(consulta, FatoFaturamento, periodo), FatoFaturamento, filtro))
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


def ticket_medio_por_procedimento(
    session: Session, periodo: Periodo, filtro: FiltroDimensoes | None = None, limite: int = 10
) -> pd.DataFrame:
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
    return _df(session, _com_dimensoes(_no_periodo(consulta, FatoFaturamento, periodo), FatoFaturamento, filtro))


# ---------------------------------------------------------------------------
# Glosa
# ---------------------------------------------------------------------------


def glosa_por_motivo(
    session: Session, periodo: Periodo, filtro: FiltroDimensoes | None = None
) -> pd.DataFrame:
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
    return _df(session, _com_dimensoes(_no_periodo(consulta, FatoGlosa, periodo), FatoGlosa, filtro))


def taxa_glosa_por_convenio(
    session: Session, periodo: Periodo, filtro: FiltroDimensoes | None = None
) -> pd.DataFrame:
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
    return _df(session, _com_dimensoes(_no_periodo(consulta, FatoFaturamento, periodo), FatoFaturamento, filtro))


# ---------------------------------------------------------------------------
# Financeiro
# ---------------------------------------------------------------------------


def fluxo_caixa_mensal(
    session: Session, periodo: Periodo, filtro: FiltroDimensoes | None = None
) -> pd.DataFrame:
    """Regime de CAIXA: dinheiro que de fato entrou e saiu.

    Antes o painel rotulado "Fluxo de Caixa" plotava cronograma de vencimentos e
    contava titulo nao pago como receita.
    """
    # Convenio/Particular so faz sentido pro lado ENTRADA (vem do titulo/lote,
    # que tem convenio real) — despesa (SAIDA) nunca tem convenio, entao fica
    # de fora dessa condicao (ver `_sem_convenio`), senao "Particular" (que
    # vira `sk_convenio IS NULL`) casaria com toda despesa.
    condicao_convenio = _condicoes_dimensoes(
        FatoFinanceiro,
        FiltroDimensoes(convenios=filtro.convenios, incluir_particular=filtro.incluir_particular)
        if filtro
        else None,
    )
    condicoes_join = [
        FatoFinanceiro.sk_tempo == DimTempo.sk_tempo,
        FatoFinanceiro.regime == "CAIXA",
        *_condicoes_dimensoes(FatoFinanceiro, _sem_convenio(filtro)),
    ]
    if condicao_convenio:
        condicoes_join.append(or_(FatoFinanceiro.fluxo == "SAIDA", *condicao_convenio))

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
        .join(FatoFinanceiro, and_(*condicoes_join), isouter=True)
        .where(and_(DimTempo.data >= periodo.inicio, DimTempo.data <= periodo.fim))
        .group_by(DimTempo.ano_mes)
        .order_by(DimTempo.ano_mes)
    )
    df = _df(session, consulta)
    if not df.empty:
        df["saldo"] = df["entradas"].astype(float) - df["saidas"].astype(float)
    return df


def previsto_x_realizado(
    session: Session, periodo: Periodo, filtro: FiltroDimensoes | None = None
) -> pd.DataFrame:
    condicao_join = and_(
        FatoFinanceiro.sk_tempo == DimTempo.sk_tempo,
        *_condicoes_dimensoes(FatoFinanceiro, filtro),
    )
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
        .join(FatoFinanceiro, condicao_join, isouter=True)
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


def dre_simplificado(
    session: Session, periodo: Periodo, filtro: FiltroDimensoes | None = None
) -> pd.DataFrame:
    """DRE gerencial em regime de caixa — F13 do relatorio de revisao."""
    entradas = session.scalar(
        _com_dimensoes(
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
            ),
            FatoFinanceiro,
            filtro,
        )
    ) or 0
    saidas = session.scalar(
        _com_dimensoes(
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
            ),
            FatoFinanceiro,
            _sem_convenio(filtro),
        )
    ) or 0
    glosado = session.scalar(
        _com_dimensoes(
            _no_periodo(
                select(func.coalesce(func.sum(FatoFaturamento.valor_glosado), 0)).select_from(FatoFaturamento),
                FatoFaturamento,
                periodo,
            ),
            FatoFaturamento,
            filtro,
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


def kpis(session: Session, periodo: Periodo, filtro: FiltroDimensoes | None = None) -> dict[str, float]:
    """Numeros de topo, todos derivados de medidas aditivas."""
    exames = session.scalar(
        _com_dimensoes(
            _no_periodo(
                select(func.coalesce(func.sum(FatoAtendimento.qtd_exames), 0))
                .select_from(FatoAtendimento)
                .where(FatoAtendimento.cancelado.is_(False)),
                FatoAtendimento,
                periodo,
            ),
            FatoAtendimento,
            filtro,
        )
    ) or 0

    faturado, glosado = session.execute(
        _com_dimensoes(
            _no_periodo(
                select(
                    func.coalesce(func.sum(FatoFaturamento.valor_faturado), 0),
                    func.coalesce(func.sum(FatoFaturamento.valor_glosado), 0),
                ).select_from(FatoFaturamento),
                FatoFaturamento,
                periodo,
            ),
            FatoFaturamento,
            filtro,
        )
    ).one()

    recebido = session.scalar(
        _com_dimensoes(
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
            ),
            FatoFinanceiro,
            filtro,
        )
    ) or 0

    tat = session.scalar(
        _com_dimensoes(
            _no_periodo(
                select(func.avg(FatoOrdemServico.tempo_ciclo_horas))
                .select_from(FatoOrdemServico)
                .where(FatoOrdemServico.tempo_ciclo_horas.is_not(None)),
                FatoOrdemServico,
                periodo,
            ),
            FatoOrdemServico,
            filtro,
        )
    )

    amostras, rejeitadas = session.execute(
        _com_dimensoes(
            _no_periodo(
                select(
                    func.coalesce(func.sum(FatoLogistica.qtd_amostras), 0),
                    func.coalesce(
                        func.sum(case((FatoLogistica.rejeitada.is_(True), 1), else_=0)), 0
                    ),
                ).select_from(FatoLogistica),
                FatoLogistica,
                periodo,
            ),
            FatoLogistica,
            filtro,
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


# ---------------------------------------------------------------------------
# Auditoria — consulta direta ao log operacional, sem ETL/fato no esquema
# estrela. E um log de eventos imutavel (nao muda de regime como financeiro,
# nao tem estados sobrepostos como OS), entao nao ha ganho em replica-lo no
# star schema so pra filtrar por periodo — a data e comparada direto contra
# `AuditoriaLog.ocorrido_em`.
# ---------------------------------------------------------------------------


def auditoria_kpis(session: Session, periodo: Periodo) -> dict[str, int]:
    ocorrencias = session.scalar(
        select(func.count(AuditoriaLog.id)).where(
            and_(
                func.date(AuditoriaLog.ocorrido_em) >= periodo.inicio,
                func.date(AuditoriaLog.ocorrido_em) <= periodo.fim,
            )
        )
    ) or 0
    return {"ocorrencias": int(ocorrencias)}


def ocorrencias_por_mes(session: Session, periodo: Periodo) -> pd.DataFrame:
    """Serie mensal. Calendario denso via `DimTempo` — mes sem ocorrencia vem
    com zero, mesmo padrao de `exames_por_mes`."""
    consulta = (
        select(
            DimTempo.ano_mes.label("mes"),
            func.count(AuditoriaLog.id).label("ocorrencias"),
        )
        .select_from(DimTempo)
        .join(AuditoriaLog, func.date(AuditoriaLog.ocorrido_em) == DimTempo.data, isouter=True)
        .where(and_(DimTempo.data >= periodo.inicio, DimTempo.data <= periodo.fim))
        .group_by(DimTempo.ano_mes)
        .order_by(DimTempo.ano_mes)
    )
    return _df(session, consulta)


def ocorrencias_por_acao(session: Session, periodo: Periodo) -> pd.DataFrame:
    consulta = (
        select(
            AuditoriaLog.acao.label("acao"),
            func.count(AuditoriaLog.id).label("ocorrencias"),
        )
        .where(
            and_(
                func.date(AuditoriaLog.ocorrido_em) >= periodo.inicio,
                func.date(AuditoriaLog.ocorrido_em) <= periodo.fim,
            )
        )
        .group_by(AuditoriaLog.acao)
        .order_by(func.count(AuditoriaLog.id).desc())
    )
    df = _df(session, consulta)
    if not df.empty:
        df["acao"] = df["acao"].map(_humanizar)
    return df


def ocorrencias_por_entidade(session: Session, periodo: Periodo) -> pd.DataFrame:
    consulta = (
        select(
            AuditoriaLog.entidade.label("entidade"),
            func.count(AuditoriaLog.id).label("ocorrencias"),
        )
        .where(
            and_(
                func.date(AuditoriaLog.ocorrido_em) >= periodo.inicio,
                func.date(AuditoriaLog.ocorrido_em) <= periodo.fim,
            )
        )
        .group_by(AuditoriaLog.entidade)
        .order_by(func.count(AuditoriaLog.id).desc())
    )
    df = _df(session, consulta)
    if not df.empty:
        df["entidade"] = df["entidade"].map(_humanizar)
    return df


def ocorrencias_recentes(session: Session, periodo: Periodo, *, limite: int = 200) -> pd.DataFrame:
    """Detalhe (nao so agregado) para a grid da pagina de auditoria."""
    consulta = (
        select(
            AuditoriaLog.ocorrido_em.label("ocorrido_em"),
            Usuario.nome.label("usuario_nome"),
            AuditoriaLog.acao.label("acao"),
            AuditoriaLog.entidade.label("entidade"),
        )
        .join(Usuario, Usuario.id == AuditoriaLog.usuario_id)
        .where(
            and_(
                func.date(AuditoriaLog.ocorrido_em) >= periodo.inicio,
                func.date(AuditoriaLog.ocorrido_em) <= periodo.fim,
            )
        )
        .order_by(AuditoriaLog.ocorrido_em.desc())
        .limit(limite)
    )
    df = _df(session, consulta)
    if not df.empty:
        df["acao"] = df["acao"].map(_humanizar)
        df["entidade"] = df["entidade"].map(_humanizar)
    return df


# ---------------------------------------------------------------------------
# Estoque — consulta direta a `InsumoMaterial`/`EstoqueMovimento`, sem ETL.
# Mesmo raciocinio da auditoria: sao tabelas operacionais de baixo volume,
# sem "regime" nem estados sobrepostos que justifiquem um fato novo no
# esquema estrela.
# ---------------------------------------------------------------------------


def estoque_kpis(session: Session, insumos: list[uuid.UUID] | None = None) -> dict[str, int]:
    """Estado atual do saldo — nao filtra por periodo (nao e serie historica)."""
    consulta_total = select(func.count(InsumoMaterial.id))
    consulta_criticos = select(func.count(InsumoMaterial.id)).where(
        InsumoMaterial.quantidade_estoque < InsumoMaterial.estoque_minimo
    )
    if insumos:
        consulta_total = consulta_total.where(InsumoMaterial.id.in_(insumos))
        consulta_criticos = consulta_criticos.where(InsumoMaterial.id.in_(insumos))
    total = session.scalar(consulta_total) or 0
    criticos = session.scalar(consulta_criticos) or 0
    return {"total_insumos": int(total), "insumos_criticos": int(criticos)}


def movimentacao_estoque_por_mes(
    session: Session, periodo: Periodo, insumos: list[uuid.UUID] | None = None
) -> pd.DataFrame:
    """Serie mensal ENTRADA x SAIDA. Calendario denso via `DimTempo`, mesmo
    padrao de `fluxo_caixa_mensal`."""
    condicao_join = func.date(EstoqueMovimento.ocorrido_em) == DimTempo.data
    if insumos:
        condicao_join = and_(condicao_join, EstoqueMovimento.insumo_material_id.in_(insumos))
    consulta = (
        select(
            DimTempo.ano_mes.label("mes"),
            func.coalesce(
                func.sum(
                    case((EstoqueMovimento.tipo == "ENTRADA", EstoqueMovimento.quantidade), else_=0)
                ),
                0,
            ).label("entradas"),
            func.coalesce(
                func.sum(
                    case((EstoqueMovimento.tipo == "SAIDA", EstoqueMovimento.quantidade), else_=0)
                ),
                0,
            ).label("saidas"),
        )
        .select_from(DimTempo)
        .join(EstoqueMovimento, condicao_join, isouter=True)
        .where(and_(DimTempo.data >= periodo.inicio, DimTempo.data <= periodo.fim))
        .group_by(DimTempo.ano_mes)
        .order_by(DimTempo.ano_mes)
    )
    return _df(session, consulta)


def insumos_maior_consumo(
    session: Session, periodo: Periodo, insumos: list[uuid.UUID] | None = None
) -> pd.DataFrame:
    """Ranking de giro: soma de saida por insumo no periodo."""
    condicoes = [
        EstoqueMovimento.tipo == "SAIDA",
        func.date(EstoqueMovimento.ocorrido_em) >= periodo.inicio,
        func.date(EstoqueMovimento.ocorrido_em) <= periodo.fim,
    ]
    if insumos:
        condicoes.append(InsumoMaterial.id.in_(insumos))
    consulta = (
        select(
            InsumoMaterial.nome.label("nome"),
            func.sum(EstoqueMovimento.quantidade).label("saida_total"),
        )
        .join(EstoqueMovimento, EstoqueMovimento.insumo_material_id == InsumoMaterial.id)
        .where(and_(*condicoes))
        .group_by(InsumoMaterial.nome)
        .order_by(func.sum(EstoqueMovimento.quantidade).desc())
    )
    return _df(session, consulta)



def insumos_criticos(session: Session, insumos: list[uuid.UUID] | None = None) -> pd.DataFrame:
    """Estado atual — mesma comparacao de `pages/compras_estoque.py` (saldo
    abaixo do minimo), so que devolvendo DataFrame em vez de lista filtrada
    em Python."""
    consulta = (
        select(
            InsumoMaterial.nome.label("nome"),
            InsumoMaterial.quantidade_estoque.label("quantidade_estoque"),
            InsumoMaterial.estoque_minimo.label("estoque_minimo"),
            (InsumoMaterial.estoque_minimo - InsumoMaterial.quantidade_estoque).label("deficit"),
        )
        .where(InsumoMaterial.quantidade_estoque < InsumoMaterial.estoque_minimo)
        .order_by((InsumoMaterial.estoque_minimo - InsumoMaterial.quantidade_estoque).desc())
    )
    if insumos:
        consulta = consulta.where(InsumoMaterial.id.in_(insumos))
    return _df(session, consulta)


# ---------------------------------------------------------------------------
# Alertas — estado atual (nao filtram por Periodo), pensados para a Visao
# Executiva dar destaque a excecoes que precisam de acao, nao so agregados.
# ---------------------------------------------------------------------------


def alertas_titulos_vencidos(session: Session) -> pd.DataFrame:
    from src.financeiro.titulo_pagar import repository as titulo_pagar_repository
    from src.financeiro.titulo_receber import repository as titulo_receber_repository

    hoje = date.today()
    linhas = [
        {
            "tipo": "A receber",
            "valor": float(titulo.valor),
            "vencimento": titulo.vencimento,
            "dias_atraso": (hoje - titulo.vencimento).days,
        }
        for titulo in titulo_receber_repository.listar_vencidos(session)
    ] + [
        {
            "tipo": "A pagar",
            "valor": float(titulo.valor),
            "vencimento": titulo.vencimento,
            "dias_atraso": (hoje - titulo.vencimento).days,
        }
        for titulo in titulo_pagar_repository.listar_vencidos(session)
    ]
    return pd.DataFrame(linhas, columns=["tipo", "valor", "vencimento", "dias_atraso"])


def alertas_malotes_sem_retorno(session: Session, *, dias_limite: int = 2) -> pd.DataFrame:
    from datetime import datetime, timezone

    from src.cadastro.unidade.models import Unidade
    from src.logistica.malote import repository as malote_repository

    agora = datetime.now(timezone.utc)
    limite = agora - timedelta(days=dias_limite)
    malotes = malote_repository.listar_em_transito_ha_mais_de(session, limite)

    unidades = {u.id: u.nome for u in session.scalars(select(Unidade)).all()}
    linhas = [
        {
            "codigo_malote": malote.codigo_malote,
            "origem": unidades.get(malote.unidade_origem_id, "-"),
            "destino": unidades.get(malote.unidade_destino_id, "-"),
            "despachado_em": malote.despachado_em,
            "dias_em_transito": (agora - malote.despachado_em).days if malote.despachado_em else None,
        }
        for malote in malotes
    ]
    return pd.DataFrame(
        linhas, columns=["codigo_malote", "origem", "destino", "despachado_em", "dias_em_transito"]
    )


# ---------------------------------------------------------------------------
# KPIs adicionais — um por pagina de BI, pedido do professor apos a
# apresentacao ("KPIs mais significativos"). Cada um usa dado que ja existe
# no fato/tabela, so nunca tinha sido lido em nenhuma metrica.
# ---------------------------------------------------------------------------


def taxa_cancelamento_itens(
    session: Session, periodo: Periodo, filtro: FiltroDimensoes | None = None
) -> float:
    """% de itens de OS cancelados no periodo — sinal de retrabalho/qualidade
    que nenhum KPI hoje mede (Produtividade). So Unidade/Convenio filtram
    aqui — `FatoOrdemServico` nao tem `sk_procedimento`."""
    total, cancelados = session.execute(
        _com_dimensoes(
            _no_periodo(
                select(
                    func.coalesce(func.sum(FatoOrdemServico.qtd_itens), 0),
                    func.coalesce(func.sum(FatoOrdemServico.qtd_itens_cancelados), 0),
                ).select_from(FatoOrdemServico),
                FatoOrdemServico,
                periodo,
            ),
            FatoOrdemServico,
            filtro,
        )
    ).one()
    total, cancelados = float(total), float(cancelados)
    return (cancelados / total * 100) if total else 0.0


def tempo_coleta_recebimento_medio(
    session: Session, periodo: Periodo, filtro: FiltroDimensoes | None = None
) -> float:
    """Media de `FatoLogistica.tempo_coleta_recebimento_horas` — coluna ja
    carregada pelo ETL mas nunca lida em nenhuma metrica de Logistica."""
    media = session.scalar(
        _com_dimensoes(
            _no_periodo(
                select(func.avg(FatoLogistica.tempo_coleta_recebimento_horas))
                .select_from(FatoLogistica)
                .where(FatoLogistica.tempo_coleta_recebimento_horas.is_not(None)),
                FatoLogistica,
                periodo,
            ),
            FatoLogistica,
            filtro,
        )
    )
    return float(media) if media is not None else 0.0


def cobertura_dias(
    session: Session, periodo: Periodo, insumos: list[uuid.UUID] | None = None
) -> float | None:
    """Dias de estoque restantes no ritmo de consumo do periodo: saldo atual
    total / consumo medio diario. Deliberadamente so quantidade, sem preco
    de compra (a valorizacao monetaria foi descartada nesta sessao).

    `None` quando nao ha consumo no periodo (sem base para estimar dias) —
    diferente de retornar `0.0`, que precisa continuar significando "estoque
    zerado com consumo ativo" (situacao bem mais grave, nao pode ficar
    escondida atras da mesma mensagem de "sem dado")."""
    consulta_saldo = select(func.coalesce(func.sum(InsumoMaterial.quantidade_estoque), 0))
    condicoes_consumo = [
        EstoqueMovimento.tipo == "SAIDA",
        func.date(EstoqueMovimento.ocorrido_em) >= periodo.inicio,
        func.date(EstoqueMovimento.ocorrido_em) <= periodo.fim,
    ]
    if insumos:
        consulta_saldo = consulta_saldo.where(InsumoMaterial.id.in_(insumos))
        condicoes_consumo.append(EstoqueMovimento.insumo_material_id.in_(insumos))
    saldo_total = session.scalar(consulta_saldo) or 0
    consumo_total = session.scalar(
        select(func.coalesce(func.sum(EstoqueMovimento.quantidade), 0)).where(and_(*condicoes_consumo))
    ) or 0
    dias = periodo.dias
    consumo_diario = float(consumo_total) / dias if dias else 0.0
    if not consumo_diario:
        return None
    return float(saldo_total) / consumo_diario
