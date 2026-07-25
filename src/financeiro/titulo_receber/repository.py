from datetime import date
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.financeiro.titulo_receber.dtos import StatusTitulo
from src.financeiro.titulo_receber.models import TituloReceber


def salvar(session: Session, titulo: TituloReceber) -> TituloReceber:
    session.add(titulo)
    return titulo


def obter_por_id(session: Session, titulo_id: UUID) -> TituloReceber | None:
    return session.get(TituloReceber, titulo_id)


def listar_todos(session: Session) -> list[TituloReceber]:
    stmt = select(TituloReceber).order_by(TituloReceber.criado_em.desc())
    return list(session.scalars(stmt).all())


def listar_pendentes(session: Session) -> list[TituloReceber]:
    stmt = (
        select(TituloReceber)
        .where(TituloReceber.status == StatusTitulo.PENDENTE)
        .order_by(TituloReceber.vencimento)
    )
    return list(session.scalars(stmt).all())


def listar_por_status(session: Session, status: str) -> list[TituloReceber]:
    stmt = select(TituloReceber).where(TituloReceber.status == status).order_by(TituloReceber.criado_em.desc())
    return list(session.scalars(stmt).all())


def listar_vencidos(session: Session) -> list[TituloReceber]:
    stmt = (
        select(TituloReceber)
        .where(TituloReceber.status == StatusTitulo.PENDENTE, TituloReceber.vencimento < date.today())
        .order_by(TituloReceber.vencimento)
    )
    return list(session.scalars(stmt).all())
