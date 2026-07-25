from collections.abc import Iterator

import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.db import session_scope


_TABELAS = (
    "conciliacoes_pagamento",
    "movimentos_caixa",
    "estoque_movimentos",
    "pedidos_itens",
    "recebimentos_insumo",
    "titulos_pagar",
    "titulos_receber",
    "glosas",
    "guias_itens",
    "pedidos_compra",
    "guias_tiss",
    "solicitacoes_compra",
    "lotes_faturamento",
    "insumos_materiais",
    "fornecedores",
    "resultados_auditoria",
    "laudos",
    "resultados",
    "valores_referencia",
    "equipamentos",
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


def _limpar(session: Session) -> None:
    session.execute(text("TRUNCATE " + ", ".join(_TABELAS) + " RESTART IDENTITY CASCADE"))
    session.commit()


@pytest.fixture()
def session() -> Iterator[Session]:
    with session_scope() as session:
        _limpar(session)
        yield session
        _limpar(session)
