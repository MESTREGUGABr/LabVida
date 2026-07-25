from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class StatusPedido(StrEnum):
    RASCUNHO = "RASCUNHO"
    APROVADO = "APROVADO"
    RECEBIDO = "RECEBIDO"
    CANCELADO = "CANCELADO"


class StatusSolicitacao(StrEnum):
    ABERTA = "ABERTA"


class PedidoItemCreate(BaseModel):
    insumo_material_id: UUID
    quantidade: float
    valor_unitario: float


class PedidoItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    pedido_compra_id: UUID
    insumo_material_id: UUID
    quantidade: float
    valor_unitario: float


class SolicitacaoCreate(BaseModel):
    fornecedor_id: UUID
    itens: list[PedidoItemCreate] = Field(default_factory=list)


class PedidoCompraRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    solicitacao_compra_id: UUID
    fornecedor_id: UUID
    status: str
    valor_total: float
    criado_em: datetime
    itens: list[PedidoItemRead] = Field(default_factory=list)


class RecebimentoInsumoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    pedido_compra_id: UUID
    recebido_em: datetime
    conferido: bool
