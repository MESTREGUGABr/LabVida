from uuid import UUID

from sqlalchemy.orm import Session

from src.cadastro.unidade import repository
from src.cadastro.unidade.dtos import SetorCreate, SetorRead, UnidadeCreate, UnidadeRead
from src.cadastro.unidade.errors import UnidadeNaoEncontrada
from src.cadastro.unidade.models import Setor, Unidade


def criar_unidade(session: Session, dto: UnidadeCreate) -> UnidadeRead:
    unidade = Unidade(nome=dto.nome, tipo=dto.tipo, endereco=dto.endereco, ativo=True)
    repository.salvar_unidade(session, unidade)
    session.commit()
    session.refresh(unidade)
    return UnidadeRead.model_validate(unidade)


def listar_unidades_ativas(session: Session) -> list[UnidadeRead]:
    return [UnidadeRead.model_validate(u) for u in repository.listar_unidades_ativas(session)]


def criar_setor(session: Session, dto: SetorCreate) -> SetorRead:
    if repository.obter_unidade_por_id(session, dto.unidade_id) is None:
        raise UnidadeNaoEncontrada("Unidade não encontrada")

    setor = Setor(unidade_id=dto.unidade_id, nome=dto.nome, ativo=True)
    repository.salvar_setor(session, setor)
    session.commit()
    session.refresh(setor)
    return SetorRead.model_validate(setor)


def listar_setores_ativos(session: Session, unidade_id: UUID) -> list[SetorRead]:
    return [SetorRead.model_validate(s) for s in repository.listar_setores_ativos(session, unidade_id)]
