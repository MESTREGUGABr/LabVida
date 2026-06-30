from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.cadastro.unidade.models import Setor, Unidade


def obter_unidade_por_id(session: Session, unidade_id: UUID) -> Unidade | None:
    return session.get(Unidade, unidade_id)


def listar_unidades_ativas(session: Session) -> list[Unidade]:
    return list(session.scalars(select(Unidade).where(Unidade.ativo.is_(True)).order_by(Unidade.nome)))


def salvar_unidade(session: Session, unidade: Unidade) -> None:
    session.add(unidade)


def obter_setor_por_id(session: Session, setor_id: UUID) -> Setor | None:
    return session.get(Setor, setor_id)


def listar_setores_ativos(session: Session, unidade_id: UUID) -> list[Setor]:
    return list(
        session.scalars(
            select(Setor)
            .where(Setor.ativo.is_(True), Setor.unidade_id == unidade_id)
            .order_by(Setor.nome)
        )
    )


def salvar_setor(session: Session, setor: Setor) -> None:
    session.add(setor)
