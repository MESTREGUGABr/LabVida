from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UsuarioRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: str
    nome: str
    ativo: bool
