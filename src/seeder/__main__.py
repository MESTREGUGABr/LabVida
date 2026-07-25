"""Seeder principal do LabVida — popula dados de exemplo em ordem de dependência.

Uso: make seeder
"""

from src.seeder.atendimento import main as seed_atendimento
from src.seeder.cadastros import main as seed_cadastros
from src.seeder.compras import main as seed_compras
from src.seeder.faturamento import main as seed_faturamento
from src.seeder.financeiro import main as seed_financeiro
from src.seeder.laboratorial import main as seed_laboratorial
from src.seeder.pacientes import main as seed_pacientes


def main() -> None:
    seed_cadastros()
    seed_pacientes()
    seed_atendimento()
    seed_laboratorial()
    seed_faturamento()
    seed_financeiro()
    seed_compras()
    print("Seeder principal finalizado — todos os módulos populados")


if __name__ == "__main__":
    main()
