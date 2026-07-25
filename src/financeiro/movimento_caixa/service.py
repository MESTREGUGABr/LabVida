from datetime import date

from sqlalchemy.orm import Session

from src.financeiro.movimento_caixa import repository
from src.financeiro.movimento_caixa.dtos import MovimentoCaixaRead, TipoMovimento


def fluxo_caixa_por_periodo(session: Session, inicio: date, fim: date) -> dict:
    movs = repository.listar_por_periodo(session, inicio, fim)
    entradas = sum(m.valor for m in movs if m.tipo == TipoMovimento.ENTRADA)
    saidas = sum(m.valor for m in movs if m.tipo == TipoMovimento.SAIDA)
    return {
        "movimentos": [MovimentoCaixaRead.model_validate(m) for m in movs],
        "total_entradas": entradas,
        "total_saidas": saidas,
        "saldo": entradas - saidas,
    }


def listar_todos(session: Session) -> list[MovimentoCaixaRead]:
    return [MovimentoCaixaRead.model_validate(m) for m in repository.listar_todos(session)]
