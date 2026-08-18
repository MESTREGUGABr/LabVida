"""Teste de regressao para formatacao de titulos vencidos no alerta da Visao Executiva."""

import re
from datetime import date
from decimal import Decimal
from pathlib import Path
import pytest
from streamlit.testing.v1 import AppTest
from sqlalchemy.orm import Session

from src.compras.pedido_compra.models import PedidoCompra  # noqa: F401
from src.financeiro.titulo_pagar.models import TituloPagar
from src.logistica.malote.models import Malote  # noqa: F401
from src.db import session_scope
from tests.bi._helpers import coletar, criar_os, faturar, liberar_laudos, montar_cadastros, titulo_receber, utc

PROJECT_ROOT = Path(__file__).parent.parent.parent


def test_alerta_titulos_vencidos_sem_corrupcao_latex_markdown(session: Session, monkeypatch) -> None:
    """Verifica se o alerta de titulos vencidos (com titulos a receber e a pagar)

    nao passa delimitadores de LaTeX '$...$' sem escape para o Streamlit (o que corrompe
    o texto entre os dois 'R$' transformando em formula matematica KaTeX).
    """
    monkeypatch.setattr("src.ui.renderizar_menu", lambda *args, **kwargs: None)

    cenario = montar_cadastros(session)
    ordem = criar_os(session, cenario, aberta_em=utc(2026, 1, 10))
    coletar(session, cenario, ordem, coletada_em=utc(2026, 1, 10, 8))
    laudos = liberar_laudos(session, ordem, liberado_em=utc(2026, 1, 11))
    lote = faturar(session, cenario, laudos, fechado_em=utc(2026, 1, 12), valor=Decimal("2726.98"))
    titulo_receber(session, lote, valor=Decimal("2726.98"), vencimento=date(2020, 1, 1), status="PENDENTE")

    session.add(
        TituloPagar(
            pedido_compra_id=None, valor=Decimal("12502.78"),
            vencimento=date(2020, 1, 1), status="PENDENTE",
        )
    )
    session.commit()

    from src.usuario.service import sincronizar_usuario
    email = "test_alerta@labvida.test"
    with session_scope() as sessao:
        usuario = sincronizar_usuario(sessao, email, "Gestor BI")
        usuario_logado = {"id": str(usuario.id), "name": "Gestor BI", "email": email}

    app = AppTest.from_file(str(PROJECT_ROOT / "pages" / "bi_visao_executiva.py"), default_timeout=60)
    app.session_state["user"] = usuario_logado
    app.run()

    assert not app.exception, f"Pagina quebrou: {app.exception}"

    # Localiza o warning de titulos vencidos
    warnings_titulos = [w for w in app.warning if "Titulos vencidos:" in w.value]
    assert len(warnings_titulos) == 1, f"Alerta de titulos vencidos nao encontrado: {app.warning}"

    texto_alerta = warnings_titulos[0].value
    # Se houver delimitadores '$' nao escapados (ex: 'R$ 2.726,98 ... R$ 12.502,78'),
    # o parser de markdown do Streamlit (remark-math/KaTeX) interpreta o conteudo
    # intermediario como expressao matematica LaTeX, corrompendo a tipografia na tela.
    # Exige que simbolos de cifrao '$' em alertas markdown sejam escapados com '\\$' ou
    # que nao ocorram pares de '$' nao escapados no texto.
    dolares_nao_escapados = re.findall(r"(?<!\\)\$", texto_alerta)
    assert len(dolares_nao_escapados) <= 1, (
        f"Alerta contem multiplos '$' nao escapados ({len(dolares_nao_escapados)} encontrados), "
        f"ativando modo matematico LaTeX no Streamlit: '{texto_alerta}'"
    )
