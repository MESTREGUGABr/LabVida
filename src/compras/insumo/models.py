import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.db import Base


def _agora() -> datetime:
    return datetime.now(timezone.utc)


class InsumoMaterial(Base):
    __tablename__ = "insumos_materiais"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    finalidade: Mapped[str] = mapped_column(String(255), nullable=False)
    quantidade_estoque: Mapped[float] = mapped_column(Numeric(12, 3), nullable=False, default=0)
    # So alerta visual (tela de Estoque) -- nao bloqueia nada, nao esta ligado
    # a nenhum procedimento. Ver F16 (candidata) em docs/roadmap-execucao.md.
    estoque_minimo: Mapped[float] = mapped_column(Numeric(12, 3), nullable=False, default=0)
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_agora)


class EstoqueMovimento(Base):
    __tablename__ = "estoque_movimentos"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    insumo_material_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("insumos_materiais.id"), nullable=False, index=True
    )
    tipo: Mapped[str] = mapped_column(String(20), nullable=False)
    quantidade: Mapped[float] = mapped_column(Numeric(12, 3), nullable=False)
    ocorrido_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_agora)
    observacao: Mapped[str | None] = mapped_column(String(255), nullable=True)
