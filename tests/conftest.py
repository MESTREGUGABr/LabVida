import os
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def _garantir_chave_lgpd_valida() -> None:
    """Garante uma LGPD_ENCRYPTION_KEY valida (Fernet) para a sessao de testes.

    O cadastro de paciente criptografa o CPF na origem; sem uma chave Fernet
    valida no ambiente, qualquer teste que crie paciente quebra. Se a chave
    estiver ausente ou invalida, define uma chave de teste deterministica.
    """
    from cryptography.fernet import Fernet

    chave = os.environ.get("LGPD_ENCRYPTION_KEY", "")
    try:
        Fernet(chave.encode())
    except (ValueError, TypeError):
        os.environ["LGPD_ENCRYPTION_KEY"] = "Q22r1OivohTtSBRaMi-hjLxXxrQ3SwEdOumlaNDfvw8="


_garantir_chave_lgpd_valida()
