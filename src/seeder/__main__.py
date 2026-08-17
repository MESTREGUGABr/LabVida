"""Seeder principal do LabVida — popula dados de exemplo em ordem de dependência.

Monta uma base de demonstração com meses de operação: cadastros, equipe,
pacientes, ordens de serviço em todos os estágios do fluxo, bancada, lotes de
faturamento com glosas, carteira financeira liquidada em parte, compras com
estoque movimentado e, por fim, a carga do BI.

Cada módulo é idempotente, então subir o container de novo não duplica nada.

Uso:
    python -m src.seeder                 # carga padrão
    python -m src.seeder --escala 0.2    # carga reduzida
    SEED_ESCALA=2 python -m src.seeder   # carga dobrada
    SEED_INICIO=2022-01-01 python -m src.seeder   # série histórica desde 2022
"""

import argparse
import time

from src.seeder import config
from src.seeder.atendimento import executar_seeder_atendimento
from src.seeder.bi import executar_seeder_bi
from src.seeder.cadastros import executar_seeder_cadastros
from src.seeder.compras import executar_seeder_compras
from src.seeder.faturamento import executar_seeder_faturamento
from src.seeder.financeiro import executar_seeder_financeiro
from src.seeder.laboratorial import executar_seeder_laboratorial
from src.seeder.pacientes import PACIENTES_PADRAO, executar_seeder_pacientes
from src.seeder.rbac import executar_seeder_rbac


def main(escala: float | None = None) -> None:
    if escala is not None:
        config.definir_escala(escala)
    config.iniciar_rng()

    inicio = time.perf_counter()
    resumo: dict[str, dict[str, int]] = {}

    resumo["RBAC e equipe"] = executar_seeder_rbac()
    resumo["Cadastros"] = executar_seeder_cadastros()

    pacientes = executar_seeder_pacientes(config.qtd(PACIENTES_PADRAO))
    resumo["Pacientes"] = {"pacientes": pacientes.pacientes_criados, "erros": len(pacientes.erros)}

    resumo["Atendimento e logística"] = executar_seeder_atendimento()
    resumo["Laboratorial"] = executar_seeder_laboratorial()
    resumo["Faturamento"] = executar_seeder_faturamento()
    resumo["Financeiro"] = executar_seeder_financeiro()
    resumo["Compras"] = executar_seeder_compras()
    resumo["BI"] = executar_seeder_bi()

    _imprimir_resumo(resumo, time.perf_counter() - inicio)


def _imprimir_resumo(resumo: dict[str, dict[str, int]], duracao: float) -> None:
    print()
    print("=" * 52)
    print(f"Seeder principal finalizado em {duracao:.1f}s (escala {config.escala():g})")
    print("=" * 52)
    for modulo, contagem in resumo.items():
        print(f"\n{modulo}")
        for chave, valor in contagem.items():
            print(f"  {chave.replace('_', ' ')}: {valor}")
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Popula a base de demonstração do LabVida")
    parser.add_argument(
        "--escala",
        type=float,
        default=None,
        help="Multiplicador de volume (padrão: variável SEED_ESCALA ou 1.0)",
    )
    main(parser.parse_args().escala)
