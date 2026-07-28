"""Geradores de documentos brasileiros válidos para os dados de demonstração.

CPF e CNPJ passam pelos validadores de dígito verificador do `src.cadastro`,
então o seeder precisa emitir documentos realmente válidos — não basta sortear
dígitos.
"""

import random


def gerar_cpf(usados: set[str] | None = None) -> str:
    """CPF com dígitos verificadores válidos, único dentro de `usados`."""
    while True:
        base = [random.randint(0, 9) for _ in range(9)]
        primeiro = _digito_cpf(base, range(10, 1, -1))
        segundo = _digito_cpf([*base, primeiro], range(11, 1, -1))
        cpf = "".join(str(d) for d in [*base, primeiro, segundo])

        if len(set(cpf)) == 1:
            continue
        if usados is None:
            return cpf
        if cpf not in usados:
            usados.add(cpf)
            return cpf


def gerar_cnpj(usados: set[str] | None = None) -> str:
    """CNPJ com dígitos verificadores válidos, único dentro de `usados`."""
    while True:
        base = [random.randint(0, 9) for _ in range(12)]
        if len(set(base)) == 1:
            continue
        primeiro = _digito_cnpj(base, [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
        segundo = _digito_cnpj([*base, primeiro], [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
        cnpj = "".join(str(d) for d in [*base, primeiro, segundo])

        if usados is None:
            return cnpj
        if cnpj not in usados:
            usados.add(cnpj)
            return cnpj


def gerar_telefone() -> str:
    """Celular no formato aceito pelos validadores (11 dígitos, DDD + 9)."""
    return f"{random.randint(11, 99)}9{random.randint(10000000, 99999999)}"


def _digito_cpf(digitos: list[int], pesos: range) -> int:
    soma = sum(digito * peso for digito, peso in zip(digitos, pesos))
    resto = soma % 11
    return 0 if resto < 2 else 11 - resto


def _digito_cnpj(digitos: list[int], pesos: list[int]) -> int:
    soma = sum(digito * peso for digito, peso in zip(digitos, pesos))
    resto = soma % 11
    return 0 if resto < 2 else 11 - resto
