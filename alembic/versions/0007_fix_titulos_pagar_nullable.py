"""Permitir titulos_pagar sem pedido_compra (entradas manuais).

Revision ID: 0007_fix_titulos_pagar_nullable
Revises: 0006_stack_c
Create Date: 2026-07-23
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '0007_fix_titulos_pagar_nullable'
down_revision: Union[str, None] = '0006_stack_c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('titulos_pagar', 'pedido_compra_id', existing_type=sa.UUID(as_uuid=True), nullable=True)


def downgrade() -> None:
    op.alter_column('titulos_pagar', 'pedido_compra_id', existing_type=sa.UUID(as_uuid=True), nullable=False)
