import uuid

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.db import Base
import src.rbac.models as _rbac_models  # noqa: F401


class Usuario(Base):
    """Identidade do operador, sincronizada do Auth0 no login.

    Estendido pela Stack D com perfil_id para RBAC. Nulo = acesso plano
    (compatível com ADR 0002 na v1).
    """

    __tablename__ = "usuarios"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    perfil_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("perfis.id"), nullable=True
    )
