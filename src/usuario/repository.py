from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.usuario.models import Usuario


def obter_por_id(session: Session, usuario_id: UUID) -> Usuario | None:
    return session.get(Usuario, usuario_id)


def obter_por_email(session: Session, email: str) -> Usuario | None:
    return session.scalar(select(Usuario).where(Usuario.email == email))


def salvar(session: Session, usuario: Usuario) -> None:
    session.add(usuario)

def listar(session: Session) -> list[Usuario]:
    return list(session.scalars(select(Usuario)).all())
