from collections.abc import Iterator

import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.db import session_scope


_TABELAS = (
    "coletas",
    "amostras",
    "autorizacoes_convenio",
    "os_status_historico",
    "os_itens",
    "ordens_servico",
    "procedimento_valores",
    "medicos",
    "procedimentos",
    "convenios",
    "setores",
    "unidades",
    "usuarios",
    "pacientes",
)


def _limpar(session: Session) -> None:
    session.execute(text("TRUNCATE " + ", ".join(_TABELAS) + " RESTART IDENTITY CASCADE"))
    session.commit()


@pytest.fixture()
def session() -> Iterator[Session]:
    with session_scope() as session:
        _limpar(session)
        yield session
        _limpar(session)
