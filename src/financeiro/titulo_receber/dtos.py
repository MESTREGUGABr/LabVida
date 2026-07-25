from datetime import date, datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class StatusTitulo(StrEnum):
    PENDENTE = "PENDENTE"
    PAGO = "PAGO"
    ATRASADO = "ATRASADO"
    CANCELADO = "CANCELADO"


class TituloReceberRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    lote_faturamento_id: UUID
    valor: float
    vencimento: date
    status: str
    criado_em: datetime
