from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ConciliacaoPagamentoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    titulo_receber_id: UUID
    valor_recebido: float
    divergencia: float
    conciliado_em: datetime
    observacao: str | None = None
