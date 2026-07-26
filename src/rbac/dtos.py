from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PerfilCreate(BaseModel):
    nome: str
    descricao: str | None = None


class PerfilRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    nome: str
    descricao: str | None = None


class PermissaoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    codigo: str
    descricao: str | None = None


class PerfilPermissaoCreate(BaseModel):
    perfil_id: UUID
    permissao_id: UUID


class VincularUsuarioPerfil(BaseModel):
    usuario_id: UUID
    perfil_id: UUID
