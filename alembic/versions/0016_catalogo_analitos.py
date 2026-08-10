"""Catalogo de analitos, exame enriquecido e faixa de referencia por sexo/idade

Fase F3, segunda migration.

O PROBLEMA

`resultados.analito` e `valores_referencia.analito` sao DUAS strings livres
independentes, sem FK entre si e sem tabela de analitos. Nenhum codigo casa uma
com a outra: a bancada digita "Hemoglobina", a faixa de referencia esta
cadastrada como "hemoglobina", e a tela nao sabe que sao a mesma coisa. Na
pratica a faixa de referencia existe no banco e **nao e aplicavel**.

Alem disso `resultados.valor` e `String(255)`: nao ha valor numerico, entao nao
da para comparar com a faixa nem marcar resultado alterado.

O QUE ENTRA

- `analitos`: catalogo com codigo, unidade de medida, casas decimais e **espaco
  para LOINC** — a espinha de terminologia que a opcao B do OMOP precisa (F13).
- `procedimento_analitos`: liga o exame aos analitos que ele mede. Hemograma e
  um painel; sem isso a bancada nao sabe o que digitar.
- `resultados.analito_id` e `valores_referencia.analito_id`: as duas pontas
  passam a apontar para a MESMA entidade.
- `resultados.valor_numerico`: valor comparavel, ao lado do texto original.
- `valores_referencia.sexo`, `idade_min`, `idade_max`: faixa de referencia de
  verdade. Hemoglobina normal de homem adulto nao e a de crianca.

BACKFILL: os analitos nascem dos nomes ja existentes nas duas tabelas,
normalizados (minusculo, sem espaco duplicado) — e por isso "Hemoglobina" e
"hemoglobina" convergem para a mesma linha, que era exatamente o problema.

Revision ID: 0016_catalogo_analitos
Revises: 0015_precos_comerciais
Create Date: 2026-08-03

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


revision: str = "0016_catalogo_analitos"
down_revision: Union[str, Sequence[str], None] = "0015_precos_comerciais"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Normalizacao usada no backfill e depois pelo ETL/servico: minusculo, sem
# espacos duplicados e sem espaco nas pontas.
_NORMALIZAR = "lower(regexp_replace(btrim({coluna}), '\\s+', ' ', 'g'))"


def upgrade() -> None:
    # ------------------------------------------------------------- analitos
    op.create_table(
        "analitos",
        sa.Column("id", UUID(as_uuid=True), nullable=False),
        sa.Column("codigo", sa.String(30), nullable=False),
        sa.Column("nome", sa.String(120), nullable=False),
        sa.Column("unidade_medida", sa.String(20), nullable=True),
        sa.Column("casas_decimais", sa.SmallInteger(), nullable=False, server_default="2"),
        # Espaco reservado para a camada de vocabulario (OMOP opcao B, fase F13).
        sa.Column("loinc", sa.String(20), nullable=True),
        sa.Column("ativo", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("codigo"),
    )
    op.create_index("ix_analitos_nome", "analitos", ["nome"])

    op.create_table(
        "procedimento_analitos",
        sa.Column("procedimento_id", UUID(as_uuid=True), nullable=False),
        sa.Column("analito_id", UUID(as_uuid=True), nullable=False),
        sa.Column("ordem", sa.SmallInteger(), nullable=False, server_default="1"),
        sa.ForeignKeyConstraint(["procedimento_id"], ["procedimentos.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["analito_id"], ["analitos.id"]),
        sa.PrimaryKeyConstraint("procedimento_id", "analito_id"),
    )

    # ------------------------------------------------- catalogo de exames
    op.add_column("procedimentos", sa.Column("mnemonico", sa.String(20), nullable=True))
    op.add_column("procedimentos", sa.Column("tipo_material", sa.String(40), nullable=True))
    op.add_column("procedimentos", sa.Column("metodo", sa.String(80), nullable=True))
    op.add_column("procedimentos", sa.Column("prazo_entrega_dias", sa.SmallInteger(), nullable=True))
    op.add_column("procedimentos", sa.Column("preparo_paciente", sa.Text(), nullable=True))
    op.create_check_constraint(
        "ck_procedimento_prazo",
        "procedimentos",
        "prazo_entrega_dias IS NULL OR prazo_entrega_dias BETWEEN 0 AND 365",
    )

    # ------------------------------------------------------ ponte nos dados
    op.add_column("resultados", sa.Column("analito_id", UUID(as_uuid=True), nullable=True))
    op.add_column("resultados", sa.Column("valor_numerico", sa.Numeric(14, 4), nullable=True))
    op.create_foreign_key(
        "fk_resultado_analito", "resultados", "analitos", ["analito_id"], ["id"]
    )

    op.add_column("valores_referencia", sa.Column("analito_id", UUID(as_uuid=True), nullable=True))
    op.add_column("valores_referencia", sa.Column("sexo", sa.String(20), nullable=True))
    op.add_column("valores_referencia", sa.Column("idade_min", sa.SmallInteger(), nullable=True))
    op.add_column("valores_referencia", sa.Column("idade_max", sa.SmallInteger(), nullable=True))
    op.create_foreign_key(
        "fk_valor_referencia_analito", "valores_referencia", "analitos", ["analito_id"], ["id"]
    )
    op.create_check_constraint(
        "ck_vr_idade",
        "valores_referencia",
        "idade_min IS NULL OR idade_max IS NULL OR idade_max >= idade_min",
    )
    op.create_check_constraint(
        "ck_vr_sexo",
        "valores_referencia",
        "sexo IS NULL OR sexo IN ('MASCULINO', 'FEMININO')",
    )

    # --------------------------------------------------------------- backfill
    # Um analito por nome normalizado, vindo das DUAS tabelas de uma vez — e o
    # que faz "Hemoglobina" e "hemoglobina" convergirem.
    op.execute(
        f"""
        INSERT INTO analitos (id, codigo, nome, unidade_medida, casas_decimais, ativo)
        SELECT gen_random_uuid(),
               left(upper(regexp_replace(nome_norm, '[^a-zA-Z0-9]', '', 'g')), 30),
               nome_exibicao,
               unidade,
               2,
               true
        FROM (
            SELECT nome_norm,
                   MIN(nome_exibicao) AS nome_exibicao,
                   MIN(unidade)       AS unidade
            FROM (
                SELECT {_NORMALIZAR.format(coluna='analito')} AS nome_norm,
                       analito AS nome_exibicao,
                       NULL::varchar AS unidade
                FROM resultados
                WHERE analito IS NOT NULL AND btrim(analito) <> ''
                UNION ALL
                SELECT {_NORMALIZAR.format(coluna='analito')} AS nome_norm,
                       analito AS nome_exibicao,
                       unidade_medida AS unidade
                FROM valores_referencia
                WHERE analito IS NOT NULL AND btrim(analito) <> ''
            ) origens
            GROUP BY nome_norm
        ) distintos
        ON CONFLICT (codigo) DO NOTHING
        """
    )

    for tabela in ("resultados", "valores_referencia"):
        op.execute(
            f"""
            UPDATE {tabela} t
            SET analito_id = a.id
            FROM analitos a
            WHERE a.codigo = left(
                upper(regexp_replace({_NORMALIZAR.format(coluna='t.analito')}, '[^a-zA-Z0-9]', '', 'g')),
                30
            )
            """
        )

    # O painel do exame sai de quem ja tem faixa de referencia cadastrada.
    op.execute(
        """
        INSERT INTO procedimento_analitos (procedimento_id, analito_id, ordem)
        SELECT DISTINCT vr.procedimento_id, vr.analito_id, 1
        FROM valores_referencia vr
        WHERE vr.analito_id IS NOT NULL
        ON CONFLICT DO NOTHING
        """
    )

    # Valor numerico so onde o texto e realmente um numero — exame qualitativo
    # ("Nao Reagente") continua so no texto, que e o correto.
    op.execute(
        """
        UPDATE resultados
        SET valor_numerico = replace(btrim(valor), ',', '.')::numeric
        WHERE valor ~ '^\\s*-?[0-9]+([.,][0-9]+)?\\s*$'
        """
    )


def downgrade() -> None:
    op.drop_constraint("ck_vr_sexo", "valores_referencia", type_="check")
    op.drop_constraint("ck_vr_idade", "valores_referencia", type_="check")
    op.drop_constraint("fk_valor_referencia_analito", "valores_referencia", type_="foreignkey")
    op.drop_column("valores_referencia", "idade_max")
    op.drop_column("valores_referencia", "idade_min")
    op.drop_column("valores_referencia", "sexo")
    op.drop_column("valores_referencia", "analito_id")

    op.drop_constraint("fk_resultado_analito", "resultados", type_="foreignkey")
    op.drop_column("resultados", "valor_numerico")
    op.drop_column("resultados", "analito_id")

    op.drop_constraint("ck_procedimento_prazo", "procedimentos", type_="check")
    for coluna in ("preparo_paciente", "prazo_entrega_dias", "metodo", "tipo_material", "mnemonico"):
        op.drop_column("procedimentos", coluna)

    op.drop_table("procedimento_analitos")
    op.drop_index("ix_analitos_nome", table_name="analitos")
    op.drop_table("analitos")
