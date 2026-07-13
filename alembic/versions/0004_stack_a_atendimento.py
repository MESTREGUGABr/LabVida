"""stack A — usuario minimo, cadastros e atendimento/coleta

Revision ID: 0004_stack_a_atendimento
Revises: 0004_criar_tabela_convenios
Create Date: 2026-06-30
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision: str = "0004_stack_a_atendimento"
down_revision: str | None = "0004_criar_tabela_convenios"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


_STATUS_OS = "('ABERTA','EM_COLETA','COLETADA','EM_ANALISE','CONCLUIDA','CANCELADA')"
_STATUS_OS_ITEM = "('SOLICITADO','COLETADO','RESULTADO_LIBERADO','FATURADO','CANCELADO')"
_STATUS_AMOSTRA = "('AGUARDANDO_COLETA','COLETADA','EM_TRANSITO','RECEBIDA','REJEITADA')"


def upgrade() -> None:
    op.create_table(
        "usuarios",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("nome", sa.String(length=120), nullable=False),
        sa.Column("ativo", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_usuarios_email"), "usuarios", ["email"], unique=True)

    op.create_table(
        "unidades",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("nome", sa.String(length=120), nullable=False),
        sa.Column("tipo", sa.String(length=7), nullable=False),
        sa.Column("endereco", sa.String(length=255), nullable=True),
        sa.Column("ativo", sa.Boolean(), nullable=False),
        sa.CheckConstraint("tipo IN ('CENTRAL','COLETA')", name="ck_unidade_tipo"),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "setores",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("unidade_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("nome", sa.String(length=120), nullable=False),
        sa.Column("ativo", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["unidade_id"], ["unidades.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_setores_unidade_id"), "setores", ["unidade_id"], unique=False)

    op.create_table(
        "procedimentos",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("codigo_tuss", sa.String(length=10), nullable=False),
        sa.Column("nome", sa.String(length=120), nullable=False),
        sa.Column("setor", sa.String(length=60), nullable=True),
        sa.Column("ativo", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_procedimentos_codigo_tuss"), "procedimentos", ["codigo_tuss"], unique=True
    )

    op.create_table(
        "procedimento_valores",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("procedimento_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("convenio_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("valor", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("vigencia_inicio", sa.Date(), nullable=False),
        sa.ForeignKeyConstraint(["procedimento_id"], ["procedimentos.id"]),
        sa.ForeignKeyConstraint(["convenio_id"], ["convenios.id"]),
        sa.UniqueConstraint(
            "procedimento_id", "convenio_id", "vigencia_inicio", name="uq_procedimento_valor_vigencia"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_procedimento_valores_procedimento_id"),
        "procedimento_valores",
        ["procedimento_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_procedimento_valores_convenio_id"),
        "procedimento_valores",
        ["convenio_id"],
        unique=False,
    )

    op.create_table(
        "medicos",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("nome", sa.String(length=120), nullable=False),
        sa.Column("crm", sa.String(length=10), nullable=False),
        sa.Column("uf_crm", sa.String(length=2), nullable=False),
        sa.Column("responsavel_tecnico", sa.Boolean(), nullable=False),
        sa.Column("ativo", sa.Boolean(), nullable=False),
        sa.UniqueConstraint("crm", "uf_crm", name="uq_medico_crm_uf"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_medicos_crm"), "medicos", ["crm"], unique=False)

    op.create_table(
        "ordens_servico",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("codigo_os", sa.String(length=20), nullable=False),
        sa.Column("paciente_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("medico_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("convenio_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("unidade_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("aberta_em", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(f"status IN {_STATUS_OS}", name="ck_os_status"),
        sa.ForeignKeyConstraint(["paciente_id"], ["pacientes.id"]),
        sa.ForeignKeyConstraint(["medico_id"], ["medicos.id"]),
        sa.ForeignKeyConstraint(["convenio_id"], ["convenios.id"]),
        sa.ForeignKeyConstraint(["unidade_id"], ["unidades.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_ordens_servico_codigo_os"), "ordens_servico", ["codigo_os"], unique=True)
    op.create_index(
        op.f("ix_ordens_servico_paciente_id"), "ordens_servico", ["paciente_id"], unique=False
    )
    op.create_index(
        op.f("ix_ordens_servico_unidade_id"), "ordens_servico", ["unidade_id"], unique=False
    )

    op.create_table(
        "os_itens",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("ordem_servico_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("procedimento_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("valor_negociado", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.CheckConstraint(f"status IN {_STATUS_OS_ITEM}", name="ck_os_item_status"),
        sa.ForeignKeyConstraint(["ordem_servico_id"], ["ordens_servico.id"]),
        sa.ForeignKeyConstraint(["procedimento_id"], ["procedimentos.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_os_itens_ordem_servico_id"), "os_itens", ["ordem_servico_id"], unique=False
    )

    op.create_table(
        "os_status_historico",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("ordem_servico_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("ocorrido_em", sa.DateTime(timezone=True), nullable=False),
        sa.Column("usuario_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.CheckConstraint(f"status IN {_STATUS_OS}", name="ck_os_historico_status"),
        sa.ForeignKeyConstraint(["ordem_servico_id"], ["ordens_servico.id"]),
        sa.ForeignKeyConstraint(["usuario_id"], ["usuarios.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_os_status_historico_ordem_servico_id"),
        "os_status_historico",
        ["ordem_servico_id"],
        unique=False,
    )

    op.create_table(
        "autorizacoes_convenio",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("ordem_servico_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("numero_guia", sa.String(length=40), nullable=False),
        sa.Column("status", sa.String(length=10), nullable=False),
        sa.Column("validade", sa.Date(), nullable=True),
        sa.CheckConstraint(
            "status IN ('PENDENTE','VALIDA','NEGADA')", name="ck_autorizacao_status"
        ),
        sa.ForeignKeyConstraint(["ordem_servico_id"], ["ordens_servico.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_autorizacoes_convenio_ordem_servico_id"),
        "autorizacoes_convenio",
        ["ordem_servico_id"],
        unique=False,
    )

    op.create_table(
        "amostras",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("ordem_servico_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("codigo_barras", sa.String(length=20), nullable=False),
        sa.Column("tipo_material", sa.String(length=40), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.CheckConstraint(f"status IN {_STATUS_AMOSTRA}", name="ck_amostra_status"),
        sa.ForeignKeyConstraint(["ordem_servico_id"], ["ordens_servico.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_amostras_codigo_barras"), "amostras", ["codigo_barras"], unique=True)
    op.create_index(
        op.f("ix_amostras_ordem_servico_id"), "amostras", ["ordem_servico_id"], unique=False
    )

    op.create_table(
        "coletas",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("amostra_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("coletor_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("coletada_em", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["amostra_id"], ["amostras.id"]),
        sa.ForeignKeyConstraint(["coletor_id"], ["usuarios.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_coletas_amostra_id"), "coletas", ["amostra_id"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_coletas_amostra_id"), table_name="coletas")
    op.drop_table("coletas")

    op.drop_index(op.f("ix_amostras_ordem_servico_id"), table_name="amostras")
    op.drop_index(op.f("ix_amostras_codigo_barras"), table_name="amostras")
    op.drop_table("amostras")

    op.drop_index(
        op.f("ix_autorizacoes_convenio_ordem_servico_id"), table_name="autorizacoes_convenio"
    )
    op.drop_table("autorizacoes_convenio")

    op.drop_index(
        op.f("ix_os_status_historico_ordem_servico_id"), table_name="os_status_historico"
    )
    op.drop_table("os_status_historico")

    op.drop_index(op.f("ix_os_itens_ordem_servico_id"), table_name="os_itens")
    op.drop_table("os_itens")

    op.drop_index(op.f("ix_ordens_servico_unidade_id"), table_name="ordens_servico")
    op.drop_index(op.f("ix_ordens_servico_paciente_id"), table_name="ordens_servico")
    op.drop_index(op.f("ix_ordens_servico_codigo_os"), table_name="ordens_servico")
    op.drop_table("ordens_servico")

    op.drop_index(op.f("ix_medicos_crm"), table_name="medicos")
    op.drop_table("medicos")

    op.drop_index(
        op.f("ix_procedimento_valores_convenio_id"), table_name="procedimento_valores"
    )
    op.drop_index(
        op.f("ix_procedimento_valores_procedimento_id"), table_name="procedimento_valores"
    )
    op.drop_table("procedimento_valores")

    op.drop_index(op.f("ix_procedimentos_codigo_tuss"), table_name="procedimentos")
    op.drop_table("procedimentos")

    op.drop_index(op.f("ix_setores_unidade_id"), table_name="setores")
    op.drop_table("setores")

    op.drop_table("unidades")

    op.drop_index(op.f("ix_usuarios_email"), table_name="usuarios")
    op.drop_table("usuarios")
