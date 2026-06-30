from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class StatusAmostra(StrEnum):
    AGUARDANDO_COLETA = "AGUARDANDO_COLETA"
    COLETADA = "COLETADA"
    EM_TRANSITO = "EM_TRANSITO"
    RECEBIDA = "RECEBIDA"
    REJEITADA = "REJEITADA"


class TipoMaterial(StrEnum):
    SANGUE = "SANGUE"
    URINA = "URINA"
    FEZES = "FEZES"
    SWAB = "SWAB"
    OUTRO = "OUTRO"


class ColetaCreate(BaseModel):
    ordem_servico_id: UUID
    tipo_material: TipoMaterial
    coletor_usuario_id: UUID


class AmostraRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    ordem_servico_id: UUID
    codigo_barras: str
    tipo_material: TipoMaterial
    status: StatusAmostra


class ColetaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    amostra_id: UUID
    coletor_id: UUID
    coletada_em: datetime
