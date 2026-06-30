from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator


class TipoUnidade(StrEnum):
    CENTRAL = "CENTRAL"
    COLETA = "COLETA"


def _normalizar_nome(nome: str) -> str:
    nome_normalizado = " ".join(nome.strip().split())
    if not (2 <= len(nome_normalizado) <= 120):
        raise ValueError("Nome inválido")
    return nome_normalizado


class UnidadeCreate(BaseModel):
    nome: str
    tipo: TipoUnidade
    endereco: str | None = None

    @field_validator("nome")
    @classmethod
    def _nome(cls, nome: str) -> str:
        return _normalizar_nome(nome)


class UnidadeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    nome: str
    tipo: TipoUnidade
    endereco: str | None
    ativo: bool


class SetorCreate(BaseModel):
    unidade_id: UUID
    nome: str

    @field_validator("nome")
    @classmethod
    def _nome(cls, nome: str) -> str:
        return _normalizar_nome(nome)


class SetorRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    unidade_id: UUID
    nome: str
    ativo: bool
