import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.db import Base


def _agora() -> datetime:
    return datetime.now(timezone.utc)


class Fornecedor(Base):
    __tablename__ = "fornecedores"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    cnpj: Mapped[str] = mapped_column(String(14), nullable=False, unique=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="ATIVO")
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_agora)


class SolicitacaoCompra(Base):
    __tablename__ = "solicitacoes_compra"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    solicitante_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False
    )
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="ABERTA")
    criada_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_agora)


class PedidoCompra(Base):
    __tablename__ = "pedidos_compra"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    solicitacao_compra_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False
    )
    fornecedor_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False
    )
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="RASCUNHO")
    valor_total: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_agora)
