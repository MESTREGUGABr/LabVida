from datetime import date, datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.financeiro.movimento_caixa.models import MovimentoCaixa


def salvar(session: Session, movimento: MovimentoCaixa) -> MovimentoCaixa:
    session.add(movimento)
    return movimento


def listar_por_periodo(session: Session, inicio: date, fim: date) -> list[MovimentoCaixa]:
    dt_inicio = datetime.combine(inicio, datetime.min.time(), tzinfo=timezone.utc)
    dt_fim = datetime.combine(fim, datetime.max.time(), tzinfo=timezone.utc)
    stmt = (
        select(MovimentoCaixa)
        .where(MovimentoCaixa.ocorrido_em.between(dt_inicio, dt_fim))
        .order_by(MovimentoCaixa.ocorrido_em.desc())
    )
    return list(session.scalars(stmt).all())


def listar_todos(session: Session) -> list[MovimentoCaixa]:
    stmt = select(MovimentoCaixa).order_by(MovimentoCaixa.ocorrido_em.desc())
    return list(session.scalars(stmt).all())
