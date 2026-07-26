from collections.abc import Sequence
from uuid import UUID

from sqlalchemy.orm import Session

from src.rbac import repository
from src.rbac.dtos import PerfilCreate, PerfilRead, PermissaoRead
from src.rbac.errors import PerfilDuplicado, PerfilNaoEncontrado
from src.rbac.models import Perfil, PerfilPermissao, Permissao
from src.usuario import repository as usuario_repository
from src.usuario.errors import UsuarioNaoEncontrado


def criar_perfil(session: Session, dto: PerfilCreate) -> PerfilRead:
    existente = repository.obter_perfil_por_nome(session, dto.nome)
    if existente is not None:
        raise PerfilDuplicado(f"Perfil '{dto.nome}' já existe")

    perfil = Perfil(nome=dto.nome, descricao=dto.descricao)
    repository.salvar_perfil(session, perfil)
    session.commit()
    session.refresh(perfil)
    return PerfilRead.model_validate(perfil)


def listar_perfis(session: Session) -> Sequence[PerfilRead]:
    return [PerfilRead.model_validate(p) for p in repository.listar_perfis(session)]


def listar_permissoes(session: Session) -> Sequence[PermissaoRead]:
    return [PermissaoRead.model_validate(p) for p in repository.listar_permissoes(session)]


def listar_permissoes_do_perfil(session: Session, perfil_id: UUID) -> Sequence[PermissaoRead]:
    perfil = repository.obter_perfil_por_id(session, perfil_id)
    if perfil is None:
        raise PerfilNaoEncontrado(f"Perfil '{perfil_id}' não encontrado")
    return [
        PermissaoRead.model_validate(p)
        for p in repository.listar_permissoes_por_perfil(session, perfil_id)
    ]


def atribuir_permissao_ao_perfil(
    session: Session, perfil_id: UUID, permissao_id: UUID
) -> PerfilRead:
    perfil = repository.obter_perfil_por_id(session, perfil_id)
    if perfil is None:
        raise PerfilNaoEncontrado(f"Perfil '{perfil_id}' não encontrado")

    permissao = session.get(Permissao, permissao_id)
    if permissao is None:
        raise PerfilNaoEncontrado(f"Permissão '{permissao_id}' não encontrada")

    vinculo = PerfilPermissao(perfil_id=perfil_id, permissao_id=permissao_id)
    repository.vincular_permissao(session, vinculo)
    session.commit()
    session.refresh(perfil)
    return PerfilRead.model_validate(perfil)


def listar_permissoes_do_usuario(session: Session, usuario_id: UUID) -> Sequence[PermissaoRead]:
    return [
        PermissaoRead.model_validate(p)
        for p in repository.listar_permissoes_por_usuario(session, usuario_id)
    ]


def vincular_usuario_ao_perfil(session: Session, usuario_id: UUID, perfil_id: UUID) -> None:
    usuario = usuario_repository.obter_por_id(session, usuario_id)
    if usuario is None:
        raise UsuarioNaoEncontrado("Usuário não encontrado")

    perfil = repository.obter_perfil_por_id(session, perfil_id)
    if perfil is None:
        raise PerfilNaoEncontrado(f"Perfil '{perfil_id}' não encontrado")

    usuario.perfil_id = perfil_id
    session.commit()
