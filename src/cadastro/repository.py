from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.cadastro.models import Paciente


def obter_por_id(session: Session, paciente_id: UUID) -> Paciente | None:
    return session.get(Paciente, paciente_id)


def obter_por_cpf(session: Session, cpf: str) -> Paciente | None:
    return session.scalar(select(Paciente).where(Paciente.cpf == cpf))


def listar_ativos_ordenados_por_nome(session: Session) -> list[Paciente]:
    return list(session.scalars(select(Paciente).where(Paciente.ativo.is_(True)).order_by(Paciente.nome)))


def salvar(session: Session, paciente: Paciente) -> None:
    session.add(paciente)
