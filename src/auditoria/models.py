import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.db import Base


class AuditoriaLog(Base):
    __tablename__ = "auditoria_log"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False, index=True
    )
    entidade: Mapped[str] = mapped_column(String(50), nullable=False)
    entidade_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    acao: Mapped[str] = mapped_column(String(30), nullable=False)
    dados: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    ocorrido_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
