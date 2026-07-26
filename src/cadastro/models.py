import uuid
from datetime import date

from sqlalchemy import Boolean, Date, Enum, LargeBinary, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.cadastro.dtos import SexoPaciente
from src.db import Base


class Paciente(Base):
    __tablename__ = "pacientes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cpf_hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)
    cpf_encrypted: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    data_nascimento: Mapped[date] = mapped_column(Date, nullable=False)
    telefone: Mapped[str] = mapped_column(String(11), nullable=False)
    sexo: Mapped[SexoPaciente] = mapped_column(
        Enum(SexoPaciente, name="sexo_paciente"),
        nullable=False,
        default=SexoPaciente.NAO_INFORMADO,
    )
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    @property
    def cpf(self) -> str:
        from src.lgpd import descriptografar_cpf

        return descriptografar_cpf(self.cpf_encrypted)

    @cpf.setter
    def cpf(self, value: str) -> None:
        from src.lgpd import criptografar_cpf, gerar_hash_cpf

        self.cpf_encrypted = criptografar_cpf(value)
        self.cpf_hash = gerar_hash_cpf(value)


from src.cadastro.convenio.models import Convenio  # noqa: E402,F401
