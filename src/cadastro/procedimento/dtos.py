import re
from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator


class ProcedimentoCreate(BaseModel):
    codigo_tuss: str
    nome: str
    setor: str | None = None

    @field_validator("codigo_tuss")
    @classmethod
    def _codigo_tuss(cls, codigo_tuss: str) -> str:
        codigo = re.sub(r"\D", "", codigo_tuss)
        if not (4 <= len(codigo) <= 10):
            raise ValueError("Código TUSS inválido")
        return codigo

    @field_validator("nome")
    @classmethod
    def _nome(cls, nome: str) -> str:
        nome_normalizado = " ".join(nome.strip().split())
        if not (2 <= len(nome_normalizado) <= 120):
            raise ValueError("Nome do Procedimento inválido")
        return nome_normalizado

    @field_validator("setor")
    @classmethod
    def _setor(cls, setor: str | None) -> str | None:
        if setor is None:
            return None
        setor_normalizado = " ".join(setor.strip().split())
        return setor_normalizado or None


class ProcedimentoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    codigo_tuss: str
    nome: str
    setor: str | None
    ativo: bool


class ProcedimentoValorCreate(BaseModel):
    procedimento_id: UUID
    convenio_id: UUID
    valor: Decimal
    vigencia_inicio: date

    @field_validator("valor")
    @classmethod
    def _valor(cls, valor: Decimal) -> Decimal:
        if valor < 0:
            raise ValueError("Valor não pode ser negativo")
        return valor


class ProcedimentoValorRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    procedimento_id: UUID
    convenio_id: UUID
    valor: Decimal
    vigencia_inicio: date
