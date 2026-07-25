import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.db import Base


def _agora() -> datetime:
    return datetime.now(timezone.utc)


class MovimentoCaixa(Base):
    __tablename__ = "movimentos_caixa"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    titulo_receber_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("titulos_receber.id"), nullable=True
    )
    titulo_pagar_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("titulos_pagar.id"), nullable=True
    )
    tipo: Mapped[str] = mapped_column(String(20), nullable=False)
    valor: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    ocorrido_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_agora)
    descricao: Mapped[str | None] = mapped_column(String(255), nullable=True)
