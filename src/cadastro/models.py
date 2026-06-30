import uuid
from datetime import date

from sqlalchemy import Boolean, Date, Enum, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.cadastro.dtos import SexoPaciente
from src.db import Base


class Paciente(Base):
    __tablename__ = "pacientes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cpf: Mapped[str] = mapped_column(String(11), nullable=False, unique=True, index=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    data_nascimento: Mapped[date] = mapped_column(Date, nullable=False)
    telefone: Mapped[str] = mapped_column(String(11), nullable=False)
    sexo: Mapped[SexoPaciente] = mapped_column(
        Enum(SexoPaciente, name="sexo_paciente"),
        nullable=False,
        default=SexoPaciente.NAO_INFORMADO,
    )
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
