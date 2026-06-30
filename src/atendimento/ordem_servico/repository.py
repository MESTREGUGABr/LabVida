from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.atendimento.ordem_servico.models import OrdemServico, OsItem, OsStatusHistorico


def obter_por_id(session: Session, ordem_servico_id: UUID) -> OrdemServico | None:
    return session.get(OrdemServico, ordem_servico_id)


def obter_por_codigo(session: Session, codigo_os: str) -> OrdemServico | None:
    return session.scalar(select(OrdemServico).where(OrdemServico.codigo_os == codigo_os))


def listar(session: Session, limite: int = 100) -> list[OrdemServico]:
    return list(
        session.scalars(select(OrdemServico).order_by(OrdemServico.aberta_em.desc()).limit(limite))
    )


def listar_por_status(session: Session, status: str) -> list[OrdemServico]:
    return list(
        session.scalars(
            select(OrdemServico)
            .where(OrdemServico.status == status)
            .order_by(OrdemServico.aberta_em.desc())
        )
    )


def salvar(session: Session, ordem_servico: OrdemServico) -> None:
    session.add(ordem_servico)


def salvar_item(session: Session, item: OsItem) -> None:
    session.add(item)


def listar_itens(session: Session, ordem_servico_id: UUID) -> list[OsItem]:
    return list(
        session.scalars(select(OsItem).where(OsItem.ordem_servico_id == ordem_servico_id))
    )


def salvar_historico(session: Session, historico: OsStatusHistorico) -> None:
    session.add(historico)


def listar_historico(session: Session, ordem_servico_id: UUID) -> list[OsStatusHistorico]:
    return list(
        session.scalars(
            select(OsStatusHistorico)
            .where(OsStatusHistorico.ordem_servico_id == ordem_servico_id)
            .order_by(OsStatusHistorico.ocorrido_em)
        )
    )
