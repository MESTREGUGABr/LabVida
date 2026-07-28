from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.rbac.models import Perfil, PerfilPermissao, Permissao
from src.usuario.models import Usuario


def obter_perfil_por_id(session: Session, perfil_id: UUID) -> Perfil | None:
    return session.get(Perfil, perfil_id)


def obter_perfil_por_nome(session: Session, nome: str) -> Perfil | None:
    return session.scalar(select(Perfil).where(Perfil.nome == nome))


def listar_perfis(session: Session) -> Sequence[Perfil]:
    return session.scalars(select(Perfil).order_by(Perfil.nome)).all()


def salvar_perfil(session: Session, perfil: Perfil) -> Perfil:
    session.add(perfil)
    return perfil


def obter_permissao_por_codigo(session: Session, codigo: str) -> Permissao | None:
    return session.scalar(select(Permissao).where(Permissao.codigo == codigo))


def listar_permissoes(session: Session) -> Sequence[Permissao]:
    return session.scalars(select(Permissao).order_by(Permissao.codigo)).all()


def salvar_permissao(session: Session, permissao: Permissao) -> Permissao:
    session.add(permissao)
    return permissao


def vincular_permissao(session: Session, vinculo: PerfilPermissao) -> PerfilPermissao:
    session.add(vinculo)
    return vinculo


def listar_permissoes_por_perfil(session: Session, perfil_id: UUID) -> Sequence[Permissao]:
    return session.scalars(
        select(Permissao)
        .join(PerfilPermissao, PerfilPermissao.permissao_id == Permissao.id)
        .where(PerfilPermissao.perfil_id == perfil_id)
        .order_by(Permissao.codigo)
    ).all()


def listar_permissoes_por_usuario(session: Session, usuario_id: UUID) -> Sequence[Permissao]:
    usuario = session.get(Usuario, usuario_id)
    if usuario is None or usuario.perfil_id is None:
        return []
    return listar_permissoes_por_perfil(session, usuario.perfil_id)


def usuario_tem_permissao(session: Session, usuario_id: UUID, codigo_permissao: str) -> bool:
    usuario = session.get(Usuario, usuario_id)
    if usuario is None or usuario.perfil_id is None:
        return False

    return session.scalar(
        select(Permissao)
        .join(PerfilPermissao, PerfilPermissao.permissao_id == Permissao.id)
        .where(
            PerfilPermissao.perfil_id == usuario.perfil_id,
            Permissao.codigo == codigo_permissao,
        )
    ) is not None


def remover_permissao(session: Session, perfil_id: UUID, permissao_id: UUID) -> None:
    vinculo = session.scalar(
        select(PerfilPermissao).where(
            PerfilPermissao.perfil_id == perfil_id,
            PerfilPermissao.permissao_id == permissao_id,
        )
    )
    if vinculo is not None:
        session.delete(vinculo)
