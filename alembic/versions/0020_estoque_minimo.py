"""Estoque minimo por insumo: alerta de estoque baixo

O modulo de Compras roda em paralelo ao fluxo assistencial (decisao ja
documentada em `arquitetura.md` — nenhum exame debita insumo real). Depois de
confirmar isso com o usuario, a decisao foi so acrescentar um alerta visual de
estoque baixo, sem ligar consumo a procedimento nem bloquear nada — essa
versao completa fica documentada como fase futura (F16 candidata, ver
`docs/roadmap-execucao.md`), nao implementada aqui.

`estoque_minimo` nasce com `DEFAULT 0` para nao quebrar os insumos ja
existentes (equivale a "sem alerta configurado").

Revision ID: 0020_estoque_minimo
Revises: 0019_lote_competencia
Create Date: 2026-08-10

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0020_estoque_minimo"
down_revision: Union[str, Sequence[str], None] = "0019_lote_competencia"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "insumos_materiais",
        sa.Column("estoque_minimo", sa.Numeric(12, 3), nullable=False, server_default="0"),
    )


def downgrade() -> None:
    op.drop_column("insumos_materiais", "estoque_minimo")
