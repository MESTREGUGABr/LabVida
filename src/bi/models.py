"""Esquema estrela do BI.

Regras de modelagem em vigor (ADR 0009):

1. **Todo fato declara grao e carrega chave natural.** A chave natural e o
   identificador da linha de origem no OLTP. E o que torna a carga idempotente
   (`ON CONFLICT DO UPDATE`), permite reconciliacao OLTP/OLAP e destrava carga
   incremental. Antes nenhum fato tinha, e o ETL so sabia apagar tudo.
2. **Medida so convive com o fato que compartilha seu grao.** `tempo_ciclo` e da
   Ordem de Servico, entao vive em `bi_fato_ordem_servico` — nao repetido em
   cada item, onde qualquer AVG ponderava a OS pelo numero de exames.
3. **Medida derivada nao vira coluna.** Ticket medio, rentabilidade e taxa de
   glosa sao calculados em `src/bi/metricas.py` sobre medidas aditivas. Razao
   pre-calculada nao reagrega: a media das medias nao e a media.
4. **Atributo que muda com o tempo e congelado no fato.** A faixa etaria do
   paciente e gravada com o valor vigente na data do fato gerador; recalcula-la
   na dimensao faria um paciente que faz 19 anos sumir retroativamente da faixa
   anterior em todo relatorio historico.
"""

import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    SmallInteger,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.db import Base

# ---------------------------------------------------------------------------
# Dimensoes
# ---------------------------------------------------------------------------


class DimTempo(Base):
    """Calendario DENSO.

    Antes as linhas nasciam sob demanda, so para datas que apareciam em algum
    fato — entao um mes sem movimento simplesmente nao existia, e a serie
    temporal PULAVA o mes em vez de mostrar zero. Uma queda de producao virava
    um buraco invisivel no grafico. Agora o ETL pre-carrega o intervalo inteiro.
    """

    __tablename__ = "bi_dim_tempo"

    sk_tempo: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    data: Mapped[date] = mapped_column(Date, nullable=False, unique=True, index=True)
    ano: Mapped[int] = mapped_column(Integer, nullable=False)
    mes: Mapped[int] = mapped_column(Integer, nullable=False)
    dia: Mapped[int] = mapped_column(Integer, nullable=False)
    dia_semana: Mapped[str] = mapped_column(String(20), nullable=False)
    dia_semana_num: Mapped[int] = mapped_column(SmallInteger, nullable=False)  # 0=segunda
    trimestre: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    semestre: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    semana_iso: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    nome_mes: Mapped[str] = mapped_column(String(20), nullable=False)
    ano_mes: Mapped[str] = mapped_column(String(7), nullable=False, index=True)  # '2026-03'
    competencia: Mapped[date] = mapped_column(Date, nullable=False, index=True)  # 1o dia do mes
    dia_util: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


class DimUnidade(Base):
    __tablename__ = "bi_dim_unidade"

    sk_unidade: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_origem: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, unique=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    tipo: Mapped[str] = mapped_column(String(10), nullable=False)


class DimSetor(Base):
    """Setor do laboratorio. Habilita produtividade e TAT por setor.

    `Procedimento.setor` e texto livre no OLTP, entao a chave natural aqui e o
    nome normalizado (casefold + trim) — ate o catalogo de exames da F3 trocar
    isso por FK de verdade.
    """

    __tablename__ = "bi_dim_setor"

    sk_setor: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    chave_natural: Mapped[str] = mapped_column(String(60), nullable=False, unique=True)
    nome: Mapped[str] = mapped_column(String(60), nullable=False)


class DimConvenio(Base):
    __tablename__ = "bi_dim_convenio"

    sk_convenio: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_origem: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, unique=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    registro_ans: Mapped[str | None] = mapped_column(String(20), nullable=True)


class DimProcedimento(Base):
    __tablename__ = "bi_dim_procedimento"

    sk_procedimento: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_origem: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, unique=True)
    codigo_tuss: Mapped[str] = mapped_column(String(20), nullable=False)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    # Antes era SEMPRE NULL: a carga passava setor=None explicitamente, embora
    # `procedimentos.setor` exista. Analise por setor nao existia.
    setor: Mapped[str | None] = mapped_column(String(60), nullable=True)
    sk_setor: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("bi_dim_setor.sk_setor"), nullable=True
    )
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


class DimPacienteAnon(Base):
    """Paciente pseudonimizado (LGPD).

    `id_origem` e o SHA-256 do UUID, nao o UUID cru, para o BI nao permitir join
    trivial de volta a `pacientes`. A faixa etaria NAO mora aqui — ela e
    congelada no fato (ADR 0009).
    """

    __tablename__ = "bi_dim_paciente_anon"

    sk_paciente: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_origem: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    sexo: Mapped[str] = mapped_column(String(20), nullable=False)


class DimFaixaEtaria(Base):
    __tablename__ = "bi_dim_faixa_etaria"

    sk_faixa_etaria: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    chave_natural: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    descricao: Mapped[str] = mapped_column(String(20), nullable=False)
    ordem: Mapped[int] = mapped_column(SmallInteger, nullable=False)


class DimMotivoGlosa(Base):
    """Motivo da glosa.

    `glosas.motivo` e `String(255)` livre no OLTP, entao a chave natural e o
    texto normalizado — "Falta de autorizacao" e "falta de autorizacao " viram
    a mesma linha. O `codigo_glosa` TISS da F8 substitui isso por codigo real.
    """

    __tablename__ = "bi_dim_motivo_glosa"

    sk_motivo_glosa: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    chave_natural: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    descricao: Mapped[str] = mapped_column(String(255), nullable=False)


# ---------------------------------------------------------------------------
# Fatos
# ---------------------------------------------------------------------------


class FatoOrdemServico(Base):
    """Grao: uma Ordem de Servico.

    Existe para tirar `tempo_ciclo` do fato de item, onde era repetido identico
    em cada linha da OS — qualquer AVG ponderava a OS pelo numero de exames, e
    uma OS com 8 exames pesava 8 vezes uma OS com 1.
    """

    __tablename__ = "bi_fato_ordem_servico"

    sk_fato: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ordem_servico_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, unique=True, index=True
    )
    sk_tempo: Mapped[int] = mapped_column(Integer, ForeignKey("bi_dim_tempo.sk_tempo"), nullable=False)
    sk_unidade: Mapped[int] = mapped_column(Integer, ForeignKey("bi_dim_unidade.sk_unidade"), nullable=False)
    sk_convenio: Mapped[int | None] = mapped_column(Integer, ForeignKey("bi_dim_convenio.sk_convenio"), nullable=True)
    sk_paciente: Mapped[int] = mapped_column(Integer, ForeignKey("bi_dim_paciente_anon.sk_paciente"), nullable=False)
    sk_faixa_etaria: Mapped[int] = mapped_column(
        Integer, ForeignKey("bi_dim_faixa_etaria.sk_faixa_etaria"), nullable=False
    )
    qtd_itens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    qtd_itens_cancelados: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    valor_total: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=Decimal("0"))
    # Tempos do ciclo, em horas. NULL enquanto a etapa nao aconteceu.
    tempo_ciclo_horas: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    tempo_coleta_recebimento_horas: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    tempo_recebimento_laudo_horas: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    concluida: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


class FatoAtendimento(Base):
    """Grao: um item de Ordem de Servico (um exame pedido)."""

    __tablename__ = "bi_fato_atendimento"

    sk_fato: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    os_item_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, unique=True, index=True
    )
    sk_tempo: Mapped[int] = mapped_column(Integer, ForeignKey("bi_dim_tempo.sk_tempo"), nullable=False)
    sk_unidade: Mapped[int] = mapped_column(Integer, ForeignKey("bi_dim_unidade.sk_unidade"), nullable=False)
    sk_convenio: Mapped[int | None] = mapped_column(Integer, ForeignKey("bi_dim_convenio.sk_convenio"), nullable=True)
    sk_procedimento: Mapped[int] = mapped_column(Integer, ForeignKey("bi_dim_procedimento.sk_procedimento"), nullable=False)
    sk_paciente: Mapped[int] = mapped_column(Integer, ForeignKey("bi_dim_paciente_anon.sk_paciente"), nullable=False)
    sk_faixa_etaria: Mapped[int] = mapped_column(
        Integer, ForeignKey("bi_dim_faixa_etaria.sk_faixa_etaria"), nullable=False
    )
    sk_setor: Mapped[int | None] = mapped_column(Integer, ForeignKey("bi_dim_setor.sk_setor"), nullable=True)
    qtd_exames: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    valor_negociado: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=Decimal("0"))
    cancelado: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    laudo_liberado: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


class FatoFaturamento(Base):
    """Grao: um item de guia TISS (um exame faturado).

    Datado pelo fechamento do lote. Item de lote ainda ABERTO nao entra — antes
    caia em `date.today()` e migrava de bucket temporal a cada execucao do ETL.
    Na onda 2 a datacao passa para a competencia do item faturavel.
    """

    __tablename__ = "bi_fato_faturamento"

    sk_fato: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    guia_item_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, unique=True, index=True
    )
    sk_tempo: Mapped[int] = mapped_column(Integer, ForeignKey("bi_dim_tempo.sk_tempo"), nullable=False)
    # Unidade REAL da OS de origem. Antes era sempre a unidade fake "consolidado",
    # entao receita por unidade nao existia.
    sk_unidade: Mapped[int] = mapped_column(Integer, ForeignKey("bi_dim_unidade.sk_unidade"), nullable=False)
    sk_convenio: Mapped[int | None] = mapped_column(Integer, ForeignKey("bi_dim_convenio.sk_convenio"), nullable=True)
    sk_procedimento: Mapped[int] = mapped_column(Integer, ForeignKey("bi_dim_procedimento.sk_procedimento"), nullable=False)
    sk_paciente: Mapped[int] = mapped_column(Integer, ForeignKey("bi_dim_paciente_anon.sk_paciente"), nullable=False)
    sk_setor: Mapped[int | None] = mapped_column(Integer, ForeignKey("bi_dim_setor.sk_setor"), nullable=True)
    valor_faturado: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=Decimal("0"))
    valor_glosado: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=Decimal("0"))
    valor_liberado: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=Decimal("0"))
    qtd_itens: Mapped[int] = mapped_column(Integer, nullable=False, default=1)


class FatoFinanceiro(Base):
    """Grao: um lancamento financeiro, por regime.

    `regime='PREVISTO'`  → um titulo, datado pelo VENCIMENTO (cronograma).
    `regime='CAIXA'`     → um movimento de caixa, datado por `ocorrido_em` (o
                           dinheiro que de fato entrou ou saiu).

    A separacao existe porque antes o ETL somava `titulo.valor` de TODO titulo em
    `valor_recebido`, independente do status: um titulo ABERTO de R$ 10.000
    aparecia como R$ 10.000 recebidos, e o painel chamava isso de "Fluxo de Caixa".
    """

    __tablename__ = "bi_fato_financeiro"
    __table_args__ = (
        UniqueConstraint("regime", "origem_tabela", "origem_id", name="uq_fato_financeiro_origem"),
    )

    sk_fato: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    regime: Mapped[str] = mapped_column(String(10), nullable=False, index=True)  # PREVISTO | CAIXA
    origem_tabela: Mapped[str] = mapped_column(String(24), nullable=False)
    origem_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    sk_tempo: Mapped[int] = mapped_column(Integer, ForeignKey("bi_dim_tempo.sk_tempo"), nullable=False)
    sk_unidade: Mapped[int] = mapped_column(Integer, ForeignKey("bi_dim_unidade.sk_unidade"), nullable=False)
    sk_convenio: Mapped[int | None] = mapped_column(Integer, ForeignKey("bi_dim_convenio.sk_convenio"), nullable=True)
    fluxo: Mapped[str] = mapped_column(String(10), nullable=False)  # ENTRADA | SAIDA
    valor_previsto: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=Decimal("0"))
    valor_realizado: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=Decimal("0"))
    liquidado: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


class FatoLogistica(Base):
    """Grao: uma amostra.

    Datado pela COLETA (`coletas.coletada_em`), nao por `date.today()` — antes
    toda a serie temporal de logistica colapsava numa barra unica em "hoje".
    `tempo_transito_horas` sai de `protocolos_recebimento.recebido_em` menos
    `malotes.despachado_em`: as duas datas ja existiam e nunca eram lidas.
    """

    __tablename__ = "bi_fato_logistica"

    sk_fato: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    amostra_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, unique=True, index=True
    )
    sk_tempo: Mapped[int] = mapped_column(Integer, ForeignKey("bi_dim_tempo.sk_tempo"), nullable=False)
    sk_unidade: Mapped[int] = mapped_column(Integer, ForeignKey("bi_dim_unidade.sk_unidade"), nullable=False)
    sk_unidade_destino: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("bi_dim_unidade.sk_unidade"), nullable=True
    )
    qtd_amostras: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    tempo_transito_horas: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    tempo_coleta_recebimento_horas: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    rejeitada: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    amostras_divergentes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    status_atual: Mapped[str] = mapped_column(String(20), nullable=False, default="")


class FatoGlosa(Base):
    """Grao: uma glosa. Habilita taxa de glosa por motivo e por convenio."""

    __tablename__ = "bi_fato_glosa"

    sk_fato: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    glosa_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, unique=True, index=True
    )
    sk_tempo: Mapped[int] = mapped_column(Integer, ForeignKey("bi_dim_tempo.sk_tempo"), nullable=False)
    sk_unidade: Mapped[int] = mapped_column(Integer, ForeignKey("bi_dim_unidade.sk_unidade"), nullable=False)
    sk_convenio: Mapped[int | None] = mapped_column(Integer, ForeignKey("bi_dim_convenio.sk_convenio"), nullable=True)
    sk_procedimento: Mapped[int] = mapped_column(Integer, ForeignKey("bi_dim_procedimento.sk_procedimento"), nullable=False)
    sk_motivo_glosa: Mapped[int] = mapped_column(
        Integer, ForeignKey("bi_dim_motivo_glosa.sk_motivo_glosa"), nullable=False
    )
    valor_glosado: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=Decimal("0"))
    valor_faturado_item: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=Decimal("0"))
    qtd_glosas: Mapped[int] = mapped_column(Integer, nullable=False, default=1)


# ---------------------------------------------------------------------------
# Observabilidade
# ---------------------------------------------------------------------------


class EtlExecucao(Base):
    """Registro de cada carga.

    Existe para o dashboard poder dizer "dados atualizados em DD/MM HH:MM".
    Sem isso o usuario nao tem como saber se o numero na tela e de hoje ou de
    tres semanas atras — e o BI so e confiavel se a data da carga for visivel.
    """

    __tablename__ = "bi_etl_execucao"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    iniciado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    finalizado_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(12), nullable=False, default="EXECUTANDO")
    modo: Mapped[str] = mapped_column(String(12), nullable=False, default="FULL")
    linhas: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    duracao_seg: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    erro: Mapped[str | None] = mapped_column(Text, nullable=True)
