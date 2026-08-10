"""Criar tabela procedimento_insumos (integracao estoque x atendimento)

Revision ID: 0021_procedimento_insumo
Revises: 0020_estoque_minimo
Create Date: 2026-08-10
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision: str = "0021_procedimento_insumo"
down_revision: Union[str, Sequence[str], None] = "0020_estoque_minimo"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "procedimentos_insumos",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("procedimento_id", UUID(as_uuid=True), sa.ForeignKey("procedimentos.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("insumo_material_id", UUID(as_uuid=True), sa.ForeignKey("insumos_materiais.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("quantidade_necessaria", sa.Numeric(12, 3), nullable=False, server_default="1.000"),
        sa.UniqueConstraint("procedimento_id", "insumo_material_id", name="uq_procedimento_insumo"),
    )


def downgrade() -> None:
    op.drop_table("procedimentos_insumos")
