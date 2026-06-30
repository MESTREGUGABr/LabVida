from datetime import date
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator


class StatusAutorizacao(StrEnum):
    PENDENTE = "PENDENTE"
    VALIDA = "VALIDA"
    NEGADA = "NEGADA"


class AutorizacaoCreate(BaseModel):
    ordem_servico_id: UUID
    numero_guia: str
    status: StatusAutorizacao = StatusAutorizacao.PENDENTE
    validade: date | None = None

    @field_validator("numero_guia")
    @classmethod
    def _numero_guia(cls, numero_guia: str) -> str:
        numero = numero_guia.strip()
        if not (1 <= len(numero) <= 40):
            raise ValueError("Número da guia inválido")
        return numero


class AutorizacaoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    ordem_servico_id: UUID
    numero_guia: str
    status: StatusAutorizacao
    validade: date | None
