"""BI: reconstrucao do esquema estrela (grao, chave natural, calendario denso)

Reescreve o esquema estrela inteiro. Toca APENAS tabelas `bi_*` — nenhuma tabela
operacional e alterada, entao o risco para o OLTP e zero.

O que muda e por que:

- **Chave natural em todo fato** (`ordem_servico_id`, `os_item_id`,
  `guia_item_id`, `amostra_id`, `glosa_id`, `origem_id`). Sem ela a carga so
  sabia apagar tudo e recarregar, e reconciliar OLTP com OLAP era impossivel.
- **`bi_fato_ordem_servico`** novo: `tempo_ciclo` sai do fato de item, onde era
  repetido identico em cada linha da OS e fazia qualquer AVG ponderar a OS pelo
  numero de exames.
- **`bi_fato_glosa`** novo: taxa de glosa por motivo e por convenio.
- **`bi_dim_tempo`** ganha `ano_mes`, `nome_mes`, `semana_iso`, `semestre`,
  `dia_util` e `competencia` — e passa a ser pre-carregada densa pelo ETL.
- **`bi_dim_setor`**, **`bi_dim_faixa_etaria`** e **`bi_dim_motivo_glosa`** novas.
- **Faixa etaria sai da dimensao de paciente e vira FK no fato** (ADR 0009):
  recalcula-la na dimensao faria um paciente que faz 19 anos sumir
  retroativamente da faixa anterior em todo relatorio historico.
- **`bi_etl_execucao`** nova: quando a carga rodou, quantas linhas, quanto durou.

Estrategia: DROP + CREATE. O BI e derivado — `python -m src.bi.etl` reconstroi
tudo a partir do operacional, entao nao ha dado a preservar. Tentar ALTER TABLE
aqui seria mais arriscado e mais longo do que recriar.

Revision ID: 0014_bi_reconstrucao
Revises: 0013_bi_paciente_hash
Create Date: 2026-08-02

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, UUID


revision: str = "0014_bi_reconstrucao"
down_revision: Union[str, Sequence[str], None] = "0013_bi_paciente_hash"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


_FATOS_ANTIGOS = (
    "bi_fato_logistica",
    "bi_fato_financeiro",
    "bi_fato_faturamento",
    "bi_fato_atendimento",
)
_DIMENSOES_ANTIGAS = (
    "bi_dim_paciente_anon",
    "bi_dim_procedimento",
    "bi_dim_convenio",
    "bi_dim_unidade",
    "bi_dim_tempo",
)


def upgrade() -> None:
    for tabela in _FATOS_ANTIGOS + _DIMENSOES_ANTIGAS:
        op.execute(f"DROP TABLE IF EXISTS {tabela} CASCADE")

    # ---------------------------------------------------------------- dimensoes
    op.create_table(
        "bi_dim_tempo",
        sa.Column("sk_tempo", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("data", sa.Date(), nullable=False),
        sa.Column("ano", sa.Integer(), nullable=False),
        sa.Column("mes", sa.Integer(), nullable=False),
        sa.Column("dia", sa.Integer(), nullable=False),
        sa.Column("dia_semana", sa.String(length=20), nullable=False),
        sa.Column("dia_semana_num", sa.SmallInteger(), nullable=False),
        sa.Column("trimestre", sa.SmallInteger(), nullable=False),
        sa.Column("semestre", sa.SmallInteger(), nullable=False),
        sa.Column("semana_iso", sa.SmallInteger(), nullable=False),
        sa.Column("nome_mes", sa.String(length=20), nullable=False),
        sa.Column("ano_mes", sa.String(length=7), nullable=False),
        sa.Column("competencia", sa.Date(), nullable=False),
        sa.Column("dia_util", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.PrimaryKeyConstraint("sk_tempo"),
        sa.UniqueConstraint("data"),
    )
    op.create_index("ix_bi_dim_tempo_data", "bi_dim_tempo", ["data"])
    op.create_index("ix_bi_dim_tempo_ano_mes", "bi_dim_tempo", ["ano_mes"])
    op.create_index("ix_bi_dim_tempo_competencia", "bi_dim_tempo", ["competencia"])

    op.create_table(
        "bi_dim_unidade",
        sa.Column("sk_unidade", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("id_origem", UUID(as_uuid=True), nullable=False),
        sa.Column("nome", sa.String(length=120), nullable=False),
        sa.Column("tipo", sa.String(length=10), nullable=False),
        sa.PrimaryKeyConstraint("sk_unidade"),
        sa.UniqueConstraint("id_origem"),
    )

    op.create_table(
        "bi_dim_setor",
        sa.Column("sk_setor", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("chave_natural", sa.String(length=60), nullable=False),
        sa.Column("nome", sa.String(length=60), nullable=False),
        sa.PrimaryKeyConstraint("sk_setor"),
        sa.UniqueConstraint("chave_natural"),
    )

    op.create_table(
        "bi_dim_convenio",
        sa.Column("sk_convenio", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("id_origem", UUID(as_uuid=True), nullable=False),
        sa.Column("nome", sa.String(length=120), nullable=False),
        sa.Column("registro_ans", sa.String(length=20), nullable=True),
        sa.PrimaryKeyConstraint("sk_convenio"),
        sa.UniqueConstraint("id_origem"),
    )

    op.create_table(
        "bi_dim_procedimento",
        sa.Column("sk_procedimento", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("id_origem", UUID(as_uuid=True), nullable=False),
        sa.Column("codigo_tuss", sa.String(length=20), nullable=False),
        sa.Column("nome", sa.String(length=120), nullable=False),
        sa.Column("setor", sa.String(length=60), nullable=True),
        sa.Column("sk_setor", sa.Integer(), nullable=True),
        sa.Column("ativo", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.ForeignKeyConstraint(["sk_setor"], ["bi_dim_setor.sk_setor"]),
        sa.PrimaryKeyConstraint("sk_procedimento"),
        sa.UniqueConstraint("id_origem"),
    )

    op.create_table(
        "bi_dim_paciente_anon",
        sa.Column("sk_paciente", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("id_origem", sa.String(length=64), nullable=False),
        sa.Column("sexo", sa.String(length=20), nullable=False),
        sa.PrimaryKeyConstraint("sk_paciente"),
        sa.UniqueConstraint("id_origem"),
    )

    op.create_table(
        "bi_dim_faixa_etaria",
        sa.Column("sk_faixa_etaria", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("chave_natural", sa.String(length=20), nullable=False),
        sa.Column("descricao", sa.String(length=20), nullable=False),
        sa.Column("ordem", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("sk_faixa_etaria"),
        sa.UniqueConstraint("chave_natural"),
    )

    op.create_table(
        "bi_dim_motivo_glosa",
        sa.Column("sk_motivo_glosa", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("chave_natural", sa.String(length=255), nullable=False),
        sa.Column("descricao", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("sk_motivo_glosa"),
        sa.UniqueConstraint("chave_natural"),
    )

    # -------------------------------------------------------------------- fatos
    op.create_table(
        "bi_fato_ordem_servico",
        sa.Column("sk_fato", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("ordem_servico_id", UUID(as_uuid=True), nullable=False),
        sa.Column("sk_tempo", sa.Integer(), nullable=False),
        sa.Column("sk_unidade", sa.Integer(), nullable=False),
        sa.Column("sk_convenio", sa.Integer(), nullable=True),
        sa.Column("sk_paciente", sa.Integer(), nullable=False),
        sa.Column("sk_faixa_etaria", sa.Integer(), nullable=False),
        sa.Column("qtd_itens", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("qtd_itens_cancelados", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("valor_total", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("tempo_ciclo_horas", sa.Numeric(10, 2), nullable=True),
        sa.Column("tempo_coleta_recebimento_horas", sa.Numeric(10, 2), nullable=True),
        sa.Column("tempo_recebimento_laudo_horas", sa.Numeric(10, 2), nullable=True),
        sa.Column("concluida", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.ForeignKeyConstraint(["sk_tempo"], ["bi_dim_tempo.sk_tempo"]),
        sa.ForeignKeyConstraint(["sk_unidade"], ["bi_dim_unidade.sk_unidade"]),
        sa.ForeignKeyConstraint(["sk_convenio"], ["bi_dim_convenio.sk_convenio"]),
        sa.ForeignKeyConstraint(["sk_paciente"], ["bi_dim_paciente_anon.sk_paciente"]),
        sa.ForeignKeyConstraint(["sk_faixa_etaria"], ["bi_dim_faixa_etaria.sk_faixa_etaria"]),
        sa.PrimaryKeyConstraint("sk_fato"),
        sa.UniqueConstraint("ordem_servico_id"),
    )
    op.create_index("ix_bi_fato_os_natural", "bi_fato_ordem_servico", ["ordem_servico_id"])

    op.create_table(
        "bi_fato_atendimento",
        sa.Column("sk_fato", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("os_item_id", UUID(as_uuid=True), nullable=False),
        sa.Column("sk_tempo", sa.Integer(), nullable=False),
        sa.Column("sk_unidade", sa.Integer(), nullable=False),
        sa.Column("sk_convenio", sa.Integer(), nullable=True),
        sa.Column("sk_procedimento", sa.Integer(), nullable=False),
        sa.Column("sk_paciente", sa.Integer(), nullable=False),
        sa.Column("sk_faixa_etaria", sa.Integer(), nullable=False),
        sa.Column("sk_setor", sa.Integer(), nullable=True),
        sa.Column("qtd_exames", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("valor_negociado", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("cancelado", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("laudo_liberado", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.ForeignKeyConstraint(["sk_tempo"], ["bi_dim_tempo.sk_tempo"]),
        sa.ForeignKeyConstraint(["sk_unidade"], ["bi_dim_unidade.sk_unidade"]),
        sa.ForeignKeyConstraint(["sk_convenio"], ["bi_dim_convenio.sk_convenio"]),
        sa.ForeignKeyConstraint(["sk_procedimento"], ["bi_dim_procedimento.sk_procedimento"]),
        sa.ForeignKeyConstraint(["sk_paciente"], ["bi_dim_paciente_anon.sk_paciente"]),
        sa.ForeignKeyConstraint(["sk_faixa_etaria"], ["bi_dim_faixa_etaria.sk_faixa_etaria"]),
        sa.ForeignKeyConstraint(["sk_setor"], ["bi_dim_setor.sk_setor"]),
        sa.PrimaryKeyConstraint("sk_fato"),
        sa.UniqueConstraint("os_item_id"),
    )
    op.create_index("ix_bi_fato_atendimento_natural", "bi_fato_atendimento", ["os_item_id"])

    op.create_table(
        "bi_fato_faturamento",
        sa.Column("sk_fato", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("guia_item_id", UUID(as_uuid=True), nullable=False),
        sa.Column("sk_tempo", sa.Integer(), nullable=False),
        sa.Column("sk_unidade", sa.Integer(), nullable=False),
        sa.Column("sk_convenio", sa.Integer(), nullable=True),
        sa.Column("sk_procedimento", sa.Integer(), nullable=False),
        sa.Column("sk_paciente", sa.Integer(), nullable=False),
        sa.Column("sk_setor", sa.Integer(), nullable=True),
        sa.Column("valor_faturado", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("valor_glosado", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("valor_liberado", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("qtd_itens", sa.Integer(), nullable=False, server_default="1"),
        sa.ForeignKeyConstraint(["sk_tempo"], ["bi_dim_tempo.sk_tempo"]),
        sa.ForeignKeyConstraint(["sk_unidade"], ["bi_dim_unidade.sk_unidade"]),
        sa.ForeignKeyConstraint(["sk_convenio"], ["bi_dim_convenio.sk_convenio"]),
        sa.ForeignKeyConstraint(["sk_procedimento"], ["bi_dim_procedimento.sk_procedimento"]),
        sa.ForeignKeyConstraint(["sk_paciente"], ["bi_dim_paciente_anon.sk_paciente"]),
        sa.ForeignKeyConstraint(["sk_setor"], ["bi_dim_setor.sk_setor"]),
        sa.PrimaryKeyConstraint("sk_fato"),
        sa.UniqueConstraint("guia_item_id"),
    )
    op.create_index("ix_bi_fato_faturamento_natural", "bi_fato_faturamento", ["guia_item_id"])

    op.create_table(
        "bi_fato_financeiro",
        sa.Column("sk_fato", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("regime", sa.String(length=10), nullable=False),
        sa.Column("origem_tabela", sa.String(length=24), nullable=False),
        sa.Column("origem_id", UUID(as_uuid=True), nullable=False),
        sa.Column("sk_tempo", sa.Integer(), nullable=False),
        sa.Column("sk_unidade", sa.Integer(), nullable=False),
        sa.Column("sk_convenio", sa.Integer(), nullable=True),
        sa.Column("fluxo", sa.String(length=10), nullable=False),
        sa.Column("valor_previsto", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("valor_realizado", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("liquidado", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.ForeignKeyConstraint(["sk_tempo"], ["bi_dim_tempo.sk_tempo"]),
        sa.ForeignKeyConstraint(["sk_unidade"], ["bi_dim_unidade.sk_unidade"]),
        sa.ForeignKeyConstraint(["sk_convenio"], ["bi_dim_convenio.sk_convenio"]),
        sa.PrimaryKeyConstraint("sk_fato"),
        sa.UniqueConstraint("regime", "origem_tabela", "origem_id", name="uq_fato_financeiro_origem"),
    )
    op.create_index("ix_bi_fato_financeiro_regime", "bi_fato_financeiro", ["regime"])

    op.create_table(
        "bi_fato_logistica",
        sa.Column("sk_fato", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("amostra_id", UUID(as_uuid=True), nullable=False),
        sa.Column("sk_tempo", sa.Integer(), nullable=False),
        sa.Column("sk_unidade", sa.Integer(), nullable=False),
        sa.Column("sk_unidade_destino", sa.Integer(), nullable=True),
        sa.Column("qtd_amostras", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("tempo_transito_horas", sa.Numeric(10, 2), nullable=True),
        sa.Column("tempo_coleta_recebimento_horas", sa.Numeric(10, 2), nullable=True),
        sa.Column("rejeitada", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("amostras_divergentes", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("status_atual", sa.String(length=20), nullable=False, server_default=""),
        sa.ForeignKeyConstraint(["sk_tempo"], ["bi_dim_tempo.sk_tempo"]),
        sa.ForeignKeyConstraint(["sk_unidade"], ["bi_dim_unidade.sk_unidade"]),
        sa.ForeignKeyConstraint(["sk_unidade_destino"], ["bi_dim_unidade.sk_unidade"]),
        sa.PrimaryKeyConstraint("sk_fato"),
        sa.UniqueConstraint("amostra_id"),
    )
    op.create_index("ix_bi_fato_logistica_natural", "bi_fato_logistica", ["amostra_id"])

    op.create_table(
        "bi_fato_glosa",
        sa.Column("sk_fato", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("glosa_id", UUID(as_uuid=True), nullable=False),
        sa.Column("sk_tempo", sa.Integer(), nullable=False),
        sa.Column("sk_unidade", sa.Integer(), nullable=False),
        sa.Column("sk_convenio", sa.Integer(), nullable=True),
        sa.Column("sk_procedimento", sa.Integer(), nullable=False),
        sa.Column("sk_motivo_glosa", sa.Integer(), nullable=False),
        sa.Column("valor_glosado", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("valor_faturado_item", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("qtd_glosas", sa.Integer(), nullable=False, server_default="1"),
        sa.ForeignKeyConstraint(["sk_tempo"], ["bi_dim_tempo.sk_tempo"]),
        sa.ForeignKeyConstraint(["sk_unidade"], ["bi_dim_unidade.sk_unidade"]),
        sa.ForeignKeyConstraint(["sk_convenio"], ["bi_dim_convenio.sk_convenio"]),
        sa.ForeignKeyConstraint(["sk_procedimento"], ["bi_dim_procedimento.sk_procedimento"]),
        sa.ForeignKeyConstraint(["sk_motivo_glosa"], ["bi_dim_motivo_glosa.sk_motivo_glosa"]),
        sa.PrimaryKeyConstraint("sk_fato"),
        sa.UniqueConstraint("glosa_id"),
    )
    op.create_index("ix_bi_fato_glosa_natural", "bi_fato_glosa", ["glosa_id"])

    # ----------------------------------------------------------- observabilidade
    op.create_table(
        "bi_etl_execucao",
        sa.Column("id", UUID(as_uuid=True), nullable=False),
        sa.Column("iniciado_em", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("finalizado_em", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(length=12), nullable=False, server_default="EXECUTANDO"),
        sa.Column("modo", sa.String(length=12), nullable=False, server_default="FULL"),
        sa.Column("linhas", JSONB(), nullable=True),
        sa.Column("duracao_seg", sa.Numeric(10, 2), nullable=True),
        sa.Column("erro", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Recria o esquema anterior, vazio.

    Reversao LOSSY por natureza: as tabelas voltam sem dados. Nao ha perda real —
    o BI e derivado do operacional e `python -m src.bi.etl` reconstroi tudo.
    """
    for tabela in (
        "bi_etl_execucao",
        "bi_fato_glosa",
        "bi_fato_logistica",
        "bi_fato_financeiro",
        "bi_fato_faturamento",
        "bi_fato_atendimento",
        "bi_fato_ordem_servico",
        "bi_dim_motivo_glosa",
        "bi_dim_faixa_etaria",
        "bi_dim_paciente_anon",
        "bi_dim_procedimento",
        "bi_dim_convenio",
        "bi_dim_setor",
        "bi_dim_unidade",
        "bi_dim_tempo",
    ):
        op.execute(f"DROP TABLE IF EXISTS {tabela} CASCADE")

    op.create_table(
        "bi_dim_tempo",
        sa.Column("sk_tempo", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("data", sa.Date(), nullable=False),
        sa.Column("ano", sa.Integer(), nullable=False),
        sa.Column("mes", sa.Integer(), nullable=False),
        sa.Column("dia", sa.Integer(), nullable=False),
        sa.Column("dia_semana", sa.String(length=20), nullable=False),
        sa.Column("trimestre", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("sk_tempo"),
        sa.UniqueConstraint("data"),
    )
    op.create_table(
        "bi_dim_unidade",
        sa.Column("sk_unidade", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("id_origem", UUID(as_uuid=True), nullable=False),
        sa.Column("nome", sa.String(length=120), nullable=False),
        sa.Column("tipo", sa.String(length=10), nullable=False),
        sa.PrimaryKeyConstraint("sk_unidade"),
        sa.UniqueConstraint("id_origem"),
    )
    op.create_table(
        "bi_dim_convenio",
        sa.Column("sk_convenio", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("id_origem", UUID(as_uuid=True), nullable=False),
        sa.Column("nome", sa.String(length=120), nullable=False),
        sa.Column("registro_ans", sa.String(length=20), nullable=True),
        sa.PrimaryKeyConstraint("sk_convenio"),
        sa.UniqueConstraint("id_origem"),
    )
    op.create_table(
        "bi_dim_procedimento",
        sa.Column("sk_procedimento", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("id_origem", UUID(as_uuid=True), nullable=False),
        sa.Column("codigo_tuss", sa.String(length=20), nullable=False),
        sa.Column("nome", sa.String(length=120), nullable=False),
        sa.Column("setor", sa.String(length=60), nullable=True),
        sa.PrimaryKeyConstraint("sk_procedimento"),
        sa.UniqueConstraint("id_origem"),
    )
    op.create_table(
        "bi_dim_paciente_anon",
        sa.Column("sk_paciente", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("id_origem", sa.String(length=64), nullable=False),
        sa.Column("faixa_etaria", sa.String(length=20), nullable=False),
        sa.Column("sexo", sa.String(length=20), nullable=False),
        sa.PrimaryKeyConstraint("sk_paciente"),
        sa.UniqueConstraint("id_origem"),
    )
    op.create_table(
        "bi_fato_atendimento",
        sa.Column("sk_fato", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("sk_tempo", sa.Integer(), nullable=False),
        sa.Column("sk_unidade", sa.Integer(), nullable=False),
        sa.Column("sk_convenio", sa.Integer(), nullable=True),
        sa.Column("sk_procedimento", sa.Integer(), nullable=False),
        sa.Column("sk_paciente", sa.Integer(), nullable=False),
        sa.Column("qtd_exames", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("tempo_ciclo_os_horas", sa.Numeric(10, 2), nullable=True),
        sa.ForeignKeyConstraint(["sk_tempo"], ["bi_dim_tempo.sk_tempo"]),
        sa.ForeignKeyConstraint(["sk_unidade"], ["bi_dim_unidade.sk_unidade"]),
        sa.ForeignKeyConstraint(["sk_convenio"], ["bi_dim_convenio.sk_convenio"]),
        sa.ForeignKeyConstraint(["sk_procedimento"], ["bi_dim_procedimento.sk_procedimento"]),
        sa.ForeignKeyConstraint(["sk_paciente"], ["bi_dim_paciente_anon.sk_paciente"]),
        sa.PrimaryKeyConstraint("sk_fato"),
    )
    op.create_table(
        "bi_fato_faturamento",
        sa.Column("sk_fato", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("sk_tempo", sa.Integer(), nullable=False),
        sa.Column("sk_unidade", sa.Integer(), nullable=False),
        sa.Column("sk_convenio", sa.Integer(), nullable=True),
        sa.Column("sk_procedimento", sa.Integer(), nullable=False),
        sa.Column("valor_faturado", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("valor_glosado", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("ticket_medio", sa.Numeric(12, 2), nullable=True),
        sa.ForeignKeyConstraint(["sk_tempo"], ["bi_dim_tempo.sk_tempo"]),
        sa.ForeignKeyConstraint(["sk_unidade"], ["bi_dim_unidade.sk_unidade"]),
        sa.ForeignKeyConstraint(["sk_convenio"], ["bi_dim_convenio.sk_convenio"]),
        sa.ForeignKeyConstraint(["sk_procedimento"], ["bi_dim_procedimento.sk_procedimento"]),
        sa.PrimaryKeyConstraint("sk_fato"),
    )
    op.create_table(
        "bi_fato_financeiro",
        sa.Column("sk_fato", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("sk_tempo", sa.Integer(), nullable=False),
        sa.Column("sk_unidade", sa.Integer(), nullable=False),
        sa.Column("sk_convenio", sa.Integer(), nullable=True),
        sa.Column("valor_recebido", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("valor_pago", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("rentabilidade", sa.Numeric(12, 2), nullable=True),
        sa.ForeignKeyConstraint(["sk_tempo"], ["bi_dim_tempo.sk_tempo"]),
        sa.ForeignKeyConstraint(["sk_unidade"], ["bi_dim_unidade.sk_unidade"]),
        sa.ForeignKeyConstraint(["sk_convenio"], ["bi_dim_convenio.sk_convenio"]),
        sa.PrimaryKeyConstraint("sk_fato"),
    )
    op.create_table(
        "bi_fato_logistica",
        sa.Column("sk_fato", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("sk_tempo", sa.Integer(), nullable=False),
        sa.Column("sk_unidade", sa.Integer(), nullable=False),
        sa.Column("qtd_amostras", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("tempo_transito_horas", sa.Numeric(10, 2), nullable=True),
        sa.Column("amostras_divergentes", sa.Integer(), nullable=False, server_default="0"),
        sa.ForeignKeyConstraint(["sk_tempo"], ["bi_dim_tempo.sk_tempo"]),
        sa.ForeignKeyConstraint(["sk_unidade"], ["bi_dim_unidade.sk_unidade"]),
        sa.PrimaryKeyConstraint("sk_fato"),
    )
