from uuid import UUID

from sqlalchemy.orm import Session

from src.cadastro.unidade import repository
from src.cadastro.unidade.dtos import SetorCreate, SetorRead, UnidadeCreate, UnidadeRead
from src.cadastro.unidade.errors import UnidadeNaoEncontrada
from src.cadastro.unidade.models import Setor, Unidade
from src.auditoria import registrar_auditoria


def criar_unidade(session: Session, dto: UnidadeCreate, usuario_id: UUID | None = None) -> UnidadeRead:
    unidade = Unidade(nome=dto.nome, tipo=dto.tipo, endereco=dto.endereco, ativo=True)
    repository.salvar_unidade(session, unidade)
    session.commit()
    session.refresh(unidade)

    if usuario_id is not None:
        registrar_auditoria(session, usuario_id, entidade="unidade",
            entidade_id=unidade.id, acao="CRIAR_UNIDADE",
            dados={"nome": unidade.nome, "tipo": unidade.tipo})

    return UnidadeRead.model_validate(unidade)


def listar_unidades_ativas(session: Session) -> list[UnidadeRead]:
    return [UnidadeRead.model_validate(u) for u in repository.listar_unidades_ativas(session)]


def criar_setor(session: Session, dto: SetorCreate, usuario_id: UUID | None = None) -> SetorRead:
    if repository.obter_unidade_por_id(session, dto.unidade_id) is None:
        raise UnidadeNaoEncontrada("Unidade não encontrada")

    setor = Setor(unidade_id=dto.unidade_id, nome=dto.nome, ativo=True)
    repository.salvar_setor(session, setor)
    session.commit()
    session.refresh(setor)

    if usuario_id is not None:
        registrar_auditoria(session, usuario_id, entidade="setor",
            entidade_id=setor.id, acao="CRIAR_SETOR",
            dados={"nome": setor.nome, "unidade_id": str(dto.unidade_id)})

    return SetorRead.model_validate(setor)


def listar_setores_ativos(session: Session, unidade_id: UUID) -> list[SetorRead]:
    return [SetorRead.model_validate(s) for s in repository.listar_setores_ativos(session, unidade_id)]
