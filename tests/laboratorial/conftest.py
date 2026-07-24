from collections.abc import Iterator

import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.db import session_scope


_TABELAS = (
    "protocolos_recebimento",
    "amostras_movimentacoes",
    "malotes_amostras",
    "malotes",
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


@pytest.fixture()
def session() -> Iterator[Session]:
    with session_scope() as session:
        query = "TRUNCATE " + ", ".join(_TABELAS) + " RESTART IDENTITY CASCADE"
        session.execute(text(query))
        session.commit()
        yield session
        session.execute(text(query))
        session.commit()
