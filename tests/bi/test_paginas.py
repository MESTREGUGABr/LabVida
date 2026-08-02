"""Renderiza os 4 dashboards de verdade, com dados carregados.

Os testes de ETL e de metricas provam que os NUMEROS estao certos; nada disso
garante que a pagina monta. Aqui cada dashboard e executado via `AppTest` sobre
uma base com dados reais — o que pega spec Altair invalida, coluna renomeada e
KeyError de DataFrame vazio antes de a tela quebrar na frente do professor.
"""

import uuid
from decimal import Decimal
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from src.bi.etl import executar_etl
from src.db import session_scope
from tests.bi._helpers import (
    coletar,
    criar_os,
    faturar,
    glosar,
    liberar_laudos,
    montar_cadastros,
    receber_em_caixa,
    titulo_receber,
    transportar,
    utc,
)

PROJECT_ROOT = Path(__file__).parent.parent.parent

_PAGINAS = [
    "bi_visao_executiva.py",
    "bi_produtividade.py",
    "bi_financeiro.py",
    "bi_logistica.py",
]


@pytest.fixture()
def base_carregada(session, monkeypatch) -> dict:
    """Cenario com movimento em dois meses + ETL rodado + usuario logado."""
    # O menu usa st.page_link, que exige registro MPA — indisponivel quando o
    # AppTest roda uma pagina isolada.
    monkeypatch.setattr("src.ui.renderizar_menu", lambda *args, **kwargs: None)

    cenario = montar_cadastros(session)

    ordem = criar_os(
        session,
        cenario,
        aberta_em=utc(2026, 1, 12),
        procedimentos=[cenario.procedimento_bioquimica, cenario.procedimento_hematologia],
        valor=Decimal("120.00"),
    )
    amostra = coletar(session, cenario, ordem, coletada_em=utc(2026, 1, 12, 9))
    transportar(
        session, cenario, amostra,
        despachado_em=utc(2026, 1, 12, 14), recebido_em=utc(2026, 1, 12, 17, 30),
    )
    laudos = liberar_laudos(session, ordem, liberado_em=utc(2026, 1, 13, 9))
    lote = faturar(session, cenario, laudos, fechado_em=utc(2026, 1, 20), valor=Decimal("120.00"))
    glosar(
        session, cenario, lote,
        valor=Decimal("30.00"), motivo="Falta de autorizacao", criado_em=utc(2026, 1, 28),
    )
    titulo = titulo_receber(
        session, lote, valor=Decimal("240.00"), vencimento=__import__("datetime").date(2026, 2, 10)
    )
    receber_em_caixa(session, titulo, valor=Decimal("210.00"), ocorrido_em=utc(2026, 2, 12))

    # Segundo mes, para as series temporais terem mais de um ponto.
    outra = criar_os(session, cenario, aberta_em=utc(2026, 2, 8), valor=Decimal("90.00"))
    coletar(session, cenario, outra, coletada_em=utc(2026, 2, 8, 10))
    laudos_outra = liberar_laudos(session, outra, liberado_em=utc(2026, 2, 9, 10))
    faturar(session, cenario, laudos_outra, fechado_em=utc(2026, 2, 25), valor=Decimal("90.00"))

    executar_etl()

    from src.rbac.repository import obter_perfil_por_nome
    from src.usuario.service import sincronizar_usuario

    email = f"bi_{uuid.uuid4().hex[:8]}@labvida.test"
    with session_scope() as sessao:
        usuario = sincronizar_usuario(sessao, email, "Gestor BI")
        admin = obter_perfil_por_nome(sessao, "admin")
        if admin is not None and usuario.perfil_id is None:
            usuario.perfil_id = admin.id
            sessao.commit()
        return {"id": str(usuario.id), "name": "Gestor BI", "email": email}


@pytest.mark.parametrize("pagina", _PAGINAS)
def test_dashboard_renderiza_com_dados(pagina: str, base_carregada: dict) -> None:
    app = AppTest.from_file(str(PROJECT_ROOT / "pages" / pagina), default_timeout=60)
    app.session_state["user"] = base_carregada
    app.run()

    assert not app.exception, f"{pagina} quebrou: {app.exception}"


@pytest.mark.parametrize("pagina", _PAGINAS)
def test_dashboard_renderiza_sem_dados(pagina: str, session, monkeypatch) -> None:
    """Base vazia nao pode dar traceback — tem que cair no estado vazio.

    E o caminho mais provavel de quebra: DataFrame vazio virando KeyError na
    hora de montar o grafico.
    """
    monkeypatch.setattr("src.ui.renderizar_menu", lambda *args, **kwargs: None)
    executar_etl()  # calendario existe, fatos nao

    from src.usuario.service import sincronizar_usuario

    email = f"bi_vazio_{uuid.uuid4().hex[:8]}@labvida.test"
    with session_scope() as sessao:
        usuario = sincronizar_usuario(sessao, email, "Gestor BI")
        usuario_logado = {"id": str(usuario.id), "name": "Gestor BI", "email": email}

    app = AppTest.from_file(str(PROJECT_ROOT / "pages" / pagina), default_timeout=60)
    app.session_state["user"] = usuario_logado
    app.run()

    assert not app.exception, f"{pagina} quebrou com base vazia: {app.exception}"
