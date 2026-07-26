"""Criar tabelas de RBAC e auditoria log — Stack D.

Revision ID: 0009_rbac_auditoria
Revises: 0008_lote_sem_convenio
Create Date: 2026-07-25

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "0009_rbac_auditoria"
down_revision: Union[str, None] = "0008_lote_sem_convenio"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "perfis",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("nome", sa.String(60), nullable=False, unique=True),
        sa.Column("descricao", sa.Text(), nullable=True),
    )

    op.create_table(
        "permissoes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("codigo", sa.String(80), nullable=False, unique=True),
        sa.Column("descricao", sa.Text(), nullable=True),
    )

    op.create_table(
        "perfil_permissao",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("perfil_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("perfis.id"), nullable=False),
        sa.Column("permissao_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("permissoes.id"), nullable=False),
    )

    op.create_table(
        "auditoria_log",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("usuario_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("usuarios.id"), nullable=False, index=True),
        sa.Column("entidade", sa.String(50), nullable=False),
        sa.Column("entidade_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("acao", sa.String(30), nullable=False),
        sa.Column("dados", postgresql.JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("ocorrido_em", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_index("idx_auditoria_entidade", "auditoria_log", ["entidade", "entidade_id"])
    op.create_index("idx_perfil_permissao_perfil", "perfil_permissao", ["perfil_id"])
    op.create_index("idx_perfil_permissao_permissao", "perfil_permissao", ["permissao_id"])

    op.add_column("usuarios", sa.Column("perfil_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("perfis.id"), nullable=True))


def downgrade() -> None:
    op.drop_column("usuarios", "perfil_id")
    op.execute("DROP INDEX IF EXISTS idx_auditoria_entidade")
    op.execute("DROP INDEX IF EXISTS idx_perfil_permissao_perfil")
    op.execute("DROP INDEX IF EXISTS idx_perfil_permissao_permissao")
    op.drop_table("auditoria_log")
    op.drop_table("perfil_permissao")
    op.drop_table("permissoes")
    op.drop_table("perfis")
