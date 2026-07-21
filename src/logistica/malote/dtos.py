from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class StatusMalote(StrEnum):
    ABERTO = "ABERTO"
    EM_TRANSITO = "EM_TRANSITO"
    RECEBIDO = "RECEBIDO"


class MaloteCreate(BaseModel):
    unidade_origem_id: UUID
    unidade_destino_id: UUID
    enviado_por_usuario_id: UUID


class MaloteItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    malote_id: UUID
    amostra_id: UUID


class MaloteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    codigo_malote: str
    unidade_origem_id: UUID
    unidade_destino_id: UUID
    enviado_por_usuario_id: UUID
    status: StatusMalote
    criado_em: datetime
    despachado_em: datetime | None = None
    itens: list[MaloteItemRead] = Field(default_factory=list)
