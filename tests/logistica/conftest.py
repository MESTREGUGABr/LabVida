from collections.abc import Iterator

import pytest
from sqlalchemy.orm import Session

from src.db import session_scope
from tests._tabelas import NUCLEO, limpar

# Sem RBAC de proposito: `perfis` vazia poe o gate em modo bootstrap e mudaria
# o que estes testes exercitam.
_TABELAS = NUCLEO


@pytest.fixture()
def session() -> Iterator[Session]:
    with session_scope() as session:
        limpar(session, _TABELAS)
        yield session
        limpar(session, _TABELAS)
