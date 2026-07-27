from collections.abc import Iterator

import pytest
from sqlalchemy.orm import Session

from src.db import session_scope
from src.rbac.models import Perfil, PerfilPermissao, Permissao
from src.usuario.models import Usuario
from src.usuario.service import sincronizar_usuario


def _limpar(session: Session) -> None:
    session.query(Usuario).update({"perfil_id": None})
    session.commit()
    for tabela in (PerfilPermissao, Permissao, Perfil):
        session.query(tabela).delete()
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


def test_sem_perfis_semeados_mantem_perfil_nulo(session: Session) -> None:
    usuario = sincronizar_usuario(session, "sem_rbac@labvida.test", "Sem RBAC")
    assert usuario.perfil_id is None


def test_primeiro_usuario_vira_admin(session: Session) -> None:
    _semear_perfis(session)
    admin = session.query(Perfil).filter_by(nome="admin").one()

    usuario = sincronizar_usuario(session, "primeiro@labvida.test", "Primeiro")

    assert usuario.perfil_id == admin.id


def test_usuarios_seguintes_recebem_visualizador(session: Session) -> None:
    _semear_perfis(session)
    admin = session.query(Perfil).filter_by(nome="admin").one()
    visualizador = session.query(Perfil).filter_by(nome="visualizador").one()

    primeiro = sincronizar_usuario(session, "adminboot@labvida.test", "Admin Boot")
    segundo = sincronizar_usuario(session, "comum@labvida.test", "Comum")

    assert primeiro.perfil_id == admin.id
    assert segundo.perfil_id == visualizador.id


def test_relogin_nao_sobrescreve_perfil_existente(session: Session) -> None:
    _semear_perfis(session)
    visualizador = session.query(Perfil).filter_by(nome="visualizador").one()

    # Primeiro usuário vira admin (bootstrap).
    sincronizar_usuario(session, "boot@labvida.test", "Boot")
    # Segundo usuário nasce visualizador...
    segundo = sincronizar_usuario(session, "promovido@labvida.test", "Promovido")
    # ...e é promovido a admin manualmente.
    usuario = session.get(Usuario, segundo.id)
    admin = session.query(Perfil).filter_by(nome="admin").one()
    usuario.perfil_id = admin.id
    session.commit()

    # Novo login do mesmo e-mail não deve rebaixar o perfil.
    relogin = sincronizar_usuario(session, "promovido@labvida.test", "Promovido")
    assert relogin.perfil_id == admin.id
    assert relogin.perfil_id != visualizador.id
