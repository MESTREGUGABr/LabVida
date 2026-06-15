from pathlib import Path

from src.config import get_auth_config


def test_auth_config_loads_from_dotenv(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("AUTH0_DOMAIN", raising=False)
    monkeypatch.delenv("AUTH0_CLIENT_ID", raising=False)
    monkeypatch.delenv("AUTH0_CLIENT_SECRET", raising=False)
    monkeypatch.delenv("APP_BASE_URL", raising=False)

    (tmp_path / ".env").write_text(
        "AUTH0_DOMAIN=labvida-test.auth0.com\n"
        "AUTH0_CLIENT_ID=test-client-id\n"
        "AUTH0_CLIENT_SECRET=test-client-secret\n"
        "APP_BASE_URL=http://localhost:8501\n"
    )

    config = get_auth_config()

    assert config.domain == "labvida-test.auth0.com"
    assert config.client_id == "test-client-id"
    assert config.client_secret == "test-client-secret"
    assert config.redirect_uri == "http://localhost:8501"


def test_auth_config_prefers_environment_over_dotenv(
    monkeypatch,
    tmp_path: Path,
) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("AUTH0_DOMAIN", "env.auth0.com")
    monkeypatch.setenv("AUTH0_CLIENT_ID", "env-client-id")
    monkeypatch.setenv("AUTH0_CLIENT_SECRET", "env-client-secret")
    monkeypatch.setenv("APP_BASE_URL", "http://env.localhost:8501")

    (tmp_path / ".env").write_text(
        "AUTH0_DOMAIN=dotenv.auth0.com\n"
        "AUTH0_CLIENT_ID=dotenv-client-id\n"
        "AUTH0_CLIENT_SECRET=dotenv-client-secret\n"
        "APP_BASE_URL=http://dotenv.localhost:8501\n"
    )

    config = get_auth_config()

    assert config.domain == "env.auth0.com"
    assert config.client_id == "env-client-id"
    assert config.client_secret == "env-client-secret"
    assert config.redirect_uri == "http://env.localhost:8501"
