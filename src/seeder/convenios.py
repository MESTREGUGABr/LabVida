import random
from dataclasses import dataclass, field

from faker import Faker
from sqlalchemy import select

from src.cadastro.dtos import ConvenioCreate
from src.cadastro.models import Convenio
from src.cadastro.service import criar_convenio
from src.db import session_scope


fake = Faker("pt_BR")


@dataclass
class ConvenioSeederResult:
    convenios_criados: int = 0
    erros: list[str] = field(default_factory=list)


def executar_seeder_convenios(quantidade: int) -> ConvenioSeederResult:
    resultado = ConvenioSeederResult()

    with session_scope() as session:
        convenios_existentes = list(session.scalars(select(Convenio)))
        nomes_usados = {c.nome.casefold() for c in convenios_existentes}
        cnpjs_usados = {c.cnpj for c in convenios_existentes if c.cnpj}

    a_criar = max(0, quantidade - len(convenios_existentes))
    for indice in range(1, a_criar + 1):
        try:
            dto = _gerar_convenio(nomes_usados, cnpjs_usados)
            with session_scope() as session:
                criar_convenio(session, dto)
            resultado.convenios_criados += 1
        except Exception as error:
            resultado.erros.append(f"Convênio {indice}: {error}")

    return resultado


def _gerar_convenio(nomes_usados: set[str], cnpjs_usados: set[str]) -> ConvenioCreate:
    nome = _gerar_nome_unico(nomes_usados)

    return ConvenioCreate(
        nome=nome,
        cnpj=_gerar_cnpj_unico(cnpjs_usados),
        telefone=_gerar_telefone(),
        email=f"faturamento@{fake.domain_name()}",
    )


def _gerar_nome_unico(nomes_usados: set[str]) -> str:
    while True:
        nome = f"{fake.company()} Saúde"
        nome_normalizado = nome.casefold()
        if nome_normalizado not in nomes_usados:
            nomes_usados.add(nome_normalizado)
            return nome


def _gerar_cnpj_unico(cnpjs_usados: set[str]) -> str:
    while True:
        cnpj = _gerar_cnpj()
        if cnpj not in cnpjs_usados:
            cnpjs_usados.add(cnpj)
            return cnpj


def _gerar_cnpj() -> str:
    while True:
        base = [random.randint(0, 9) for _ in range(12)]
        if len(set(base)) > 1:
            break

    primeiro = _calcular_digito_cnpj(base, [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
    segundo = _calcular_digito_cnpj([*base, primeiro], [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
    return "".join(str(digito) for digito in [*base, primeiro, segundo])


def _calcular_digito_cnpj(digitos: list[int], pesos: list[int]) -> int:
    soma = sum(digito * peso for digito, peso in zip(digitos, pesos))
    resto = soma % 11
    return 0 if resto < 2 else 11 - resto


def _gerar_telefone() -> str:
    ddd = random.randint(11, 99)
    numero = random.randint(900000000, 999999999)
    return f"{ddd}{numero}"


def reportar_resultado_convenios(resultado: ConvenioSeederResult) -> None:
    print(f"Convênios criados: {resultado.convenios_criados}")

    if not resultado.erros:
        print("Erros em Convênios: 0")
        return

    print(f"Erros em Convênios: {len(resultado.erros)}")
    for erro in resultado.erros:
        print(f"- {erro}")
