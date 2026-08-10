from collections.abc import Iterator

import pytest
from sqlalchemy.orm import Session

from src.db import session_scope
from tests._tabelas import BI, CICLO_COMPLETO, limpar

# O ETL le o operacional inteiro, entao o cenario precisa nascer do zero nos dois
# lados: senao dado de outro teste entra na carga e quebra as reconciliacoes.
_TABELAS = BI + CICLO_COMPLETO


@pytest.fixture()
def session() -> Iterator[Session]:
    with session_scope() as session:
        limpar(session, _TABELAS)
        yield session
        limpar(session, _TABELAS)
