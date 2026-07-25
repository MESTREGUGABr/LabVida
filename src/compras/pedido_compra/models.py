import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base


def _agora() -> datetime:
    return datetime.now(timezone.utc)


class SolicitacaoCompra(Base):
    __tablename__ = "solicitacoes_compra"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    solicitante_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False
    )
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="ABERTA")
    criada_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_agora)

    pedido: Mapped["PedidoCompra | None"] = relationship(
        "PedidoCompra", back_populates="solicitacao", uselist=False, cascade="all, delete-orphan"
    )


class PedidoCompra(Base):
    __tablename__ = "pedidos_compra"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    solicitacao_compra_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("solicitacoes_compra.id"), nullable=False
    )
    fornecedor_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("fornecedores.id"), nullable=False
    )
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="RASCUNHO")
    valor_total: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_agora)

    solicitacao: Mapped["SolicitacaoCompra"] = relationship("SolicitacaoCompra", back_populates="pedido")
    itens: Mapped[list["PedidoItem"]] = relationship("PedidoItem", back_populates="pedido", cascade="all, delete-orphan")
    recebimento: Mapped["RecebimentoInsumo | None"] = relationship(
        "RecebimentoInsumo", back_populates="pedido", uselist=False, cascade="all, delete-orphan"
    )


class PedidoItem(Base):
    __tablename__ = "pedidos_itens"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pedido_compra_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("pedidos_compra.id"), nullable=False, index=True
    )
    insumo_material_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("insumos_materiais.id"), nullable=False
    )
    quantidade: Mapped[float] = mapped_column(Numeric(12, 3), nullable=False)
    valor_unitario: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)

    pedido: Mapped["PedidoCompra"] = relationship("PedidoCompra", back_populates="itens")


class RecebimentoInsumo(Base):
    __tablename__ = "recebimentos_insumo"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pedido_compra_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("pedidos_compra.id"), nullable=False, index=True
    )
    recebido_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_agora)
    conferido: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    pedido: Mapped["PedidoCompra"] = relationship("PedidoCompra", back_populates="recebimento")
