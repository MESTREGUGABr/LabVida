from datetime import date, timedelta
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
from src.auditoria import registrar_auditoria


def criar_procedimento(session: Session, dto: ProcedimentoCreate, usuario_id: UUID | None = None) -> ProcedimentoRead:
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

    if usuario_id is not None:
        registrar_auditoria(session, usuario_id, entidade="procedimento",
            entidade_id=procedimento.id, acao="CRIAR_PROCEDIMENTO",
            dados={"codigo_tuss": procedimento.codigo_tuss, "nome": procedimento.nome})

    return ProcedimentoRead.model_validate(procedimento)


def listar_procedimentos_ativos(session: Session) -> list[ProcedimentoRead]:
    return [ProcedimentoRead.model_validate(p) for p in repository.listar_ativos(session)]


def definir_valor(session: Session, dto: ProcedimentoValorCreate, usuario_id: UUID | None = None) -> ProcedimentoValorRead:
    """Define o preco vigente a partir de uma data.

    `convenio_id=None` cadastra na **tabela particular**.

    Antes de inserir, ENCERRA a vigencia em aberto do mesmo par
    (procedimento, convenio) no dia anterior. Sem isso o `EXCLUDE` do banco
    rejeita a insercao — e e proposital: duas faixas de vigencia sobrepostas
    significariam dois precos validos na mesma data.
    """
    if repository.obter_por_id(session, dto.procedimento_id) is None:
        raise ProcedimentoNaoEncontrado("Procedimento não encontrado")
    if dto.convenio_id is not None and convenio_repository.obter_por_id(session, dto.convenio_id) is None:
        raise ConvenioNaoEncontrado("Convênio não encontrado")

    anterior = repository.obter_vigencia_aberta(session, dto.procedimento_id, dto.convenio_id)
    if anterior is not None:
        if anterior.vigencia_inicio >= dto.vigencia_inicio:
            raise ValueError(
                "Ja existe preco vigente a partir de "
                f"{anterior.vigencia_inicio.strftime('%d/%m/%Y')}. "
                "O novo preco precisa comecar depois dessa data."
            )
        anterior.vigencia_fim = dto.vigencia_inicio - timedelta(days=1)
        session.flush()

    valor = ProcedimentoValor(
        procedimento_id=dto.procedimento_id,
        convenio_id=dto.convenio_id,
        valor=dto.valor,
        vigencia_inicio=dto.vigencia_inicio,
    )
    repository.salvar_valor(session, valor)
    session.commit()
    session.refresh(valor)

    if usuario_id is not None:
        registrar_auditoria(session, usuario_id, entidade="procedimento_valor",
            entidade_id=valor.id, acao="DEFINIR_VALOR_PROCEDIMENTO",
            dados={"procedimento_id": str(dto.procedimento_id), "valor": str(dto.valor)})

    return ProcedimentoValorRead.model_validate(valor)


def obter_valor_vigente(
    session: Session, procedimento_id: UUID, convenio_id: UUID | None, na_data: date | None = None
) -> Decimal | None:
    valor = repository.obter_valor_vigente(
        session, procedimento_id, convenio_id, na_data or date.today()
    )
    return valor.valor if valor else None


def vincular_insumo_procedimento(
    session: Session, procedimento_id: UUID, insumo_material_id: UUID, quantidade_necessaria: float = 1.0
) -> None:
    repository.vincular_insumo(session, procedimento_id, insumo_material_id, quantidade_necessaria)
    session.commit()

