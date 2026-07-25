from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.financeiro.titulo_pagar.dtos import StatusTitulo
from src.financeiro.titulo_pagar.models import TituloPagar


def salvar(session: Session, titulo: TituloPagar) -> TituloPagar:
    session.add(titulo)
    return titulo


def obter_por_id(session: Session, titulo_id: UUID) -> TituloPagar | None:
    return session.get(TituloPagar, titulo_id)


def listar_todos(session: Session) -> list[TituloPagar]:
    stmt = select(TituloPagar).order_by(TituloPagar.criado_em.desc())
    return list(session.scalars(stmt).all())


def listar_pendentes(session: Session) -> list[TituloPagar]:
    stmt = (
        select(TituloPagar)
        .where(TituloPagar.status == StatusTitulo.PENDENTE)
        .order_by(TituloPagar.vencimento)
    )
    return list(session.scalars(stmt).all())
