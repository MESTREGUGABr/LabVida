from datetime import date
from uuid import UUID

from sqlalchemy.orm import Session

from src.atendimento.autorizacao import repository
from src.atendimento.autorizacao.dtos import AutorizacaoCreate, AutorizacaoRead, StatusAutorizacao
from src.atendimento.autorizacao.errors import OrdemServicoInexistente
from src.atendimento.autorizacao.models import AutorizacaoConvenio
from src.atendimento.ordem_servico import repository as os_repository


def registrar_autorizacao(session: Session, dto: AutorizacaoCreate) -> AutorizacaoRead:
    if os_repository.obter_por_id(session, dto.ordem_servico_id) is None:
        raise OrdemServicoInexistente("Ordem de Serviço não encontrada")

    autorizacao = AutorizacaoConvenio(
        ordem_servico_id=dto.ordem_servico_id,
        numero_guia=dto.numero_guia,
        status=dto.status,
        validade=dto.validade,
    )
    repository.salvar(session, autorizacao)
    session.commit()
    session.refresh(autorizacao)
    return AutorizacaoRead.model_validate(autorizacao)


def listar_autorizacoes(session: Session, ordem_servico_id: UUID) -> list[AutorizacaoRead]:
    return [
        AutorizacaoRead.model_validate(a) for a in repository.listar_por_os(session, ordem_servico_id)
    ]


def possui_autorizacao_valida(session: Session, ordem_servico_id: UUID) -> bool:
    hoje = date.today()
    for autorizacao in repository.listar_por_os(session, ordem_servico_id):
        if autorizacao.status == StatusAutorizacao.VALIDA and (
            autorizacao.validade is None or autorizacao.validade >= hoje
        ):
            return True
    return False
