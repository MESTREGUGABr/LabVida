import os
from collections.abc import Iterator

import pytest
from cryptography.fernet import Fernet
from sqlalchemy.orm import Session

from src.db import session_scope
from src.lgpd import criptografar_cpf, descriptografar_cpf, gerar_hash_cpf, mascarar_cpf

CHAVE = Fernet.generate_key().decode()


@pytest.fixture(autouse=True)
def _set_key(monkeypatch) -> None:
    monkeypatch.setenv("LGPD_ENCRYPTION_KEY", CHAVE)


def test_criptografar_descriptografar() -> None:
    cpf = "52998224725"
    encrypted = criptografar_cpf(cpf)
    assert isinstance(encrypted, bytes)
    assert encrypted != cpf.encode()
    assert descriptografar_cpf(encrypted) == cpf


def test_hash_cpf_deterministico() -> None:
    cpf = "52998224725"
    h1 = gerar_hash_cpf(cpf)
    h2 = gerar_hash_cpf(cpf)
    assert h1 == h2
    assert len(h1) == 64


def test_hash_diferente_para_cpfs_diferentes() -> None:
    h1 = gerar_hash_cpf("52998224725")
    h2 = gerar_hash_cpf("12345678909")
    assert h1 != h2


def test_mascarar_cpf() -> None:
    assert mascarar_cpf("52998224725") == "***.982.247-**"
    assert mascarar_cpf("123") == "***.***.***-**"
