"""Preco particular, vigencia com fim e condicoes comerciais do convenio

Fase F3. Primeira migration da trilha de faturamento.

O QUE MUDA E POR QUE

1. `procedimento_valores.convenio_id` passa a aceitar NULL = **tabela
   particular**. Hoje e impossivel ter preco de balcao: o valor do particular e
   digitado a mao na abertura da OS, sem governanca e sem historico.

2. `vigencia_fim` + `EXCLUDE` de nao-sobreposicao. Sem fim de vigencia, inserir
   um preco retroativo muda silenciosamente o resultado de consultas
   historicas, e nao ha como encerrar nem corrigir um preco. O `EXCLUDE` e a
   prova, no banco, de que existe no maximo UM preco vigente por data.

3. `NULLS NOT DISTINCT` no unique (PG15+): sem isso o unique nao segura preco
   particular duplicado, porque em SQL `NULL <> NULL`.

4. `convenios.prazo_pagamento_dias` e `dia_vencimento`: o vencimento do titulo
   e `hoje + 30` hardcoded em `fechar_lote`.

5. `os_itens.valor_tabela`, `origem_valor` e `motivo_excecao`: hoje o operador
   digita um valor na abertura da OS e ele SOBRESCREVE a tabela sem nenhuma
   checagem, sem registrar o que a tabela dizia nem por que foi mudado.

Revision ID: 0015_precos_comerciais  (o id cabe em varchar(32) do alembic_version)
Revises: 0014_bi_reconstrucao
Create Date: 2026-08-02

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0015_precos_comerciais"
down_revision: Union[str, Sequence[str], None] = "0014_bi_reconstrucao"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_UUID_PARTICULAR = "00000000-0000-0000-0000-000000000000"


def upgrade() -> None:
    # ------------------------------------------------ procedimento_valores
    op.alter_column("procedimento_valores", "convenio_id", nullable=True)
    op.add_column("procedimento_valores", sa.Column("vigencia_fim", sa.Date(), nullable=True))

    op.create_check_constraint(
        "ck_pv_vigencia",
        "procedimento_valores",
        "vigencia_fim IS NULL OR vigencia_fim >= vigencia_inicio",
    )
    op.create_check_constraint("ck_pv_valor", "procedimento_valores", "valor >= 0")

    # BACKFILL: encadeia o fim de vigencia das linhas ja existentes. Cada preco
    # termina no dia anterior ao inicio do proximo do mesmo par
    # (procedimento, convenio) — senao o EXCLUDE abaixo rejeita tudo o que hoje
    # esta empilhado com vigencias abertas.
    op.execute(
        """
        WITH proximas AS (
            SELECT id,
                   LEAD(vigencia_inicio) OVER (
                       PARTITION BY procedimento_id, convenio_id
                       ORDER BY vigencia_inicio
                   ) AS proxima
            FROM procedimento_valores
        )
        UPDATE procedimento_valores pv
        SET vigencia_fim = proximas.proxima - INTERVAL '1 day'
        FROM proximas
        WHERE proximas.id = pv.id AND proximas.proxima IS NOT NULL
        """
    )

    op.drop_constraint("uq_procedimento_valor_vigencia", "procedimento_valores", type_="unique")
    op.execute(
        """
        CREATE UNIQUE INDEX uq_pv_vigencia
        ON procedimento_valores (procedimento_id, convenio_id, vigencia_inicio)
        NULLS NOT DISTINCT
        """
    )

    # `EXCLUDE ... USING gist` sobre daterange: a garantia de que nao existem
    # duas faixas de vigencia sobrepostas para o mesmo procedimento e convenio.
    # O COALESCE existe porque NULL (particular) nao compara com `=`.
    op.execute("CREATE EXTENSION IF NOT EXISTS btree_gist")
    op.execute(
        f"""
        ALTER TABLE procedimento_valores
        ADD CONSTRAINT ex_pv_sem_sobreposicao
        EXCLUDE USING gist (
            procedimento_id WITH =,
            COALESCE(convenio_id, '{_UUID_PARTICULAR}'::uuid) WITH =,
            daterange(vigencia_inicio, COALESCE(vigencia_fim, 'infinity'::date), '[]') WITH &&
        )
        """
    )

    # ------------------------------------------------------------ convenios
    op.add_column(
        "convenios",
        sa.Column("prazo_pagamento_dias", sa.Integer(), nullable=False, server_default="30"),
    )
    op.add_column("convenios", sa.Column("dia_vencimento", sa.SmallInteger(), nullable=True))
    op.create_check_constraint(
        "ck_convenio_prazo", "convenios", "prazo_pagamento_dias BETWEEN 0 AND 365"
    )
    op.create_check_constraint(
        "ck_convenio_dia_vencimento",
        "convenios",
        "dia_vencimento IS NULL OR dia_vencimento BETWEEN 1 AND 28",
    )

    # ------------------------------------------------------------- os_itens
    op.add_column("os_itens", sa.Column("valor_tabela", sa.Numeric(12, 2), nullable=True))
    op.add_column(
        "os_itens",
        sa.Column("origem_valor", sa.String(16), nullable=False, server_default="TABELA"),
    )
    op.add_column("os_itens", sa.Column("motivo_excecao", sa.String(255), nullable=True))

    # BACKFILL: o valor de tabela vigente na data de abertura da OS. Onde nao
    # havia preco cadastrado, `valor_tabela` fica NULL e a origem vira
    # SEM_TABELA — o que e a verdade sobre o historico, nao um chute.
    op.execute(
        """
        UPDATE os_itens oi
        SET valor_tabela = pv.valor
        FROM ordens_servico os, procedimento_valores pv
        WHERE os.id = oi.ordem_servico_id
          AND pv.procedimento_id = oi.procedimento_id
          AND pv.convenio_id IS NOT DISTINCT FROM os.convenio_id
          AND pv.vigencia_inicio <= os.aberta_em::date
          AND (pv.vigencia_fim IS NULL OR pv.vigencia_fim >= os.aberta_em::date)
        """
    )
    op.execute("UPDATE os_itens SET origem_valor = 'SEM_TABELA' WHERE valor_tabela IS NULL")
    op.execute(
        """
        UPDATE os_itens SET origem_valor = 'NEGOCIADO'
        WHERE valor_tabela IS NOT NULL AND valor_negociado <> valor_tabela
        """
    )

    # CHECK depois do backfill: se um dado historico violar, a migration falha
    # ruidosamente em vez de criar a constraint sobre dado inconsistente.
    op.create_check_constraint(
        "ck_os_item_origem_valor",
        "os_itens",
        "origem_valor IN ('TABELA', 'NEGOCIADO', 'SEM_TABELA')",
    )


def downgrade() -> None:
    op.drop_constraint("ck_os_item_origem_valor", "os_itens", type_="check")
    op.drop_column("os_itens", "motivo_excecao")
    op.drop_column("os_itens", "origem_valor")
    op.drop_column("os_itens", "valor_tabela")

    op.drop_constraint("ck_convenio_dia_vencimento", "convenios", type_="check")
    op.drop_constraint("ck_convenio_prazo", "convenios", type_="check")
    op.drop_column("convenios", "dia_vencimento")
    op.drop_column("convenios", "prazo_pagamento_dias")

    op.execute("ALTER TABLE procedimento_valores DROP CONSTRAINT ex_pv_sem_sobreposicao")
    op.execute("DROP INDEX IF EXISTS uq_pv_vigencia")

    # Reversao LOSSY: preco particular (convenio_id NULL) nao cabe no schema
    # anterior, que exigia convenio. Removido antes de restaurar o NOT NULL.
    op.execute("DELETE FROM procedimento_valores WHERE convenio_id IS NULL")

    op.drop_constraint("ck_pv_valor", "procedimento_valores", type_="check")
    op.drop_constraint("ck_pv_vigencia", "procedimento_valores", type_="check")
    op.drop_column("procedimento_valores", "vigencia_fim")
    op.alter_column("procedimento_valores", "convenio_id", nullable=False)
    op.create_unique_constraint(
        "uq_procedimento_valor_vigencia",
        "procedimento_valores",
        ["procedimento_id", "convenio_id", "vigencia_inicio"],
    )
