from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TipoMovimentoEstoque(StrEnum):
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"


class InsumoCreate(BaseModel):
    nome: str
    finalidade: str


class InsumoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    nome: str
    finalidade: str
    quantidade_estoque: float
    criado_em: datetime


class EstoqueMovimentoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    insumo_material_id: UUID
    tipo: str
    quantidade: float
    ocorrido_em: datetime
    observacao: str | None = None
