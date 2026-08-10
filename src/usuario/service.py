from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from src.usuario import repository
from src.usuario.dtos import UsuarioRead
from src.usuario.email import validar_email
from src.usuario.errors import CredenciaisInvalidas, EmailJaCadastrado, UsuarioNaoEncontrado
from src.usuario.models import Usuario
from src.usuario.senha import hash_senha, verificar_senha

_PERFIL_ADMIN = "admin"


def _to_read(usuario: Usuario) -> UsuarioRead:
    return UsuarioRead.model_validate(usuario).model_copy(
        update={"tem_senha": usuario.senha_hash is not None}
    )


def sincronizar_usuario(session: Session, email: str, nome: str) -> UsuarioRead:
    """Garante uma linha em `usuarios` para a identidade, sem senha.

    Idempotente por e-mail: cria na primeira vez, atualiza o nome nas seguintes.
    Base de `criar_usuario_com_senha` — não define credencial por si só; quem
    chama decide se e como a senha é atribuída. Ao criar, atribui um perfil
    inicial (ver `_atribuir_perfil_inicial`).
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
    return _to_read(usuario)


def criar_usuario_com_senha(session: Session, email: str, nome: str, senha: str) -> UsuarioRead:
    """Cadastro local (aba "Criar conta"). Reaproveita `sincronizar_usuario` +
    `_atribuir_perfil_inicial` (todo cadastro novo vira `admin` — projeto
    acadêmico, ver docstring de `_atribuir_perfil_inicial`) e só então define
    a senha.
    """
    email_normalizado = email.strip().lower()
    validar_email(email_normalizado)
    if repository.obter_por_email(session, email_normalizado) is not None:
        raise EmailJaCadastrado("Este e-mail já está cadastrado.")

    senha_hash = hash_senha(senha)  # valida a política antes de tocar o banco

    usuario_read = sincronizar_usuario(session, email_normalizado, nome)
    usuario = repository.obter_por_id(session, usuario_read.id)
    usuario.senha_hash = senha_hash
    usuario.senha_definida_em = datetime.now(timezone.utc)
    session.commit()
    session.refresh(usuario)
    return _to_read(usuario)


def autenticar(session: Session, email: str, senha: str) -> UsuarioRead:
    """Aba "Entrar". Uma única exceção para todo caso de falha — e-mail
    inexistente, senha errada, conta sem senha ou conta inativa — para não dar
    a um invasor nenhuma pista sobre qual dessas situações ocorreu.
    """
    email_normalizado = email.strip().lower()
    usuario = repository.obter_por_email(session, email_normalizado)

    senha_hash = usuario.senha_hash if usuario is not None else None
    senha_ok = verificar_senha(senha, senha_hash)

    if usuario is None or not usuario.ativo or not senha_ok:
        raise CredenciaisInvalidas("E-mail ou senha inválidos.")

    return _to_read(usuario)


def definir_senha(session: Session, usuario_id: UUID, nova_senha: str) -> UsuarioRead:
    """Usada pelo admin (cadastro/redefinição) e por `alterar_propria_senha`."""
    usuario = repository.obter_por_id(session, usuario_id)
    if usuario is None:
        raise UsuarioNaoEncontrado("Usuário não encontrado")

    usuario.senha_hash = hash_senha(nova_senha)
    usuario.senha_definida_em = datetime.now(timezone.utc)
    session.commit()
    session.refresh(usuario)
    return _to_read(usuario)


def alterar_propria_senha(
    session: Session, usuario_id: UUID, senha_atual: str, nova_senha: str
) -> UsuarioRead:
    usuario = repository.obter_por_id(session, usuario_id)
    if usuario is None:
        raise UsuarioNaoEncontrado("Usuário não encontrado")

    if not verificar_senha(senha_atual, usuario.senha_hash):
        raise CredenciaisInvalidas("Senha atual incorreta.")

    return definir_senha(session, usuario_id, nova_senha)


def _atribuir_perfil_inicial(session: Session, usuario: Usuario) -> None:
    """Define o perfil de um usuário recém-criado, encerrando o acesso plano.

    Projeto acadêmico, sem produção real: todo cadastro novo recebe `admin`
    diretamente, sem distinguir "primeiro usuário" — decisão deliberada para
    facilitar testes (qualquer conta criada já pode administrar o sistema).
    Se o RBAC ainda não foi semeado (perfil `admin` inexistente), mantém
    `perfil_id=None` — o shell cai no fallback de acesso plano (ADR 0002).
    """
    from src.rbac import repository as rbac_repository

    admin = rbac_repository.obter_perfil_por_nome(session, _PERFIL_ADMIN)
    if admin is not None:
        usuario.perfil_id = admin.id


def obter_usuario_por_id(session: Session, usuario_id: UUID) -> UsuarioRead:
    usuario = repository.obter_por_id(session, usuario_id)
    if usuario is None:
        raise UsuarioNaoEncontrado("Usuário não encontrado")
    return _to_read(usuario)


def listar_usuarios(session: Session) -> list[UsuarioRead]:
    return [_to_read(u) for u in repository.listar(session)]
