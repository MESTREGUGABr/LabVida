from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from src.atendimento.amostra import repository as amostra_repository
from src.atendimento.amostra.dtos import AmostraRead, StatusAmostra
from src.atendimento.ordem_servico import repository as os_repository
from src.atendimento.ordem_servico import service as os_service
from src.atendimento.ordem_servico.dtos import StatusOrdemServico
from src.logistica.malote import repository as malote_repository
from src.logistica.malote.dtos import StatusMalote
from src.logistica.malote.errors import MaloteNaoEncontrado
from src.logistica.recebimento import repository
from src.logistica.recebimento.dtos import (
    AmostraMovimentacaoRead,
    ProtocoloRecebimentoCreate,
    ProtocoloRecebimentoRead,
)
from src.logistica.recebimento.errors import (
    MaloteJaRecebido,
    MaloteNaoEstaEmTransito,
    UsuarioRecebedorInvalido,
)
from src.logistica.recebimento.models import AmostraMovimentacao, ProtocoloRecebimento
from src.usuario import repository as usuario_repository


def _agora() -> datetime:
    return datetime.now(timezone.utc)


def receber_malote(session: Session, dto: ProtocoloRecebimentoCreate) -> ProtocoloRecebimentoRead:
    malote = malote_repository.obter_por_id(session, dto.malote_id)
    if malote is None:
        raise MaloteNaoEncontrado("Malote não encontrado")
    if malote.status == StatusMalote.RECEBIDO:
        raise MaloteJaRecebido("Malote já foi recebido anteriormente")
    if malote.status != StatusMalote.EM_TRANSITO:
        raise MaloteNaoEstaEmTransito("Apenas malotes em trânsito podem ser recebidos")

    usuario = usuario_repository.obter_por_id(session, dto.recebido_por_usuario_id)
    if usuario is None or not usuario.ativo:
        raise UsuarioRecebedorInvalido("Usuário recebedor inválido ou inativo")

    # Recusa por amostra (issue #16): a lista explícita manda; sem lista, um
    # integridade_ok=False mantém o comportamento antigo de recusar o malote inteiro.
    rejeitadas = set(dto.amostras_rejeitadas)
    rejeitar_todas = not dto.integridade_ok and not rejeitadas
    houve_rejeicao = rejeitar_todas or bool(rejeitadas)

    protocolo = ProtocoloRecebimento(
        malote_id=malote.id,
        recebido_por_usuario_id=dto.recebido_por_usuario_id,
        integridade_ok=not houve_rejeicao,
        observacao=dto.observacao,
        recebido_em=_agora(),
    )
    repository.salvar_protocolo(session, protocolo)
    malote.status = StatusMalote.RECEBIDO

    ordens_para_transicionar: set[UUID] = set()

    for item in malote.itens:
        amostra = amostra_repository.obter_por_id(session, item.amostra_id)
        if amostra is None:
            continue

        rejeitada = rejeitar_todas or amostra.id in rejeitadas
        status_alvo = StatusAmostra.REJEITADA if rejeitada else StatusAmostra.RECEBIDA
        if rejeitada:
            obs = f"Recebimento no central (rejeitada: {dto.observacao or 'sem motivo'})"
        else:
            obs = "Recebimento no central (íntegra)"

        amostra.status = status_alvo
        mov = AmostraMovimentacao(
            amostra_id=amostra.id,
            status=status_alvo,
            usuario_id=dto.recebido_por_usuario_id,
            unidade_id=malote.unidade_destino_id,
            observacao=obs,
            ocorrido_em=_agora(),
        )
        repository.salvar_movimentacao(session, mov)

        if not rejeitada:
            ordens_para_transicionar.add(amostra.ordem_servico_id)

    for ordem_id in ordens_para_transicionar:
        ordem = os_repository.obter_por_id(session, ordem_id)
        if ordem is not None and ordem.status != StatusOrdemServico.EM_ANALISE:
            os_service.registrar_transicao(
                session, ordem, StatusOrdemServico.EM_ANALISE, dto.recebido_por_usuario_id
            )

    session.commit()
    session.refresh(protocolo)
    return ProtocoloRecebimentoRead.model_validate(protocolo)


def listar_amostras_do_malote(session: Session, malote_id: UUID) -> list[AmostraRead]:
    """Amostras (com código de barras/material) de um malote, para a conferência."""
    malote = malote_repository.obter_por_id(session, malote_id)
    if malote is None:
        raise MaloteNaoEncontrado("Malote não encontrado")
    amostras = []
    for item in malote.itens:
        amostra = amostra_repository.obter_por_id(session, item.amostra_id)
        if amostra is not None:
            amostras.append(AmostraRead.model_validate(amostra))
    return amostras


def obter_protocolo(session: Session, malote_id: UUID) -> ProtocoloRecebimentoRead | None:
    protocolo = repository.obter_protocolo_por_malote(session, malote_id)
    return ProtocoloRecebimentoRead.model_validate(protocolo) if protocolo else None


def listar_historico_amostra(session: Session, amostra_id: UUID) -> list[AmostraMovimentacaoRead]:
    movs = repository.listar_movimentacoes_por_amostra(session, amostra_id)
    return [AmostraMovimentacaoRead.model_validate(m) for m in movs]
