import uuid

from sqlalchemy import Boolean, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.db import Base


class Medico(Base):
    __tablename__ = "medicos"
    __table_args__ = (UniqueConstraint("crm", "uf_crm", name="uq_medico_crm_uf"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    crm: Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    uf_crm: Mapped[str] = mapped_column(String(2), nullable=False)
    responsavel_tecnico: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
