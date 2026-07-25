from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.compras.insumo.models import EstoqueMovimento, InsumoMaterial


def salvar_insumo(session: Session, insumo: InsumoMaterial) -> InsumoMaterial:
    session.add(insumo)
    return insumo


def obter_insumo_por_id(session: Session, insumo_id: UUID) -> InsumoMaterial | None:
    return session.get(InsumoMaterial, insumo_id)


def listar_insumos(session: Session) -> list[InsumoMaterial]:
    stmt = select(InsumoMaterial).order_by(InsumoMaterial.nome)
    return list(session.scalars(stmt).all())


def salvar_movimento(session: Session, mov: EstoqueMovimento) -> EstoqueMovimento:
    session.add(mov)
    return mov


def listar_movimentos_por_insumo(session: Session, insumo_id: UUID) -> list[EstoqueMovimento]:
    stmt = (
        select(EstoqueMovimento)
        .where(EstoqueMovimento.insumo_material_id == insumo_id)
        .order_by(EstoqueMovimento.ocorrido_em.desc())
    )
    return list(session.scalars(stmt).all())


def listar_todos_movimentos(session: Session) -> list[EstoqueMovimento]:
    stmt = select(EstoqueMovimento).order_by(EstoqueMovimento.ocorrido_em.desc())
    return list(session.scalars(stmt).all())
