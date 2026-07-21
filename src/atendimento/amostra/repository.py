from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.atendimento.amostra.models import Amostra, Coleta


def obter_por_id(session: Session, amostra_id: UUID) -> Amostra | None:
    return session.get(Amostra, amostra_id)


def obter_por_codigo_barras(session: Session, codigo_barras: str) -> Amostra | None:
    return session.scalar(select(Amostra).where(Amostra.codigo_barras == codigo_barras))


def listar_por_os(session: Session, ordem_servico_id: UUID) -> list[Amostra]:
    return list(
        session.scalars(
            select(Amostra)
            .where(Amostra.ordem_servico_id == ordem_servico_id)
            .order_by(Amostra.codigo_barras)
        )
    )


def listar_por_status(session: Session, status: str) -> list[Amostra]:
    return list(
        session.scalars(
            select(Amostra)
            .where(Amostra.status == status)
            .order_by(Amostra.codigo_barras)
        )
    )


def salvar_amostra(session: Session, amostra: Amostra) -> None:
    session.add(amostra)


def salvar_coleta(session: Session, coleta: Coleta) -> None:
    session.add(coleta)
