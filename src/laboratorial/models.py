import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base


class StatusResultado(enum.Enum):
    AGUARDANDO_REVISAO = "AGUARDANDO_REVISAO"
    REVISADO = "REVISADO"


class StatusLaudo(enum.Enum):
    RASCUNHO = "RASCUNHO"
    LIBERADO = "LIBERADO"


class ProtocoloEquipamento(enum.Enum):
    HL7 = "HL7"
    ASTM = "ASTM"


class Equipamento(Base):
    __tablename__ = "equipamentos"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    setor_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)  # FK para setor (Cadastro)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    protocolo: Mapped[ProtocoloEquipamento] = mapped_column(Enum(ProtocoloEquipamento, name="protocolo_equipamento"), nullable=False)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


class ValorReferencia(Base):
    __tablename__ = "valores_referencia"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    procedimento_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)  # FK para procedimento (Cadastro)
    analito: Mapped[str] = mapped_column(String(120), nullable=False)
    minimo: Mapped[float | None] = mapped_column(Numeric(10, 4), nullable=True)
    maximo: Mapped[float | None] = mapped_column(Numeric(10, 4), nullable=True)
    valor_esperado_texto: Mapped[str | None] = mapped_column(String(120), nullable=True)
    unidade_medida: Mapped[str | None] = mapped_column(String(50), nullable=True)


class Resultado(Base):
    __tablename__ = "resultados"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    os_item_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)  # FK para os_item (Atendimento)
    equipamento_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("equipamentos.id"), nullable=True)
    analito: Mapped[str] = mapped_column(String(120), nullable=False)
    valor: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[StatusResultado] = mapped_column(Enum(StatusResultado, name="status_resultado"), nullable=False, default=StatusResultado.AGUARDANDO_REVISAO)
    importado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))


class Laudo(Base):
    __tablename__ = "laudos"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    os_item_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, unique=True)  # FK para os_item
    responsavel_tecnico_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)  # FK para medico responsavel
    status: Mapped[StatusLaudo] = mapped_column(Enum(StatusLaudo, name="status_laudo"), nullable=False, default=StatusLaudo.RASCUNHO)
    liberado_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    assinatura_digital: Mapped[str | None] = mapped_column(Text, nullable=True)


class ResultadoAuditoria(Base):
    __tablename__ = "resultados_auditoria"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resultado_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("resultados.id"), nullable=False, index=True)
    usuario_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)  # FK para usuario
    valor_anterior: Mapped[str] = mapped_column(String(255), nullable=False)
    valor_novo: Mapped[str] = mapped_column(String(255), nullable=False)
    ocorrido_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    resultado = relationship("Resultado")
