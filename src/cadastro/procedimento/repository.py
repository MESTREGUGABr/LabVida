from datetime import date
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.cadastro.procedimento.models import Procedimento, ProcedimentoValor


def obter_por_id(session: Session, procedimento_id: UUID) -> Procedimento | None:
    return session.get(Procedimento, procedimento_id)


def obter_por_codigo_tuss(session: Session, codigo_tuss: str) -> Procedimento | None:
    return session.scalar(select(Procedimento).where(Procedimento.codigo_tuss == codigo_tuss))


def listar_ativos(session: Session) -> list[Procedimento]:
    return list(
        session.scalars(
            select(Procedimento).where(Procedimento.ativo.is_(True)).order_by(Procedimento.nome)
        )
    )


def salvar(session: Session, procedimento: Procedimento) -> None:
    session.add(procedimento)


def salvar_valor(session: Session, valor: ProcedimentoValor) -> None:
    session.add(valor)


def obter_valor_vigente(
    session: Session, procedimento_id: UUID, convenio_id: UUID, na_data: date
) -> ProcedimentoValor | None:
    return session.scalar(
        select(ProcedimentoValor)
        .where(
            ProcedimentoValor.procedimento_id == procedimento_id,
            ProcedimentoValor.convenio_id == convenio_id,
            ProcedimentoValor.vigencia_inicio <= na_data,
        )
        .order_by(ProcedimentoValor.vigencia_inicio.desc())
        .limit(1)
    )
