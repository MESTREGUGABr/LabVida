"""Marca de consumo de insumo por item da OS (corrige consumo em dobro na coleta)

`0021_procedimento_insumo` (outro integrante da equipe) ligou consumo de
insumo a procedimento e passou a debitar estoque a cada `registrar_coleta` --
mas reprocessava TODOS os itens ativos da OS a cada chamada, sem nenhuma
marca de "ja processado". Como a tela de coleta orienta registrar uma coleta
por tipo de material (`pages/atendimento_coleta.py`), qualquer OS com mais de
um tipo de exame dispara `registrar_coleta` varias vezes, e cada chamada
consumia o MESMO insumo de novo.

`insumo_consumido_em` marca, por item, o instante em que o insumo dele foi
debitado -- nunca mais que uma vez, independente de quantas coletas a OS
tiver. Mesmo padrao de marca temporal ja usado em `Competencia.fechada_em`.

Revision ID: 0022_os_item_insumo_consumido
Revises: 0021_procedimento_insumo
Create Date: 2026-08-10

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0022_os_item_insumo_consumido"
down_revision: Union[str, Sequence[str], None] = "0021_procedimento_insumo"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "os_itens",
        sa.Column("insumo_consumido_em", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("os_itens", "insumo_consumido_em")
