import argparse
import sys

from src.seeder.convenios import (
    executar_seeder_convenios,
    reportar_resultado_convenios,
)
from src.seeder.pacientes import (
    executar_seeder_pacientes,
    reportar_resultado_pacientes,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Popula Cadastros de exemplo no LabVida")
    parser.add_argument(
        "--pacientes",
        type=int,
        default=20,
        help="Quantidade de Pacientes gerados",
    )
    parser.add_argument(
        "--convenios",
        type=int,
        default=10,
        help="Quantidade de Convênios gerados",
    )
    args = parser.parse_args()

    resultado_pacientes = executar_seeder_pacientes(args.pacientes)
    resultado_convenios = executar_seeder_convenios(args.convenios)

    print("Seeder finalizado")
    reportar_resultado_pacientes(resultado_pacientes)
    reportar_resultado_convenios(resultado_convenios)

    if resultado_pacientes.erros or resultado_convenios.erros:
        sys.exit(1)
from src.seeder.atendimento import main as seed_atendimento
from src.seeder.cadastros import main as seed_cadastros
from src.seeder.pacientes import main as seed_pacientes


if __name__ == "__main__":
    seed_cadastros()
    seed_pacientes()
    seed_atendimento()
