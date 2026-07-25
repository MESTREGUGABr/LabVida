import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base


def _agora() -> datetime:
    return datetime.now(timezone.utc)


class LoteFaturamento(Base):
    __tablename__ = "lotes_faturamento"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo_lote: Mapped[str] = mapped_column(String(20), nullable=False, unique=True, index=True)
    convenio_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("convenios.id"), nullable=True, index=True
    )
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="ABERTO")
    valor_total: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_agora)
    fechado_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    guias: Mapped[list["GuiaTiss"]] = relationship(
        "GuiaTiss", back_populates="lote", cascade="all, delete-orphan"
    )


class GuiaTiss(Base):
    __tablename__ = "guias_tiss"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lote_faturamento_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("lotes_faturamento.id"), nullable=False, index=True
    )
    codigo_tiss: Mapped[str] = mapped_column(String(30), nullable=False)
    status_pre_auditoria: Mapped[str] = mapped_column(String(30), nullable=False, default="PENDENTE")
    xml_tiss: Mapped[str | None] = mapped_column(Text, nullable=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_agora)

    lote: Mapped["LoteFaturamento"] = relationship("LoteFaturamento", back_populates="guias")
    itens: Mapped[list["GuiaItem"]] = relationship(
        "GuiaItem", back_populates="guia", cascade="all, delete-orphan"
    )


class GuiaItem(Base):
    __tablename__ = "guias_itens"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    guia_tiss_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("guias_tiss.id"), nullable=False, index=True
    )
    laudo_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("laudos.id"), nullable=False, unique=True
    )
    procedimento_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("procedimentos.id"), nullable=False
    )
    valor_faturado: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="FATURADO")
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_agora)

    guia: Mapped["GuiaTiss"] = relationship("GuiaTiss", back_populates="itens")
