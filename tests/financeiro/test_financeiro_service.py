from datetime import date, timedelta
from decimal import Decimal

import pytest
from sqlalchemy.orm import Session

import src.compras.pedido_compra.models as _compras  # noqa: F401 — FK resolution

from src.faturamento.lote_faturamento.dtos import GuiaItemCreate, LoteFaturamentoCreate
from src.faturamento.lote_faturamento.service import adicionar_guia_item, criar_lote, fechar_lote, listar_lotes
from src.financeiro.titulo_pagar.dtos import StatusTitulo
from src.financeiro.titulo_pagar.models import TituloPagar
from src.financeiro.titulo_receber.errors import FinanceiroError, TituloReceberJaBaixado, TituloReceberNaoEncontrado
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


def test_baixar_titulo_receber_recarregado_do_banco(session: Session) -> None:
    """Regressão: a tela baixa títulos lidos do banco, não recém-criados.

    Nesse caminho `valor` volta como Decimal enquanto o valor pago chega como
    float — subtrair um do outro estourava TypeError e derrubava toda baixa.
    """
    from src.financeiro.conciliacao_pagamento.service import listar_por_titulo
    from src.financeiro.titulo_receber.models import TituloReceber

    base = montar_base(session)
    titulo = TituloReceber(
        lote_faturamento_id=base.lote_id,
        valor=Decimal("30.87"),
        vencimento=date.today() + timedelta(days=30),
        status="PENDENTE",
    )
    session.add(titulo)
    session.commit()
    session.expire_all()

    resultado = baixar_receber(session, titulo.id, 25.50)

    assert resultado.status == StatusTitulo.PAGO
    conciliacoes = listar_por_titulo(session, titulo.id)
    assert len(conciliacoes) == 1
    assert Decimal(str(conciliacoes[0].divergencia)) == Decimal("5.37")


def test_baixar_titulo_receber_integral_nao_gera_conciliacao(session: Session) -> None:
    from src.financeiro.conciliacao_pagamento.service import listar_por_titulo
    from src.financeiro.titulo_receber.models import TituloReceber

    base = montar_base(session)
    titulo = TituloReceber(
        lote_faturamento_id=base.lote_id,
        valor=Decimal("30.87"),
        vencimento=date.today() + timedelta(days=30),
        status="PENDENTE",
    )
    session.add(titulo)
    session.commit()
    session.expire_all()

    baixar_receber(session, titulo.id, 30.87)

    assert listar_por_titulo(session, titulo.id) == []


def test_baixar_titulo_receber_registra_auditoria(session: Session) -> None:
    from src.auditoria.models import AuditoriaLog
    from src.financeiro.titulo_receber.models import TituloReceber

    base = montar_base(session)
    titulo = TituloReceber(
        lote_faturamento_id=base.lote_id,
        valor=100.00,
        vencimento=date.today() + timedelta(days=30),
        status="PENDENTE",
    )
    session.add(titulo)
    session.commit()

    baixar_receber(session, titulo.id, 100.00, usuario_id=base.usuario_id)

    logs = session.query(AuditoriaLog).filter_by(acao="BAIXAR_TITULO_RECEBER").all()
    assert len(logs) == 1
    assert logs[0].entidade_id == titulo.id
    assert logs[0].usuario_id == base.usuario_id


def test_baixar_titulo_pagar_registra_auditoria(session: Session) -> None:
    from src.auditoria.models import AuditoriaLog

    base = montar_base(session)
    titulo = TituloPagar(
        pedido_compra_id=None,
        valor=250.00,
        vencimento=date.today() + timedelta(days=20),
        status="PENDENTE",
    )
    salvar_pagar(session, titulo)
    session.commit()

    baixar_pagar(session, titulo.id, usuario_id=base.usuario_id)

    logs = session.query(AuditoriaLog).filter_by(acao="BAIXAR_TITULO_PAGAR").all()
    assert len(logs) == 1
    assert logs[0].entidade_id == titulo.id
    assert logs[0].usuario_id == base.usuario_id


def test_baixar_titulo_rejeita_sem_permissao(session: Session) -> None:
    from src.financeiro.titulo_receber.models import TituloReceber
    from src.rbac.models import Perfil
    from src.usuario.service import sincronizar_usuario

    base = montar_base(session)

    perfil = Perfil(nome="financeiro_test", descricao="Sem financeiro")
    session.add(perfil)
    session.flush()

    usuario_sem = sincronizar_usuario(session, "semfinanceiro@labvida.test", "Sem Financeiro")
    usuario_sem.perfil_id = perfil.id
    session.flush()

    titulo = TituloReceber(
        lote_faturamento_id=base.lote_id,
        valor=100.00,
        vencimento=date.today() + timedelta(days=30),
        status="PENDENTE",
    )
    session.add(titulo)
    session.commit()

    with pytest.raises(FinanceiroError, match="sem permissão"):
        baixar_receber(session, titulo.id, 100.00, usuario_id=usuario_sem.id)

    session.query(Perfil).filter_by(id=perfil.id).delete()
    session.flush()
