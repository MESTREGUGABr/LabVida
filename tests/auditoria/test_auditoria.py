from collections.abc import Iterator
from uuid import UUID

import pytest
from sqlalchemy.orm import Session

from src.auditoria import registrar_auditoria
from src.auditoria.models import AuditoriaLog
from src.db import session_scope
from src.usuario.models import Usuario


@pytest.fixture()
def session() -> Iterator[Session]:
    with session_scope() as s:
        s.query(AuditoriaLog).delete()
        s.commit()
        yield s


@pytest.fixture()
def usuario_id(session: Session) -> str:
    from src.usuario.service import sincronizar_usuario
    u = sincronizar_usuario(session, f"auditor_{id(session)}@teste.com", "Auditor Teste")
    return str(u.id)


def test_registrar_auditoria(session: Session, usuario_id: str) -> None:
    uid = UUID(usuario_id)
    registrar_auditoria(session, uid, "ordem_servico", uid, "CRIAR", {"status": "ABERTA"})
    session.commit()

    logs = session.query(AuditoriaLog).all()
    assert len(logs) == 1
    assert logs[0].entidade == "ordem_servico"
    assert logs[0].acao == "CRIAR"
    assert logs[0].dados == {"status": "ABERTA"}


def test_registrar_multiplas_auditorias(session: Session, usuario_id: str) -> None:
    uid = UUID(usuario_id)
    registrar_auditoria(session, uid, "laudo", uid, "LIBERAR", {})
    registrar_auditoria(session, uid, "lote", uid, "FECHAR", {"titulo": "abc"})
    session.commit()

    logs = session.query(AuditoriaLog).all()
    assert len(logs) == 2
