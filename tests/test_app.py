from pathlib import Path

from streamlit.testing.v1 import AppTest

PROJECT_ROOT = Path(__file__).parent.parent


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


def test_cadastro_convenios_redirects_when_not_logged_in(monkeypatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://labvida:labvida@postgres:5432/labvida")

    app = AppTest.from_file(str(PROJECT_ROOT / "pages" / "cadastro_convenios.py"))
    app.run()

    assert not app.exception
