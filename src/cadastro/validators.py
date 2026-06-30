import re


def normalizar_cpf_paciente(cpf: str) -> str:
    cpf_normalizado = re.sub(r"\D", "", cpf)
    if not _cpf_valido(cpf_normalizado):
        raise ValueError("CPF do Paciente inválido")
    return cpf_normalizado


def normalizar_telefone_paciente(telefone: str) -> str:
    telefone_normalizado = re.sub(r"\D", "", telefone)
    if len(telefone_normalizado) not in (10, 11):
        raise ValueError("Telefone do Paciente inválido")
    return telefone_normalizado


def normalizar_nome_paciente(nome: str) -> str:
    nome_normalizado = " ".join(nome.strip().split())
    if not (2 <= len(nome_normalizado) <= 120):
        raise ValueError("Nome do Paciente inválido")
    return nome_normalizado


def _cpf_valido(cpf: str) -> bool:
    if len(cpf) != 11 or len(set(cpf)) == 1:
        return False

    digitos = [int(digito) for digito in cpf]
    primeiro = _calcular_digito_cpf(digitos[:9], range(10, 1, -1))
    segundo = _calcular_digito_cpf(digitos[:10], range(11, 1, -1))
    return digitos[9] == primeiro and digitos[10] == segundo


def _calcular_digito_cpf(digitos: list[int], pesos: range) -> int:
    soma = sum(digito * peso for digito, peso in zip(digitos, pesos))
    resto = soma % 11
    return 0 if resto < 2 else 11 - resto
