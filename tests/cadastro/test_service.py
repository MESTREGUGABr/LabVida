from collections.abc import Iterator
from datetime import date, timedelta
from uuid import uuid4

import pytest
from sqlalchemy.orm import Session

from src.cadastro.dtos import PacienteCreate, PacienteUpdate, SexoPaciente
from src.cadastro.errors import CpfPacienteDuplicado, PacienteNaoEncontrado
from src.cadastro.models import Paciente
from src.cadastro.service import (
    atualizar_paciente,
    criar_paciente,
    inativar_paciente,
    listar_pacientes_ativos,
    obter_paciente_por_id,
)
from src.db import session_scope


@pytest.fixture()
def session() -> Iterator[Session]:
    with session_scope() as session:
        session.query(Paciente).delete()
        session.commit()
        yield session
        session.query(Paciente).delete()
        session.commit()


def _paciente_create(cpf: str = "52998224725", nome: str = "Ana Maria") -> PacienteCreate:
    return PacienteCreate(
        cpf=cpf,
        nome=nome,
        data_nascimento=date.today() - timedelta(days=1),
        telefone="87999991234",
        sexo=SexoPaciente.FEMININO,
    )


def test_cria_paciente_ativo(session: Session) -> None:
    paciente = criar_paciente(session, _paciente_create())

    assert paciente.id
    assert paciente.cpf == "52998224725"
    assert paciente.nome == "Ana Maria"


def test_rejeita_cpf_duplicado_mesmo_com_paciente_inativo(session: Session) -> None:
    paciente = criar_paciente(session, _paciente_create())
    inativar_paciente(session, paciente.id)

    with pytest.raises(CpfPacienteDuplicado, match="Paciente já cadastrado com este CPF"):
        criar_paciente(session, _paciente_create())


def test_lista_apenas_pacientes_ativos_ordenados_por_nome(session: Session) -> None:
    criar_paciente(session, _paciente_create(cpf="52998224725", nome="Bruno Silva"))
    maria = criar_paciente(session, _paciente_create(cpf="15350946056", nome="Maria Souza"))
    ana = criar_paciente(session, _paciente_create(cpf="11144477735", nome="Ana Costa"))
    inativar_paciente(session, maria.id)

    pacientes = listar_pacientes_ativos(session)

    assert [paciente.nome for paciente in pacientes] == ["Ana Costa", "Bruno Silva"]
    assert ana.id in [paciente.id for paciente in pacientes]


def test_obtem_paciente_por_id_mesmo_inativo(session: Session) -> None:
    paciente = criar_paciente(session, _paciente_create())
    inativar_paciente(session, paciente.id)

    encontrado = obter_paciente_por_id(session, paciente.id)

    assert encontrado.id == paciente.id


def test_atualiza_paciente_parcialmente(session: Session) -> None:
    paciente = criar_paciente(session, _paciente_create())

    atualizado = atualizar_paciente(session, paciente.id, PacienteUpdate(nome="  Ana   Clara  "))

    assert atualizado.nome == "Ana Clara"
    assert atualizado.cpf == "52998224725"


def test_atualizar_cpf_rejeita_cpf_de_outro_paciente(session: Session) -> None:
    paciente = criar_paciente(session, _paciente_create(cpf="52998224725"))
    criar_paciente(session, _paciente_create(cpf="15350946056", nome="Bruno Silva"))

    with pytest.raises(CpfPacienteDuplicado, match="Paciente já cadastrado com este CPF"):
        atualizar_paciente(session, paciente.id, PacienteUpdate(cpf="153.509.460-56"))


def test_inativar_paciente_eh_idempotente(session: Session) -> None:
    paciente = criar_paciente(session, _paciente_create())

    inativar_paciente(session, paciente.id)
    inativar_paciente(session, paciente.id)

    assert obter_paciente_por_id(session, paciente.id).id == paciente.id


def test_paciente_nao_encontrado(session: Session) -> None:
    with pytest.raises(PacienteNaoEncontrado, match="Paciente não encontrado"):
        obter_paciente_por_id(session, uuid4())
