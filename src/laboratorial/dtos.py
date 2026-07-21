from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.laboratorial.models import ProtocoloEquipamento, StatusLaudo, StatusResultado


# --- Equipamento ---
class EquipamentoCreate(BaseModel):
    setor_id: UUID
    nome: str
    protocolo: ProtocoloEquipamento


class EquipamentoUpdate(BaseModel):
    setor_id: UUID | None = None
    nome: str | None = None
    protocolo: ProtocoloEquipamento | None = None


class EquipamentoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    setor_id: UUID
    nome: str
    protocolo: ProtocoloEquipamento


# --- ValorReferencia ---
class ValorReferenciaCreate(BaseModel):
    procedimento_id: UUID
    analito: str
    minimo: float | None = None
    maximo: float | None = None
    valor_esperado_texto: str | None = None
    unidade_medida: str | None = None


class ValorReferenciaUpdate(BaseModel):
    procedimento_id: UUID | None = None
    analito: str | None = None
    minimo: float | None = None
    maximo: float | None = None
    valor_esperado_texto: str | None = None
    unidade_medida: str | None = None


class ValorReferenciaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    procedimento_id: UUID
    analito: str
    minimo: float | None = None
    maximo: float | None = None
    valor_esperado_texto: str | None = None
    unidade_medida: str | None = None


# --- Resultado ---
class ResultadoCreate(BaseModel):
    os_item_id: UUID
    equipamento_id: UUID | None = None
    analito: str
    valor: str
    status: StatusResultado = Field(default=StatusResultado.AGUARDANDO_REVISAO)
    usuario_id: UUID  # Utilizado para auditoria ao criar


class ResultadoUpdate(BaseModel):
    equipamento_id: UUID | None = None
    valor: str | None = None
    status: StatusResultado | None = None
    usuario_id: UUID  # Obrigatório para auditoria na atualização


class ResultadoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    os_item_id: UUID
    equipamento_id: UUID | None = None
    analito: str
    valor: str
    status: StatusResultado
    importado_em: datetime


# --- ResultadoAuditoria ---
class ResultadoAuditoriaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    resultado_id: UUID
    usuario_id: UUID
    valor_anterior: str
    valor_novo: str
    ocorrido_em: datetime


# --- Laudo ---
class LaudoCreate(BaseModel):
    os_item_id: UUID
    responsavel_tecnico_id: UUID | None = None


class LaudoUpdate(BaseModel):
    status: StatusLaudo | None = None
    responsavel_tecnico_id: UUID | None = None
    assinatura_digital: str | None = None


class LaudoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    os_item_id: UUID
    responsavel_tecnico_id: UUID | None = None
    status: StatusLaudo
    liberado_em: datetime | None = None
    assinatura_digital: str | None = None
