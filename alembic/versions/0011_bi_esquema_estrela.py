
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "0011_bi_esquema_estrela"
down_revision: Union[str, None] = "0010_lgpd_cpf_encrypted"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "bi_dim_tempo",
        sa.Column("sk_tempo", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("data", sa.Date, nullable=False, unique=True),
        sa.Column("ano", sa.Integer, nullable=False),
        sa.Column("mes", sa.Integer, nullable=False),
        sa.Column("dia", sa.Integer, nullable=False),
        sa.Column("dia_semana", sa.String(20), nullable=False),
        sa.Column("trimestre", sa.Integer, nullable=False),
    )
    op.create_index("ix_bi_dim_tempo_data", "bi_dim_tempo", ["data"])

    op.create_table(
        "bi_dim_unidade",
        sa.Column("sk_unidade", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("id_origem", postgresql.UUID(as_uuid=True), nullable=False, unique=True),
        sa.Column("nome", sa.String(120), nullable=False),
        sa.Column("tipo", sa.String(10), nullable=False),
    )

    op.create_table(
        "bi_dim_convenio",
        sa.Column("sk_convenio", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("id_origem", postgresql.UUID(as_uuid=True), nullable=False, unique=True),
        sa.Column("nome", sa.String(120), nullable=False),
        sa.Column("registro_ans", sa.String(20), nullable=True),
    )

    op.create_table(
        "bi_dim_procedimento",
        sa.Column("sk_procedimento", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("id_origem", postgresql.UUID(as_uuid=True), nullable=False, unique=True),
        sa.Column("codigo_tuss", sa.String(20), nullable=False),
        sa.Column("nome", sa.String(120), nullable=False),
        sa.Column("setor", sa.String(60), nullable=True),
    )

    op.create_table(
        "bi_dim_paciente_anon",
        sa.Column("sk_paciente", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("id_origem", postgresql.UUID(as_uuid=True), nullable=False, unique=True),
        sa.Column("faixa_etaria", sa.String(20), nullable=False),
        sa.Column("sexo", sa.String(20), nullable=False),
    )

    # --- Tabelas-fato ---
    op.create_table(
        "bi_fato_atendimento",
        sa.Column("sk_fato", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("sk_tempo", sa.Integer, sa.ForeignKey("bi_dim_tempo.sk_tempo"), nullable=False),
        sa.Column("sk_unidade", sa.Integer, sa.ForeignKey("bi_dim_unidade.sk_unidade"), nullable=False),
        sa.Column("sk_convenio", sa.Integer, sa.ForeignKey("bi_dim_convenio.sk_convenio"), nullable=True),
        sa.Column("sk_procedimento", sa.Integer, sa.ForeignKey("bi_dim_procedimento.sk_procedimento"), nullable=False),
        sa.Column("sk_paciente", sa.Integer, sa.ForeignKey("bi_dim_paciente_anon.sk_paciente"), nullable=False),
        sa.Column("qtd_exames", sa.Integer, nullable=False, server_default=sa.text("1")),
        sa.Column("tempo_ciclo_os_horas", sa.Numeric(10, 2), nullable=True),
    )
    op.create_index("ix_bi_fato_atend_tempo", "bi_fato_atendimento", ["sk_tempo"])
    op.create_index("ix_bi_fato_atend_unidade", "bi_fato_atendimento", ["sk_unidade"])

    op.create_table(
        "bi_fato_faturamento",
        sa.Column("sk_fato", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("sk_tempo", sa.Integer, sa.ForeignKey("bi_dim_tempo.sk_tempo"), nullable=False),
        sa.Column("sk_unidade", sa.Integer, sa.ForeignKey("bi_dim_unidade.sk_unidade"), nullable=False),
        sa.Column("sk_convenio", sa.Integer, sa.ForeignKey("bi_dim_convenio.sk_convenio"), nullable=True),
        sa.Column("sk_procedimento", sa.Integer, sa.ForeignKey("bi_dim_procedimento.sk_procedimento"), nullable=False),
        sa.Column("valor_faturado", sa.Numeric(12, 2), nullable=False, server_default=sa.text("0")),
        sa.Column("valor_glosado", sa.Numeric(12, 2), nullable=False, server_default=sa.text("0")),
        sa.Column("ticket_medio", sa.Numeric(12, 2), nullable=True),
    )
    op.create_index("ix_bi_fato_fatur_tempo", "bi_fato_faturamento", ["sk_tempo"])

    op.create_table(
        "bi_fato_financeiro",
        sa.Column("sk_fato", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("sk_tempo", sa.Integer, sa.ForeignKey("bi_dim_tempo.sk_tempo"), nullable=False),
        sa.Column("sk_unidade", sa.Integer, sa.ForeignKey("bi_dim_unidade.sk_unidade"), nullable=False),
        sa.Column("sk_convenio", sa.Integer, sa.ForeignKey("bi_dim_convenio.sk_convenio"), nullable=True),
        sa.Column("valor_recebido", sa.Numeric(12, 2), nullable=False, server_default=sa.text("0")),
        sa.Column("valor_pago", sa.Numeric(12, 2), nullable=False, server_default=sa.text("0")),
        sa.Column("rentabilidade", sa.Numeric(12, 2), nullable=True),
    )
    op.create_index("ix_bi_fato_finan_tempo", "bi_fato_financeiro", ["sk_tempo"])

    op.create_table(
        "bi_fato_logistica",
        sa.Column("sk_fato", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("sk_tempo", sa.Integer, sa.ForeignKey("bi_dim_tempo.sk_tempo"), nullable=False),
        sa.Column("sk_unidade", sa.Integer, sa.ForeignKey("bi_dim_unidade.sk_unidade"), nullable=False),
        sa.Column("qtd_amostras", sa.Integer, nullable=False, server_default=sa.text("0")),
        sa.Column("tempo_transito_horas", sa.Numeric(10, 2), nullable=True),
        sa.Column("amostras_divergentes", sa.Integer, nullable=False, server_default=sa.text("0")),
    )
    op.create_index("ix_bi_fato_logis_tempo", "bi_fato_logistica", ["sk_tempo"])


def downgrade() -> None:
    op.drop_table("bi_fato_logistica")
    op.drop_table("bi_fato_financeiro")
    op.drop_table("bi_fato_faturamento")
    op.drop_table("bi_fato_atendimento")
    op.drop_table("bi_dim_paciente_anon")
    op.drop_table("bi_dim_procedimento")
    op.drop_table("bi_dim_convenio")
    op.drop_table("bi_dim_unidade")
    op.drop_table("bi_dim_tempo")
