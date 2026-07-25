"""Permitir lote de faturamento sem convênio (OS Particular).

Revision ID: 0008_lote_sem_convenio
Revises: 0007_fix_titulos_pagar_nullable
Create Date: 2026-07-25
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '0008_lote_sem_convenio'
down_revision: Union[str, None] = '0007_fix_titulos_pagar_nullable'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('lotes_faturamento', 'convenio_id', existing_type=sa.UUID(as_uuid=True), nullable=True)


def downgrade() -> None:
    op.alter_column('lotes_faturamento', 'convenio_id', existing_type=sa.UUID(as_uuid=True), nullable=False)
