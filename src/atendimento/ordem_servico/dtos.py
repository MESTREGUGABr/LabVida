from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class StatusOrdemServico(StrEnum):
    ABERTA = "ABERTA"
    EM_COLETA = "EM_COLETA"
    COLETADA = "COLETADA"
    EM_ANALISE = "EM_ANALISE"
    CONCLUIDA = "CONCLUIDA"
    CANCELADA = "CANCELADA"


class StatusOsItem(StrEnum):
    SOLICITADO = "SOLICITADO"
    COLETADO = "COLETADO"
    RESULTADO_LIBERADO = "RESULTADO_LIBERADO"
    FATURADO = "FATURADO"
    CANCELADO = "CANCELADO"


class OsItemInput(BaseModel):
    procedimento_id: UUID
    valor_negociado: Decimal | None = None


class OrdemServicoCreate(BaseModel):
    paciente_id: UUID
    unidade_id: UUID
    medico_id: UUID | None = None
    convenio_id: UUID | None = None
    itens: list[OsItemInput] = Field(min_length=1)


class OsItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    procedimento_id: UUID
    valor_negociado: Decimal
    status: StatusOsItem


class OrdemServicoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    codigo_os: str
    paciente_id: UUID
    medico_id: UUID | None
    convenio_id: UUID | None
    unidade_id: UUID
    status: StatusOrdemServico
    aberta_em: datetime


class OsStatusHistoricoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    status: StatusOrdemServico
    ocorrido_em: datetime
    usuario_id: UUID | None
