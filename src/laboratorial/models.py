import enum
from decimal import Decimal
import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, SmallInteger, Boolean, DateTime, Enum, ForeignKey, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base
from src.atendimento.ordem_servico import models as ordem_servico_models  # noqa: F401
from src.cadastro.medico import models as medico_models  # noqa: F401
from src.cadastro.procedimento import models as procedimento_models  # noqa: F401
from src.cadastro.unidade import models as unidade_models  # noqa: F401
from src.usuario import models as usuario_models  # noqa: F401


class StatusResultado(str, enum.Enum):
    AGUARDANDO_REVISAO = "AGUARDANDO_REVISAO"
    REVISADO = "REVISADO"


class StatusLaudo(str, enum.Enum):
    RASCUNHO = "RASCUNHO"
    LIBERADO = "LIBERADO"


class ProtocoloEquipamento(str, enum.Enum):
    HL7 = "HL7"
    ASTM = "ASTM"


class Equipamento(Base):
    __tablename__ = "equipamentos"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    setor_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("setores.id"), nullable=False)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    protocolo: Mapped[ProtocoloEquipamento] = mapped_column(Enum(ProtocoloEquipamento, name="protocolo_equipamento"), nullable=False)


class Analito(Base):
    """Catalogo de analitos — o elo que faltava.

    Antes, `Resultado.analito` e `ValorReferencia.analito` eram duas strings
    livres independentes: a bancada digitava "Hemoglobina", a faixa estava
    cadastrada como "hemoglobina", e nenhum codigo casava as duas. A faixa de
    referencia existia no banco e nao era aplicavel.
    """

    __tablename__ = "analitos"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    unidade_medida: Mapped[str | None] = mapped_column(String(20), nullable=True)
    casas_decimais: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=2)
    # Espaco para a camada de vocabulario (OMOP opcao B, fase F13).
    loinc: Mapped[str | None] = mapped_column(String(20), nullable=True)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


class ProcedimentoAnalito(Base):
    """Painel: quais analitos um exame mede. Hemograma e um painel."""

    __tablename__ = "procedimento_analitos"

    procedimento_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("procedimentos.id", ondelete="CASCADE"), primary_key=True
    )
    analito_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("analitos.id"), primary_key=True
    )
    ordem: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1)


class ValorReferencia(Base):
    __tablename__ = "valores_referencia"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    procedimento_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("procedimentos.id"), nullable=False)
    analito: Mapped[str] = mapped_column(String(120), nullable=False)
    analito_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("analitos.id"), nullable=True
    )
    # Faixa de referencia de verdade: hemoglobina normal de homem adulto nao e
    # a de crianca. Antes nao havia recorte nenhum.
    sexo: Mapped[str | None] = mapped_column(String(20), nullable=True)
    idade_min: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    idade_max: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    minimo: Mapped[float | None] = mapped_column(Numeric(10, 4), nullable=True)
    maximo: Mapped[float | None] = mapped_column(Numeric(10, 4), nullable=True)
    valor_esperado_texto: Mapped[str | None] = mapped_column(String(120), nullable=True)
    unidade_medida: Mapped[str | None] = mapped_column(String(50), nullable=True)


class Resultado(Base):
    __tablename__ = "resultados"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    os_item_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("os_itens.id"), nullable=False, index=True)
    equipamento_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("equipamentos.id"), nullable=True)
    analito: Mapped[str] = mapped_column(String(120), nullable=False)
    analito_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("analitos.id"), nullable=True
    )
    valor: Mapped[str] = mapped_column(String(255), nullable=False)
    # Valor comparavel com a faixa. O texto original fica em `valor` porque
    # exame qualitativo ("Nao Reagente") nao vira numero.
    valor_numerico: Mapped[Decimal | None] = mapped_column(Numeric(14, 4), nullable=True)
    status: Mapped[StatusResultado] = mapped_column(Enum(StatusResultado, name="status_resultado"), nullable=False, default=StatusResultado.AGUARDANDO_REVISAO)
    importado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())


class Laudo(Base):
    __tablename__ = "laudos"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    os_item_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("os_itens.id"), nullable=False, unique=True)
    responsavel_tecnico_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("medicos.id"), nullable=True)
    status: Mapped[StatusLaudo] = mapped_column(Enum(StatusLaudo, name="status_laudo"), nullable=False, default=StatusLaudo.RASCUNHO)
    liberado_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    assinatura_digital: Mapped[str | None] = mapped_column(Text, nullable=True)


class ResultadoAuditoria(Base):
    __tablename__ = "resultados_auditoria"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resultado_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("resultados.id"), nullable=False, index=True)
    usuario_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    valor_anterior: Mapped[str] = mapped_column(String(255), nullable=False)
    valor_novo: Mapped[str] = mapped_column(String(255), nullable=False)
    ocorrido_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    resultado = relationship("Resultado")
