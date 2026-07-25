from datetime import date, timedelta

import pytest
from sqlalchemy.orm import Session

import src.compras.pedido_compra.models as _compras  # noqa: F401 — FK resolution

from src.faturamento.lote_faturamento.dtos import GuiaItemCreate, LoteFaturamentoCreate
from src.faturamento.lote_faturamento.service import adicionar_guia_item, criar_lote, fechar_lote, listar_lotes
from src.financeiro.titulo_pagar.dtos import StatusTitulo
from src.financeiro.titulo_pagar.models import TituloPagar
from src.financeiro.titulo_receber.errors import TituloReceberJaBaixado, TituloReceberNaoEncontrado
from src.financeiro.titulo_receber.service import (
    baixar_titulo as baixar_receber,
    listar_pendentes,
    listar_todos,
)
from src.financeiro.titulo_pagar.errors import TituloPagarJaBaixado, TituloPagarNaoEncontrado
from src.financeiro.titulo_pagar.repository import salvar as salvar_pagar
from src.financeiro.titulo_pagar.service import baixar_titulo as baixar_pagar
from src.financeiro.movimento_caixa.service import fluxo_caixa_por_periodo
from tests.financeiro._helpers import montar_base


def test_baixar_titulo_receber(session: Session) -> None:
    base = montar_base(session)

    titulos = listar_pendentes(session)
    assert len(titulos) == 0


def test_baixar_titulo_receber_nao_encontrado(session: Session) -> None:
    from uuid import uuid4

    with pytest.raises(TituloReceberNaoEncontrado):
        baixar_receber(session, uuid4(), 100.0)


def test_baixar_titulo_pagar(session: Session) -> None:
    hoje = date.today()
    titulo = TituloPagar(
        pedido_compra_id=None,
        valor=500.00,
        vencimento=hoje + timedelta(days=30),
        status="PENDENTE",
    )
    salvar_pagar(session, titulo)
    session.commit()

    resultado = baixar_pagar(session, titulo.id)
    assert resultado.status == StatusTitulo.PAGO


def test_baixar_titulo_pagar_ja_pago(session: Session) -> None:
    hoje = date.today()
    titulo = TituloPagar(
        pedido_compra_id=None,
        valor=300.00,
        vencimento=hoje + timedelta(days=15),
        status="PENDENTE",
    )
    salvar_pagar(session, titulo)
    session.commit()

    baixar_pagar(session, titulo.id)

    with pytest.raises(TituloPagarJaBaixado):
        baixar_pagar(session, titulo.id)


def test_fluxo_caixa_vazio(session: Session) -> None:
    hoje = date.today()
    resultado = fluxo_caixa_por_periodo(session, hoje, hoje + timedelta(days=30))
    assert resultado["total_entradas"] == 0
    assert resultado["total_saidas"] == 0
    assert resultado["saldo"] == 0
