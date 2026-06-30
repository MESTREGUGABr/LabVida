import pytest

from src.cadastro.validators import (
    normalizar_cnpj_convenio,
    normalizar_cpf_paciente,
    normalizar_nome_convenio,
    normalizar_nome_paciente,
    normalizar_telefone_convenio,
    normalizar_telefone_paciente,
)


def test_normaliza_cpf_do_paciente_com_mascara() -> None:
    assert normalizar_cpf_paciente("529.982.247-25") == "52998224725"


@pytest.mark.parametrize("cpf", ["123.456.789-00", "111.111.111-11", "123"])
def test_rejeita_cpf_do_paciente_invalido(cpf: str) -> None:
    with pytest.raises(ValueError, match="CPF do Paciente inválido"):
        normalizar_cpf_paciente(cpf)


def test_normaliza_telefone_do_paciente_com_mascara() -> None:
    assert normalizar_telefone_paciente("(87) 99999-1234") == "87999991234"


@pytest.mark.parametrize("telefone", ["+55 (87) 99999-1234", "99999-1234", "abc"])
def test_rejeita_telefone_do_paciente_invalido(telefone: str) -> None:
    with pytest.raises(ValueError, match="Telefone do Paciente inválido"):
        normalizar_telefone_paciente(telefone)


def test_normaliza_nome_do_paciente() -> None:
    assert normalizar_nome_paciente("  Ana   Maria  ") == "Ana Maria"


@pytest.mark.parametrize("nome", ["", " A "])
def test_rejeita_nome_do_paciente_invalido(nome: str) -> None:
    with pytest.raises(ValueError, match="Nome do Paciente inválido"):
        normalizar_nome_paciente(nome)


def test_normaliza_cnpj_do_convenio_com_mascara() -> None:
    assert normalizar_cnpj_convenio("12.345.678/0001-95") == "12345678000195"


@pytest.mark.parametrize("cnpj", ["", "11111111111111", "12.345.678/0001-00"])
def test_rejeita_cnpj_do_convenio_invalido(cnpj: str) -> None:
    with pytest.raises(ValueError, match="CNPJ do Convênio inválido"):
        normalizar_cnpj_convenio(cnpj)


def test_normaliza_telefone_do_convenio_com_mascara() -> None:
    assert normalizar_telefone_convenio("(87) 99999-1234") == "87999991234"


def test_normaliza_nome_do_convenio() -> None:
    assert normalizar_nome_convenio("  Unimed   Recife  ") == "Unimed Recife"
