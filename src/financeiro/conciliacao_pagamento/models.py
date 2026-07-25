import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.db import Base


def _agora() -> datetime:
    return datetime.now(timezone.utc)


class ConciliacaoPagamento(Base):
    __tablename__ = "conciliacoes_pagamento"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    titulo_receber_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("titulos_receber.id"), nullable=False, index=True
    )
    valor_recebido: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    divergencia: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    conciliado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_agora)
    observacao: Mapped[str | None] = mapped_column(String(255), nullable=True)
