"""store the user who cancels an OS item"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision: str = "0009_cancelamento_item"
down_revision: str | None = "0008_lote_sem_convenio"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "os_itens",
        sa.Column("cancelado_por_usuario_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_foreign_key(
        "fk_os_itens_cancelado_por_usuario_id",
        "os_itens",
        "usuarios",
        ["cancelado_por_usuario_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint("fk_os_itens_cancelado_por_usuario_id", "os_itens", type_="foreignkey")
    op.drop_column("os_itens", "cancelado_por_usuario_id")
