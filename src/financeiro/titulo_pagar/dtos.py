from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.financeiro.titulo_receber.dtos import StatusTitulo


class TituloPagarRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    pedido_compra_id: UUID | None = None
    valor: float
    vencimento: date
    status: str
    criado_em: datetime
