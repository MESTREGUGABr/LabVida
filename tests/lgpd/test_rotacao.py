import os
from collections.abc import Iterator
from datetime import date

import pytest
from cryptography.fernet import Fernet
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.cadastro.dtos import PacienteCreate, SexoPaciente
from src.cadastro.models import Paciente
from src.cadastro.service import criar_paciente
from src.db import session_scope
from src.lgpd.rotacao import rotacionar_chave


@pytest.fixture()
def session() -> Iterator[Session]:
    with session_scope() as s:
        s.execute(text("TRUNCATE pacientes RESTART IDENTITY CASCADE"))
        s.commit()
        yield s
        s.execute(text("TRUNCATE pacientes RESTART IDENTITY CASCADE"))
        s.commit()


def test_rotacionar_chave_recriptografa_cpf(session: Session) -> None:
    chave_antiga = os.environ["LGPD_ENCRYPTION_KEY"]
    chave_nova = Fernet.generate_key().decode()

    paciente = criar_paciente(
        session,
        PacienteCreate(
            cpf="52998224725",
            nome="Ana Rotacao",
            data_nascimento=date(1990, 1, 1),
            telefone="87999991234",
            sexo=SexoPaciente.FEMININO,
        ),
    )
    modelo = session.get(Paciente, paciente.id)
    hash_antes = modelo.cpf_hash
    cipher_antes = bytes(modelo.cpf_encrypted)

    total = rotacionar_chave(session, chave_antiga, chave_nova)

    assert total == 1
    session.refresh(modelo)
    # O CPF em claro é recuperável com a NOVA chave...
    assert Fernet(chave_nova.encode()).decrypt(modelo.cpf_encrypted).decode() == "52998224725"
    # ...o hash não muda e o ciphertext mudou.
    assert modelo.cpf_hash == hash_antes
    assert bytes(modelo.cpf_encrypted) != cipher_antes
