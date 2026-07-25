from uuid import UUID

from sqlalchemy.orm import Session

from src.compras.insumo import repository
from src.compras.insumo.dtos import EstoqueMovimentoRead, InsumoCreate, InsumoRead
from src.compras.insumo.errors import InsumoNaoEncontrado
from src.compras.insumo.models import InsumoMaterial


def criar_insumo(session: Session, dto: InsumoCreate) -> InsumoRead:
    insumo = InsumoMaterial(nome=dto.nome, finalidade=dto.finalidade)
    repository.salvar_insumo(session, insumo)
    session.commit()
    session.refresh(insumo)
    return InsumoRead.model_validate(insumo)


def listar_insumos(session: Session) -> list[InsumoRead]:
    return [InsumoRead.model_validate(i) for i in repository.listar_insumos(session)]


def obter_insumo(session: Session, insumo_id: UUID) -> InsumoRead:
    insumo = repository.obter_insumo_por_id(session, insumo_id)
    if insumo is None:
        raise InsumoNaoEncontrado("Insumo não encontrado")
    return InsumoRead.model_validate(insumo)


def listar_movimentos_por_insumo(session: Session, insumo_id: UUID) -> list[EstoqueMovimentoRead]:
    return [
        EstoqueMovimentoRead.model_validate(m)
        for m in repository.listar_movimentos_por_insumo(session, insumo_id)
    ]


def listar_todos_movimentos(session: Session) -> list[EstoqueMovimentoRead]:
    return [
        EstoqueMovimentoRead.model_validate(m)
        for m in repository.listar_todos_movimentos(session)
    ]
