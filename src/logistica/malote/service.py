import uuid
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from src.atendimento.amostra import repository as amostra_repository
from src.atendimento.amostra.dtos import StatusAmostra
from src.cadastro.unidade import repository as unidade_repository
from src.logistica.malote import repository
from src.logistica.malote.dtos import MaloteCreate, MaloteRead, StatusMalote
from src.logistica.malote.errors import (
    AmostraInvalidaParaMalote,
    MaloteFechadoOuInvalido,
    MaloteNaoEncontrado,
    UnidadeOuUsuarioInvalido,
)
from src.logistica.malote.models import Malote, MaloteAmostra
from src.logistica.recebimento import repository as movimentacao_repository
from src.logistica.recebimento.models import AmostraMovimentacao
from src.usuario import repository as usuario_repository


def _agora() -> datetime:
    return datetime.now(timezone.utc)


def criar_malote(session: Session, dto: MaloteCreate) -> MaloteRead:
    origem = unidade_repository.obter_unidade_por_id(session, dto.unidade_origem_id)
    if origem is None or not origem.ativo:
        raise UnidadeOuUsuarioInvalido("Unidade de origem inválida ou inativa")

    destino = unidade_repository.obter_unidade_por_id(session, dto.unidade_destino_id)
    if destino is None or not destino.ativo:
        raise UnidadeOuUsuarioInvalido("Unidade de destino inválida ou inativa")

    usuario = usuario_repository.obter_por_id(session, dto.enviado_por_usuario_id)
    if usuario is None or not usuario.ativo:
        raise UnidadeOuUsuarioInvalido("Usuário remetente inválido ou inativo")

    malote = Malote(
        codigo_malote=_gerar_codigo_malote(session),
        unidade_origem_id=dto.unidade_origem_id,
        unidade_destino_id=dto.unidade_destino_id,
        enviado_por_usuario_id=dto.enviado_por_usuario_id,
        status=StatusMalote.ABERTO,
    )
    repository.salvar_malote(session, malote)
    session.commit()
    session.refresh(malote)
    return MaloteRead.model_validate(malote)


def adicionar_amostra_ao_malote(session: Session, malote_id: UUID, amostra_id: UUID) -> MaloteRead:
    malote = repository.obter_por_id(session, malote_id)
    if malote is None:
        raise MaloteNaoEncontrado("Malote não encontrado")
    if malote.status != StatusMalote.ABERTO:
        raise MaloteFechadoOuInvalido("Apenas malotes ABERTOS podem receber amostras")

    amostra = amostra_repository.obter_por_id(session, amostra_id)
    if amostra is None:
        raise AmostraInvalidaParaMalote("Amostra não encontrada")
    if amostra.status != StatusAmostra.COLETADA:
        raise AmostraInvalidaParaMalote("Apenas amostras com status COLETADA podem ser adicionadas ao malote")

    item_existente = repository.obter_item_por_amostra(session, amostra_id)
    if item_existente is not None:
        raise AmostraInvalidaParaMalote("Amostra já está vinculada a um malote")

    item = MaloteAmostra(malote_id=malote.id, amostra_id=amostra.id)
    repository.vincular_amostra(session, item)
    session.commit()
    session.refresh(malote)
    return MaloteRead.model_validate(malote)


def despachar_malote(session: Session, malote_id: UUID, usuario_id: UUID) -> MaloteRead:
    malote = repository.obter_por_id(session, malote_id)
    if malote is None:
        raise MaloteNaoEncontrado("Malote não encontrado")
    if malote.status != StatusMalote.ABERTO:
        raise MaloteFechadoOuInvalido("Malote já foi despachado ou fechado")
    if not malote.itens:
        raise MaloteFechadoOuInvalido("Não é possível despachar um malote sem amostras")

    usuario = usuario_repository.obter_por_id(session, usuario_id)
    if usuario is None or not usuario.ativo:
        raise UnidadeOuUsuarioInvalido("Usuário remetente inválido ou inativo")

    malote.status = StatusMalote.EM_TRANSITO
    malote.despachado_em = _agora()

    for item in malote.itens:
        amostra = amostra_repository.obter_por_id(session, item.amostra_id)
        if amostra is not None:
            amostra.status = StatusAmostra.EM_TRANSITO
            mov = AmostraMovimentacao(
                amostra_id=amostra.id,
                status=StatusAmostra.EM_TRANSITO,
                usuario_id=usuario_id,
                unidade_id=malote.unidade_origem_id,
                observacao=f"Em trânsito no malote {malote.codigo_malote}",
                ocorrido_em=_agora(),
            )
            movimentacao_repository.salvar_movimentacao(session, mov)

    session.commit()
    session.refresh(malote)
    return MaloteRead.model_validate(malote)


def obter_malote(session: Session, malote_id: UUID) -> MaloteRead | None:
    malote = repository.obter_por_id(session, malote_id)
    return MaloteRead.model_validate(malote) if malote else None


def obter_malote_por_codigo(session: Session, codigo_malote: str) -> MaloteRead | None:
    malote = repository.obter_por_codigo(session, codigo_malote)
    return MaloteRead.model_validate(malote) if malote else None


def listar_malotes_por_unidade_origem(session: Session, unidade_origem_id: UUID) -> list[MaloteRead]:
    return [MaloteRead.model_validate(m) for m in repository.listar_por_unidade_origem(session, unidade_origem_id)]


def listar_malotes_em_transito_para_unidade(session: Session, unidade_destino_id: UUID) -> list[MaloteRead]:
    return [MaloteRead.model_validate(m) for m in repository.listar_em_transito_para_unidade(session, unidade_destino_id)]


def _gerar_codigo_malote(session: Session) -> str:
    for _ in range(10):
        codigo = f"ML{uuid.uuid4().hex[:12].upper()}"
        if repository.obter_por_codigo(session, codigo) is None:
            return codigo
    raise RuntimeError("Não foi possível gerar um código de malote único")
