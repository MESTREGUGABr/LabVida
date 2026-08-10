from pathlib import Path

import pytest

from src.config import get_database_url, get_senha_padrao_seed


def test_database_url_loads_from_dotenv(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("DATABASE_URL", raising=False)

    (tmp_path / ".env").write_text(
        "DATABASE_URL=postgresql+psycopg://labvida:labvida@postgres:5432/labvida\n"
    )

    assert get_database_url() == "postgresql+psycopg://labvida:labvida@postgres:5432/labvida"


def test_database_url_prefers_environment_over_dotenv(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://env/db")

    (tmp_path / ".env").write_text("DATABASE_URL=postgresql+psycopg://dotenv/db\n")

    assert get_database_url() == "postgresql+psycopg://env/db"


def test_database_url_rejeita_variavel_obrigatoria_ausente(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("DATABASE_URL", raising=False)

    with pytest.raises(RuntimeError, match="DATABASE_URL environment variable is required"):
        get_database_url()


def test_senha_padrao_seed_usa_default_quando_env_ausente(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("SENHA_PADRAO_SEED", raising=False)
    (tmp_path / ".env").write_text("DATABASE_URL=postgresql+psycopg://x/db\n")

    assert get_senha_padrao_seed() == "labvida123"


def test_senha_padrao_seed_le_da_env(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("SENHA_PADRAO_SEED", "outra-senha-123")

    assert get_senha_padrao_seed() == "outra-senha-123"
