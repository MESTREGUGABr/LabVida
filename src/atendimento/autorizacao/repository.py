from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.atendimento.autorizacao.models import AutorizacaoConvenio


def listar_por_os(session: Session, ordem_servico_id: UUID) -> list[AutorizacaoConvenio]:
    return list(
        session.scalars(
            select(AutorizacaoConvenio).where(
                AutorizacaoConvenio.ordem_servico_id == ordem_servico_id
            )
        )
    )


def salvar(session: Session, autorizacao: AutorizacaoConvenio) -> None:
    session.add(autorizacao)
