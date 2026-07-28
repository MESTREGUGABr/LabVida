import uuid
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import select

from src.auditoria import registrar_auditoria
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
    ItemNaoPodeSerCancelado,
    OrdemServicoNaoPodeSerCancelada,
    OrdemServicoNaoEncontrada,
    OsItemNaoEncontrado,
    PacienteInvalidoParaOS,
    ProcedimentoInvalidoParaOS,
    UnidadeInvalidaParaOS,
    UsuarioNaoAutorizadoParaCancelamento,
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
from src.usuario import repository as usuario_repository


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

    if usuario_id is not None:
        registrar_auditoria(
            session,
            usuario_id,
            entidade="ordem_servico",
            entidade_id=ordem.id,
            acao="ABRIR_OS",
            dados={"codigo_os": ordem.codigo_os, "itens": len(dto.itens)},
        )

    session.commit()
    session.refresh(ordem)
    return OrdemServicoRead.model_validate(ordem)


def obter_os(session: Session, ordem_servico_id: UUID) -> OrdemServicoRead:
    ordem = repository.obter_por_id(session, ordem_servico_id)
    if ordem is None:
        raise OrdemServicoNaoEncontrada("Ordem de Serviço não encontrada")
    return OrdemServicoRead.model_validate(ordem)


def listar_os(
    session: Session,
    busca: str | None = None,
    status: str | None = None,
    limite: int = 100,
    offset: int = 0,
) -> list[OrdemServicoRead]:
    ordens = repository.listar_filtrado(
        session, busca=busca, status=status, limite=limite, offset=offset
    )
    return [OrdemServicoRead.model_validate(o) for o in ordens]


def contar_os(session: Session, busca: str | None = None, status: str | None = None) -> int:
    return repository.contar_filtrado(session, busca=busca, status=status)


def listar_itens(session: Session, ordem_servico_id: UUID) -> list[OsItemRead]:
    return [OsItemRead.model_validate(i) for i in repository.listar_itens(session, ordem_servico_id)]


def listar_historico(session: Session, ordem_servico_id: UUID) -> list[OsStatusHistoricoRead]:
    return [
        OsStatusHistoricoRead.model_validate(h)
        for h in repository.listar_historico(session, ordem_servico_id)
    ]


def _validar_permissao_cancelar(session: Session, usuario_id: UUID) -> None:
    """Bloqueia cancelamento quando RBAC está ativo e usuário não tem permissão."""
    from src.rbac.models import Perfil
    from src.rbac.repository import usuario_tem_permissao

    if session.scalar(select(Perfil.id).limit(1)) is None:
        return

    if not usuario_tem_permissao(session, usuario_id, "atendimento:cancelar_os"):
        raise UsuarioNaoAutorizadoParaCancelamento(
            "Usuário sem permissão para cancelar itens"
        )


def cancelar_item_os(session: Session, os_item_id: UUID, usuario_id: UUID) -> OsItemRead:
    """Cancela um item ativo e recalcula o status agregado da sua OS.

    Todas as validações acontecem antes da primeira alteração persistente. O
    commit único mantém item, OS e histórico na mesma transação.
    """
    usuario = usuario_repository.obter_por_id(session, usuario_id)
    if usuario is None or not usuario.ativo:
        raise UsuarioNaoAutorizadoParaCancelamento("Usuário inválido ou inativo")

    _validar_permissao_cancelar(session, usuario_id)

    item = repository.obter_item_por_id(session, os_item_id)
    if item is None:
        raise OsItemNaoEncontrado("Item da Ordem de Serviço não encontrado")

    ordem = repository.obter_por_id(session, item.ordem_servico_id)
    if ordem is None:
        raise OrdemServicoNaoEncontrada("Ordem de Serviço não encontrada")
    _validar_item_cancelavel(session, item)
    if ordem.status in {StatusOrdemServico.CONCLUIDA, StatusOrdemServico.CANCELADA}:
        raise ItemNaoPodeSerCancelado("Não é possível cancelar item de uma OS terminal")

    item.status = StatusOsItem.CANCELADO
    item.cancelado_por_usuario_id = usuario_id
    _atualizar_status_agregado(session, ordem, usuario_id)
    registrar_auditoria(
        session,
        usuario_id,
        entidade="os_item",
        entidade_id=item.id,
        acao="CANCELAR_ITEM",
        dados={
            "ordem_servico_id": str(item.ordem_servico_id),
            "procedimento_id": str(item.procedimento_id),
        },
    )
    session.commit()
    session.refresh(item)
    return OsItemRead.model_validate(item)


def cancelar_os(session: Session, ordem_servico_id: UUID, usuario_id: UUID) -> OrdemServicoRead:
    """Cancela integralmente uma OS quando nenhum item concluído a impede."""
    usuario = usuario_repository.obter_por_id(session, usuario_id)
    if usuario is None or not usuario.ativo:
        raise UsuarioNaoAutorizadoParaCancelamento("Usuário inválido ou inativo")

    _validar_permissao_cancelar(session, usuario_id)

    ordem = repository.obter_por_id(session, ordem_servico_id)
    if ordem is None:
        raise OrdemServicoNaoEncontrada("Ordem de Serviço não encontrada")
    itens = repository.listar_itens(session, ordem.id)
    if not itens:
        raise OrdemServicoNaoPodeSerCancelada("Ordem de Serviço sem itens")
    if ordem.status in {StatusOrdemServico.CONCLUIDA, StatusOrdemServico.CANCELADA}:
        raise OrdemServicoNaoPodeSerCancelada("Ordem de Serviço já está em estado terminal")

    if any(
        item.status == StatusOsItem.RESULTADO_LIBERADO
        or repository.item_tem_laudo_liberado(session, item.id)
        or repository.item_faturado(session, item)
        for item in itens
    ):
        raise OrdemServicoNaoPodeSerCancelada(
            "A OS contém item com Laudo liberado ou faturado"
        )

    for item in itens:
        item.status = StatusOsItem.CANCELADO
        item.cancelado_por_usuario_id = usuario_id
    _atualizar_status_agregado(session, ordem, usuario_id)
    registrar_auditoria(
        session,
        usuario_id,
        entidade="ordem_servico",
        entidade_id=ordem.id,
        acao="CANCELAR_OS",
        dados={"codigo_os": ordem.codigo_os},
    )
    session.commit()
    session.refresh(ordem)
    return OrdemServicoRead.model_validate(ordem)


def _validar_item_cancelavel(session: Session, item: OsItem) -> None:
    if item.status == StatusOsItem.CANCELADO:
        raise ItemNaoPodeSerCancelado("Item já está cancelado")
    if item.status == StatusOsItem.RESULTADO_LIBERADO:
        raise ItemNaoPodeSerCancelado("Item com Laudo liberado não pode ser cancelado")
    if repository.item_tem_laudo_liberado(session, item.id):
        raise ItemNaoPodeSerCancelado("Item com Laudo liberado não pode ser cancelado")
    if repository.item_faturado(session, item):
        raise ItemNaoPodeSerCancelado("Item faturado não pode ser cancelado")


def _atualizar_status_agregado(
    session: Session, ordem: OrdemServico, usuario_id: UUID
) -> None:
    itens = repository.listar_itens(session, ordem.id)
    if not itens:
        return
    if all(item.status == StatusOsItem.CANCELADO for item in itens):
        novo_status = StatusOrdemServico.CANCELADA
    else:
        ativos = [item for item in itens if item.status != StatusOsItem.CANCELADO]
        todos_liberados = all(
            repository.item_tem_laudo_liberado(session, item.id) for item in ativos
        )
        novo_status = StatusOrdemServico.CONCLUIDA if todos_liberados else ordem.status
    if novo_status != ordem.status:
        registrar_transicao(session, ordem, novo_status, usuario_id)


def registrar_transicao(
    session: Session, ordem: OrdemServico, novo_status: StatusOrdemServico, usuario_id: UUID | None
) -> None:
    """Aplica a transição de status na OS e registra o histórico (sem commit).

    Pensado para ser chamado dentro da transação de outro service (ex.: coleta),
    garantindo atomicidade da operação ponta a ponta.
    """
    if ordem.status == novo_status:
        return
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
