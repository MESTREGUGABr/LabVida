"""merge heads: stack C (cancelamento de OS) e stack D (RBAC/LGPD/BI)

Une as duas cabeças que surgiram do merge da Stack D na main:
- 0009_cancelamento_item (auditoria de cancelamento de item de OS, Stack B/C)
- 0011_bi_esquema_estrela (RBAC/auditoria -> LGPD -> BI, Stack D)

Migration apenas estrutural (sem DDL): reconcilia o grafo para que
`alembic upgrade head` volte a ter cabeca unica.

Revision ID: 0012_merge_heads_c_d
Revises: 0009_cancelamento_item, 0011_bi_esquema_estrela
Create Date: 2026-07-26

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0012_merge_heads_c_d"
down_revision: Union[str, Sequence[str], None] = (
    "0009_cancelamento_item",
    "0011_bi_esquema_estrela",
)
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
