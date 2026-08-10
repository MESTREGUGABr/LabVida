from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UsuarioRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: str
    nome: str
    ativo: bool
    perfil_id: UUID | None = None
    tem_senha: bool = False
    """Derivado de `senha_hash is not None`. Nunca expor o hash em si."""
