import argparse
import random
import sys
from dataclasses import dataclass, field
from datetime import date

from faker import Faker
from sqlalchemy import delete

from src.cadastro.dtos import PacienteCreate, SexoPaciente
from src.cadastro.models import Paciente
from src.cadastro.service import criar_paciente
from src.db import session_scope


fake = Faker("pt_BR")


@dataclass
class SeederResult:
    pacientes_criados: int = 0
    erros: list[str] = field(default_factory=list)


def executar_seeder_pacientes(quantidade: int) -> SeederResult:
    resultado = SeederResult()

    try:
        with session_scope() as session:
            session.execute(delete(Paciente))
            session.commit()
    except Exception as error:
        resultado.erros.append(f"Erro ao limpar Pacientes: {error}")
        return resultado

    cpfs_usados: set[str] = set()
    for indice in range(1, quantidade + 1):
        try:
            dto = _gerar_paciente(cpfs_usados)
            with session_scope() as session:
                criar_paciente(session, dto)
            resultado.pacientes_criados += 1
        except Exception as error:
            resultado.erros.append(f"Paciente {indice}: {error}")

    return resultado


def main() -> None:
    parser = argparse.ArgumentParser(description="Popula Pacientes de exemplo no LabVida")
    parser.add_argument(
        "--pacientes",
        type=int,
        default=20,
        help="Quantidade de Pacientes gerados",
    )
    args = parser.parse_args()

    resultado = executar_seeder_pacientes(args.pacientes)
    _reportar_resultado(resultado)

    if resultado.erros:
        sys.exit(1)


def _gerar_paciente(cpfs_usados: set[str]) -> PacienteCreate:
    cpf = _gerar_cpf_unico(cpfs_usados)
    sexo = random.choice(list(SexoPaciente))
    nome = fake.name()

    return PacienteCreate(
        cpf=cpf,
        nome=nome,
        data_nascimento=fake.date_of_birth(minimum_age=18, maximum_age=90),
        telefone=_gerar_telefone(),
        sexo=sexo,
    )


def _gerar_cpf_unico(cpfs_usados: set[str]) -> str:
    while True:
        cpf = _gerar_cpf()
        if cpf not in cpfs_usados:
            cpfs_usados.add(cpf)
            return cpf


def _gerar_cpf() -> str:
    base = [random.randint(0, 9) for _ in range(9)]
    primeiro = _calcular_digito_cpf(base, range(10, 1, -1))
    segundo = _calcular_digito_cpf([*base, primeiro], range(11, 1, -1))
    return "".join(str(digito) for digito in [*base, primeiro, segundo])


def _calcular_digito_cpf(digitos: list[int], pesos: range) -> int:
    soma = sum(digito * peso for digito, peso in zip(digitos, pesos))
    resto = soma % 11
    return 0 if resto < 2 else 11 - resto


def _gerar_telefone() -> str:
    ddd = random.randint(11, 99)
    numero = random.randint(900000000, 999999999)
    return f"{ddd}{numero}"


def _reportar_resultado(resultado: SeederResult) -> None:
    print("Seeder finalizado")
    reportar_resultado_pacientes(resultado)


def reportar_resultado_pacientes(resultado: SeederResult) -> None:
    print(f"Pacientes criados: {resultado.pacientes_criados}")

    if not resultado.erros:
        print("Erros em Pacientes: 0")
        return

    print(f"Erros em Pacientes: {len(resultado.erros)}")
    for erro in resultado.erros:
        print(f"- {erro}")
