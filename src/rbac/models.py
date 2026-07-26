import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.db import Base


class Perfil(Base):
    __tablename__ = "perfis"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(60), nullable=False, unique=True)
    descricao: Mapped[str | None] = mapped_column(Text, nullable=True)


class Permissao(Base):
    __tablename__ = "permissoes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
    descricao: Mapped[str | None] = mapped_column(Text, nullable=True)


class PerfilPermissao(Base):
    __tablename__ = "perfil_permissao"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    perfil_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("perfis.id"), nullable=False
    )
    permissao_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("permissoes.id"), nullable=False
    )
