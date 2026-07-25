from uuid import UUID

from sqlalchemy.orm import Session

from src.compras.fornecedor import repository
from src.compras.fornecedor.dtos import FornecedorCreate, FornecedorRead, StatusFornecedor
from src.compras.fornecedor.errors import CnpjDuplicado, FornecedorNaoEncontrado
from src.compras.fornecedor.models import Fornecedor


def criar_fornecedor(session: Session, dto: FornecedorCreate) -> FornecedorRead:
    existente = repository.obter_por_cnpj(session, dto.cnpj)
    if existente is not None:
        raise CnpjDuplicado(f"CNPJ {dto.cnpj} já cadastrado")

    fornecedor = Fornecedor(nome=dto.nome, cnpj=dto.cnpj, status=StatusFornecedor.ATIVO)
    repository.salvar(session, fornecedor)
    session.commit()
    session.refresh(fornecedor)
    return FornecedorRead.model_validate(fornecedor)


def alternar_status(session: Session, fornecedor_id: UUID, ativo: bool) -> FornecedorRead:
    fornecedor = repository.obter_por_id(session, fornecedor_id)
    if fornecedor is None:
        raise FornecedorNaoEncontrado("Fornecedor não encontrado")
    fornecedor.status = StatusFornecedor.ATIVO if ativo else StatusFornecedor.INATIVO
    session.commit()
    session.refresh(fornecedor)
    return FornecedorRead.model_validate(fornecedor)


def listar_ativos(session: Session) -> list[FornecedorRead]:
    return [FornecedorRead.model_validate(f) for f in repository.listar_ativos(session)]


def listar_todos(session: Session) -> list[FornecedorRead]:
    return [FornecedorRead.model_validate(f) for f in repository.listar_todos(session)]


def obter_por_id(session: Session, fornecedor_id: UUID) -> FornecedorRead:
    fornecedor = repository.obter_por_id(session, fornecedor_id)
    if fornecedor is None:
        raise FornecedorNaoEncontrado("Fornecedor não encontrado")
    return FornecedorRead.model_validate(fornecedor)


def editar_fornecedor(session: Session, fornecedor_id: UUID, nome: str) -> FornecedorRead:
    fornecedor = repository.obter_por_id(session, fornecedor_id)
    if fornecedor is None:
        raise FornecedorNaoEncontrado("Fornecedor não encontrado")
    fornecedor.nome = nome.strip()
    session.commit()
    session.refresh(fornecedor)
    return FornecedorRead.model_validate(fornecedor)
