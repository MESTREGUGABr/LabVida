import os

from dotenv import load_dotenv


# Fuso unico de apuracao da competencia (ADR 0007).
#
# A competencia sai do fato gerador, que e TIMESTAMPTZ em UTC. Um laudo liberado
# as 22h de 28/02 em Garanhuns e 2026-03-01T01:00Z: apurar em UTC jogaria a
# receita para marco. A escolha e IMUTAVEL na pratica — reapurar competencia
# depois que existirem competencias fechadas exige reprocessar todo o ledger.
TZ_OPERACAO = "America/Recife"


def get_database_url() -> str:
    load_dotenv(dotenv_path=".env")
    return _get_required_env("DATABASE_URL")


def get_senha_padrao_seed() -> str:
    """Senha usada pelo seeder para todos os usuários de demonstração (F15).

    Só afeta `python -m src.seeder` — nunca é lida pelo fluxo de login real.
    Tem um default de conveniência para `docker compose up` funcionar de
    primeira; documentado em `.env.exemplo` para quem quiser sobrescrever.
    """
    load_dotenv(dotenv_path=".env")
    return os.environ.get("SENHA_PADRAO_SEED", "labvida123")


def _get_required_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"{name} environment variable is required")
    return value
