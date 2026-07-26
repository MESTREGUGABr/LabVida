"""Criptografar CPF do paciente (LGPD) — Stack D.

Adiciona cpf_hash (SHA-256, para buscas/uniqueness) e cpf_encrypted (Fernet).
Remove a coluna cpf em texto puro.

Revision ID: 0010_lgpd_cpf_encrypted
Revises: 0009_rbac_auditoria
Create Date: 2026-07-25

"""
import hashlib
import os
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "0010_lgpd_cpf_encrypted"
down_revision: Union[str, None] = "0009_rbac_auditoria"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _obter_fernet():
    from cryptography.fernet import Fernet

    chave = os.environ.get("LGPD_ENCRYPTION_KEY", "")
    if not chave:
        raise RuntimeError("LGPD_ENCRYPTION_KEY não configurada")
    return Fernet(chave.encode())


def upgrade() -> None:
    fernet = _obter_fernet()

    op.add_column("pacientes", sa.Column("cpf_hash", sa.String(64), nullable=True))
    op.add_column("pacientes", sa.Column("cpf_encrypted", sa.LargeBinary, nullable=True))

    conn = op.get_bind()
    rows = conn.execute(sa.text("SELECT id, cpf FROM pacientes")).fetchall()

    for paciente_id, cpf in rows:
        if cpf is None:
            continue
        cpf_hash = hashlib.sha256(cpf.encode()).hexdigest()
        cpf_encrypted = fernet.encrypt(cpf.encode())
        conn.execute(
            sa.text("UPDATE pacientes SET cpf_hash = :hash, cpf_encrypted = :enc WHERE id = :id"),
            {"hash": cpf_hash, "enc": cpf_encrypted, "id": paciente_id},
        )

    op.alter_column("pacientes", "cpf_hash", nullable=False)
    op.alter_column("pacientes", "cpf_encrypted", nullable=False)

    op.create_unique_constraint("uq_pacientes_cpf_hash", "pacientes", ["cpf_hash"])
    op.create_index("ix_pacientes_cpf_hash", "pacientes", ["cpf_hash"])

    op.drop_index("ix_pacientes_cpf", table_name="pacientes")
    op.drop_column("pacientes", "cpf")


def downgrade() -> None:
    fernet = _obter_fernet()

    op.add_column("pacientes", sa.Column("cpf", sa.String(11), nullable=True))

    conn = op.get_bind()
    rows = conn.execute(sa.text("SELECT id, cpf_encrypted FROM pacientes")).fetchall()

    for paciente_id, cpf_encrypted in rows:
        if cpf_encrypted is None:
            continue
        cpf = fernet.decrypt(cpf_encrypted).decode()
        conn.execute(
            sa.text("UPDATE pacientes SET cpf = :cpf WHERE id = :id"),
            {"cpf": cpf, "id": paciente_id},
        )

    op.alter_column("pacientes", "cpf", nullable=False)
    op.create_unique_constraint("uq_pacientes_cpf", "pacientes", ["cpf"])
    op.create_index("ix_pacientes_cpf", "pacientes", ["cpf"])

    op.drop_index("ix_pacientes_cpf_hash", table_name="pacientes")
    op.drop_constraint("uq_pacientes_cpf_hash", "pacientes", type_="unique")
    op.drop_column("pacientes", "cpf_encrypted")
    op.drop_column("pacientes", "cpf_hash")
