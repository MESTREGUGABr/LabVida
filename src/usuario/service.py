from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.usuario import repository
from src.usuario.dtos import UsuarioRead
from src.usuario.errors import UsuarioNaoEncontrado
from src.usuario.models import Usuario

_PERFIL_ADMIN = "admin"
_PERFIL_PADRAO = "visualizador"


def sincronizar_usuario(session: Session, email: str, nome: str) -> UsuarioRead:
    """Garante uma linha em `usuarios` para a identidade vinda do Auth0.

    Idempotente por e-mail: cria na primeira vez, atualiza o nome nas seguintes.
    Chamado no login para que coleta/histórico tenham um ator com FK válida.
    Ao criar, atribui um perfil inicial (ver `_atribuir_perfil_inicial`).
    """
    email_normalizado = email.strip().lower()
    nome_normalizado = " ".join(nome.strip().split()) or email_normalizado

    usuario = repository.obter_por_email(session, email_normalizado)
    if usuario is None:
        usuario = Usuario(email=email_normalizado, nome=nome_normalizado, ativo=True)
        repository.salvar(session, usuario)
        _atribuir_perfil_inicial(session, usuario)
    else:
        usuario.nome = nome_normalizado
        usuario.ativo = True
        if usuario.perfil_id is None:
            _atribuir_perfil_inicial(session, usuario)

    session.commit()
    session.refresh(usuario)
    return UsuarioRead.model_validate(usuario)


def _atribuir_perfil_inicial(session: Session, usuario: Usuario) -> None:
    """Define o perfil de um usuário recém-criado, encerrando o acesso plano.

    Bootstrap: enquanto não houver nenhum admin, o primeiro usuário criado vira
    `admin` (para que exista quem gerencie perfis); os demais recebem o perfil
    mínimo `visualizador`. Se o RBAC ainda não foi semeado (perfis inexistentes),
    mantém `perfil_id=None` — o shell cai no fallback de acesso plano (ADR 0002).
    """
    from src.rbac import repository as rbac_repository

    admin = rbac_repository.obter_perfil_por_nome(session, _PERFIL_ADMIN)
    if admin is None:
        return

    ja_existe_admin = session.scalar(
        select(Usuario.id).where(Usuario.perfil_id == admin.id).limit(1)
    )
    if ja_existe_admin is None:
        usuario.perfil_id = admin.id
        return

    padrao = rbac_repository.obter_perfil_por_nome(session, _PERFIL_PADRAO)
    if padrao is not None:
        usuario.perfil_id = padrao.id


def obter_usuario_por_id(session: Session, usuario_id: UUID) -> UsuarioRead:
    usuario = repository.obter_por_id(session, usuario_id)
    if usuario is None:
        raise UsuarioNaoEncontrado("Usuário não encontrado")
    return UsuarioRead.model_validate(usuario)

def listar_usuarios(session: Session) -> list[UsuarioRead]:
    return [UsuarioRead.model_validate(u) for u in repository.listar(session)]
