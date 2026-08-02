"""Renderiza TODAS as telas com um usuario logado.

Rede de seguranca da fase F1, que reescreve navegacao, grids e formularios em
sequencia. Um smoke test por pagina custa segundos e pega a classe de erro mais
comum numa refatoracao de UI — import quebrado, coluna renomeada, `KeyError` em
lista vazia — antes de alguem abrir a tela.

Nao valida conteudo: valida que a pagina MONTA. As asserções de conteudo ficam
nos testes por dominio.
"""

import uuid
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from src.db import session_scope

PROJECT_ROOT = Path(__file__).parent.parent
PAGINAS = sorted(p.name for p in (PROJECT_ROOT / "pages").glob("*.py"))


@pytest.fixture(scope="module")
def admin_logado() -> dict:
    """Usuario com perfil admin — vê todas as telas."""
    from src.rbac.repository import obter_perfil_por_nome
    from src.seeder.rbac import executar_seeder_rbac
    from src.usuario.service import sincronizar_usuario

    executar_seeder_rbac()  # idempotente: garante perfis e permissoes

    email = f"smoke_{uuid.uuid4().hex[:8]}@labvida.test"
    with session_scope() as session:
        # `sincronizar_usuario` devolve DTO: o vinculo de perfil tem que ser
        # feito na linha ORM, senao o teste roda em modo bootstrap (acesso
        # plano) e nao exercita o gate de RBAC.
        from src.usuario.models import Usuario

        lido = sincronizar_usuario(session, email, "Smoke Admin")
        usuario = session.get(Usuario, lido.id)
        admin = obter_perfil_por_nome(session, "admin")
        assert admin is not None, "seed de RBAC nao criou o perfil admin"
        usuario.perfil_id = admin.id
        session.commit()
        return {"id": str(usuario.id), "name": "Smoke Admin", "email": email}


def test_ha_paginas_para_testar() -> None:
    """Guarda contra o glob silenciosamente vazio, que faria a suite passar sem
    testar nada."""
    assert len(PAGINAS) >= 25


@pytest.mark.parametrize("pagina", PAGINAS)
def test_pagina_monta(pagina: str, admin_logado: dict, monkeypatch) -> None:
    # `st.page_link` exige o registro de paginas MPA, indisponivel quando o
    # AppTest roda uma pagina isolada. Neutralizamos o menu e o proprio
    # `page_link` (a home usa atalhos diretos) para o teste focar no corpo da
    # tela. Some quando a navegacao migrar para `st.navigation` (F1.2).
    import streamlit

    monkeypatch.setattr("src.ui.renderizar_menu", lambda *args, **kwargs: None)
    monkeypatch.setattr(streamlit, "page_link", lambda *args, **kwargs: None)

    app = AppTest.from_file(str(PROJECT_ROOT / "pages" / pagina), default_timeout=60)
    app.session_state["user"] = admin_logado
    app.run()

    assert not app.exception, f"{pagina} nao monta: {app.exception}"
