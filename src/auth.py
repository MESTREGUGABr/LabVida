"""Auth0 OAuth 2.0 / OIDC authentication with PKCE."""

import base64
import hashlib
import secrets
from dataclasses import dataclass
from urllib.parse import urlencode

import httpx


@dataclass
class AuthConfig:
    domain: str
    client_id: str
    client_secret: str
    redirect_uri: str = "http://localhost:8501"


@dataclass
class User:
    name: str
    email: str
    picture: str | None = None


def _base64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def generate_pkce() -> tuple[str, str]:
    code_verifier = secrets.token_urlsafe(64)
    digest = hashlib.sha256(code_verifier.encode()).digest()
    code_challenge = _base64url(digest)
    return code_verifier, code_challenge


def build_login_url(config: AuthConfig) -> tuple[str, str]:
    code_verifier, code_challenge = generate_pkce()

    params = {
        "response_type": "code",
        "client_id": config.client_id,
        "redirect_uri": config.redirect_uri,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "scope": "openid profile email",
        "state": code_verifier,
        "connection": "google-oauth2",
    }
    url = f"https://{config.domain}/authorize?{urlencode(params)}"
    return url, code_verifier


def exchange_code(
    config: AuthConfig,
    code: str,
    code_verifier: str,
) -> dict:
    response = httpx.post(
        f"https://{config.domain}/oauth/token",
        json={
            "grant_type": "authorization_code",
            "client_id": config.client_id,
            "client_secret": config.client_secret,
            "code": code,
            "redirect_uri": config.redirect_uri,
            "code_verifier": code_verifier,
        },
    )
    response.raise_for_status()
    return response.json()


def fetch_user(config: AuthConfig, access_token: str) -> User:
    response = httpx.get(
        f"https://{config.domain}/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    response.raise_for_status()
    data = response.json()
    return User(
        name=data.get("name", ""),
        email=data.get("email", ""),
        picture=data.get("picture"),
    )


def build_logout_url(config: AuthConfig) -> str:
    params = {
        "client_id": config.client_id,
        "returnTo": config.redirect_uri,
    }
    return f"https://{config.domain}/v2/logout?{urlencode(params)}"
