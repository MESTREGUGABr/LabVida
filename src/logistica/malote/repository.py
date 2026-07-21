from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.logistica.malote.dtos import StatusMalote
from src.logistica.malote.models import Malote, MaloteAmostra


def salvar_malote(session: Session, malote: Malote) -> Malote:
    session.add(malote)
    return malote


def obter_por_id(session: Session, malote_id: UUID) -> Malote | None:
    return session.get(Malote, malote_id)


def obter_por_codigo(session: Session, codigo_malote: str) -> Malote | None:
    stmt = select(Malote).where(Malote.codigo_malote == codigo_malote)
    return session.execute(stmt).scalar_one_or_none()


def listar_por_unidade_origem(session: Session, unidade_origem_id: UUID) -> list[Malote]:
    stmt = (
        select(Malote)
        .where(Malote.unidade_origem_id == unidade_origem_id)
        .order_by(Malote.criado_em.desc())
    )
    return list(session.scalars(stmt).all())


def listar_em_transito_para_unidade(session: Session, unidade_destino_id: UUID) -> list[Malote]:
    stmt = (
        select(Malote)
        .where(
            Malote.unidade_destino_id == unidade_destino_id,
            Malote.status == StatusMalote.EM_TRANSITO.value,
        )
        .order_by(Malote.criado_em.desc())
    )
    return list(session.scalars(stmt).all())


def vincular_amostra(session: Session, item: MaloteAmostra) -> MaloteAmostra:
    session.add(item)
    return item


def obter_item_por_amostra(session: Session, amostra_id: UUID) -> MaloteAmostra | None:
    stmt = select(MaloteAmostra).where(MaloteAmostra.amostra_id == amostra_id)
    return session.execute(stmt).scalar_one_or_none()
