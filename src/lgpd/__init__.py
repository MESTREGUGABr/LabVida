import hashlib
import os

from cryptography.fernet import Fernet


def _obter_chave() -> bytes:
    chave = os.environ.get("LGPD_ENCRYPTION_KEY", "")
    if not chave:
        raise RuntimeError("LGPD_ENCRYPTION_KEY não configurada no ambiente")
    return chave.encode()


def _get_fernet() -> Fernet:
    return Fernet(_obter_chave())


def gerar_hash_cpf(cpf: str) -> str:
    return hashlib.sha256(cpf.encode()).hexdigest()


def criptografar_cpf(cpf: str) -> bytes:
    return _get_fernet().encrypt(cpf.encode())


def descriptografar_cpf(encrypted: bytes) -> str:
    return _get_fernet().decrypt(encrypted).decode()


def mascarar_cpf(cpf: str) -> str:
    if len(cpf) != 11:
        return "***.***.***-**"
    return f"***.{cpf[3:6]}.{cpf[6:9]}-**"
