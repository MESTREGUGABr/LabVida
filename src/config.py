import os

from dotenv import load_dotenv

from src.auth import AuthConfig


def get_auth_config() -> AuthConfig:
    load_dotenv(dotenv_path=".env")

    return AuthConfig(
        domain=os.environ["AUTH0_DOMAIN"],
        client_id=os.environ["AUTH0_CLIENT_ID"],
        client_secret=os.environ["AUTH0_CLIENT_SECRET"],
        redirect_uri=os.environ.get("APP_BASE_URL", "http://localhost:8501"),
    )
