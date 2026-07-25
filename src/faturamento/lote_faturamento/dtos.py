from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class StatusLote(StrEnum):
    ABERTO = "ABERTO"
    FECHADO = "FECHADO"


class StatusGuiaTiss(StrEnum):
    PENDENTE = "PENDENTE"
    APROVADA = "APROVADA"
    REJEITADA = "REJEITADA"
    ENVIADA = "ENVIADA"


class StatusGuiaItem(StrEnum):
    FATURADO = "FATURADO"
    GLOSADO = "GLOSADO"


class LoteFaturamentoCreate(BaseModel):
    convenio_id: UUID | None = None


class GuiaTissCreate(BaseModel):
    codigo_tiss: str = ""


class GuiaItemCreate(BaseModel):
    laudo_id: UUID
    procedimento_id: UUID
    valor_faturado: float


class GuiaTissRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    lote_faturamento_id: UUID
    codigo_tiss: str
    status_pre_auditoria: str
    xml_tiss: str | None = None
    criado_em: datetime
    itens: list["GuiaItemRead"] = Field(default_factory=list)


class GuiaItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    guia_tiss_id: UUID
    laudo_id: UUID
    procedimento_id: UUID
    valor_faturado: float
    status: str
    criado_em: datetime


class LoteFaturamentoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    codigo_lote: str
    convenio_id: UUID | None = None
    status: StatusLote
    valor_total: float
    criado_em: datetime
    fechado_em: datetime | None = None
    guias: list[GuiaTissRead] = Field(default_factory=list)
