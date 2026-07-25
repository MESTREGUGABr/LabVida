from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator


class GlosaCreate(BaseModel):
    guia_item_id: UUID
    motivo: str
    valor_glosado: float

    @field_validator("motivo")
    @classmethod
    def motivo_nao_vazio(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Motivo da glosa não pode ser vazio")
        return v.strip()


class GlosaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    guia_item_id: UUID
    motivo: str
    valor_glosado: float
    unidade_origem_id: UUID
    criado_em: datetime


class GlosaListagemRead(BaseModel):
    id: UUID
    guia_item_id: UUID
    codigo_lote: str
    convenio_nome: str
    procedimento_nome: str
    motivo: str
    valor_glosado: float
    valor_faturado: float
    criado_em: datetime
