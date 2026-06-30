from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator


class StatusConvenio(StrEnum):
    ATIVO = "ATIVO"
    INATIVO = "INATIVO"


class ConvenioCreate(BaseModel):
    nome: str
    registro_ans: str | None = None

    @field_validator("nome")
    @classmethod
    def _nome(cls, nome: str) -> str:
        nome_normalizado = " ".join(nome.strip().split())
        if not (2 <= len(nome_normalizado) <= 120):
            raise ValueError("Nome do Convênio inválido")
        return nome_normalizado

    @field_validator("registro_ans")
    @classmethod
    def _registro_ans(cls, registro_ans: str | None) -> str | None:
        if registro_ans is None:
            return None
        registro = registro_ans.strip()
        return registro or None


class ConvenioRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    nome: str
    registro_ans: str | None
    status: StatusConvenio
