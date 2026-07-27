from collections.abc import Iterator
from datetime import date
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

PROJECT_ROOT = Path(__file__).parent.parent


@pytest.fixture()
def usuario_logado(monkeypatch) -> dict:
    """Simula a sessao pos-login: usuario sincronizado do Auth0 (shell exige user["id"]).

    O menu lateral usa st.page_link, que exige o registro de paginas MPA — indisponivel
    quando o AppTest roda uma pagina isolada. Neutralizamos o menu para focar na pagina.
    """
    import uuid
    from src.db import session_scope
    from src.usuario.service import sincronizar_usuario

    monkeypatch.setattr("src.ui.renderizar_menu", lambda *args, **kwargs: None)

    email = f"operador_{uuid.uuid4().hex[:8]}@labvida.test"
    with session_scope() as session:
        usuario = sincronizar_usuario(session, email, "Operador Teste")
        return {
            "id": str(usuario.id),
            "name": "Operador Teste",
            "email": email,
        }



@pytest.fixture()
def paciente_ativo() -> Iterator[None]:
    from src.cadastro.dtos import PacienteCreate
    from src.cadastro.models import Paciente
    from src.cadastro.service import criar_paciente
    from src.db import session_scope

    with session_scope() as session:
        session.query(Paciente).delete()
        session.commit()
        criar_paciente(
            session,
            PacienteCreate(
                cpf="52998224725",
                nome="Ana Maria",
                data_nascimento=date(1996, 7, 18),
                telefone="87999991234",
            ),
        )
        yield
        session.query(Paciente).delete()
        session.commit()


def test_login_page_renders(monkeypatch) -> None:
    monkeypatch.setenv("AUTH0_DOMAIN", "labvida-test.auth0.com")
    monkeypatch.setenv("AUTH0_CLIENT_ID", "test-client-id")
    monkeypatch.setenv("AUTH0_CLIENT_SECRET", "test-client-secret")
    monkeypatch.setenv("APP_BASE_URL", "http://localhost:8501")

    app = AppTest.from_file(str(PROJECT_ROOT / "app.py"))
    app.run()

    assert not app.exception

    all_markdown = " ".join(md.value for md in app.markdown)
    assert "LabVida" in all_markdown
    assert "Entrar com Google" in all_markdown


def test_home_page_redirects_when_not_logged_in() -> None:
    app = AppTest.from_file(str(PROJECT_ROOT / "pages" / "home.py"))
    app.run()

    assert not app.exception


def test_cadastro_pacientes_redirects_when_not_logged_in(monkeypatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://labvida:labvida@postgres:5432/labvida")

    app = AppTest.from_file(str(PROJECT_ROOT / "pages" / "cadastro_pacientes.py"))
    app.run()

    assert not app.exception


def test_cadastro_pacientes_substitui_janela_padrao_por_limite_tecnico(usuario_logado) -> None:
    app = AppTest.from_file(str(PROJECT_ROOT / "pages" / "cadastro_pacientes.py"))
    app.session_state["user"] = usuario_logado
    app.run()

    assert app.date_input[0].min == date(1000, 1, 1)


def test_edicao_paciente_substitui_janela_padrao_por_limite_tecnico(usuario_logado, paciente_ativo) -> None:
    app = AppTest.from_file(str(PROJECT_ROOT / "pages" / "cadastro_pacientes.py"))
    app.session_state["user"] = usuario_logado
    app.run()

    assert app.date_input[1].min == date(1000, 1, 1)


def test_cadastro_convenios_redirects_when_not_logged_in(monkeypatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://labvida:labvida@postgres:5432/labvida")

    app = AppTest.from_file(str(PROJECT_ROOT / "pages" / "cadastro_convenios.py"))
    app.run()

    assert not app.exception


def test_home_quick_links_do_not_use_raw_html_href(usuario_logado, monkeypatch) -> None:
    calls = []
    monkeypatch.setattr("streamlit.page_link", lambda page, label=None, **kwargs: calls.append((page, label)))

    app = AppTest.from_file(str(PROJECT_ROOT / "pages" / "home.py"))
    app.session_state["user"] = usuario_logado
    app.run()

    assert not app.exception
    assert ("pages/atendimento_os.py", "Abrir OS") in calls
    assert ("pages/atendimento_coleta.py", "Registrar Coleta") in calls
    assert ("pages/laboratorio_laudos.py", "Novo Laudo") in calls
    assert ("pages/faturamento_guias.py", "Faturar") in calls


