import uuid

from sqlalchemy import Boolean, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.cadastro.convenio.dtos import StatusConvenio
from src.db import Base


class Convenio(Base):
    __tablename__ = "convenios"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    nome_normalizado: Mapped[str] = mapped_column(String(120), nullable=False, unique=True, index=True)
    cnpj: Mapped[str | None] = mapped_column(String(14), nullable=True, unique=True, index=True)
    telefone: Mapped[str | None] = mapped_column(String(11), nullable=True)
    email: Mapped[str | None] = mapped_column(String(254), nullable=True)
    registro_ans: Mapped[str | None] = mapped_column(String(20), nullable=True)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    status: Mapped[str] = mapped_column(String(7), nullable=False, default=StatusConvenio.ATIVO)
