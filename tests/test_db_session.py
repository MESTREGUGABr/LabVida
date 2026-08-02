"""Regressão: `session_scope` precisa fazer rollback quando o bloco falha.

Antes havia só `finally: session.close()`. Uma exceção no meio de um service que
já tinha dado flush deixava a transação suja até o close, e o comportamento
dependia de detalhe de implementação do SQLAlchemy em vez de ser explícito.
"""

import uuid

import pytest
from sqlalchemy import select, text

from src.cadastro.unidade.models import Unidade
from src.db import engine, session_scope


def test_flush_sem_commit_nao_persiste_quando_o_bloco_falha() -> None:
    nome = f"Unidade Rollback {uuid.uuid4().hex[:8]}"

    with pytest.raises(RuntimeError, match="falha proposital"):
        with session_scope() as session:
            session.add(Unidade(nome=nome, tipo="CENTRAL"))
            session.flush()  # a linha existe na transação, mas não foi commitada
            raise RuntimeError("falha proposital")

    with session_scope() as session:
        encontrada = session.scalar(select(Unidade).where(Unidade.nome == nome))

    assert encontrada is None


def test_sessao_seguinte_nao_herda_transacao_abortada() -> None:
    """Erro de SQL numa sessão não pode contaminar a próxima que pegar a conexão."""
    with pytest.raises(Exception):
        with session_scope() as session:
            session.execute(text("SELECT * FROM tabela_que_nao_existe"))

    with session_scope() as session:
        assert session.execute(text("SELECT 1")).scalar_one() == 1


def test_engine_configurado_para_conexao_ociosa() -> None:
    """`pool_pre_ping` descarta conexão morta antes da query, em vez de estourar."""
    assert engine.pool._pre_ping is True
