from datetime import date
from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session

from src.cadastro.convenio import repository as convenio_repository
from src.cadastro.convenio.errors import ConvenioNaoEncontrado
from src.cadastro.procedimento import repository
from src.cadastro.procedimento.dtos import (
    ProcedimentoCreate,
    ProcedimentoRead,
    ProcedimentoValorCreate,
    ProcedimentoValorRead,
)
from src.cadastro.procedimento.errors import CodigoTussDuplicado, ProcedimentoNaoEncontrado
from src.cadastro.procedimento.models import Procedimento, ProcedimentoValor


def criar_procedimento(session: Session, dto: ProcedimentoCreate) -> ProcedimentoRead:
    if repository.obter_por_codigo_tuss(session, dto.codigo_tuss):
        raise CodigoTussDuplicado("Procedimento já cadastrado com este código TUSS")

    procedimento = Procedimento(
        codigo_tuss=dto.codigo_tuss,
        nome=dto.nome,
        setor=dto.setor,
        ativo=True,
    )
    repository.salvar(session, procedimento)
    session.commit()
    session.refresh(procedimento)
    return ProcedimentoRead.model_validate(procedimento)


def listar_procedimentos_ativos(session: Session) -> list[ProcedimentoRead]:
    return [ProcedimentoRead.model_validate(p) for p in repository.listar_ativos(session)]


def definir_valor(session: Session, dto: ProcedimentoValorCreate) -> ProcedimentoValorRead:
    if repository.obter_por_id(session, dto.procedimento_id) is None:
        raise ProcedimentoNaoEncontrado("Procedimento não encontrado")
    if convenio_repository.obter_por_id(session, dto.convenio_id) is None:
        raise ConvenioNaoEncontrado("Convênio não encontrado")

    valor = ProcedimentoValor(
        procedimento_id=dto.procedimento_id,
        convenio_id=dto.convenio_id,
        valor=dto.valor,
        vigencia_inicio=dto.vigencia_inicio,
    )
    repository.salvar_valor(session, valor)
    session.commit()
    session.refresh(valor)
    return ProcedimentoValorRead.model_validate(valor)


def obter_valor_vigente(
    session: Session, procedimento_id: UUID, convenio_id: UUID, na_data: date | None = None
) -> Decimal | None:
    valor = repository.obter_valor_vigente(
        session, procedimento_id, convenio_id, na_data or date.today()
    )
    return valor.valor if valor else None
