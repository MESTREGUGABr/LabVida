from datetime import date, timedelta

import pytest
from pydantic import ValidationError

from src.cadastro.dtos import ConvenioCreate, ConvenioUpdate, PacienteCreate, PacienteUpdate, SexoPaciente


def test_paciente_create_normaliza_dados_e_define_sexo_nao_informado() -> None:
    dto = PacienteCreate(
        cpf="529.982.247-25",
        nome="  Ana   Maria  ",
        data_nascimento=date.today() - timedelta(days=1),
        telefone="(87) 99999-1234",
    )

    assert dto.cpf == "52998224725"
    assert dto.nome == "Ana Maria"
    assert dto.telefone == "87999991234"
    assert dto.sexo == SexoPaciente.NAO_INFORMADO


def test_paciente_create_rejeita_data_nascimento_futura_ou_hoje() -> None:
    with pytest.raises(ValidationError, match="Data de nascimento deve ser anterior à data atual"):
        PacienteCreate(
            cpf="52998224725",
            nome="Ana Maria",
            data_nascimento=date.today(),
            telefone="87999991234",
        )


def test_paciente_update_parcial_normaliza_campos_enviados() -> None:
    dto = PacienteUpdate(nome="  Ana   Maria  ")

    assert dto.nome == "Ana Maria"
    assert dto.cpf is None


def test_paciente_update_rejeita_payload_vazio() -> None:
    with pytest.raises(ValidationError, match="Informe ao menos um campo para atualizar"):
        PacienteUpdate()


def test_convenio_create_normaliza_dados_opcionais() -> None:
    dto = ConvenioCreate(
        nome="  Unimed   Recife  ",
        cnpj="12.345.678/0001-95",
        telefone="(87) 99999-1234",
        email="  FINANCEIRO@UNIMED.TEST  ",
    )

    assert dto.nome == "Unimed Recife"
    assert dto.cnpj == "12345678000195"
    assert dto.telefone == "87999991234"
    assert dto.email == "financeiro@unimed.test"


def test_convenio_update_permite_limpar_campo_opcional() -> None:
    dto = ConvenioUpdate(cnpj=None)

    assert dto.cnpj is None


def test_convenio_update_rejeita_payload_vazio() -> None:
    with pytest.raises(ValidationError, match="Informe ao menos um campo para atualizar"):
        ConvenioUpdate()
