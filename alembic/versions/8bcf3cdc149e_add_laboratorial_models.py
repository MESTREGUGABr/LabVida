"""add laboratorial models

Revision ID: 8bcf3cdc149e
Revises: 0005_stack_b_logistica
Create Date: 2026-07-21 14:35:58.372930

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '8bcf3cdc149e'
down_revision: Union[str, None] = '0005_stack_b_logistica'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
