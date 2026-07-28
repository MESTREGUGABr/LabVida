"""Seed do BI — carrega o esquema estrela a partir da base transacional.

Não inventa dado: roda o ETL de `src.bi.etl`, que lê o operacional já semeado e
materializa dimensões e fatos. Como o ETL recarrega os fatos do zero, rodar de
novo é seguro.
"""

from sqlalchemy import func, select

from src.bi.etl import executar_etl
from src.bi.models import (
    FatoAtendimento,
    FatoFaturamento,
    FatoFinanceiro,
    FatoLogistica,
)
from src.db import session_scope

_FATOS = {
    "fato_atendimento": FatoAtendimento,
    "fato_faturamento": FatoFaturamento,
    "fato_financeiro": FatoFinanceiro,
    "fato_logistica": FatoLogistica,
}


def executar_seeder_bi() -> dict[str, int]:
    executar_etl()

    with session_scope() as session:
        return {
            nome: session.scalar(select(func.count()).select_from(modelo)) or 0
            for nome, modelo in _FATOS.items()
        }


def main() -> None:
    contagem = executar_seeder_bi()
    print("Seed BI finalizado")
    for chave, valor in contagem.items():
        print(f"{chave}: {valor}")


if __name__ == "__main__":
    main()
