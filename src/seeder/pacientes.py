"""Seed de Pacientes.

Cada CPF é gerado com dígito verificador válido e criptografado na origem pelo
service (LGPD), então este seeder também exercita o caminho de cifra do CPF.
"""

import argparse
import random
import sys
from dataclasses import dataclass, field

from sqlalchemy import select

from src.cadastro.dtos import PacienteCreate, SexoPaciente
from src.cadastro.models import Paciente
from src.cadastro.service import criar_paciente
from src.db import session_scope
from src.seeder.config import fake, qtd
from src.seeder.documentos import gerar_cpf, gerar_telefone

PACIENTES_PADRAO = 220


@dataclass
class SeederResult:
    pacientes_criados: int = 0
    erros: list[str] = field(default_factory=list)


def executar_seeder_pacientes(quantidade: int) -> SeederResult:
    resultado = SeederResult()

    with session_scope() as session:
        pacientes_existentes = list(session.scalars(select(Paciente)))
        cpfs_usados = {p.cpf for p in pacientes_existentes}

        a_criar = max(0, quantidade - len(pacientes_existentes))
        for indice in range(1, a_criar + 1):
            try:
                criar_paciente(session, _gerar_paciente(cpfs_usados))
                resultado.pacientes_criados += 1
            except Exception as error:
                resultado.erros.append(f"Paciente {indice}: {error}")

    return resultado


def main(quantidade: int | None = None) -> None:
    resultado = executar_seeder_pacientes(quantidade if quantidade is not None else qtd(PACIENTES_PADRAO))
    _reportar_resultado(resultado)

    if resultado.erros:
        sys.exit(1)


def _gerar_paciente(cpfs_usados: set[str]) -> PacienteCreate:
    return PacienteCreate(
        cpf=gerar_cpf(cpfs_usados),
        nome=fake.name(),
        data_nascimento=fake.date_of_birth(minimum_age=1, maximum_age=95),
        telefone=gerar_telefone(),
        sexo=random.choice(list(SexoPaciente)),
    )


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Popula Pacientes de exemplo no LabVida")
    parser.add_argument(
        "--pacientes",
        type=int,
        default=qtd(PACIENTES_PADRAO),
        help="Quantidade de Pacientes gerados",
    )
    main(parser.parse_args().pacientes)
