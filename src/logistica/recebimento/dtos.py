from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.atendimento.amostra.dtos import StatusAmostra


class ProtocoloRecebimentoCreate(BaseModel):
    malote_id: UUID
    recebido_por_usuario_id: UUID
    integridade_ok: bool = True
    observacao: str | None = None


class ProtocoloRecebimentoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    malote_id: UUID
    recebido_por_usuario_id: UUID
    integridade_ok: bool
    observacao: str | None = None
    recebido_em: datetime


class AmostraMovimentacaoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    amostra_id: UUID
    status: StatusAmostra
    usuario_id: UUID
    unidade_id: UUID
    observacao: str | None = None
    ocorrido_em: datetime
