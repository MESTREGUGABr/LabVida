"""Metricas de alerta (Visao Executiva) — titulos vencidos e malotes sem
retorno. Sao consultas do estado ATUAL (nao recebem `Periodo`), entao os
testes usam datas ancoradas em `date.today()`/`datetime.now()` em vez de
datas fixas de 2026.
"""

from datetime import date, datetime, timedelta, timezone
from decimal import Decimal

from sqlalchemy.orm import Session

from src.bi import metricas
from src.financeiro.titulo_pagar.models import TituloPagar
from src.logistica.malote.models import Malote
from tests.bi._helpers import coletar, criar_os, faturar, liberar_laudos, montar_cadastros, titulo_receber, utc


def test_alertas_titulos_vencidos_combina_receber_e_pagar(session: Session) -> None:
    cenario = montar_cadastros(session)
    ordem = criar_os(session, cenario, aberta_em=utc(2026, 1, 10))
    coletar(session, cenario, ordem, coletada_em=utc(2026, 1, 10, 8))
    laudos = liberar_laudos(session, ordem, liberado_em=utc(2026, 1, 11))
    lote = faturar(session, cenario, laudos, fechado_em=utc(2026, 1, 12), valor=Decimal("50.00"))
    titulo_receber(session, lote, valor=Decimal("50.00"), vencimento=date(2020, 1, 1), status="PENDENTE")

    session.add(
        TituloPagar(
            pedido_compra_id=None, valor=Decimal("80.00"),
            vencimento=date(2020, 1, 1), status="PENDENTE",
        )
    )
    session.commit()

    df = metricas.alertas_titulos_vencidos(session)

    assert set(df["tipo"]) == {"A receber", "A pagar"}
    assert (df["dias_atraso"] > 0).all()


def test_alertas_titulos_vencidos_ignora_pagos_e_futuros(session: Session) -> None:
    session.add(
        TituloPagar(
            pedido_compra_id=None, valor=Decimal("10.00"),
            vencimento=date(2020, 1, 1), status="PAGO",
        )
    )
    session.add(
        TituloPagar(
            pedido_compra_id=None, valor=Decimal("10.00"),
            vencimento=date(2099, 1, 1), status="PENDENTE",
        )
    )
    session.commit()

    df = metricas.alertas_titulos_vencidos(session)
    assert df.empty


def test_alertas_malotes_sem_retorno_respeita_dias_limite(session: Session) -> None:
    cenario = montar_cadastros(session)
    agora = datetime.now(timezone.utc)

    antigo = Malote(
        codigo_malote="ML-ANTIGO",
        unidade_origem_id=cenario.unidade_coleta,
        unidade_destino_id=cenario.unidade_central,
        enviado_por_usuario_id=cenario.usuario,
        status="EM_TRANSITO",
        despachado_em=agora - timedelta(days=10),
    )
    recente = Malote(
        codigo_malote="ML-RECENTE",
        unidade_origem_id=cenario.unidade_coleta,
        unidade_destino_id=cenario.unidade_central,
        enviado_por_usuario_id=cenario.usuario,
        status="EM_TRANSITO",
        despachado_em=agora - timedelta(hours=1),
    )
    recebido = Malote(
        codigo_malote="ML-RECEBIDO",
        unidade_origem_id=cenario.unidade_coleta,
        unidade_destino_id=cenario.unidade_central,
        enviado_por_usuario_id=cenario.usuario,
        status="RECEBIDO",
        despachado_em=agora - timedelta(days=10),
    )
    session.add_all([antigo, recente, recebido])
    session.commit()

    df = metricas.alertas_malotes_sem_retorno(session, dias_limite=2)

    assert list(df["codigo_malote"]) == ["ML-ANTIGO"]
    assert df.iloc[0]["dias_em_transito"] >= 9
