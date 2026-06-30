import os

from dotenv import load_dotenv

from src.auth import AuthConfig


def get_database_url() -> str:
    load_dotenv(dotenv_path=".env")
    return _get_required_env("DATABASE_URL")


def get_auth_config() -> AuthConfig:
    load_dotenv(dotenv_path=".env")

    return AuthConfig(
        domain=_get_required_env("AUTH0_DOMAIN"),
        client_id=_get_required_env("AUTH0_CLIENT_ID"),
        client_secret=_get_required_env("AUTH0_CLIENT_SECRET"),
        redirect_uri=os.environ.get("APP_BASE_URL", "http://localhost:8501"),
    )


def _get_required_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"{name} environment variable is required")
    return value
