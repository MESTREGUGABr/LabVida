from uuid import UUID

from sqlalchemy.orm import Session

from src.financeiro.conciliacao_pagamento import repository
from src.financeiro.conciliacao_pagamento.dtos import ConciliacaoPagamentoRead


def listar_por_titulo(session: Session, titulo_receber_id: UUID) -> list[ConciliacaoPagamentoRead]:
    return [
        ConciliacaoPagamentoRead.model_validate(c)
        for c in repository.listar_por_titulo(session, titulo_receber_id)
    ]


def listar_todas(session: Session) -> list[ConciliacaoPagamentoRead]:
    return [
        ConciliacaoPagamentoRead.model_validate(c)
        for c in repository.listar_todas(session)
    ]
