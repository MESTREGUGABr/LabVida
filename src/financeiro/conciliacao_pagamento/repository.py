from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.financeiro.conciliacao_pagamento.models import ConciliacaoPagamento


def listar_por_titulo(session: Session, titulo_receber_id: UUID) -> list[ConciliacaoPagamento]:
    stmt = (
        select(ConciliacaoPagamento)
        .where(ConciliacaoPagamento.titulo_receber_id == titulo_receber_id)
        .order_by(ConciliacaoPagamento.conciliado_em.desc())
    )
    return list(session.scalars(stmt).all())


def listar_todas(session: Session) -> list[ConciliacaoPagamento]:
    stmt = select(ConciliacaoPagamento).order_by(ConciliacaoPagamento.conciliado_em.desc())
    return list(session.scalars(stmt).all())
