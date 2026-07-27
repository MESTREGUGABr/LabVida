from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.db import Base


class DimTempo(Base):
    __tablename__ = "bi_dim_tempo"

    sk_tempo: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    data: Mapped[date] = mapped_column(Date, nullable=False, unique=True)
    ano: Mapped[int] = mapped_column(Integer, nullable=False)
    mes: Mapped[int] = mapped_column(Integer, nullable=False)
    dia: Mapped[int] = mapped_column(Integer, nullable=False)
    dia_semana: Mapped[str] = mapped_column(String(20), nullable=False)
    trimestre: Mapped[int] = mapped_column(Integer, nullable=False)


class DimUnidade(Base):
    __tablename__ = "bi_dim_unidade"

    sk_unidade: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_origem: Mapped[str] = mapped_column(UUID(as_uuid=True), nullable=False, unique=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    tipo: Mapped[str] = mapped_column(String(10), nullable=False)


class DimConvenio(Base):
    __tablename__ = "bi_dim_convenio"

    sk_convenio: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_origem: Mapped[str] = mapped_column(UUID(as_uuid=True), nullable=False, unique=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    registro_ans: Mapped[str | None] = mapped_column(String(20), nullable=True)


class DimProcedimento(Base):
    __tablename__ = "bi_dim_procedimento"

    sk_procedimento: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_origem: Mapped[str] = mapped_column(UUID(as_uuid=True), nullable=False, unique=True)
    codigo_tuss: Mapped[str] = mapped_column(String(20), nullable=False)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    setor: Mapped[str | None] = mapped_column(String(60), nullable=True)


class DimPacienteAnon(Base):
    __tablename__ = "bi_dim_paciente_anon"

    sk_paciente: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Pseudônimo: hash SHA-256 do UUID do paciente (não o UUID cru), para o BI não
    # permitir join trivial de volta a `pacientes`. Mantém estabilidade para o upsert.
    id_origem: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    faixa_etaria: Mapped[str] = mapped_column(String(20), nullable=False)
    sexo: Mapped[str] = mapped_column(String(20), nullable=False)


class FatoAtendimento(Base):
    __tablename__ = "bi_fato_atendimento"

    sk_fato: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sk_tempo: Mapped[int] = mapped_column(Integer, ForeignKey("bi_dim_tempo.sk_tempo"), nullable=False)
    sk_unidade: Mapped[int] = mapped_column(Integer, ForeignKey("bi_dim_unidade.sk_unidade"), nullable=False)
    sk_convenio: Mapped[int | None] = mapped_column(Integer, ForeignKey("bi_dim_convenio.sk_convenio"), nullable=True)
    sk_procedimento: Mapped[int] = mapped_column(Integer, ForeignKey("bi_dim_procedimento.sk_procedimento"), nullable=False)
    sk_paciente: Mapped[int] = mapped_column(Integer, ForeignKey("bi_dim_paciente_anon.sk_paciente"), nullable=False)
    qtd_exames: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    tempo_ciclo_os_horas: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)


class FatoFaturamento(Base):
    __tablename__ = "bi_fato_faturamento"

    sk_fato: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sk_tempo: Mapped[int] = mapped_column(Integer, ForeignKey("bi_dim_tempo.sk_tempo"), nullable=False)
    sk_unidade: Mapped[int] = mapped_column(Integer, ForeignKey("bi_dim_unidade.sk_unidade"), nullable=False)
    sk_convenio: Mapped[int | None] = mapped_column(Integer, ForeignKey("bi_dim_convenio.sk_convenio"), nullable=True)
    sk_procedimento: Mapped[int] = mapped_column(Integer, ForeignKey("bi_dim_procedimento.sk_procedimento"), nullable=False)
    valor_faturado: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=Decimal("0"))
    valor_glosado: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=Decimal("0"))
    ticket_medio: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)


class FatoFinanceiro(Base):
    __tablename__ = "bi_fato_financeiro"

    sk_fato: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sk_tempo: Mapped[int] = mapped_column(Integer, ForeignKey("bi_dim_tempo.sk_tempo"), nullable=False)
    sk_unidade: Mapped[int] = mapped_column(Integer, ForeignKey("bi_dim_unidade.sk_unidade"), nullable=False)
    sk_convenio: Mapped[int | None] = mapped_column(Integer, ForeignKey("bi_dim_convenio.sk_convenio"), nullable=True)
    valor_recebido: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=Decimal("0"))
    valor_pago: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=Decimal("0"))
    rentabilidade: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)


class FatoLogistica(Base):
    __tablename__ = "bi_fato_logistica"

    sk_fato: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sk_tempo: Mapped[int] = mapped_column(Integer, ForeignKey("bi_dim_tempo.sk_tempo"), nullable=False)
    sk_unidade: Mapped[int] = mapped_column(Integer, ForeignKey("bi_dim_unidade.sk_unidade"), nullable=False)
    qtd_amostras: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    tempo_transito_horas: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    amostras_divergentes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
