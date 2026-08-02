from datetime import date
from uuid import UUID

from sqlalchemy import or_, select
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
    session: Session, procedimento_id: UUID, convenio_id: UUID | None, na_data: date
) -> ProcedimentoValor | None:
    """Preco vigente NA DATA informada.

    `convenio_id=None` significa tabela particular, e a comparacao usa
    `IS NOT DISTINCT FROM` porque em SQL `NULL = NULL` e nulo, nao verdadeiro —
    com `==` o preco particular nunca seria encontrado.

    O filtro de `vigencia_fim` e o que impede um preco encerrado de continuar
    respondendo por consultas de datas posteriores.
    """
    return session.scalar(
        select(ProcedimentoValor)
        .where(
            ProcedimentoValor.procedimento_id == procedimento_id,
            ProcedimentoValor.convenio_id.is_not_distinct_from(convenio_id),
            ProcedimentoValor.vigencia_inicio <= na_data,
            or_(
                ProcedimentoValor.vigencia_fim.is_(None),
                ProcedimentoValor.vigencia_fim >= na_data,
            ),
        )
        .order_by(ProcedimentoValor.vigencia_inicio.desc())
        .limit(1)
    )


def obter_vigencia_aberta(
    session: Session, procedimento_id: UUID, convenio_id: UUID | None
) -> ProcedimentoValor | None:
    """Preco em aberto (sem `vigencia_fim`) — o que `definir_valor` precisa
    encerrar antes de inserir o novo, senao o EXCLUDE do banco rejeita."""
    return session.scalar(
        select(ProcedimentoValor)
        .where(
            ProcedimentoValor.procedimento_id == procedimento_id,
            ProcedimentoValor.convenio_id.is_not_distinct_from(convenio_id),
            ProcedimentoValor.vigencia_fim.is_(None),
        )
        .order_by(ProcedimentoValor.vigencia_inicio.desc())
        .limit(1)
    )
