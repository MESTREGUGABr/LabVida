from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from src.auditoria.models import AuditoriaLog


def registrar_auditoria(
    session: Session,
    usuario_id: UUID,
    entidade: str,
    entidade_id: UUID | None,
    acao: str,
    dados: dict | None = None,
) -> None:
    log = AuditoriaLog(
        usuario_id=usuario_id,
        entidade=entidade,
        entidade_id=entidade_id,
        acao=acao,
        dados=dados or {},
    )
    session.add(log)
