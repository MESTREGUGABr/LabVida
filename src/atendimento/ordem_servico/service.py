import uuid
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from src.atendimento.ordem_servico import repository
from src.atendimento.ordem_servico.dtos import (
    OrdemServicoCreate,
    OrdemServicoRead,
    OsItemRead,
    OsStatusHistoricoRead,
    StatusOrdemServico,
    StatusOsItem,
)
from src.atendimento.ordem_servico.errors import (
    ConvenioInvalidoParaOS,
    MedicoInvalidoParaOS,
    OrdemServicoNaoEncontrada,
    PacienteInvalidoParaOS,
    ProcedimentoInvalidoParaOS,
    UnidadeInvalidaParaOS,
    ValorItemNaoDefinido,
)
from src.atendimento.ordem_servico.models import OrdemServico, OsItem, OsStatusHistorico
from src.cadastro.convenio import repository as convenio_repository
from src.cadastro.convenio.dtos import StatusConvenio
from src.cadastro import repository as paciente_repository
from src.cadastro.medico import repository as medico_repository
from src.cadastro.procedimento import repository as procedimento_repository
from src.cadastro.procedimento.service import obter_valor_vigente
from src.cadastro.unidade import repository as unidade_repository


def abrir_os(session: Session, dto: OrdemServicoCreate, usuario_id: UUID | None = None) -> OrdemServicoRead:
    """Abre a Ordem de Serviço (entidade-espinha) validando os pré-requisitos.

    Regras: paciente ativo, unidade ativa, médico (se informado) ativo, convênio
    (se informado) ATIVO, ao menos um item com procedimento ativo e valor definido.
    Tudo numa única transação: OS + itens + primeiro histórico de status.
    """
    paciente = paciente_repository.obter_por_id(session, dto.paciente_id)
    if paciente is None or not paciente.ativo:
        raise PacienteInvalidoParaOS("Paciente inválido ou inativo")

    unidade = unidade_repository.obter_unidade_por_id(session, dto.unidade_id)
    if unidade is None or not unidade.ativo:
        raise UnidadeInvalidaParaOS("Unidade inválida ou inativa")

    if dto.medico_id is not None:
        medico = medico_repository.obter_por_id(session, dto.medico_id)
        if medico is None or not medico.ativo:
            raise MedicoInvalidoParaOS("Médico inválido ou inativo")

    convenio = None
    if dto.convenio_id is not None:
        convenio = convenio_repository.obter_por_id(session, dto.convenio_id)
        if convenio is None or convenio.status != StatusConvenio.ATIVO:
            raise ConvenioInvalidoParaOS("Convênio inválido ou inativo")

    ordem = OrdemServico(
        codigo_os=_gerar_codigo_os(session),
        paciente_id=dto.paciente_id,
        medico_id=dto.medico_id,
        convenio_id=dto.convenio_id,
        unidade_id=dto.unidade_id,
        status=StatusOrdemServico.ABERTA,
    )
    repository.salvar(session, ordem)
    session.flush()

    for entrada in dto.itens:
        procedimento = procedimento_repository.obter_por_id(session, entrada.procedimento_id)
        if procedimento is None or not procedimento.ativo:
            raise ProcedimentoInvalidoParaOS("Procedimento inválido ou inativo")

        valor = entrada.valor_negociado
        if valor is None and convenio is not None:
            valor = obter_valor_vigente(session, procedimento.id, convenio.id)
        if valor is None:
            raise ValorItemNaoDefinido(
                f"Valor não definido para o procedimento {procedimento.nome}"
            )

        repository.salvar_item(
            session,
            OsItem(
                ordem_servico_id=ordem.id,
                procedimento_id=procedimento.id,
                valor_negociado=valor,
                status=StatusOsItem.SOLICITADO,
            ),
        )

    _registrar_historico(session, ordem.id, StatusOrdemServico.ABERTA, usuario_id)

    session.commit()
    session.refresh(ordem)
    return OrdemServicoRead.model_validate(ordem)


def obter_os(session: Session, ordem_servico_id: UUID) -> OrdemServicoRead:
    ordem = repository.obter_por_id(session, ordem_servico_id)
    if ordem is None:
        raise OrdemServicoNaoEncontrada("Ordem de Serviço não encontrada")
    return OrdemServicoRead.model_validate(ordem)


def listar_os(session: Session) -> list[OrdemServicoRead]:
    return [OrdemServicoRead.model_validate(o) for o in repository.listar(session)]


def listar_itens(session: Session, ordem_servico_id: UUID) -> list[OsItemRead]:
    return [OsItemRead.model_validate(i) for i in repository.listar_itens(session, ordem_servico_id)]


def listar_historico(session: Session, ordem_servico_id: UUID) -> list[OsStatusHistoricoRead]:
    return [
        OsStatusHistoricoRead.model_validate(h)
        for h in repository.listar_historico(session, ordem_servico_id)
    ]


def registrar_transicao(
    session: Session, ordem: OrdemServico, novo_status: StatusOrdemServico, usuario_id: UUID | None
) -> None:
    """Aplica a transição de status na OS e registra o histórico (sem commit).

    Pensado para ser chamado dentro da transação de outro service (ex.: coleta),
    garantindo atomicidade da operação ponta a ponta.
    """
    ordem.status = novo_status
    _registrar_historico(session, ordem.id, novo_status, usuario_id)


def _registrar_historico(
    session: Session, ordem_servico_id: UUID, status: StatusOrdemServico, usuario_id: UUID | None
) -> None:
    repository.salvar_historico(
        session,
        OsStatusHistorico(ordem_servico_id=ordem_servico_id, status=status, usuario_id=usuario_id),
    )


def _gerar_codigo_os(session: Session) -> str:
    ano = datetime.now(timezone.utc).year
    for _ in range(10):
        codigo = f"OS-{ano}-{uuid.uuid4().hex[:6].upper()}"
        if repository.obter_por_codigo(session, codigo) is None:
            return codigo
    raise RuntimeError("Não foi possível gerar um código de OS único")
