from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.cadastro.models import Convenio, Paciente


def obter_por_id(session: Session, paciente_id: UUID) -> Paciente | None:
    return session.get(Paciente, paciente_id)


def obter_por_cpf(session: Session, cpf: str) -> Paciente | None:
    return session.scalar(select(Paciente).where(Paciente.cpf == cpf))


def listar_ativos_ordenados_por_nome(session: Session) -> list[Paciente]:
    return list(session.scalars(select(Paciente).where(Paciente.ativo.is_(True)).order_by(Paciente.nome)))


def salvar(session: Session, paciente: Paciente) -> None:
    session.add(paciente)


def obter_convenio_por_nome_normalizado(session: Session, nome_normalizado: str) -> Convenio | None:
    return session.scalar(select(Convenio).where(Convenio.nome_normalizado == nome_normalizado))


def obter_convenio_por_id(session: Session, convenio_id: UUID) -> Convenio | None:
    return session.get(Convenio, convenio_id)


def obter_convenio_por_cnpj(session: Session, cnpj: str) -> Convenio | None:
    return session.scalar(select(Convenio).where(Convenio.cnpj == cnpj))


def listar_convenios_ordenados_por_nome(session: Session) -> list[Convenio]:
    return list(session.scalars(select(Convenio).order_by(Convenio.nome)))


def salvar_convenio(session: Session, convenio: Convenio) -> None:
    session.add(convenio)
