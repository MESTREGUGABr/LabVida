import re
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator


UFS_VALIDAS = frozenset(
    {
        "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS",
        "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC",
        "SP", "SE", "TO",
    }
)


class MedicoCreate(BaseModel):
    nome: str
    crm: str
    uf_crm: str
    responsavel_tecnico: bool = False

    @field_validator("nome")
    @classmethod
    def _nome(cls, nome: str) -> str:
        nome_normalizado = " ".join(nome.strip().split())
        if not (2 <= len(nome_normalizado) <= 120):
            raise ValueError("Nome do Médico inválido")
        return nome_normalizado

    @field_validator("crm")
    @classmethod
    def _crm(cls, crm: str) -> str:
        crm_normalizado = re.sub(r"\D", "", crm)
        if not (4 <= len(crm_normalizado) <= 10):
            raise ValueError("CRM inválido")
        return crm_normalizado

    @field_validator("uf_crm")
    @classmethod
    def _uf(cls, uf_crm: str) -> str:
        uf = uf_crm.strip().upper()
        if uf not in UFS_VALIDAS:
            raise ValueError("UF do CRM inválida")
        return uf


class MedicoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    nome: str
    crm: str
    uf_crm: str
    responsavel_tecnico: bool
    ativo: bool
