from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.logistica.recebimento.models import AmostraMovimentacao, ProtocoloRecebimento


def salvar_protocolo(session: Session, protocolo: ProtocoloRecebimento) -> ProtocoloRecebimento:
    session.add(protocolo)
    return protocolo


def salvar_movimentacao(session: Session, movimentacao: AmostraMovimentacao) -> AmostraMovimentacao:
    session.add(movimentacao)
    return movimentacao


def obter_protocolo_por_malote(session: Session, malote_id: UUID) -> ProtocoloRecebimento | None:
    stmt = select(ProtocoloRecebimento).where(ProtocoloRecebimento.malote_id == malote_id)
    return session.execute(stmt).scalar_one_or_none()


def listar_movimentacoes_por_amostra(session: Session, amostra_id: UUID) -> list[AmostraMovimentacao]:
    stmt = (
        select(AmostraMovimentacao)
        .where(AmostraMovimentacao.amostra_id == amostra_id)
        .order_by(AmostraMovimentacao.ocorrido_em.asc())
    )
    return list(session.scalars(stmt).all())
