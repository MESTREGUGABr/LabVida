from uuid import UUID

from sqlalchemy.orm import Session

from src.usuario import repository
from src.usuario.dtos import UsuarioRead
from src.usuario.errors import UsuarioNaoEncontrado
from src.usuario.models import Usuario


def sincronizar_usuario(session: Session, email: str, nome: str) -> UsuarioRead:
    """Garante uma linha em `usuarios` para a identidade vinda do Auth0.

    Idempotente por e-mail: cria na primeira vez, atualiza o nome nas seguintes.
    Chamado no login para que coleta/histórico tenham um ator com FK válida.
    """
    email_normalizado = email.strip().lower()
    nome_normalizado = " ".join(nome.strip().split()) or email_normalizado

    usuario = repository.obter_por_email(session, email_normalizado)
    if usuario is None:
        usuario = Usuario(email=email_normalizado, nome=nome_normalizado, ativo=True)
        repository.salvar(session, usuario)
    else:
        usuario.nome = nome_normalizado
        usuario.ativo = True

    session.commit()
    session.refresh(usuario)
    return UsuarioRead.model_validate(usuario)


def obter_usuario_por_id(session: Session, usuario_id: UUID) -> UsuarioRead:
    usuario = repository.obter_por_id(session, usuario_id)
    if usuario is None:
        raise UsuarioNaoEncontrado("Usuário não encontrado")
    return UsuarioRead.model_validate(usuario)

def listar_usuarios(session: Session) -> list[UsuarioRead]:
    return [UsuarioRead.model_validate(u) for u in repository.listar(session)]
