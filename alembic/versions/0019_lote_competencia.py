"""Competencia no lote de faturamento: agrupamento mensal por convenio

Fase F6 (parcial). Resolve o apontamento sobre poluicao visual: hoje cada
clique em "Criar Lote" cria um lote novo, mesmo que ja exista um aberto para
o mesmo convenio no mesmo mes. Esta migration adiciona a coluna que falta
para o servico (`src/faturamento/lote_faturamento/service.py::criar_lote`)
reaproveitar o lote certo em vez de espalhar varios soltos.

ESCOPO REDUZIDO EM RELACAO A docs/plano-faturamento-competencia.md

O plano original (F5-F11) preve renomear lote->remessa, criar
`itens_faturaveis` e mudar a guia para 1-por-paciente/mes. Aqui so o
essencial: `competencia DATE` no lote existente + unicidade
(convenio_id, competencia) entre lotes ABERTO. Nomes de tabela/coluna do
resto da cadeia (`guias_tiss.lote_faturamento_id` etc.) continuam intactos --
glosa, bi/etl e financeiro dependem deles.

BACKFILL: cada lote existente ganha a competencia do MES EM QUE FOI CRIADO
(`date_trunc('month', criado_em)`), aproximacao pragmatica -- nao ha lote em
producao real (projeto de faculdade), so dados de seed/demo.

Revision ID: 0019_lote_competencia
Revises: 0018_login_local
Create Date: 2026-08-10

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0019_lote_competencia"
down_revision: Union[str, Sequence[str], None] = "0018_login_local"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("lotes_faturamento", sa.Column("competencia", sa.Date(), nullable=True))

    # Garante uma linha em `competencias` para o mes de cada lote existente
    # antes de criar a FK -- mesmo padrao de backfill continuo da 0017.
    op.execute(
        """
        INSERT INTO competencias (competencia, status, criada_em, fechada_em)
        SELECT DISTINCT date_trunc('month', criado_em)::date, 'FECHADA', now(),
               date_trunc('month', criado_em) + interval '1 month'
        FROM lotes_faturamento
        ON CONFLICT (competencia) DO NOTHING
        """
    )
    op.execute(
        """
        UPDATE competencias
        SET status = 'ABERTA', fechada_em = NULL
        WHERE competencia = date_trunc('month', CURRENT_DATE)::date
        """
    )

    op.execute(
        "UPDATE lotes_faturamento SET competencia = date_trunc('month', criado_em)::date"
    )
    op.alter_column("lotes_faturamento", "competencia", nullable=False)
    op.create_foreign_key(
        "fk_lotes_faturamento_competencia",
        "lotes_faturamento", "competencias",
        ["competencia"], ["competencia"],
    )
    op.create_index("ix_lotes_faturamento_competencia", "lotes_faturamento", ["competencia"])

    # No maximo um lote ABERTO por convenio+competencia. NULLS NOT DISTINCT
    # cobre o particular (convenio_id NULL) tambem -- mesmo idioma de
    # `uq_pv_vigencia` em 0015_precos_comerciais.py.
    op.execute(
        """
        CREATE UNIQUE INDEX uq_lote_aberto_convenio_competencia
        ON lotes_faturamento (convenio_id, competencia)
        NULLS NOT DISTINCT
        WHERE status = 'ABERTO'
        """
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS uq_lote_aberto_convenio_competencia")
    op.drop_index("ix_lotes_faturamento_competencia", table_name="lotes_faturamento")
    op.drop_constraint("fk_lotes_faturamento_competencia", "lotes_faturamento", type_="foreignkey")
    op.drop_column("lotes_faturamento", "competencia")
