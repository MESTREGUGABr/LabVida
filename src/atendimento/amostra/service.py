import uuid
from uuid import UUID

from sqlalchemy.orm import Session

from src.atendimento.amostra import repository
from src.atendimento.amostra.dtos import AmostraRead, ColetaCreate, StatusAmostra
from src.atendimento.amostra.errors import ColetaNaoPermitida, ColetorInvalido, OrdemServicoInexistente
from src.atendimento.amostra.models import Amostra, Coleta
from src.atendimento.ordem_servico import repository as os_repository
from src.atendimento.ordem_servico import service as os_service
from src.atendimento.ordem_servico.dtos import StatusOrdemServico
from src.usuario import repository as usuario_repository


_STATUS_OS_BLOQUEIA_COLETA = {StatusOrdemServico.CONCLUIDA, StatusOrdemServico.CANCELADA}


def registrar_coleta(session: Session, dto: ColetaCreate) -> AmostraRead:
    """Registra a coleta: cria a amostra (cadeia de custódia) e vincula o coletor.

    Numa transação só: gera a amostra COLETADA com código de barras, grava a
    coleta com o usuário coletor e transiciona a OS para COLETADA (com histórico).
    A pendência logística (amostra_movimentacao) é aberta pela Stack B a partir
    daqui.
    """
    ordem = os_repository.obter_por_id(session, dto.ordem_servico_id)
    if ordem is None:
        raise OrdemServicoInexistente("Ordem de Serviço não encontrada")
    if ordem.status in _STATUS_OS_BLOQUEIA_COLETA:
        raise ColetaNaoPermitida("Ordem de Serviço não permite novas coletas")

    coletor = usuario_repository.obter_por_id(session, dto.coletor_usuario_id)
    if coletor is None or not coletor.ativo:
        raise ColetorInvalido("Coletor inválido ou inativo")

    amostra = Amostra(
        ordem_servico_id=ordem.id,
        codigo_barras=_gerar_codigo_barras(session),
        tipo_material=dto.tipo_material,
        status=StatusAmostra.COLETADA,
    )
    repository.salvar_amostra(session, amostra)
    session.flush()

    repository.salvar_coleta(
        session, Coleta(amostra_id=amostra.id, coletor_id=coletor.id)
    )

    if ordem.status != StatusOrdemServico.COLETADA:
        os_service.registrar_transicao(session, ordem, StatusOrdemServico.COLETADA, coletor.id)

    session.commit()
    session.refresh(amostra)
    return AmostraRead.model_validate(amostra)


def listar_amostras(session: Session, ordem_servico_id: UUID) -> list[AmostraRead]:
    return [AmostraRead.model_validate(a) for a in repository.listar_por_os(session, ordem_servico_id)]


def _gerar_codigo_barras(session: Session) -> str:
    for _ in range(10):
        codigo = f"AM{uuid.uuid4().hex[:12].upper()}"
        if repository.obter_por_codigo_barras(session, codigo) is None:
            return codigo
    raise RuntimeError("Não foi possível gerar um código de barras único")
