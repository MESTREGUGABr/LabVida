import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.db import Base


def _agora() -> datetime:
    return datetime.now(timezone.utc)


class Amostra(Base):
    __tablename__ = "amostras"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ordem_servico_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("ordens_servico.id"), nullable=False, index=True
    )
    codigo_barras: Mapped[str] = mapped_column(String(20), nullable=False, unique=True, index=True)
    tipo_material: Mapped[str] = mapped_column(String(40), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)


class Coleta(Base):
    __tablename__ = "coletas"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    amostra_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("amostras.id"), nullable=False, unique=True, index=True
    )
    coletor_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False
    )
    coletada_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_agora)
