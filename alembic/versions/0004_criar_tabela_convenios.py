"""criar tabela convenios

Revision ID: 0004_criar_tabela_convenios
Revises: 0003_criar_tabela_pacientes
Create Date: 2026-06-30 00:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision: str = "0004_criar_tabela_convenios"
down_revision: str | None = "0003_criar_tabela_pacientes"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "convenios",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("nome", sa.String(length=120), nullable=False),
        sa.Column("nome_normalizado", sa.String(length=120), nullable=False),
        sa.Column("cnpj", sa.String(length=14), nullable=True),
        sa.Column("telefone", sa.String(length=11), nullable=True),
        sa.Column("email", sa.String(length=254), nullable=True),
        sa.Column("ativo", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_convenios_nome_normalizado"), "convenios", ["nome_normalizado"], unique=True)
    op.create_index(op.f("ix_convenios_cnpj"), "convenios", ["cnpj"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_convenios_cnpj"), table_name="convenios")
    op.drop_index(op.f("ix_convenios_nome_normalizado"), table_name="convenios")
    op.drop_table("convenios")
