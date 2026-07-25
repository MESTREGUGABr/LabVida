from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator


class StatusFornecedor(StrEnum):
    ATIVO = "ATIVO"
    INATIVO = "INATIVO"


class FornecedorCreate(BaseModel):
    nome: str
    cnpj: str

    @field_validator("nome")
    @classmethod
    def _nome(cls, v: str) -> str:
        nome = v.strip()
        if not nome:
            raise ValueError("Nome do fornecedor não pode ser vazio")
        return nome

    @field_validator("cnpj")
    @classmethod
    def _cnpj(cls, v: str) -> str:
        cnpj = "".join(c for c in v if c.isdigit())
        if len(cnpj) != 14:
            raise ValueError("CNPJ deve ter 14 dígitos")
        return cnpj


class FornecedorRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    nome: str
    cnpj: str
    status: str
    criado_em: datetime
