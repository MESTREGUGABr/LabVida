"""criar tabela pacientes

Revision ID: 0003_criar_tabela_pacientes
Revises:
Create Date: 2026-06-26
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision: str = "0003_criar_tabela_pacientes"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    sexo_paciente = postgresql.ENUM(
        "MASCULINO",
        "FEMININO",
        "NAO_INFORMADO",
        name="sexo_paciente",
        create_type=False,
    )
    sexo_paciente.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "pacientes",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("cpf", sa.String(length=11), nullable=False),
        sa.Column("nome", sa.String(length=120), nullable=False),
        sa.Column("data_nascimento", sa.Date(), nullable=False),
        sa.Column("telefone", sa.String(length=11), nullable=False),
        sa.Column("sexo", sexo_paciente, nullable=False),
        sa.Column("ativo", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_pacientes_cpf"), "pacientes", ["cpf"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_pacientes_cpf"), table_name="pacientes")
    op.drop_table("pacientes")
    sa.Enum(name="sexo_paciente").drop(op.get_bind(), checkfirst=True)
