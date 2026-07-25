from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.atendimento.ordem_servico.models import OrdemServico, OsItem
from src.faturamento.lote_faturamento.dtos import StatusLote
from src.faturamento.lote_faturamento.models import GuiaItem, GuiaTiss, LoteFaturamento
from src.laboratorial.models import Laudo, StatusLaudo


def salvar_lote(session: Session, lote: LoteFaturamento) -> LoteFaturamento:
    session.add(lote)
    return lote


def obter_lote_por_id(session: Session, lote_id: UUID) -> LoteFaturamento | None:
    return session.get(LoteFaturamento, lote_id)


def obter_lote_por_codigo(session: Session, codigo_lote: str) -> LoteFaturamento | None:
    stmt = select(LoteFaturamento).where(LoteFaturamento.codigo_lote == codigo_lote)
    return session.execute(stmt).scalar_one_or_none()


def listar_lotes(session: Session) -> list[LoteFaturamento]:
    stmt = select(LoteFaturamento).order_by(LoteFaturamento.criado_em.desc())
    return list(session.scalars(stmt).all())


def listar_lotes_abertos(session: Session) -> list[LoteFaturamento]:
    stmt = (
        select(LoteFaturamento)
        .where(LoteFaturamento.status == StatusLote.ABERTO)
        .order_by(LoteFaturamento.criado_em.desc())
    )
    return list(session.scalars(stmt).all())


def salvar_guia(session: Session, guia: GuiaTiss) -> GuiaTiss:
    session.add(guia)
    return guia


def obter_guia_por_id(session: Session, guia_id: UUID) -> GuiaTiss | None:
    return session.get(GuiaTiss, guia_id)


def salvar_guia_item(session: Session, item: GuiaItem) -> GuiaItem:
    session.add(item)
    return item


def obter_item_por_laudo(session: Session, laudo_id: UUID) -> GuiaItem | None:
    stmt = select(GuiaItem).where(GuiaItem.laudo_id == laudo_id)
    return session.execute(stmt).scalar_one_or_none()


def obter_guia_item_por_id(session: Session, guia_item_id: UUID) -> GuiaItem | None:
    return session.get(GuiaItem, guia_item_id)


def listar_itens_por_guia(session: Session, guia_tiss_id: UUID) -> list[GuiaItem]:
    stmt = select(GuiaItem).where(GuiaItem.guia_tiss_id == guia_tiss_id)
    return list(session.scalars(stmt).all())


def contar_laudos_pendentes_por_convenio(session: Session, convenio_id: UUID | None) -> int:
    subquery_faturados = select(GuiaItem.laudo_id)
    stmt = (
        select(func.count(Laudo.id))
        .join(OsItem, Laudo.os_item_id == OsItem.id)
        .join(OrdemServico, OsItem.ordem_servico_id == OrdemServico.id)
        .where(
            Laudo.status == StatusLaudo.LIBERADO,
            Laudo.id.not_in(subquery_faturados),
            OrdemServico.convenio_id == convenio_id,
        )
    )
    return session.execute(stmt).scalar_one()


def listar_laudos_liberados_por_convenio(session: Session, convenio_id: UUID | None) -> list[dict]:
    subquery_faturados = select(GuiaItem.laudo_id)
    stmt = (
        select(Laudo.id, Laudo.os_item_id, Laudo.status, Laudo.liberado_em, OsItem.procedimento_id)
        .join(OsItem, Laudo.os_item_id == OsItem.id)
        .join(OrdemServico, OsItem.ordem_servico_id == OrdemServico.id)
        .where(
            Laudo.status == StatusLaudo.LIBERADO,
            Laudo.id.not_in(subquery_faturados),
            OrdemServico.convenio_id == convenio_id,
        )
    )
    results = session.execute(stmt).all()
    return [
        {
            "laudo_id": r.id,
            "os_item_id": r.os_item_id,
            "procedimento_id": r.procedimento_id,
            "status": r.status.value,
            "liberado_em": r.liberado_em,
        }
        for r in results
    ]
