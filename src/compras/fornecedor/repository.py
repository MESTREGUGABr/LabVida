from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.compras.fornecedor.dtos import StatusFornecedor
from src.compras.fornecedor.models import Fornecedor


def salvar(session: Session, fornecedor: Fornecedor) -> Fornecedor:
    session.add(fornecedor)
    return fornecedor


def obter_por_id(session: Session, fornecedor_id: UUID) -> Fornecedor | None:
    return session.get(Fornecedor, fornecedor_id)


def obter_por_cnpj(session: Session, cnpj: str) -> Fornecedor | None:
    stmt = select(Fornecedor).where(Fornecedor.cnpj == cnpj)
    return session.execute(stmt).scalar_one_or_none()


def listar_ativos(session: Session) -> list[Fornecedor]:
    stmt = (
        select(Fornecedor)
        .where(Fornecedor.status == StatusFornecedor.ATIVO)
        .order_by(Fornecedor.nome)
    )
    return list(session.scalars(stmt).all())


def listar_todos(session: Session) -> list[Fornecedor]:
    stmt = select(Fornecedor).order_by(Fornecedor.nome)
    return list(session.scalars(stmt).all())
