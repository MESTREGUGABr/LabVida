import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base


def _agora() -> datetime:
    return datetime.now(timezone.utc)


class Malote(Base):
    __tablename__ = "malotes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo_malote: Mapped[str] = mapped_column(String(20), nullable=False, unique=True, index=True)
    unidade_origem_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("unidades.id"), nullable=False, index=True
    )
    unidade_destino_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("unidades.id"), nullable=False, index=True
    )
    enviado_por_usuario_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False
    )
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="ABERTO")
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_agora)
    despachado_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    itens: Mapped[list["MaloteAmostra"]] = relationship(
        "MaloteAmostra", back_populates="malote", cascade="all, delete-orphan"
    )


class MaloteAmostra(Base):
    __tablename__ = "malotes_amostras"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    malote_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("malotes.id"), nullable=False, index=True
    )
    amostra_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("amostras.id"), nullable=False, unique=True, index=True
    )

    malote: Mapped["Malote"] = relationship("Malote", back_populates="itens")
