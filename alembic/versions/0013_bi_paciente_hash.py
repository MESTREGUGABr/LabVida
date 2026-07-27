"""BI: id_origem do paciente passa a ser hash SHA-256 (VARCHAR 64), não o UUID cru

Endurece a anonimização do BI (LGPD): a dimensão de paciente deixa de guardar o
UUID do paciente e passa a guardar um pseudônimo (hash), evitando join trivial de
volta a `pacientes`. O BI é reconstruível via ETL.

Revision ID: 0013_bi_paciente_hash
Revises: 0012_merge_heads_c_d
Create Date: 2026-07-27

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


revision: str = "0013_bi_paciente_hash"
down_revision: Union[str, Sequence[str], None] = "0012_merge_heads_c_d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "bi_dim_paciente_anon",
        "id_origem",
        type_=sa.String(length=64),
        existing_nullable=False,
        postgresql_using="id_origem::text",
    )


def downgrade() -> None:
    # Hashes não convertem para UUID; o BI é reconstruível, então zeramos a dimensão
    # (e os fatos dependentes) antes de reverter o tipo.
    op.execute("TRUNCATE bi_dim_paciente_anon CASCADE")
    op.alter_column(
        "bi_dim_paciente_anon",
        "id_origem",
        type_=UUID(as_uuid=True),
        existing_nullable=False,
        postgresql_using="id_origem::uuid",
    )
