"""Competencia como eixo de apuracao

Fase F4. Responde ao apontamento do professor: "colocar mes do faturamento" e
"por que lotes e nao periodos".

POR QUE UMA TABELA, E NAO SO UMA COLUNA `competencia DATE`

O professor pediu *fluxo de fechamento*. Fechamento exige um objeto com estado,
autor, instante e totais congelados. Coluna nao tem onde guardar isso, e sem
estado nao existe "nao pode mais lancar em marco".

POR QUE PK NATURAL `DATE`, quebrando a convencao de UUID do repositorio

O lancamento guarda `competencia DATE`, que e ao mesmo tempo a FK e a dimensao
de consulta: `GROUP BY competencia` e `WHERE competencia = '2026-03-01'` sem
join nenhum. Com PK UUID seria preciso `competencia_id UUID` E `competencia
DATE` denormalizada em cada lancamento — duas colunas para o mesmo fato, que
podem divergir. Aqui nao podem.

BACKFILL: serie mensal CONTINUA de min ate max de `laudos.liberado_em`, via
`generate_series`. Continua e nao "meses que tem laudo": sem isso um mes vazio
nao existiria e a primeira FK apontando para ele falharia.

Revision ID: 0017_competencias
Revises: 0016_catalogo_analitos
Create Date: 2026-08-03

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


revision: str = "0017_competencias"
down_revision: Union[str, Sequence[str], None] = "0016_catalogo_analitos"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# ADR 0007. Repetido literalmente em todo SQL que derive competencia.
_TZ = "America/Recife"


def upgrade() -> None:
    op.create_table(
        "competencias",
        sa.Column("competencia", sa.Date(), nullable=False),
        sa.Column("status", sa.String(10), nullable=False, server_default="ABERTA"),
        # Apuracao congelada no fechamento. O recebimento continua vivo depois,
        # entao ele NAO congela aqui.
        sa.Column("valor_faturado", sa.Numeric(14, 2), nullable=True),
        sa.Column("valor_glosado", sa.Numeric(14, 2), nullable=True),
        sa.Column("valor_liberado", sa.Numeric(14, 2), nullable=True),
        sa.Column("qtd_laudos", sa.Integer(), nullable=True),
        sa.Column("qtd_guias", sa.Integer(), nullable=True),
        sa.Column("qtd_lotes", sa.Integer(), nullable=True),
        sa.Column("criada_em", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("fechada_em", sa.DateTime(timezone=True), nullable=True),
        sa.Column("fechada_por_usuario_id", UUID(as_uuid=True), nullable=True),
        sa.Column("reaberta_em", sa.DateTime(timezone=True), nullable=True),
        sa.Column("justificativa", sa.String(255), nullable=True),
        sa.ForeignKeyConstraint(["fechada_por_usuario_id"], ["usuarios.id"]),
        sa.PrimaryKeyConstraint("competencia"),
        # PK e sempre o primeiro dia do mes: e o que garante que a chave natural
        # identifica o MES, e nao uma data qualquer dentro dele.
        sa.CheckConstraint("EXTRACT(DAY FROM competencia) = 1", name="ck_competencia_dia_um"),
        sa.CheckConstraint("status IN ('ABERTA','FECHADA')", name="ck_competencia_status"),
        sa.CheckConstraint(
            "status = 'ABERTA' OR fechada_em IS NOT NULL", name="ck_competencia_fechamento"
        ),
    )
    op.create_index("ix_competencias_status", "competencias", ["status"])

    # Serie mensal continua cobrindo todo o historico de laudos + o mes corrente.
    op.execute(
        f"""
        INSERT INTO competencias (competencia, status, criada_em, fechada_em)
        -- `fechada_em` ja no INSERT: o CHECK `status='ABERTA' OR fechada_em IS
        -- NOT NULL` e avaliado por linha inserida, entao preencher depois com
        -- UPDATE seria tarde demais.
        SELECT gs::date, 'FECHADA', now(), (gs + interval '1 month')
        FROM generate_series(
            COALESCE(
                (SELECT date_trunc('month', MIN(liberado_em) AT TIME ZONE '{_TZ}')
                 FROM laudos WHERE liberado_em IS NOT NULL),
                date_trunc('month', CURRENT_DATE)
            ),
            date_trunc('month', CURRENT_DATE),
            interval '1 month'
        ) gs
        ON CONFLICT DO NOTHING
        """
    )

    # O mes corrente nasce ABERTO.
    op.execute(
        """
        UPDATE competencias
        SET status = 'ABERTA', fechada_em = NULL
        WHERE competencia = date_trunc('month', CURRENT_DATE)::date
        """
    )


def downgrade() -> None:
    op.drop_index("ix_competencias_status", table_name="competencias")
    op.drop_table("competencias")
