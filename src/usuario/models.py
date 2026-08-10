import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.db import Base
import src.rbac.models as _rbac_models  # noqa: F401


class Usuario(Base):
    """Identidade do operador, autenticada localmente por e-mail e senha (F15).

    Estendido pela Stack D com perfil_id para RBAC. Nulo = acesso plano
    (compatível com ADR 0002 na v1). `senha_hash` nulo significa conta sem
    credencial — login sempre recusado, nunca "aceita qualquer senha".
    """

    __tablename__ = "usuarios"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    perfil_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("perfis.id"), nullable=True
    )
    senha_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    senha_definida_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
