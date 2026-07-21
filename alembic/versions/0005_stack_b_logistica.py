"""stack B — logistica de amostras e cadeia de custodia

Revision ID: 0005_stack_b_logistica
Revises: 0004_stack_a_atendimento
Create Date: 2026-07-21
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision: str = "0005_stack_b_logistica"
down_revision: str | None = "0004_stack_a_atendimento"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


_STATUS_MALOTE = "('ABERTO','EM_TRANSITO','RECEBIDO')"
_STATUS_MOVIMENTACAO = "('COLETADA','EM_TRANSITO','RECEBIDA','REJEITADA')"


def upgrade() -> None:
    op.create_table(
        "malotes",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("codigo_malote", sa.String(length=20), nullable=False),
        sa.Column("unidade_origem_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("unidade_destino_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("enviado_por_usuario_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("criado_em", sa.DateTime(timezone=True), nullable=False),
        sa.Column("despachado_em", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(f"status IN {_STATUS_MALOTE}", name="ck_malote_status"),
        sa.ForeignKeyConstraint(["unidade_origem_id"], ["unidades.id"]),
        sa.ForeignKeyConstraint(["unidade_destino_id"], ["unidades.id"]),
        sa.ForeignKeyConstraint(["enviado_por_usuario_id"], ["usuarios.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_malotes_codigo_malote"), "malotes", ["codigo_malote"], unique=True)
    op.create_index(op.f("ix_malotes_unidade_origem_id"), "malotes", ["unidade_origem_id"], unique=False)
    op.create_index(op.f("ix_malotes_unidade_destino_id"), "malotes", ["unidade_destino_id"], unique=False)

    op.create_table(
        "malotes_amostras",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("malote_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("amostra_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(["malote_id"], ["malotes.id"]),
        sa.ForeignKeyConstraint(["amostra_id"], ["amostras.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_malotes_amostras_malote_id"), "malotes_amostras", ["malote_id"], unique=False)
    op.create_index(op.f("ix_malotes_amostras_amostra_id"), "malotes_amostras", ["amostra_id"], unique=True)

    op.create_table(
        "amostras_movimentacoes",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("amostra_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("usuario_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("unidade_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("observacao", sa.String(length=255), nullable=True),
        sa.Column("ocorrido_em", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(f"status IN {_STATUS_MOVIMENTACAO}", name="ck_movimentacao_status"),
        sa.ForeignKeyConstraint(["amostra_id"], ["amostras.id"]),
        sa.ForeignKeyConstraint(["usuario_id"], ["usuarios.id"]),
        sa.ForeignKeyConstraint(["unidade_id"], ["unidades.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_amostras_movimentacoes_amostra_id"), "amostras_movimentacoes", ["amostra_id"], unique=False)

    op.create_table(
        "protocolos_recebimento",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("malote_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("recebido_por_usuario_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("integridade_ok", sa.Boolean(), nullable=False),
        sa.Column("observacao", sa.Text(), nullable=True),
        sa.Column("recebido_em", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["malote_id"], ["malotes.id"]),
        sa.ForeignKeyConstraint(["recebido_por_usuario_id"], ["usuarios.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_protocolos_recebimento_malote_id"), "protocolos_recebimento", ["malote_id"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_protocolos_recebimento_malote_id"), table_name="protocolos_recebimento")
    op.drop_table("protocolos_recebimento")

    op.drop_index(op.f("ix_amostras_movimentacoes_amostra_id"), table_name="amostras_movimentacoes")
    op.drop_table("amostras_movimentacoes")

    op.drop_index(op.f("ix_malotes_amostras_amostra_id"), table_name="malotes_amostras")
    op.drop_index(op.f("ix_malotes_amostras_malote_id"), table_name="malotes_amostras")
    op.drop_table("malotes_amostras")

    op.drop_index(op.f("ix_malotes_unidade_destino_id"), table_name="malotes")
    op.drop_index(op.f("ix_malotes_unidade_origem_id"), table_name="malotes")
    op.drop_index(op.f("ix_malotes_codigo_malote"), table_name="malotes")
    op.drop_table("malotes")
