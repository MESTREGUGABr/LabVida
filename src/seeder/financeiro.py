"""Seed mínimo de Financeiro para testes da Fase 2.

Cria TituloPagar fake (pois a criação real virá da Fase 3 - Compras).
Idempotente: só insere se a tabela estiver vazia.
"""

from datetime import date, timedelta
from decimal import Decimal

from sqlalchemy.orm import Session

from src.db import session_scope
from src.financeiro.titulo_pagar import repository as tp_repository
from src.financeiro.titulo_pagar.models import TituloPagar


def executar_seeder_financeiro() -> dict[str, int]:
    contagem = {"titulos_pagar": 0}

    with session_scope() as session:
        existentes = tp_repository.listar_todos(session)
        if existentes:
            return contagem

        hoje = date.today()
        titulos = [
            TituloPagar(
                pedido_compra_id=None,
                valor=1500.00,
                vencimento=hoje + timedelta(days=15),
                status="PENDENTE",
            ),
            TituloPagar(
                pedido_compra_id=None,
                valor=890.00,
                vencimento=hoje + timedelta(days=30),
                status="PENDENTE",
            ),
            TituloPagar(
                pedido_compra_id=None,
                valor=420.00,
                vencimento=hoje - timedelta(days=5),
                status="PENDENTE",
            ),
        ]
        for t in titulos:
            tp_repository.salvar(session, t)
        session.commit()
        contagem["titulos_pagar"] = len(titulos)

    return contagem


def main() -> None:
    contagem = executar_seeder_financeiro()
    print("Seed financeiro finalizado")
    for chave, valor in contagem.items():
        print(f"{chave}: {valor}")


if __name__ == "__main__":
    main()
