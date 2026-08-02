import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import Boolean, Date, ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.db import Base


class Procedimento(Base):
    __tablename__ = "procedimentos"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo_tuss: Mapped[str] = mapped_column(String(10), nullable=False, unique=True, index=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    setor: Mapped[str | None] = mapped_column(String(60), nullable=True)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


class ProcedimentoValor(Base):
    __tablename__ = "procedimento_valores"
    # A unicidade vive no indice `uq_pv_vigencia` (NULLS NOT DISTINCT, PG15+) e
    # a nao-sobreposicao no EXCLUDE `ex_pv_sem_sobreposicao` — ambos criados na
    # migration 0015, porque o SQLAlchemy nao expressa nenhum dos dois.

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    procedimento_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("procedimentos.id"), nullable=False, index=True
    )
    # NULL = tabela particular / balcao. Ate a fase F3 o particular era digitado
    # a mao na abertura da OS, sem governanca e sem historico.
    convenio_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("convenios.id"), nullable=True, index=True
    )
    valor: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    vigencia_inicio: Mapped[date] = mapped_column(Date, nullable=False)
    # NULL = vigente por prazo indeterminado. O EXCLUDE no banco garante que
    # nao existem duas faixas sobrepostas para o mesmo procedimento/convenio.
    vigencia_fim: Mapped[date | None] = mapped_column(Date, nullable=True)
