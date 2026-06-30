from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.cadastro.medico.models import Medico


def obter_por_id(session: Session, medico_id: UUID) -> Medico | None:
    return session.get(Medico, medico_id)


def obter_por_crm(session: Session, crm: str, uf_crm: str) -> Medico | None:
    return session.scalar(select(Medico).where(Medico.crm == crm, Medico.uf_crm == uf_crm))


def listar_ativos(session: Session) -> list[Medico]:
    return list(session.scalars(select(Medico).where(Medico.ativo.is_(True)).order_by(Medico.nome)))


def salvar(session: Session, medico: Medico) -> None:
    session.add(medico)
