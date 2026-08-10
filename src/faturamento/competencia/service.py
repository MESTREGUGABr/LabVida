"""Apuracao e fechamento de competencia (fase F4).

Responde a dois apontamentos do professor de uma vez: "colocar mes do
faturamento" e "por que lotes e nao periodos". A resposta e que **competencia e
o eixo**; lote/remessa e so o envelope enviado ao convenio.

Principio que rege tudo aqui: **competencia e carimbada no fato gerador, nao no
ato de faturar.** Laudo liberado em marco gera receita de marco, mesmo que seja
faturado em maio. Sem isso, atrasar o faturamento moveria a receita de mes, e
nenhum indicador por periodo faria sentido.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timezone
from decimal import Decimal
from uuid import UUID
from zoneinfo import ZoneInfo

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.auditoria import registrar_auditoria
from src.config import TZ_OPERACAO
from src.faturamento.competencia.errors import (
    CompetenciaAnteriorAberta,
    CompetenciaFechada,
    CompetenciaJaFechada,
    CompetenciaNaoEncontrada,
    JustificativaObrigatoria,
)
from src.faturamento.competencia.models import Competencia
from src.faturamento.glosa.models import Glosa
from src.faturamento.lote_faturamento.models import GuiaItem, GuiaTiss, LoteFaturamento
from src.laboratorial.models import Laudo, StatusLaudo

_FUSO = ZoneInfo(TZ_OPERACAO)


def competencia_de(instante: datetime) -> date:
    """Competencia de um fato gerador (ADR 0007).

    O instante e TIMESTAMPTZ em UTC; a competencia sai do calendario LOCAL. Um
    laudo liberado as 22h de 28/02 em Garanhuns e `2026-03-01T01:00Z` — apurar
    em UTC jogaria a receita para marco.

    Este e o UNICO ponto do sistema que converte instante em competencia.
    """
    if instante.tzinfo is None:
        instante = instante.replace(tzinfo=timezone.utc)
    local = instante.astimezone(_FUSO)
    return date(local.year, local.month, 1)


def competencia_corrente() -> date:
    return competencia_de(datetime.now(timezone.utc))


def obter(session: Session, competencia: date) -> Competencia | None:
    return session.get(Competencia, competencia)


def obter_ou_criar(session: Session, competencia: date) -> Competencia:
    """Competencia nasce sob demanda, sempre no primeiro dia do mes."""
    normalizada = competencia.replace(day=1)
    existente = session.get(Competencia, normalizada)
    if existente is not None:
        return existente

    nova = Competencia(competencia=normalizada, status="ABERTA")
    session.add(nova)
    session.flush()
    return nova


def exigir_aberta(session: Session, competencia: date) -> Competencia:
    """Guarda usado por todo lancamento que carimba competencia."""
    registro = obter_ou_criar(session, competencia)
    if not registro.aberta:
        raise CompetenciaFechada(
            f"A competencia {registro.competencia.strftime('%m/%Y')} esta fechada. "
            "Reabra-a para lancar nela."
        )
    return registro


def competencia_de_lancamento(session: Session, fato_gerador_em: datetime) -> tuple[date, date | None]:
    """Competencia efetiva de um lancamento, e a original se houver desvio.

    Regra do lancamento retroativo: se a competencia do fato gerador ja esta
    FECHADA, o lancamento cai na competencia ABERTA corrente e guarda a
    original. Fechado e imutavel; retroativo e rastreavel — as duas coisas
    juntas so cabem se o desvio ficar registrado.
    """
    natural = competencia_de(fato_gerador_em)
    registro = obter_ou_criar(session, natural)
    if registro.aberta:
        return natural, None

    corrente = obter_ou_criar(session, competencia_corrente())
    return corrente.competencia, natural


@dataclass(frozen=True)
class ApuracaoCompetencia:
    """Espelho do periodo. Calculado ao vivo enquanto a competencia esta aberta;
    congelado nas colunas da tabela quando ela fecha."""

    competencia: date
    status: str
    valor_faturado: Decimal
    valor_glosado: Decimal
    valor_liberado: Decimal
    qtd_laudos: int
    qtd_guias: int
    qtd_lotes: int
    laudos_nao_faturados: int

    @property
    def taxa_glosa(self) -> float:
        if not self.valor_faturado:
            return 0.0
        return float(self.valor_glosado / self.valor_faturado * 100)


def _limites(competencia: date) -> tuple[datetime, datetime]:
    """Intervalo [inicio, fim) do mes, em instantes UTC.

    Comparar `liberado_em AT TIME ZONE` linha a linha impediria o uso de indice;
    converter as BORDAS uma vez resolve e mantem a semantica do fuso.
    """
    inicio_local = datetime(competencia.year, competencia.month, 1, tzinfo=_FUSO)
    if competencia.month == 12:
        fim_local = datetime(competencia.year + 1, 1, 1, tzinfo=_FUSO)
    else:
        fim_local = datetime(competencia.year, competencia.month + 1, 1, tzinfo=_FUSO)
    return inicio_local.astimezone(timezone.utc), fim_local.astimezone(timezone.utc)


def apurar(session: Session, competencia: date) -> ApuracaoCompetencia:
    """Apura o periodo pelo FATO GERADOR (laudo liberado), nao pela data de faturar.

    Enquanto o modelo de item faturavel nao existe (fase F5), a apuracao usa o
    laudo como fato gerador e o `guias_itens` como valor faturado — que e a
    ligacao disponivel hoje.
    """
    registro = obter_ou_criar(session, competencia.replace(day=1))
    if not registro.aberta and registro.valor_faturado is not None:
        # Fechada: devolve o que foi congelado, nao um recalculo que poderia
        # divergir do que o gestor viu no fechamento.
        return ApuracaoCompetencia(
            competencia=registro.competencia,
            status=registro.status,
            valor_faturado=registro.valor_faturado or Decimal("0"),
            valor_glosado=registro.valor_glosado or Decimal("0"),
            valor_liberado=registro.valor_liberado or Decimal("0"),
            qtd_laudos=registro.qtd_laudos or 0,
            qtd_guias=registro.qtd_guias or 0,
            qtd_lotes=registro.qtd_lotes or 0,
            laudos_nao_faturados=0,
        )

    inicio, fim = _limites(registro.competencia)

    laudos_do_periodo = (
        select(Laudo.id)
        .where(
            Laudo.status == StatusLaudo.LIBERADO,
            Laudo.liberado_em >= inicio,
            Laudo.liberado_em < fim,
        )
        .subquery()
    )

    qtd_laudos = session.scalar(
        select(func.count()).select_from(laudos_do_periodo)
    ) or 0

    faturado, qtd_guias, qtd_lotes = session.execute(
        select(
            func.coalesce(func.sum(GuiaItem.valor_faturado), 0),
            func.count(func.distinct(GuiaItem.guia_tiss_id)),
            func.count(func.distinct(GuiaTiss.lote_faturamento_id)),
        )
        .select_from(GuiaItem)
        .join(GuiaTiss, GuiaTiss.id == GuiaItem.guia_tiss_id)
        .join(LoteFaturamento, LoteFaturamento.id == GuiaTiss.lote_faturamento_id)
        .where(GuiaItem.laudo_id.in_(select(laudos_do_periodo.c.id)))
    ).one()

    glosado = session.scalar(
        select(func.coalesce(func.sum(Glosa.valor_glosado), 0))
        .select_from(Glosa)
        .join(GuiaItem, GuiaItem.id == Glosa.guia_item_id)
        .where(GuiaItem.laudo_id.in_(select(laudos_do_periodo.c.id)))
    ) or Decimal("0")

    faturados = session.scalar(
        select(func.count(func.distinct(GuiaItem.laudo_id))).where(
            GuiaItem.laudo_id.in_(select(laudos_do_periodo.c.id))
        )
    ) or 0

    faturado = Decimal(str(faturado))
    glosado = Decimal(str(glosado))

    return ApuracaoCompetencia(
        competencia=registro.competencia,
        status=registro.status,
        valor_faturado=faturado,
        valor_glosado=glosado,
        valor_liberado=faturado - glosado,
        qtd_laudos=qtd_laudos,
        qtd_guias=qtd_guias or 0,
        qtd_lotes=qtd_lotes or 0,
        # O numero que o professor quer ver: quanto do mes ainda nao virou receita.
        laudos_nao_faturados=qtd_laudos - faturados,
    )


def listar(session: Session, limite: int = 24) -> list[Competencia]:
    return list(
        session.scalars(
            select(Competencia).order_by(Competencia.competencia.desc()).limit(limite)
        ).all()
    )


def fechar(
    session: Session,
    competencia: date,
    usuario_id: UUID | None = None,
    justificativa: str | None = None,
) -> Competencia:
    """Fecha o periodo e CONGELA a apuracao.

    Exige que todas as anteriores estejam fechadas: fechar marco com fevereiro
    aberto permitiria lancar em fevereiro depois, e o total de marco ja estaria
    congelado — o balanco nunca mais fecharia.
    """
    registro = obter(session, competencia.replace(day=1))
    if registro is None:
        raise CompetenciaNaoEncontrada(f"Competencia {competencia:%m/%Y} nao existe")
    if not registro.aberta:
        raise CompetenciaJaFechada(f"Competencia {registro.competencia:%m/%Y} ja esta fechada")

    anterior_aberta = session.scalar(
        select(Competencia.competencia)
        .where(
            Competencia.competencia < registro.competencia,
            Competencia.status == "ABERTA",
        )
        .order_by(Competencia.competencia)
        .limit(1)
    )
    if anterior_aberta is not None:
        raise CompetenciaAnteriorAberta(
            f"Feche antes a competencia {anterior_aberta:%m/%Y}."
        )

    apuracao = apurar(session, registro.competencia)

    registro.valor_faturado = apuracao.valor_faturado
    registro.valor_glosado = apuracao.valor_glosado
    registro.valor_liberado = apuracao.valor_liberado
    registro.qtd_laudos = apuracao.qtd_laudos
    registro.qtd_guias = apuracao.qtd_guias
    registro.qtd_lotes = apuracao.qtd_lotes
    registro.status = "FECHADA"
    registro.fechada_em = datetime.now(timezone.utc)
    registro.fechada_por_usuario_id = usuario_id
    registro.justificativa = justificativa

    if usuario_id is not None:
        registrar_auditoria(
            session,
            usuario_id,
            entidade="competencia",
            entidade_id=None,
            acao="FECHAR_COMPETENCIA",
            dados={
                "competencia": registro.competencia.isoformat(),
                "valor_faturado": str(apuracao.valor_faturado),
                "laudos_nao_faturados": apuracao.laudos_nao_faturados,
            },
        )

    session.commit()
    return registro


def reabrir(
    session: Session, competencia: date, usuario_id: UUID | None = None, justificativa: str = ""
) -> Competencia:
    """Reabre um periodo fechado. Exige justificativa: reabertura e excecao."""
    registro = obter(session, competencia.replace(day=1))
    if registro is None:
        raise CompetenciaNaoEncontrada(f"Competencia {competencia:%m/%Y} nao existe")
    if registro.aberta:
        return registro
    if not (justificativa or "").strip():
        raise JustificativaObrigatoria(
            "Informe o motivo da reabertura — ela desfaz um fechamento contabil."
        )

    registro.status = "ABERTA"
    registro.fechada_em = None
    registro.reaberta_em = datetime.now(timezone.utc)
    registro.justificativa = justificativa.strip()

    if usuario_id is not None:
        registrar_auditoria(
            session,
            usuario_id,
            entidade="competencia",
            entidade_id=None,
            acao="REABRIR_COMPETENCIA",
            dados={
                "competencia": registro.competencia.isoformat(),
                "justificativa": justificativa.strip(),
            },
        )

    session.commit()
    return registro
