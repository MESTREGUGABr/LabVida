import sys
from pathlib import Path

from streamlit.testing.v1 import AppTest

PROJECT_ROOT = Path(__file__).parent.parent


def test_login_page_renders() -> None:
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))

    app = AppTest.from_file(str(PROJECT_ROOT / "app.py"))
    app.run()

    assert not app.exception

    all_markdown = " ".join(md.value for md in app.markdown)
    assert "LabVida" in all_markdown
    assert "Entrar com Google" in all_markdown


def test_home_page_redirects_when_not_logged_in() -> None:
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))

    app = AppTest.from_file(str(PROJECT_ROOT / "pages" / "home.py"))
    app.run()

    assert not app.exception
