from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator

from src.cadastro.validators import normalizar_cnpj_convenio, normalizar_nome_convenio, normalizar_telefone_convenio


class StatusConvenio(StrEnum):
    ATIVO = "ATIVO"
    INATIVO = "INATIVO"


class ConvenioCreate(BaseModel):
    nome: str
    cnpj: str | None = None
    telefone: str | None = None
    email: str | None = None
    registro_ans: str | None = None

    @field_validator("nome")
    @classmethod
    def _nome(cls, nome: str) -> str:
        return normalizar_nome_convenio(nome)

    @field_validator("cnpj")
    @classmethod
    def _cnpj(cls, cnpj: str | None) -> str | None:
        return normalizar_cnpj_convenio(cnpj) if cnpj else None

    @field_validator("telefone")
    @classmethod
    def _telefone(cls, telefone: str | None) -> str | None:
        return normalizar_telefone_convenio(telefone) if telefone else None

    @field_validator("email")
    @classmethod
    def _email(cls, email: str | None) -> str | None:
        return email.strip().lower() if email else None

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
    cnpj: str | None = None
    telefone: str | None = None
    email: str | None = None
    registro_ans: str | None
    status: StatusConvenio
    ativo: bool


class ConvenioUpdate(BaseModel):
    nome: str | None = None
    cnpj: str | None = None
    telefone: str | None = None
    email: str | None = None
    ativo: bool | None = None

    @field_validator("nome")
    @classmethod
    def _nome(cls, nome: str | None) -> str | None:
        return normalizar_nome_convenio(nome) if nome is not None else None

    @field_validator("cnpj")
    @classmethod
    def _cnpj(cls, cnpj: str | None) -> str | None:
        return normalizar_cnpj_convenio(cnpj) if cnpj else None

    @field_validator("telefone")
    @classmethod
    def _telefone(cls, telefone: str | None) -> str | None:
        return normalizar_telefone_convenio(telefone) if telefone else None

    @field_validator("email")
    @classmethod
    def _email(cls, email: str | None) -> str | None:
        return email.strip().lower() if email else None
