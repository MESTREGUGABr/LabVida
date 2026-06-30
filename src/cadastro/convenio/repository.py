from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.cadastro.convenio.dtos import StatusConvenio
from src.cadastro.convenio.models import Convenio


def obter_por_id(session: Session, convenio_id: UUID) -> Convenio | None:
    return session.get(Convenio, convenio_id)


def listar_ordenados_por_nome(session: Session) -> list[Convenio]:
    return list(session.scalars(select(Convenio).order_by(Convenio.nome)))


def listar_ativos(session: Session) -> list[Convenio]:
    return list(
        session.scalars(
            select(Convenio).where(Convenio.status == StatusConvenio.ATIVO).order_by(Convenio.nome)
        )
    )


def salvar(session: Session, convenio: Convenio) -> None:
    session.add(convenio)
