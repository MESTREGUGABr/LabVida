from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TipoMovimento(StrEnum):
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"


class MovimentoCaixaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    titulo_receber_id: UUID | None = None
    titulo_pagar_id: UUID | None = None
    tipo: str
    valor: float
    ocorrido_em: datetime
    descricao: str | None = None
