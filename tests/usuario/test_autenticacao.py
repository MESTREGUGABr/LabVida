import uuid
from collections.abc import Iterator

import pytest
from sqlalchemy.orm import Session

from src.db import session_scope
from src.rbac.models import Perfil, PerfilPermissao, Permissao
from src.usuario.errors import CredenciaisInvalidas, EmailInvalido, EmailJaCadastrado
from src.usuario.models import Usuario
from src.usuario.service import alterar_propria_senha, autenticar, criar_usuario_com_senha


def _limpar(session: Session) -> None:
    session.query(Usuario).update({"perfil_id": None})
    session.commit()
    for tabela in (PerfilPermissao, Permissao, Perfil):
        session.query(tabela).delete()
    session.commit()
    session.query(Usuario).delete()
    session.commit()


@pytest.fixture()
def session() -> Iterator[Session]:
    with session_scope() as s:
        _limpar(s)
        yield s
        _limpar(s)


def _semear_perfis(session: Session) -> None:
    session.add_all([Perfil(nome="admin"), Perfil(nome="visualizador")])
    session.commit()


def _email(prefixo: str) -> str:
    return f"{prefixo}_{uuid.uuid4().hex[:8]}@labvida.test"


def test_criar_usuario_com_senha_autentica_depois(session: Session) -> None:
    email = _email("novo")
    criar_usuario_com_senha(session, email, "Novo Usuário", "senha-forte-123")

    logado = autenticar(session, email, "senha-forte-123")
    assert logado.email == email
    assert logado.tem_senha is True


def test_todo_cadastro_vira_admin(session: Session) -> None:
    """Projeto acadêmico, sem produção real: todo cadastro novo vira admin."""
    _semear_perfis(session)
    admin = session.query(Perfil).filter_by(nome="admin").one()

    primeiro = criar_usuario_com_senha(session, _email("admin"), "Admin", "senha-forte-123")
    segundo = criar_usuario_com_senha(session, _email("comum"), "Comum", "senha-forte-123")

    assert primeiro.perfil_id == admin.id
    assert segundo.perfil_id == admin.id


def test_cadastro_com_email_duplicado_falha(session: Session) -> None:
    email = _email("dup")
    criar_usuario_com_senha(session, email, "Original", "senha-forte-123")
    with pytest.raises(EmailJaCadastrado):
        criar_usuario_com_senha(session, email, "Duplicado", "outra-senha-123")


def test_cadastro_com_email_invalido_falha(session: Session) -> None:
    with pytest.raises(EmailInvalido):
        criar_usuario_com_senha(session, "nao-e-email", "Sem Email", "senha-forte-123")


def test_autenticar_com_senha_errada_falha(session: Session) -> None:
    email = _email("errada")
    criar_usuario_com_senha(session, email, "Usuário", "senha-forte-123")
    with pytest.raises(CredenciaisInvalidas):
        autenticar(session, email, "senha-incorreta")


def test_autenticar_email_inexistente_falha(session: Session) -> None:
    with pytest.raises(CredenciaisInvalidas):
        autenticar(session, _email("fantasma"), "qualquer-coisa")


def test_autenticar_usuario_sem_senha_falha(session: Session) -> None:
    """Regressão do bug mais perigoso desta fase: `senha_hash IS NULL` nunca loga."""
    email = _email("sem_senha")
    usuario = Usuario(email=email, nome="Legado sem senha", ativo=True)
    session.add(usuario)
    session.commit()

    with pytest.raises(CredenciaisInvalidas):
        autenticar(session, email, "qualquer-coisa")


def test_autenticar_usuario_inativo_falha(session: Session) -> None:
    email = _email("inativo")
    criado = criar_usuario_com_senha(session, email, "Inativo", "senha-forte-123")
    usuario = session.get(Usuario, criado.id)
    usuario.ativo = False
    session.commit()

    with pytest.raises(CredenciaisInvalidas):
        autenticar(session, email, "senha-forte-123")


def test_alterar_propria_senha_com_senha_atual_correta(session: Session) -> None:
    email = _email("troca")
    criado = criar_usuario_com_senha(session, email, "Troca", "senha-forte-123")

    alterar_propria_senha(session, criado.id, "senha-forte-123", "senha-nova-456")

    autenticar(session, email, "senha-nova-456")
    with pytest.raises(CredenciaisInvalidas):
        autenticar(session, email, "senha-forte-123")


def test_alterar_propria_senha_com_senha_atual_errada_falha(session: Session) -> None:
    email = _email("troca_falha")
    criado = criar_usuario_com_senha(session, email, "Troca Falha", "senha-forte-123")

    with pytest.raises(CredenciaisInvalidas):
        alterar_propria_senha(session, criado.id, "senha-errada", "senha-nova-456")
