from datetime import date
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from src.cadastro.validators import (
    normalizar_cpf_paciente,
    normalizar_nome_paciente,
    normalizar_telefone_paciente,
)


class SexoPaciente(StrEnum):
    MASCULINO = "MASCULINO"
    FEMININO = "FEMININO"
    NAO_INFORMADO = "NAO_INFORMADO"


class PacienteCreate(BaseModel):
    cpf: str
    nome: str
    data_nascimento: date
    telefone: str
    sexo: SexoPaciente = SexoPaciente.NAO_INFORMADO

    @field_validator("cpf")
    @classmethod
    def _normalizar_cpf(cls, cpf: str) -> str:
        return normalizar_cpf_paciente(cpf)

    @field_validator("nome")
    @classmethod
    def _normalizar_nome(cls, nome: str) -> str:
        return normalizar_nome_paciente(nome)

    @field_validator("telefone")
    @classmethod
    def _normalizar_telefone(cls, telefone: str) -> str:
        return normalizar_telefone_paciente(telefone)

    @field_validator("data_nascimento")
    @classmethod
    def _validar_data_nascimento(cls, data_nascimento: date) -> date:
        if data_nascimento >= date.today():
            raise ValueError("Data de nascimento deve ser anterior à data atual")
        return data_nascimento


class PacienteUpdate(BaseModel):
    cpf: str | None = None
    nome: str | None = None
    data_nascimento: date | None = None
    telefone: str | None = None
    sexo: SexoPaciente | None = None

    @field_validator("cpf")
    @classmethod
    def _normalizar_cpf(cls, cpf: str | None) -> str | None:
        return normalizar_cpf_paciente(cpf) if cpf is not None else None

    @field_validator("nome")
    @classmethod
    def _normalizar_nome(cls, nome: str | None) -> str | None:
        return normalizar_nome_paciente(nome) if nome is not None else None

    @field_validator("telefone")
    @classmethod
    def _normalizar_telefone(cls, telefone: str | None) -> str | None:
        return normalizar_telefone_paciente(telefone) if telefone is not None else None

    @field_validator("data_nascimento")
    @classmethod
    def _validar_data_nascimento(cls, data_nascimento: date | None) -> date | None:
        if data_nascimento is not None and data_nascimento >= date.today():
            raise ValueError("Data de nascimento deve ser anterior à data atual")
        return data_nascimento

    @model_validator(mode="after")
    def _validar_nao_vazio(self) -> "PacienteUpdate":
        if all(valor is None for valor in self.model_dump().values()):
            raise ValueError("Informe ao menos um campo para atualizar")
        return self


class PacienteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    cpf: str
    nome: str
    data_nascimento: date
    telefone: str
    sexo: SexoPaciente = Field(default=SexoPaciente.NAO_INFORMADO)
