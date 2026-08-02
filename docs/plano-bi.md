# LabVida — Plano de Reconstrução do BI

> Documento de **planejamento**. Nada aqui foi implementado ainda.
> Roteiro de execução: [roadmap-execucao.md](roadmap-execucao.md) — fases **F2** (onda 1) e **F12** (onda 2).
> Responde aos apontamentos do professor: *"implementar período no BI"* e *"Altair melhor para BI"*.

## Contexto

O professor pediu duas coisas no BI. Este plano entrega as duas — e resolve o problema maior que apareceu ao conferir o código: **o BI atual mente**. Não é imprecisão de arredondamento; são medidas erradas, séries temporais colapsadas e um ETL que produz números diferentes a cada execução sobre os mesmos dados de origem.

Cada afirmação abaixo foi conferida linha a linha em [src/bi/etl.py](../src/bi/etl.py), [src/bi/models.py](../src/bi/models.py) e nas 3 páginas `pages/bi_*.py`.

**Achado central de planejamento:** os documentos anteriores tratavam o BI como Fase 6, dependente de toda a remodelagem de faturamento. **Está errado.** Cerca de 70% do trabalho de BI não depende de competência nem de item faturável — as datas e medidas que faltam **já existem no OLTP e simplesmente não são consultadas**. O BI pode começar hoje, em paralelo.

---

## Sumário

1. [Diagnóstico verificado](#1-diagnóstico-verificado)
2. [Arquitetura alvo](#2-arquitetura-alvo)
3. [Modelo dimensional](#3-modelo-dimensional)
4. [ETL — idempotente, incremental, observável](#4-etl--idempotente-incremental-observável)
5. [Camada semântica de métricas](#5-camada-semântica-de-métricas)
6. [Catálogo de indicadores](#6-catálogo-de-indicadores)
7. [Dashboards e Altair](#7-dashboards-e-altair)
8. [Filtro de período](#8-filtro-de-período)
9. [Testes](#9-testes)
10. [As duas ondas](#10-as-duas-ondas)
11. [Riscos e decisões](#11-riscos-e-decisões)

---

## 1. Diagnóstico verificado

### 1.1 Os oito bugs que fazem o BI mentir

| # | Bug | Onde | Efeito |
|---|---|---|---|
| **B1** | `_sk_tempo(session, date.today())` **dentro do loop de amostras** | [etl.py:196](../src/bi/etl.py#L196) | **Toda a série temporal de logística é uma barra única em "hoje".** O gráfico "Amostras por Unidade" é o total histórico fingindo ser do dia |
| **B2** | `valor_recebido = t.valor` para **todo** `TituloReceber`, independente do status | [etl.py:188](../src/bi/etl.py#L188) | Título ABERTO de R$10.000 entra como **R$10.000 recebidos**. Não é só data errada — **a medida está errada**. O KPI "Fluxo de Caixa" mostra dinheiro que nunca entrou |
| **B3** | `FatoFaturamento` de lote aberto cai em `date.today()` | [etl.py:174](../src/bi/etl.py#L174) | Itens migram de bucket temporal a cada execução do ETL |
| **B4** | `_sk_procedimento(..., setor=None)` explícito | [etl.py:137](../src/bi/etl.py#L137) | `DimProcedimento.setor` é **sempre NULL** — embora `Procedimento.setor` exista como `String(60)` no OLTP. Análise por setor não existe |
| **B5** | `FatoFaturamento` sempre na unidade fake "consolidado" | [etl.py:181](../src/bi/etl.py#L181) | Receita por unidade é impossível. A dimensão está lá, o fato aponta para um UUID zerado |
| **B6** | `FatoFinanceiro.sk_convenio = None` hardcoded | [etl.py:188,192](../src/bi/etl.py#L188) | A FK existe no modelo e **nunca** é preenchida. Recebimento por convênio não existe |
| **B7** | `_sk_paciente` só cria, nunca atualiza | [etl.py:89-108](../src/bi/etl.py#L89-L108) | Faixa etária **congelada na primeira carga**. Vale para todas as dimensões: convênio renomeado nunca propaga ao BI |
| **B8** | `DimTempo` é criada sob demanda, só para datas que aparecem em fatos | [etl.py:38-49](../src/bi/etl.py#L38-L49) | Dimensão **esparsa**: mês sem fato não existe na tabela, então a série temporal **pula o mês** em vez de mostrar zero. Uma queda de produção vira um buraco invisível no gráfico |

> B8 não está catalogado em nenhum documento anterior.

### 1.2 Dois problemas de grão

**G1 — `tempo_ciclo_os_horas` está no grão errado.** O fato é gravado por `OsItem` ([etl.py:164-166](../src/bi/etl.py#L164-L166)), mas o tempo de ciclo é atributo da **OS** e é repetido idêntico em cada item dela. Qualquer `AVG()` pondera a OS pelo número de exames — uma OS com 8 exames pesa 8× uma OS com 1 exame. O indicador que a `RESENHA` declara pronto está **estatisticamente errado**.

**G2 — Nenhum fato tem chave natural.** Não existe `os_item_id`, `amostra_id`, `guia_item_id` nem `titulo_id` em fato nenhum. Consequências: carga incremental impossível, reconciliação OLTP↔OLAP impossível, deduplicação impossível. O ETL só sabe `DELETE FROM` tudo e recarregar ([etl.py:144-148](../src/bi/etl.py#L144-L148)).

### 1.3 O ETL não é idempotente — e não tem teste

`date.today()` aparece **4 vezes** dentro de `_carga_fatos` (linhas 174, 186, 190, 196). Rodar ontem e hoje produz números diferentes para os mesmos dados de origem.

`_carga_fatos` **não tem um único teste**. [tests/bi/test_etl.py](../tests/bi/test_etl.py) cobre apenas `_carga_dimensoes`, com 2 testes (dimensão populada e paciente anonimizado). Nada detectaria a regressão de nenhum dos 8 bugs acima.

### 1.4 Performance

`_tempo_ciclo_os` ([etl.py:111](../src/bi/etl.py#L111)) executa 2 queries por OS, dentro do loop de OS. Com as ~400 OS da base de demonstração são 800 round-trips só para esse indicador, mais um `SELECT` por `_sk_*` por linha de fato. É a razão dos ~35s de seed. Com volume real não escala.

### 1.5 Dashboards

- **11 queries SQL em string inline** dentro das 3 páginas. Nada é testável sem subir o Streamlit.
- **Zero filtros de data.** Todo agregado é "desde o início dos tempos"; apenas 2 das 11 queries sequer tocam `bi_dim_tempo`. É exatamente o que o professor apontou.
- **10 gráficos** em `st.bar_chart`/`st.line_chart`: sem tooltip, sem formatação pt-BR, sem escala de cor, sem drill-down. Altair 6.2.2 **já está instalado** e não é usado em lugar nenhum.
- [bi_logistica.py:52-60](../pages/bi_logistica.py#L52-L60) consulta a tabela operacional `amostras` **direto**, furando o modelo dimensional — viola a regra #35 do próprio `revisao-final.md`.
- Formatação monetária inconsistente entre páginas (`formatar_brl` só em `bi_financeiro`).
- O usuário **não tem como saber quando o ETL rodou pela última vez**. O número na tela pode ser de ontem ou de três semanas atrás.

### 1.6 O que já existe no OLTP e o BI ignora

Esta é a tabela que muda o sequenciamento do projeto. Todas as correções abaixo são **OLAP-side, sem migration no operacional**:

| Medida que falta | Fonte que **já existe** hoje | Destrava |
|---|---|---|
| Data da amostra (B1) | `Coleta.coletada_em` (1:1 com amostra, `amostra_id` UNIQUE) | Série temporal de logística |
| Data de movimentação | `AmostraMovimentacao.ocorrido_em` + `unidade_id` + `status` | Cadeia de custódia datada |
| `tempo_transito_horas` (nunca populado) | `ProtocoloRecebimento.recebido_em − Malote.despachado_em` | Indicador de trânsito de malote |
| Regime de caixa **real** (B2) | `MovimentoCaixa.tipo` (ENTRADA/SAIDA) + `valor` + `ocorrido_em` | Fluxo de caixa realizado × previsto |
| Data de conclusão da OS | `OsStatusHistorico.ocorrido_em` + `status` | TAT correto, sem `OrdemServico.fechada_em` |
| Setor do procedimento (B4) | `Procedimento.setor` (`String(60)`) | Produtividade por setor |
| Motivo da glosa | `Glosa.motivo` + `unidade_origem_id` + `criado_em` | Taxa de glosa por motivo |

> Correção de rumo em relação ao plano anterior: [plano-evolucao-erp.md](plano-evolucao-erp.md) §5.1 afirma que B1 "não há como corrigir sem mexer no OLTP: `Amostra` não tem timestamp algum". É verdade que `Amostra` não tem timestamp — mas `Coleta`, `AmostraMovimentacao`, `Malote` e `ProtocoloRecebimento` têm, e são suficientes. Nenhuma migration é necessária para consertar o `FatoLogistica`.

---

## 2. Arquitetura alvo

```
OLTP
 │
 ├─→ src/bi/etl/           extração e carga — idempotente, incremental, observável
 │     ├─ dimensoes.py
 │     ├─ fatos.py
 │     └─ execucao.py      registro de cada carga
 │
 ├─→ src/bi/models.py      star schema: 7 dimensões, 6 fatos
 │
 ├─→ src/bi/metricas.py    CAMADA SEMÂNTICA — 1 função = 1 indicador, tipada e testável
 │
 ├─→ src/bi/graficos.py    specs Altair reutilizáveis + tema único
 │
 └─→ pages/bi_*.py         só orquestra: filtro → métrica → gráfico
```

**Regra de arquitetura: nenhum SQL em `pages/`.** Hoje há 11 queries inline. Depois, zero. É o que permite testar um indicador sem subir o Streamlit — hoje impossível.

---

## 3. Modelo dimensional

### 3.1 Dimensões

| Dimensão | Hoje | Alvo |
|---|---|---|
| `bi_dim_tempo` | esparsa, 7 colunas, `trimestre` nunca usado | **densa** — pré-carregada por `generate_series` cobrindo min→max do OLTP + mês corrente. Novas colunas: `ano_mes` (`'2026-03'`), `nome_mes`, `semana_iso`, `semestre`, `dia_util` (bool), `competencia` (1º dia do mês) |
| `bi_dim_unidade` | ok | + `ativo`; upsert **com update** de atributos |
| `bi_dim_convenio` | ok | + `ativo`; upsert com update |
| `bi_dim_procedimento` | `setor` sempre NULL (B4) | `setor` preenchido de `Procedimento.setor`; ganha `sk_setor` quando o catálogo de exames existir (F3) |
| `bi_dim_paciente_anon` | faixa congelada na 1ª carga (B7) | mantém só `sexo` e o hash SHA-256. A **faixa etária sai da dimensão** e passa a ser gravada no fato ([ADR 0009](adr/0009-grao-chave-natural-e-medidas-derivadas-no-bi.md), decisão 4) |
| **`bi_dim_setor`** | — | **nova** — setor × unidade. Habilita produtividade e TAT por setor |
| **`bi_dim_motivo_glosa`** | — | **nova** — `Glosa.motivo` normalizado (hoje texto livre; vira código TISS na F8) |

A anonimização do paciente (`id_origem` = SHA-256, só `faixa_etaria` e `sexo` expostos) é mantida integralmente — é requisito LGPD e regra #37 do `revisao-final.md`.

### 3.2 Fatos

Cada fato passa a declarar **grão** e **chave natural** explícitos.

| Fato | Grão | Chave natural | Medidas |
|---|---|---|---|
| **`bi_fato_ordem_servico`** *(novo)* | 1 OS | `ordem_servico_id` | `tempo_ciclo_horas`, `tempo_coleta_recebimento_h`, `tempo_recebimento_laudo_h`, `qtd_itens`, `valor_total` |
| `bi_fato_atendimento` | 1 item de OS | `os_item_id` | `qtd_exames`, `valor_negociado`, `sk_faixa_etaria` (congelada na data do fato) — **perde** `tempo_ciclo_os_horas` (vai para o fato de OS, resolve G1) |
| `bi_fato_faturamento` | 1 item faturado | `guia_item_id` → `item_faturavel_id` na onda 2 | `valor_faturado`, `valor_glosado`, `valor_liberado`, `valor_recebido`; **unidade real** (resolve B5) |
| `bi_fato_financeiro` | 1 lançamento por regime | `titulo_id` + `regime` / `movimento_caixa_id` | `valor_previsto` e `valor_realizado` **separados** (resolve B2); `sk_convenio` preenchido (resolve B6) |
| `bi_fato_logistica` | 1 amostra | `amostra_id` | `qtd_amostras`, `tempo_transito_horas` (destravado), `amostras_divergentes` — datado pela coleta (resolve B1) |
| **`bi_fato_glosa`** *(novo)* | 1 glosa | `glosa_id` | `valor_glosado`, `valor_recuperado` (onda 2), por motivo e convênio |

Colunas hoje **nunca populadas** que passam a ter valor: `FatoLogistica.tempo_transito_horas`, `FatoFaturamento.ticket_medio` (vira medida derivada na camada semântica, não coluna), `FatoFinanceiro.rentabilidade` (idem — sai do modelo, vira métrica calculada).

> Decisão: medidas **derivadas** (ticket médio, rentabilidade, taxa de glosa) saem das tabelas de fato e passam a viver em `metricas.py`. Guardar razão pré-calculada em fato é o erro clássico que impede reagregação — a média de médias não é a média.

---

## 4. ETL — idempotente, incremental, observável

### 4.1 Idempotência

- **Zero `date.today()`** em `_carga_fatos`. Toda data vem do fato gerador.
- Carga por chave natural: `INSERT ... ON CONFLICT (chave_natural) DO UPDATE`. O `DELETE FROM` total vira modo explícito `--full`.
- **Teste obrigatório:** rodar o ETL 2× produz linhas byte a byte idênticas.

### 4.2 Incremental

Com chave natural em todo fato, a carga passa a processar só o que mudou desde a última execução (`bi_etl_execucao.finalizado_em`), com fallback para carga cheia.

### 4.3 Performance

Os loops Python com N+1 dão lugar a **uma query agregada por fato**. `_tempo_ciclo_os` (800 round-trips hoje) vira um único `SELECT` com `MIN`/`MAX` agrupado por OS.

### 4.4 Observabilidade

```sql
CREATE TABLE bi_etl_execucao (
  id            UUID PRIMARY KEY,
  iniciado_em   TIMESTAMPTZ NOT NULL DEFAULT now(),
  finalizado_em TIMESTAMPTZ,
  status        VARCHAR(12) NOT NULL CHECK (status IN ('EXECUTANDO','SUCESSO','ERRO')),
  modo          VARCHAR(12) NOT NULL CHECK (modo IN ('INCREMENTAL','FULL')),
  linhas        JSONB,      -- {"fato_atendimento": 1240, ...}
  duracao_seg   NUMERIC(10,2),
  erro          TEXT
);
```

Cada dashboard passa a exibir **"Dados atualizados em DD/MM/AAAA HH:MM"**. Hoje o usuário não tem como saber se o número na tela é de ontem ou de três semanas atrás.

---

## 5. Camada semântica de métricas

`src/bi/metricas.py` — cada indicador é uma função tipada que recebe o mesmo objeto de período e devolve um `DataFrame`:

```python
@dataclass(frozen=True)
class Periodo:
    inicio: date
    fim: date
    competencia: date | None = None      # onda 2

def exames_por_unidade(session, periodo: Periodo) -> pd.DataFrame
def ticket_medio_por_convenio(session, periodo: Periodo) -> pd.DataFrame
def tat_coleta_laudo(session, periodo: Periodo, por: Literal["setor","procedimento","unidade"]) -> pd.DataFrame
def taxa_glosa_por_motivo(session, periodo: Periodo) -> pd.DataFrame
def fluxo_caixa(session, periodo: Periodo, regime: Literal["CAIXA","COMPETENCIA"]) -> pd.DataFrame
def aging_carteira(session, periodo: Periodo) -> pd.DataFrame
def dre_simplificado(session, periodo: Periodo) -> pd.DataFrame
def curva_abc_procedimentos(session, periodo: Periodo) -> pd.DataFrame
...
```

Ganhos: cada indicador ganha teste próprio; o filtro de período é aplicado **uma vez, de forma uniforme** (`WHERE bi_dim_tempo.data BETWEEN :inicio AND :fim`) em vez de 11 SQLs cada um decidindo sozinho; e a mesma métrica pode alimentar gráfico, tabela e export sem duplicar SQL.

---

## 6. Catálogo de indicadores

| Indicador | Fonte | Onda | Origem do pedido |
|---|---|---|---|
| Exames por unidade / mês / convênio / faixa etária | `fato_atendimento` | 1 | já existe, ganha período |
| **Ticket médio por exame e por convênio** | `fato_faturamento` | 1 | F14 do `revisao-final` |
| **TAT — tempo médio coleta→laudo**, por setor/procedimento/unidade | `fato_ordem_servico` | 1 | F15 — corrigido no grão (G1) |
| **Tempo médio de trânsito de malote** | `fato_logistica` | 1 | coluna morta destravada |
| Curva ABC de procedimentos por receita | `fato_faturamento` | 1 | novo |
| Sazonalidade por dia da semana | `fato_atendimento` × `dim_tempo` | 1 | novo — `dia_semana` já existe e nunca foi usado |
| **Fluxo de caixa realizado** (regime de caixa) | `movimentos_caixa` | 1 | corrige B2 |
| Aging da carteira (títulos por faixa de vencimento) | `fato_financeiro` | 1 | novo |
| Produtividade por setor | `fato_atendimento` × `dim_setor` | 1 | destravado por B4 |
| Taxa de divergência logística por unidade | `fato_logistica` | 1 | já existe, ganha período |
| **Taxa de glosa por convênio e por motivo** | `fato_glosa` | 1 (motivo texto) → 2 (código TISS) | pedido do professor |
| Receita por competência × regime de caixa | `fato_faturamento` | 2 | pedido do professor |
| **DRE gerencial simplificado** | `fato_financeiro` + categorias | 2 | F13 |
| Divergências abertas por severidade e valor em risco | `divergencias` | 2 | pedido do professor |
| Previsto × realizado por competência | `fato_financeiro` | 2 | — |

---

## 7. Dashboards e Altair

### 7.1 Quatro páginas

| Página | Estado | Conteúdo |
|---|---|---|
| **`bi_visao_executiva.py`** | **nova** | KPIs consolidados, DRE simplificado, receita × recebimento, alertas (divergências, títulos vencidos, remessas sem retorno) |
| `bi_produtividade.py` | reescrita | Exames, TAT, produtividade por setor, sazonalidade, curva ABC |
| `bi_logistica.py` | reescrita | Amostras datadas de verdade, tempo de trânsito, divergências — **sem query no OLTP** |
| `bi_financeiro.py` | reescrita | Fluxo de caixa realizado × previsto, ticket médio, glosa por motivo, aging |

### 7.2 `src/bi/graficos.py` — specs Altair

Funções nomeadas, não Altair solto nas páginas:

```python
def barra_categorica(df, *, x, y, cor=None, titulo, formato_y="moeda") -> alt.Chart
def linha_temporal(df, *, x, y, serie=None, titulo) -> alt.Chart
def barra_empilhada(df, *, x, y, serie, titulo) -> alt.Chart
def donut(df, *, categoria, valor, titulo) -> alt.Chart
def heatmap_sazonalidade(df, *, dia_semana, periodo, valor) -> alt.Chart
def waterfall_dre(df, *, categoria, valor) -> alt.Chart
```

Tema único em `src/bi/tema_altair.py`: paleta consistente entre as 4 páginas, `tooltip` com rótulos em pt-BR, eixo monetário com separador brasileiro (`R$ 1.234,56`), tipografia alinhada ao `ui_css.py` existente.

**Drill-down:** `alt.selection_point()` + `st.altair_chart(..., on_select="rerun")` — clicar num convênio no gráfico filtra os demais gráficos da página. É o F27 do `revisao-final`, pendente desde sempre.

**Zero dependência nova:** `altair==6.2.2` já está em [requirements.txt](../requirements.txt).

---

## 8. Filtro de período

`src/bi/filtros.py` — um componente compartilhado pelas 4 páginas:

- `st.segmented_control` com presets: **Mês atual · Últimos 3 meses · Ano · Personalizado**
- `st.date_input` de intervalo no modo personalizado
- Estado em `st.session_state`, propagado como `Periodo` para toda métrica
- Na onda 2 ganha o modo **Competência** (seletor de competência substitui o intervalo de datas)

Comparação com período anterior (`Δ%` no `st.metric`) sai de graça: mesma métrica, dois `Periodo`.

---

## 9. Testes

Hoje: 2 testes, ambos de dimensão. Alvo:

| Categoria | Teste |
|---|---|
| **Idempotência** | rodar `executar_etl()` 2× → contagem e soma idênticas em todos os fatos |
| **Reconciliação** | `SUM(fato_faturamento.valor_faturado)` = `SUM(guias_itens.valor_faturado)` no OLTP; idem para cada fato |
| **Grão** | nenhuma chave natural duplicada em fato nenhum |
| **B1** | amostras coletadas em meses diferentes caem em `sk_tempo` diferentes |
| **B2** | título ABERTO **não** entra em `valor_realizado`; movimento de ENTRADA entra |
| **B4** | `DimProcedimento.setor` não é NULL quando o procedimento tem setor |
| **B7** | dimensão atualizada quando o atributo muda na origem |
| **B8** | `DimTempo` densa — nenhum mês faltando entre min e max |
| **G1** | `AVG(tempo_ciclo)` do fato de OS ≠ média ponderada por item (o número certo) |
| **Métricas** | um teste por função de `metricas.py`, com dados controlados |

O seeder continua sendo o teste de integração de fato — ele atravessa ~400 OS pelo fluxo real.

---

## 10. As duas ondas

### Onda 1 — BI independente (**F2** do roadmap, começa junto com F1)

Não depende de competência, item faturável, remessa nem baixa parcial.

- Correção dos 8 bugs + os 2 problemas de grão
- `DimTempo` densa, `DimSetor`, `DimMotivoGlosa`
- `FatoOrdemServico` novo; chaves naturais em todos os fatos
- ETL idempotente + incremental + `bi_etl_execucao`
- `metricas.py`, `graficos.py`, `filtros.py`
- 4 dashboards em Altair com filtro de período e drill-down
- Suíte de testes de BI

**Migration:** uma só (`0014_bi_reconstrucao`, ver nota de numeração no roadmap) — só tabelas `bi_*`, zero impacto no OLTP. Reversível por `DROP`/recarga: o BI é derivado, não é fonte da verdade.

### Onda 2 — BI sobre o modelo novo (**F12** do roadmap)

Depende de F4 (competência), F8 (glosa) e F10 (baixa parcial).

- Competência como eixo de datação do faturamento
- `FatoGlosa` com código TISS e recurso/recuperação
- Previsto × realizado com baixas parciais reais
- DRE gerencial com categorias de despesa
- Painel de divergências no BI executivo
- Unidade real no faturamento (via `itens_faturaveis.unidade_id`)

---

## 11. Riscos e decisões

**Decisões tomadas (02/08/2026) — [ADR 0009](adr/0009-grao-chave-natural-e-medidas-derivadas-no-bi.md), `accepted`:**

1. ✅ **Faixa etária congelada no fato**, não recalculada na dimensão. Recalcular faria um paciente que faz 19 anos "sumir" retroativamente da faixa anterior em todo relatório histórico, mudando números de meses já fechados.
2. ✅ **Medidas derivadas fora do fato.** `ticket_medio` e `rentabilidade` saem das tabelas (nunca tiveram valor gravado, então não há perda histórica) e viram funções em `metricas.py`.
3. ✅ **Chave natural e grão explícitos em todo fato**; medida no grão errado vira fato próprio (`bi_fato_ordem_servico`).

**Ainda em aberto:**

4. **Carga incremental na primeira versão ou só idempotência?** Incremental é mais trabalho e o volume atual não exige. **Recomendação: entregar idempotência + chave natural na onda 1** (que é justamente o que destrava o incremental depois), **e deixar o incremental para a onda 2.** Não bloqueia o início da F2.

**Riscos técnicos:**

5. **A base de demonstração vai mudar de aparência.** Corrigir B1/B2/B3 muda todos os números dos dashboards — para melhor, mas quem viu a versão anterior vai estranhar. Combinar com a equipe antes de apresentar.
6. **`Glosa.motivo` é texto livre `String(255)`.** `DimMotivoGlosa` na onda 1 vai agrupar por string — "Falta de autorização" e "falta de autorizacao" viram dois motivos. Normalizar no ETL (casefold + trim) mitiga; a solução real é o `codigo_glosa` TISS da F8.
7. **`FatoFinanceiro` com dois regimes na mesma tabela** exige disciplina de `WHERE regime = ...` em toda métrica. Alternativa: duas tabelas. **Recomendação: uma tabela com coluna `regime`,** porque a comparação previsto × realizado é o indicador mais pedido e ficaria com join desnecessário.
8. **Drill-down com `on_select` dispara rerun da página.** Sem `st.fragment` (F1), a página inteira recarrega a cada clique no gráfico. **F2 depende de F1 para o drill-down ficar fluido** — o resto de F2 é independente.
