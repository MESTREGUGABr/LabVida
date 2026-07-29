<!-- Anexo tecnico do docs/plano-evolucao-erp.md (secao 3). -->

> **Anexo tecnico** do [Plano de Evolucao para ERP de Verdade](plano-evolucao-erp.md), secao 3.
> Detalha o DDL, as migrations com backfill e as assinaturas de servico da remodelagem
> de Faturamento e Financeiro. Documento de planejamento — nada aqui foi implementado ainda.

# Remodelagem de Faturamento e Financeiro — LabVida

## 0. Resumo da decisão arquitetural

Três eixos, nessa ordem de precedência:

1. **Competência é carimbada no fato gerador, não no ato de faturar.** O laudo liberado cria imediatamente um `ItemFaturavel` com `competencia` derivada de `laudo.liberado_em`. Faturar em maio um laudo de março não move a receita para maio.
2. **Guia é o documento do atendimento (1 OS = 1 guia); remessa é o envelope enviado ao convênio (N guias).** É o que o TISS realmente é e é o que o professor pediu com "por paciente – por lote".
3. **Divergência é entidade de primeira classe**, detectada por 5 gatilhos e apresentada num painel único. `conciliacoes_pagamento` morre absorvida por ela.

---

## 1. Modelo de dados alvo

### 1.1 Competência — tabela, com PK natural `DATE`

**Decisão: tabela `competencias`, PK natural = primeiro dia do mês.**

Por que não só uma coluna `competencia DATE` nos itens: o professor pediu *fluxo de fechamento*. Fechamento exige um objeto com estado, autor, instante e totais congelados. Coluna não tem onde guardar isso, e sem estado não existe "não pode mais lançar em março".

Por que PK natural `DATE` e não UUID (quebra deliberada da convenção do repo): o item guarda `competencia DATE`, que é **ao mesmo tempo a FK e a dimensão de consulta**. `GROUP BY competencia` e `WHERE competencia = '2026-03-01'` sem join nenhum, índice barato. Com PK UUID você precisaria de `competencia_id UUID` **e** `competencia DATE` denormalizada nos itens — duas colunas para o mesmo fato, que podem divergir. Aqui não podem.

```sql
CREATE TABLE competencias (
  competencia            DATE PRIMARY KEY
                         CHECK (EXTRACT(DAY FROM competencia) = 1),
  status                 VARCHAR(10) NOT NULL DEFAULT 'ABERTA'
                         CHECK (status IN ('ABERTA','FECHADA')),
  -- apuração congelada no fechamento (recebimento continua vivo depois, não congela)
  valor_faturado         NUMERIC(14,2),
  valor_glosado          NUMERIC(14,2),
  valor_liberado         NUMERIC(14,2),
  qtd_itens_faturaveis   INTEGER,
  qtd_guias              INTEGER,
  qtd_remessas           INTEGER,
  criada_em              TIMESTAMPTZ NOT NULL DEFAULT now(),
  fechada_em             TIMESTAMPTZ,
  fechada_por_usuario_id UUID REFERENCES usuarios(id),
  reaberta_em            TIMESTAMPTZ,
  justificativa          VARCHAR(255),
  CHECK (status = 'ABERTA' OR fechada_em IS NOT NULL)
);
CREATE INDEX ix_competencias_status ON competencias (status);
```

Competência é **global do laboratório** (eixo contábil). O que é por convênio é a remessa.

**Regra do fuso — decisão que precisa de martelo.** `liberado_em` é `TIMESTAMPTZ` em UTC. Um laudo liberado às `2026-03-01T01:00Z` foi liberado em **28/02 às 22h em Recife**. `date_trunc('month', liberado_em)` daria março; o correto é fevereiro. Definir `TZ_OPERACAO = "America/Recife"` em `src/config.py` e usar em **um único helper** `competencia_de(instante)` — e a mesma expressão `AT TIME ZONE 'America/Recife'` em todo SQL de backfill. Vale um ADR.

**Regra do lançamento retroativo:** se a competência do fato gerador está FECHADA, o item nasce na competência ABERTA corrente, guarda `competencia_original` e gera divergência informativa `COMPETENCIA_FECHADA_RETROATIVA`. Fechado é imutável; retroativo é rastreável.

### 1.2 Item faturável — o ledger que resolve metade dos bugs

```sql
CREATE TABLE itens_faturaveis (
  id                UUID PRIMARY KEY,
  laudo_id          UUID NOT NULL UNIQUE REFERENCES laudos(id),
  os_item_id        UUID NOT NULL REFERENCES os_itens(id),
  ordem_servico_id  UUID NOT NULL REFERENCES ordens_servico(id),
  paciente_id       UUID NOT NULL REFERENCES pacientes(id),
  convenio_id       UUID          REFERENCES convenios(id),   -- NULL = particular
  unidade_id        UUID NOT NULL REFERENCES unidades(id),
  procedimento_id   UUID NOT NULL REFERENCES procedimentos(id),
  competencia       DATE NOT NULL REFERENCES competencias(competencia),
  competencia_original DATE,                                   -- preenchida só em lançamento retroativo
  fato_gerador_em   TIMESTAMPTZ NOT NULL,                      -- = laudo.liberado_em
  valor_tabela      NUMERIC(12,2),                             -- preço vigente na data do fato gerador; NULL = sem tabela
  valor_previsto    NUMERIC(12,2) NOT NULL CHECK (valor_previsto > 0),
  status            VARCHAR(24) NOT NULL DEFAULT 'A_FATURAR',
  criado_em         TIMESTAMPTZ NOT NULL DEFAULT now(),
  CHECK (status IN ('A_FATURAR','FATURADO','GLOSADO_A_REAPRESENTAR','PERDIDO','CANCELADO'))
);
CREATE INDEX ix_if_apuracao ON itens_faturaveis (competencia, convenio_id, status);
CREATE INDEX ix_if_pendentes ON itens_faturaveis (convenio_id, competencia)
  WHERE status IN ('A_FATURAR','GLOSADO_A_REAPRESENTAR');
CREATE INDEX ix_if_os ON itens_faturaveis (ordem_servico_id);
```

Os atalhos denormalizados (`ordem_servico_id`, `paciente_id`, `convenio_id`, `unidade_id`) são deliberados: hoje `glosa/repository.py` faz 5 joins para descobrir a unidade de origem, e `_unidade_do_guia_item` faz outros 3. Aqui é uma coluna.

**Como isso destrava o `laudo_id UNIQUE`:** o UNIQUE está *certo* — um laudo tem exatamente um fato gerador. Ele só estava na tabela errada. Sobe para `itens_faturaveis.laudo_id`; `guias_itens` passa a apontar para `item_faturavel_id` **sem** unique, permitindo N apresentações. A vigência é garantida por índice parcial (§1.4). Item 100% glosado vira `GLOSADO_A_REAPRESENTAR` e **reaparece na lista de pendentes**. Receita deixa de evaporar.

`valor_previsto NOT NULL` mata o fallback mágico `50.0` de `lote_faturamento/repository.py:102` — não existe mais caso falsy.

### 1.3 Guia por paciente/atendimento

Grão = **OrdemServico** (1 OS = 1 atendimento de 1 paciente). É o grão da guia SP/SADT.

```sql
ALTER TABLE guias_tiss
  ADD COLUMN remessa_id            UUID     REFERENCES remessas_faturamento(id),  -- NULLABLE: guia existe antes da remessa
  ADD COLUMN ordem_servico_id      UUID NOT NULL REFERENCES ordens_servico(id),
  ADD COLUMN paciente_id           UUID NOT NULL REFERENCES pacientes(id),
  ADD COLUMN convenio_id           UUID     REFERENCES convenios(id),
  ADD COLUMN competencia           DATE NOT NULL REFERENCES competencias(competencia),
  ADD COLUMN numero_guia_prestador VARCHAR(20) NOT NULL,
  ADD COLUMN numero_guia_operadora VARCHAR(20),
  ADD COLUMN senha_autorizacao     VARCHAR(20),
  ADD COLUMN data_atendimento      DATE NOT NULL,
  ADD COLUMN valor_apresentado     NUMERIC(12,2) NOT NULL DEFAULT 0,
  ADD COLUMN valor_glosado         NUMERIC(12,2) NOT NULL DEFAULT 0,
  ADD COLUMN valor_liberado        NUMERIC(12,2) GENERATED ALWAYS AS (valor_apresentado - valor_glosado) STORED,
  ADD COLUMN status                VARCHAR(20) NOT NULL DEFAULT 'ABERTA';
  -- status_pre_auditoria: mantida, e agora efetivamente escrita
ALTER TABLE guias_tiss ADD CONSTRAINT uq_guia_prestador UNIQUE (numero_guia_prestador);
ALTER TABLE guias_tiss ADD CONSTRAINT ck_guia_status
  CHECK (status IN ('ABERTA','EM_REMESSA','ENVIADA','PROCESSADA','CANCELADA'));

-- no máximo uma guia ABERTA por OS por competência; histórico ilimitado (reapresentação)
CREATE UNIQUE INDEX uq_guia_aberta_os_comp
  ON guias_tiss (ordem_servico_id, competencia) WHERE status = 'ABERTA';
```

`_obter_ou_criar_guia` (o bug de `lote.guias[0]`) é substituído por `obter_ou_criar_guia_aberta(ordem_servico_id, competencia)`, e o índice parcial garante a unicidade no banco, não só na aplicação.

Numeração: **SEQUENCE Postgres** `seq_guia_prestador` / `seq_remessa`, no lugar dos loops de retry com `uuid4().hex`. TISS espera numeração sequencial do prestador. Ressalva a registrar: `nextval` não é transacional — rollback deixa buraco na numeração. Aceitável e padrão; documentar.

### 1.4 Item da guia

```sql
ALTER TABLE guias_itens
  ADD COLUMN item_faturavel_id UUID NOT NULL REFERENCES itens_faturaveis(id),
  ADD COLUMN valor_glosado     NUMERIC(12,2) NOT NULL DEFAULT 0,
  ADD COLUMN valor_liberado    NUMERIC(12,2) GENERATED ALWAYS AS (valor_faturado - valor_glosado) STORED,
  ADD COLUMN sequencial        SMALLINT NOT NULL DEFAULT 1,     -- ordem do item dentro da guia (TISS)
  DROP CONSTRAINT guias_itens_laudo_id_key,
  DROP COLUMN laudo_id;                                          -- ver §5, decisão em aberto
ALTER TABLE guias_itens
  ADD CONSTRAINT ck_gi_glosa CHECK (valor_glosado >= 0 AND valor_glosado <= valor_faturado),
  ADD CONSTRAINT ck_gi_status CHECK (status IN ('FATURADO','GLOSADO_PARCIAL','GLOSADO_TOTAL','CANCELADO'));

-- no máximo um item VIGENTE por item faturável (glosado total sai do conjunto e libera reapresentação)
CREATE UNIQUE INDEX uq_guia_item_vigente
  ON guias_itens (item_faturavel_id) WHERE status IN ('FATURADO','GLOSADO_PARCIAL');
```

`valor_glosado` como **total corrente mantido pelo service com CHECK** é o que resolve o bug de `glosa/service.py:32` no nível do banco: glosas cumulativas passando de 100% viram violação de constraint, não silêncio.

### 1.5 Remessa (o que sobra do lote)

```sql
ALTER TABLE lotes_faturamento RENAME TO remessas_faturamento;
ALTER TABLE remessas_faturamento RENAME COLUMN codigo_lote TO numero_remessa;
ALTER TABLE remessas_faturamento
  ADD COLUMN competencia         DATE NOT NULL REFERENCES competencias(competencia),
  ADD COLUMN valor_apresentado   NUMERIC(14,2) NOT NULL DEFAULT 0,   -- ex-valor_total
  ADD COLUMN valor_glosado       NUMERIC(14,2) NOT NULL DEFAULT 0,
  ADD COLUMN valor_liberado      NUMERIC(14,2) GENERATED ALWAYS AS (valor_apresentado - valor_glosado) STORED,
  ADD COLUMN qtd_guias           INTEGER NOT NULL DEFAULT 0,
  ADD COLUMN protocolo_operadora VARCHAR(40),
  ADD COLUMN enviada_em          TIMESTAMPTZ,
  ADD COLUMN retorno_em          TIMESTAMPTZ;
ALTER TABLE remessas_faturamento ADD CONSTRAINT ck_remessa_status
  CHECK (status IN ('ABERTA','FECHADA','ENVIADA','RETORNADA','CANCELADA'));

-- no máximo uma remessa ABERTA por convênio+competência; NULLS NOT DISTINCT cobre particular (PG15+)
CREATE UNIQUE INDEX uq_remessa_aberta ON remessas_faturamento (convenio_id, competencia)
  NULLS NOT DISTINCT WHERE status = 'ABERTA';
```

`valor_total` vira `valor_apresentado` (o nome contábil correto). O acumulador `_acumular()` some: o total passa a ser **recalculado** a partir de `SUM(guias.valor_apresentado)` em `recalcular_totais_remessa()`, e a diferença entre acumulado e soma vira a divergência `TOTAL_REMESSA_DIVERGENTE`.

Particular: guia particular **não entra em remessa** (`remessa_id IS NULL`). Título nasce da guia (§1.7).

### 1.6 Glosa com ciclo de vida

```sql
ALTER TABLE glosas
  ADD COLUMN codigo_glosa              VARCHAR(10),        -- código TISS da operadora
  ADD COLUMN status                    VARCHAR(24) NOT NULL DEFAULT 'ACEITA',
  ADD COLUMN competencia_item          DATE NOT NULL REFERENCES competencias(competencia),
  ADD COLUMN competencia_reconhecimento DATE NOT NULL REFERENCES competencias(competencia),
  ADD COLUMN convenio_id               UUID REFERENCES convenios(id),
  ADD COLUMN registrada_por_usuario_id UUID REFERENCES usuarios(id);
ALTER TABLE glosas
  ADD CONSTRAINT ck_glosa_valor CHECK (valor_glosado > 0),
  ADD CONSTRAINT ck_glosa_status CHECK (status IN
    ('ACEITA','EM_RECURSO','RECUPERADA','RECUPERADA_PARCIAL','IRRECUPERAVEL','REAPRESENTADA'));

CREATE TABLE recursos_glosa (
  id               UUID PRIMARY KEY,
  glosa_id         UUID NOT NULL REFERENCES glosas(id),
  tentativa        SMALLINT NOT NULL DEFAULT 1,
  justificativa    TEXT NOT NULL,
  valor_recorrido  NUMERIC(12,2) NOT NULL CHECK (valor_recorrido > 0),
  protocolo        VARCHAR(40),
  status           VARCHAR(12) NOT NULL DEFAULT 'ABERTO'
                   CHECK (status IN ('ABERTO','ACEITO','NEGADO','PARCIAL')),
  valor_recuperado NUMERIC(12,2) NOT NULL DEFAULT 0,
  aberto_em        TIMESTAMPTZ NOT NULL DEFAULT now(),
  respondido_em    TIMESTAMPTZ,
  usuario_id       UUID REFERENCES usuarios(id),
  UNIQUE (glosa_id, tentativa),
  CHECK (valor_recuperado <= valor_recorrido),
  CHECK (status = 'ABERTO' OR respondido_em IS NOT NULL)
);
```

**Dois remédios distintos, deliberadamente separados:**
- **Recurso**: contesta administrativamente. Aceito → convênio paga sem nova guia. Vive em `recursos_glosa`.
- **Reapresentação**: corrige o erro (TUSS, senha) e reenvia em guia nova. Vive como transição `item_faturavel.status → GLOSADO_A_REAPRESENTAR`.

**Competência dupla (regime de competência vs. caixa):** `competencia_item` é a do fato gerador — é o que entra na taxa de glosa do mês de origem. `competencia_reconhecimento` é a competência aberta em que a glosa chegou — é onde o efeito financeiro é reconhecido. Sem isso, glosa que chega em julho sobre item de março ou (a) trava porque março está fechado, ou (b) contamina a taxa de glosa de julho. Ambos errados.

### 1.7 Título a receber com baixa parcial

```sql
ALTER TABLE titulos_receber RENAME COLUMN lote_faturamento_id TO remessa_id;
ALTER TABLE titulos_receber
  ALTER COLUMN remessa_id DROP NOT NULL,
  ADD COLUMN origem         VARCHAR(20) NOT NULL DEFAULT 'REMESSA',
  ADD COLUMN guia_tiss_id   UUID REFERENCES guias_tiss(id),
  ADD COLUMN convenio_id    UUID REFERENCES convenios(id),
  ADD COLUMN paciente_id    UUID REFERENCES pacientes(id),
  ADD COLUMN competencia    DATE NOT NULL REFERENCES competencias(competencia),
  ADD COLUMN numero_parcela SMALLINT NOT NULL DEFAULT 1,
  ADD COLUMN total_parcelas SMALLINT NOT NULL DEFAULT 1,
  ADD COLUMN valor_glosado  NUMERIC(12,2) NOT NULL DEFAULT 0,
  ADD COLUMN valor_pago     NUMERIC(12,2) NOT NULL DEFAULT 0,
  ADD COLUMN saldo          NUMERIC(12,2) GENERATED ALWAYS AS (valor - valor_glosado - valor_pago) STORED,
  ADD COLUMN emissao        DATE NOT NULL DEFAULT CURRENT_DATE,
  ADD COLUMN data_baixa     DATE,
  ADD COLUMN cancelado_em   TIMESTAMPTZ,
  ADD COLUMN motivo_cancelamento VARCHAR(255);
ALTER TABLE titulos_receber
  ADD CONSTRAINT ck_tr_status CHECK (status IN ('ABERTO','PARCIAL','LIQUIDADO','CANCELADO')),
  ADD CONSTRAINT ck_tr_valores CHECK (valor > 0 AND valor_pago >= 0 AND valor_glosado >= 0
                                      AND valor_glosado <= valor AND valor_pago <= valor - valor_glosado),
  ADD CONSTRAINT ck_tr_origem CHECK (
    (origem = 'REMESSA'         AND remessa_id IS NOT NULL AND convenio_id IS NOT NULL AND paciente_id IS NULL)
 OR (origem = 'GUIA_PARTICULAR' AND guia_tiss_id IS NOT NULL AND paciente_id IS NOT NULL AND convenio_id IS NULL)
 OR (origem = 'AVULSO'          AND remessa_id IS NULL AND guia_tiss_id IS NULL));
CREATE INDEX ix_tr_carteira ON titulos_receber (status, vencimento) WHERE status IN ('ABERTO','PARCIAL');
CREATE INDEX ix_tr_competencia ON titulos_receber (competencia, convenio_id);

CREATE TABLE baixas_titulo_receber (
  id                 UUID PRIMARY KEY,
  titulo_receber_id  UUID NOT NULL REFERENCES titulos_receber(id),
  valor_recebido     NUMERIC(12,2) NOT NULL CHECK (valor_recebido > 0),  -- dinheiro que entrou
  valor_aplicado     NUMERIC(12,2) NOT NULL CHECK (valor_aplicado > 0),  -- parte abatida do título
  recebido_em        DATE NOT NULL,
  forma              VARCHAR(20) NOT NULL
                     CHECK (forma IN ('PIX','TED','BOLETO','DINHEIRO','CARTAO','OUTRO')),
  movimento_caixa_id UUID REFERENCES movimentos_caixa(id),
  observacao         VARCHAR(255),
  usuario_id         UUID REFERENCES usuarios(id),
  estornada_em       TIMESTAMPTZ,
  criado_em          TIMESTAMPTZ NOT NULL DEFAULT now(),
  CHECK (valor_aplicado <= valor_recebido)
);
```

- `valor_pago` = `SUM(baixas.valor_aplicado)`, mantido pelo service. `saldo` é gerado. `status` transiciona `ABERTO → PARCIAL → LIQUIDADO`, com `data_baixa` preenchida só na liquidação. Baixa parcial passa a existir.
- **Pagamento a maior:** `valor_aplicado` é capado no saldo; `valor_recebido` registra o que entrou de fato; o excedente vira divergência `RECEBIMENTO_MAIOR`. É o único jeito de o caixa bater com o extrato e o título não ficar com saldo negativo. (Decisão discutível — ver §6.)
- **`ATRASADO` sai do enum.** Não há job/cron neste stack, então status persistido "atrasado" seria sempre mentira. Vira atributo derivado `em_atraso = vencimento < hoje AND saldo > 0` no `TituloReceberRead` + filtro no repository. `CANCELADO` passa a ser alcançável via `cancelar_titulo()`.
- **Vencimento deixa de ser `hoje + 30` hardcoded:** `ALTER TABLE convenios ADD COLUMN prazo_pagamento_dias INTEGER NOT NULL DEFAULT 30, ADD COLUMN dia_vencimento SMALLINT`. Vencimento = `remessa.fechada_em + convenio.prazo_pagamento_dias` (ou próximo `dia_vencimento`).

### 1.8 Divergências — o pedido explícito do professor

Uma tabela, append-only, com detecção idempotente.

```sql
CREATE TABLE divergencias (
  id             UUID PRIMARY KEY,
  tipo           VARCHAR(32) NOT NULL,
  severidade     VARCHAR(12) NOT NULL CHECK (severidade IN ('BLOQUEIO','ALERTA','INFORMATIVA')),
  entidade       VARCHAR(24) NOT NULL
                 CHECK (entidade IN ('item_faturavel','guia_tiss','guia_item','remessa','titulo_receber','competencia')),
  entidade_id    UUID NOT NULL,
  competencia    DATE REFERENCES competencias(competencia),
  convenio_id    UUID REFERENCES convenios(id),
  unidade_id     UUID REFERENCES unidades(id),
  valor_esperado NUMERIC(14,2),
  valor_apurado  NUMERIC(14,2),
  diferenca      NUMERIC(14,2) GENERATED ALWAYS AS
                 (COALESCE(valor_apurado,0) - COALESCE(valor_esperado,0)) STORED,
  descricao      VARCHAR(255) NOT NULL,
  status         VARCHAR(16) NOT NULL DEFAULT 'ABERTA'
                 CHECK (status IN ('ABERTA','JUSTIFICADA','CORRIGIDA','IGNORADA')),
  detectada_em   TIMESTAMPTZ NOT NULL DEFAULT now(),
  detectada_por  VARCHAR(28) NOT NULL,   -- PRE_AUDITORIA | FECHAMENTO_REMESSA | BAIXA_TITULO | FECHAMENTO_COMPETENCIA | FATO_GERADOR
  resolvida_em   TIMESTAMPTZ,
  resolvida_por_usuario_id UUID REFERENCES usuarios(id),
  justificativa  VARCHAR(255),
  CHECK (status = 'ABERTA' OR resolvida_em IS NOT NULL)
);
-- detector reexecutável sem duplicar
CREATE UNIQUE INDEX uq_divergencia_aberta ON divergencias (tipo, entidade, entidade_id)
  WHERE status = 'ABERTA';
CREATE INDEX ix_div_painel ON divergencias (competencia, severidade, status);
```

**Catálogo de tipos, onde é detectado, e o que faz:**

| Tipo | Onde detecta | Severidade | Efeito |
|---|---|---|---|
| `SEM_PRECO_TABELA` | fato gerador + pré-auditoria | BLOQUEIO (convênio) / ALERTA (particular) | trava fechamento da remessa |
| `VALOR_ACIMA_TABELA` | fato gerador + pré-auditoria | ALERTA (BLOQUEIO se > tolerância) | avisa; exige justificativa p/ fechar |
| `VALOR_ABAIXO_TABELA` | fato gerador + pré-auditoria | ALERTA | perda de receita, só avisa |
| `TOTAL_GUIA_DIVERGENTE` | pré-auditoria | BLOQUEIO | `guia.valor_apresentado ≠ SUM(itens)` |
| `TOTAL_REMESSA_DIVERGENTE` | fechar remessa | BLOQUEIO | `remessa.valor_apresentado ≠ SUM(guias)` |
| `TUSS_INVALIDO` | pré-auditoria | BLOQUEIO | (a validação que já existe, agora registrada) |
| `LAUDO_NAO_LIBERADO` | pré-auditoria | BLOQUEIO | idem |
| `RECEBIMENTO_MENOR` | baixa de título | ALERTA | recebido < (faturado − glosado) |
| `RECEBIMENTO_MAIOR` | baixa de título | ALERTA | excedente não aplicado |
| `GLOSA_EXCEDE_FATURADO` | registrar glosa | BLOQUEIO | acumulado > 100% (também barrado por CHECK) |
| `REMESSA_SEM_RETORNO` | fechamento de competência | INFORMATIVA | ENVIADA há > 45 dias |
| `COMPETENCIA_NAO_FATURADA` | fechamento de competência | ALERTA | há `A_FATURAR` na competência a fechar |
| `LAUDO_SEM_ITEM_FATURAVEL` | fechamento de competência | BLOQUEIO | falha de integração (também valida o backfill) |
| `COMPETENCIA_FECHADA_RETROATIVA` | fato gerador | INFORMATIVA | lançamento caiu em competência posterior |

**Cobertura dos três casos que você pediu:** valor faturado vs tabela → tipos 1–3; soma do lote vs itens → tipos 4–5; recebido vs faturado−glosado → tipos 8–9.

**Apresentação:** nova página `pages/faturamento_divergencias.py` — KPIs (abertas por severidade, valor em risco), filtros competência/convênio/tipo/severidade/status, ações justificar / marcar corrigida / ignorar. Além disso: badge de contagem nas telas de remessa e de contas.

`conciliacoes_pagamento` é exatamente `RECEBIMENTO_MENOR` — some, com os dados migrados.

### 1.9 Preço particular e vigência

```sql
ALTER TABLE procedimento_valores
  ALTER COLUMN convenio_id DROP NOT NULL,          -- NULL = tabela particular / balcão
  ADD COLUMN vigencia_fim DATE,
  ADD CONSTRAINT ck_pv_vigencia CHECK (vigencia_fim IS NULL OR vigencia_fim >= vigencia_inicio),
  ADD CONSTRAINT ck_pv_valor CHECK (valor >= 0),
  DROP CONSTRAINT uq_procedimento_valor_vigencia;

CREATE UNIQUE INDEX uq_pv_vigencia
  ON procedimento_valores (procedimento_id, convenio_id, vigencia_inicio) NULLS NOT DISTINCT;

CREATE EXTENSION IF NOT EXISTS btree_gist;
ALTER TABLE procedimento_valores ADD CONSTRAINT ex_pv_sem_sobreposicao
  EXCLUDE USING gist (
    procedimento_id WITH =,
    COALESCE(convenio_id, '00000000-0000-0000-0000-000000000000'::uuid) WITH =,
    daterange(vigencia_inicio, COALESCE(vigencia_fim, 'infinity'::date), '[]') WITH &&
  );
```

`NULLS NOT DISTINCT` (PG15+) é obrigatório: sem ele o unique não segura preço particular duplicado, porque `NULL <> NULL`. O `EXCLUDE` mata sobreposição de vigências no banco — é a prova de que "existe exatamente um preço vigente por data".

`definir_valor()` passa a **encerrar automaticamente** a vigência anterior (`vigencia_fim = nova.vigencia_inicio - 1 dia`), senão o `EXCLUDE` rejeita.
`obter_valor_vigente(session, procedimento_id, convenio_id: UUID | None, na_data)` usa `convenio_id IS NOT DISTINCT FROM :convenio_id` e filtra `vigencia_fim IS NULL OR vigencia_fim >= na_data`.

### 1.10 Regra do valor pelos procedimentos — três pontos de aplicação

```sql
ALTER TABLE os_itens
  ADD COLUMN valor_tabela  NUMERIC(12,2),
  ADD COLUMN origem_valor  VARCHAR(16) NOT NULL DEFAULT 'TABELA'
             CHECK (origem_valor IN ('TABELA','NEGOCIADO','SEM_TABELA')),
  ADD COLUMN motivo_excecao VARCHAR(255),
  ADD CONSTRAINT ck_os_item_excecao
    CHECK (origem_valor <> 'NEGOCIADO' OR motivo_excecao IS NOT NULL);
```

1. **`abrir_os` (`src/atendimento/ordem_servico/service.py:89-110`)** — a tabela vira a fonte da verdade, inclusive para particular (que agora tem tabela). Se o operador digitar valor divergente: exige a permissão `faturamento:valor_excecao` **e** um motivo; grava `origem_valor='NEGOCIADO'` + `valor_tabela` (o que a tabela dizia). Sem a permissão, o campo é read-only na tela. Isso encerra o "sobrescreve a tabela sem checagem".
2. **Liberação do laudo → item faturável** — recalcula `valor_tabela` **na data do fato gerador** (não na data de hoje) e compara com `valor_previsto`. Divergiu → registra `VALOR_ACIMA/ABAIXO_TABELA` já na origem, meses antes de alguém tentar faturar.
3. **Pré-auditoria da guia / fechamento da remessa** — revalida contra a tabela vigente na competência.

**Resposta a "bloqueia, avisa ou registra?": registra sempre; bloqueia só severidade BLOQUEIO; avisa em ALERTA.** BLOQUEIO = ausência de preço em tabela para convênio, soma inconsistente, TUSS inválido, laudo não liberado, glosa > faturado. ALERTA = valor fora da tabela acima da tolerância (`TOLERANCIA_VALOR_PCT = Decimal("0.00")` por padrão, configurável). ALERTA pode ser fechado com justificativa por quem tem `faturamento:justificar_divergencia`.

A UI de `pages/faturamento_guias.py:172` deixa de ser `number_input` livre: passa a exibir o valor de tabela, com edição só sob permissão.

### 1.11 Caixa, contas e a pagar

```sql
CREATE TABLE contas_bancarias (
  id UUID PRIMARY KEY, nome VARCHAR(80) NOT NULL, banco VARCHAR(60),
  agencia VARCHAR(10), conta VARCHAR(20),
  saldo_inicial NUMERIC(14,2) NOT NULL DEFAULT 0,
  ativo BOOLEAN NOT NULL DEFAULT true, criado_em TIMESTAMPTZ NOT NULL DEFAULT now()
);

ALTER TABLE movimentos_caixa
  ADD COLUMN conta_bancaria_id UUID NOT NULL REFERENCES contas_bancarias(id),
  ADD COLUMN categoria    VARCHAR(28) NOT NULL DEFAULT 'OUTROS',
  ADD COLUMN unidade_id   UUID REFERENCES unidades(id),
  ADD COLUMN competencia  DATE NOT NULL REFERENCES competencias(competencia),
  ADD COLUMN baixa_receber_id UUID REFERENCES baixas_titulo_receber(id),
  ADD COLUMN baixa_pagar_id   UUID REFERENCES baixas_titulo_pagar(id),
  ADD COLUMN estornado_em TIMESTAMPTZ,
  ADD COLUMN estorno_de_movimento_id UUID REFERENCES movimentos_caixa(id);
ALTER TABLE movimentos_caixa
  ADD CONSTRAINT ck_mc_um_vinculo CHECK (num_nonnulls(titulo_receber_id, titulo_pagar_id) <= 1),
  ADD CONSTRAINT ck_mc_tipo_coerente CHECK (
    (tipo = 'ENTRADA' AND titulo_pagar_id IS NULL) OR (tipo = 'SAIDA' AND titulo_receber_id IS NULL)),
  ADD CONSTRAINT ck_mc_valor CHECK (valor > 0);
CREATE INDEX ix_mc_extrato ON movimentos_caixa (conta_bancaria_id, ocorrido_em);
CREATE INDEX ix_mc_competencia ON movimentos_caixa (competencia, categoria);

ALTER TABLE titulos_pagar
  ADD COLUMN descricao     VARCHAR(140) NOT NULL DEFAULT '',
  ADD COLUMN fornecedor_id UUID REFERENCES fornecedores(id),
  ADD COLUMN categoria     VARCHAR(28) NOT NULL DEFAULT 'OUTROS',
  ADD COLUMN competencia   DATE NOT NULL REFERENCES competencias(competencia),
  ADD COLUMN valor_pago    NUMERIC(12,2) NOT NULL DEFAULT 0,
  ADD COLUMN saldo         NUMERIC(12,2) GENERATED ALWAYS AS (valor - valor_pago) STORED,
  ADD COLUMN data_baixa    DATE;
-- + baixas_titulo_pagar, espelho de baixas_titulo_receber
```

`CHECK (num_nonnulls(...) <= 1)` e não `= 1`: lançamento avulso de caixa (sem título) é legítimo. O par de CHECKs resolve o buraco que você apontou.

`categoria` (`RECEITA_CONVENIO`, `RECEITA_PARTICULAR`, `DESPESA_FIXA`, `DESPESA_INSUMO`, `IMPOSTO`, `FOLHA`, `OUTROS`) em vez de plano de contas + centro de custo completo. Centro de custo fica fora de escopo (§6).

### 1.12 Grafo resultante

```
competencias (DATE PK, ABERTA|FECHADA)
    │ (todo lançamento aponta pra cá)
    ├──────────────┬──────────────┬──────────────┬──────────────┐
    ▼              ▼              ▼              ▼              ▼
itens_faturaveis  guias_tiss  remessas_fat.  titulos_receber  movimentos_caixa
    │ 1:1 laudo       │ 1:1 OS       │              │
    │                 │              │              ├─ N baixas_titulo_receber ─→ movimentos_caixa
    └──1:N──→ guias_itens ──N:1──────┘              │
                  │  (partial unique: 1 vigente/item)│
                  ├──1:N──→ glosas ──1:N──→ recursos_glosa
                  │            └─ abate ─────────────┘
                  │
             divergencias (polimórfica: entidade + entidade_id)
```

---

## 2. Migrations — 9 revisões lineares a partir de `0013_bi_paciente_hash`

**Regra do repositório a partir daqui:** `revision` string **igual** ao prefixo do arquivo, `down_revision` explícito, e **escritas à mão** (`alembic revision -m`, sem `--autogenerate`). Motivo crítico: o autogenerate **nunca detecta rename** — ele emite `drop_table` + `create_table`, o que destruiria os 73 lotes. O alvo `make revision` do Makefile usa `--autogenerate`; documentar no README que ele não serve para esta remodelagem.

| # | Arquivo | Conteúdo | Backfill |
|---|---|---|---|
| 0014 | `0014_precos_e_condicoes_comerciais.py` | `procedimento_valores` nullable + `vigencia_fim` + `NULLS NOT DISTINCT` + `btree_gist`/EXCLUDE; `convenios.prazo_pagamento_dias`/`dia_vencimento`; `os_itens.valor_tabela`/`origem_valor`/`motivo_excecao` | encadear `vigencia_fim` das vigências existentes; `os_itens.valor_tabela` via lookup na data da OS |
| 0015 | `0015_competencias.py` | tabela `competencias` | gerar série mensal contínua de min→max de `laudos.liberado_em`, todas FECHADA, mês corrente ABERTA |
| 0016 | `0016_itens_faturaveis.py` | tabela + índices | um item por laudo LIBERADO, competência via `AT TIME ZONE`, status derivado da existência de `guias_itens.laudo_id` |
| 0017 | `0017_remessa.py` | rename tabela+coluna, novas colunas, `seq_remessa`, unique parcial | `competencia` da remessa = competência mínima dos seus itens; `valor_apresentado` = `valor_total` |
| 0018 | `0018_guia_por_paciente.py` | colunas da guia, `seq_guia_prestador`, `guias_itens.item_faturavel_id`, drop `laudo_id` + seu UNIQUE, uniques parciais | **explosão das guias degeneradas** (detalhe abaixo) |
| 0019 | `0019_glosa_ciclo_de_vida.py` | colunas de `glosas`, tabela `recursos_glosa` | `status='ACEITA'`; `competencia_item` = do item; `competencia_reconhecimento` = competência de `criado_em`; recalcular `guias_itens.valor_glosado` = `SUM(glosas)` |
| 0020 | `0020_divergencias.py` | tabela + uniques | migrar `conciliacoes_pagamento` → `divergencias(RECEBIMENTO_MENOR)`; **drop `conciliacoes_pagamento`** |
| 0021 | `0021_titulo_receber_baixa_parcial.py` | rename FK, colunas, CHECKs, `baixas_titulo_receber` | reconstruir `valor_pago`/`status`/`data_baixa` a partir de `movimentos_caixa`; criar uma baixa por movimento de ENTRADA |
| 0022 | `0022_caixa_contas_e_pagar.py` | `contas_bancarias`, colunas de `movimentos_caixa` e `titulos_pagar`, `baixas_titulo_pagar` | criar conta "Conta Corrente Principal"; vincular todos os movimentos; categoria por heurística (tem `titulo_receber_id`→receita, `pedido_compra_id`→insumo, resto→fixa) |

### Ordenação obrigatória

**0018 depende de `guias_itens.laudo_id` ainda existir** para fazer o join `guias_itens → laudos → itens_faturaveis`. Por isso o drop da coluna é a *última* operação de 0018, depois da explosão e do preenchimento de `item_faturavel_id`. Inverter isso quebra a migration.

### A explosão das guias (0018) — o backfill não trivial

```sql
-- 1. vincular guias_itens ao item faturável (usa laudo_id, que ainda existe)
UPDATE guias_itens gi SET item_faturavel_id = f.id
FROM itens_faturaveis f WHERE f.laudo_id = gi.laudo_id;
-- se sobrar NULL aqui, o backfill de 0016 falhou → deixar NOT NULL falhar de propósito

-- 2. criar uma guia nova por (remessa, OS)
CREATE TEMP TABLE _mapa AS
SELECT DISTINCT g.lote_faturamento_id AS remessa_id, f.ordem_servico_id, f.paciente_id,
       f.convenio_id, f.competencia, gen_random_uuid() AS nova_guia_id
FROM guias_itens gi
JOIN guias_tiss g ON g.id = gi.guia_tiss_id
JOIN itens_faturaveis f ON f.id = gi.item_faturavel_id;

INSERT INTO guias_tiss (id, remessa_id, ordem_servico_id, paciente_id, convenio_id, competencia,
                        numero_guia_prestador, data_atendimento, codigo_tiss,
                        status, status_pre_auditoria, criado_em)
SELECT m.nova_guia_id, m.remessa_id, m.ordem_servico_id, m.paciente_id, m.convenio_id, m.competencia,
       'GP-' || lpad(nextval('seq_guia_prestador')::text, 8, '0'),
       os.aberta_em::date, 'TISS-MIGRADA',
       CASE WHEN r.status = 'ABERTA' THEN 'ABERTA' ELSE 'ENVIADA' END, 'APROVADA', r.criado_em
FROM _mapa m
JOIN ordens_servico os ON os.id = m.ordem_servico_id
JOIN remessas_faturamento r ON r.id = m.remessa_id;

-- 3. reapontar os itens
UPDATE guias_itens gi SET guia_tiss_id = m.nova_guia_id
FROM itens_faturaveis f, guias_tiss g, _mapa m
WHERE f.id = gi.item_faturavel_id AND g.id = gi.guia_tiss_id
  AND m.remessa_id = g.remessa_id AND m.ordem_servico_id = f.ordem_servico_id;

-- 4. apagar as guias degeneradas (agora órfãs)
DELETE FROM guias_tiss WHERE codigo_tiss <> 'TISS-MIGRADA'
  AND id NOT IN (SELECT guia_tiss_id FROM guias_itens);

-- 5. recalcular totais
UPDATE guias_tiss g SET valor_apresentado = s.total
FROM (SELECT guia_tiss_id, SUM(valor_faturado) total FROM guias_itens GROUP BY 1) s
WHERE s.guia_tiss_id = g.id;
UPDATE remessas_faturamento r SET valor_apresentado = s.total, qtd_guias = s.qtd
FROM (SELECT remessa_id, SUM(valor_apresentado) total, COUNT(*) qtd FROM guias_tiss
      WHERE remessa_id IS NOT NULL GROUP BY 1) s
WHERE s.remessa_id = r.id;
```

### Backfill de competência (0015)

```sql
INSERT INTO competencias (competencia, status, criada_em)
SELECT gs::date, 'FECHADA', now()
FROM generate_series(
  (SELECT date_trunc('month', MIN(liberado_em) AT TIME ZONE 'America/Recife') FROM laudos WHERE liberado_em IS NOT NULL),
  date_trunc('month', CURRENT_DATE),
  interval '1 month') gs
ON CONFLICT DO NOTHING;

UPDATE competencias SET status='ABERTA', fechada_em=NULL
WHERE competencia = date_trunc('month', CURRENT_DATE)::date;

UPDATE competencias SET fechada_em = (competencia + interval '1 month')
WHERE status='FECHADA' AND fechada_em IS NULL;
```

`generate_series` garante que não haja buraco de mês, mesmo que um mês não tenha tido laudo. Sem isso, uma FK falha na primeira competência vazia.

### Regras de segurança dos backfills

- **CHECKs entram no fim da migration**, depois do backfill. Se um dado histórico violar (ex.: `valor_pago > valor`), a migration **falha ruidosamente** em vez de o CHECK ser criado sobre dado inconsistente.
- Colunas novas `NOT NULL` entram em três passos: `ADD COLUMN` nullable → `UPDATE` de backfill → `ALTER ... SET NOT NULL`. Se sobrar NULL, o `SET NOT NULL` falha — é o teste de completude do backfill embutido na própria migration.
- `downgrade()` de cada migration: escrever de verdade para o rename e as colunas; para as tabelas novas, `drop_table`. Onde a reversão for lossy (explosão de guias, drop de `conciliacoes_pagamento`), documentar no docstring — o precedente já existe em `0013`.

---

## 3. Camada de serviço

### 3.1 Reorganização de pacotes

```
src/faturamento/
  competencia/     {models,dtos,repository,service,errors}.py    [novo]
  item_faturavel/  {models,dtos,repository,service,errors}.py    [novo]
  guia/            {models,dtos,repository,service,errors}.py    [novo — GuiaTiss, GuiaItem]
  remessa/         {models,dtos,repository,service,errors}.py    [ex-lote_faturamento — Remessa]
  glosa/           {models,dtos,repository,service,errors}.py    [+ RecursoGlosa]
  divergencia/     {models,dtos,repository,service,errors}.py    [novo]
src/financeiro/
  conta_bancaria/  {models,dtos,repository,service}.py           [novo]
  titulo_receber/  [+ baixa]
  conciliacao_pagamento/                                          [DELETADO]
```

`src/faturamento/lote_faturamento/` deixa de existir.

### 3.2 Assinaturas centrais

```python
# src/faturamento/competencia/service.py
def competencia_de(instante: datetime) -> date
def obter_ou_criar(session, competencia: date) -> CompetenciaRead
def competencia_de_lancamento(session, fato_gerador_em: datetime) -> tuple[date, date | None]
def apurar(session, competencia: date) -> ApuracaoCompetencia
def fechar(session, competencia: date, usuario_id: UUID, justificativa: str | None = None) -> CompetenciaRead
def reabrir(session, competencia: date, usuario_id: UUID, justificativa: str) -> CompetenciaRead
def exigir_aberta(session, competencia: date) -> None          # guard usado por todo lançamento

# src/faturamento/item_faturavel/service.py
def gerar_item_faturavel(session, laudo_id: UUID) -> ItemFaturavelRead    # SEM commit
def listar_a_faturar(session, competencia=None, convenio_id=None, unidade_id=None) -> list[...]
def contar_a_faturar(session, competencia=None, convenio_id=None) -> int
def liberar_para_reapresentacao(session, item_id, usuario_id) -> ItemFaturavelRead
def baixar_como_perda(session, item_id, usuario_id, motivo) -> ItemFaturavelRead
def cancelar_item_faturavel(session, item_id, motivo, usuario_id) -> ItemFaturavelRead

# src/faturamento/guia/service.py
def obter_ou_criar_guia_aberta(session, ordem_servico_id: UUID, competencia: date) -> GuiaTiss  # SEM commit
def adicionar_itens(session, itens_faturaveis_ids: list[UUID], usuario_id) -> list[GuiaTissRead]
def remover_item(session, guia_item_id, usuario_id) -> GuiaTissRead
def pre_auditar_guia(session, guia_id) -> ResultadoPreAuditoria    # {ok, bloqueios, alertas}
def recalcular_totais(session, guia) -> None                       # SEM commit
def gerar_xml_tiss(session, guia_id) -> str
def registrar_retorno(session, guia_id, numero_guia_operadora, usuario_id) -> GuiaTissRead

# src/faturamento/remessa/service.py
def abrir_remessa(session, convenio_id: UUID | None, competencia: date, usuario_id) -> RemessaRead
def montar_remessa_automatica(session, convenio_id, competencia, usuario_id) -> RemessaRead
def incluir_guias(session, remessa_id, guia_ids, usuario_id) -> RemessaRead
def pre_auditar_remessa(session, remessa_id) -> ResultadoPreAuditoria
def fechar_remessa(session, remessa_id, usuario_id) -> RemessaRead
def enviar_remessa(session, remessa_id, usuario_id) -> RemessaRead
def registrar_retorno_remessa(session, remessa_id, protocolo, usuario_id) -> RemessaRead

# src/faturamento/glosa/service.py
def registrar_glosa(session, dto: GlosaCreate, usuario_id) -> GlosaRead      # valida ACUMULADO
def abrir_recurso(session, dto: RecursoGlosaCreate, usuario_id) -> RecursoGlosaRead
def responder_recurso(session, recurso_id, aceito, valor_recuperado, protocolo, usuario_id)
def reapresentar_item(session, guia_item_id, usuario_id) -> ItemFaturavelRead
def resumo_glosas(session, competencia=None, convenio_id=None) -> ResumoGlosas

# src/faturamento/divergencia/service.py
def registrar(session, dto: DivergenciaCreate) -> DivergenciaRead    # idempotente (unique parcial)
def detectar_no_item(session, item_faturavel_id) -> list[DivergenciaRead]
def detectar_na_guia(session, guia_id) -> list[DivergenciaRead]
def detectar_na_remessa(session, remessa_id) -> list[DivergenciaRead]
def detectar_no_recebimento(session, titulo_id, valor_recebido, valor_aplicado) -> list[...]
def detectar_na_competencia(session, competencia) -> list[DivergenciaRead]
def ha_bloqueio_aberto(session, entidade: str, entidade_id: UUID) -> bool
def justificar(session, divergencia_id, justificativa, usuario_id) -> DivergenciaRead

# src/financeiro/titulo_receber/service.py
def gerar_titulo_de_remessa(session, remessa) -> TituloReceber        # SEM commit
def gerar_titulo_particular(session, guia) -> TituloReceber           # SEM commit
def criar_titulo_avulso(session, dto, usuario_id) -> TituloReceberRead
def baixar_titulo(session, titulo_id, dto: BaixaReceberCreate, usuario_id) -> TituloReceberRead
def estornar_baixa(session, baixa_id, motivo, usuario_id) -> TituloReceberRead
def abater_glosa(session, titulo_id, valor, glosa_id, usuario_id) -> TituloReceberRead
def cancelar_titulo(session, titulo_id, motivo, usuario_id) -> TituloReceberRead
def posicao_carteira(session, competencia=None) -> PosicaoCarteira

# src/financeiro/titulo_pagar/service.py
def criar_despesa_avulsa(session, dto: DespesaAvulsaCreate, usuario_id) -> TituloPagarRead   # o que faltava
def baixar_titulo(session, titulo_id, dto: BaixaPagarCreate, usuario_id) -> TituloPagarRead  # parcial

# src/financeiro/movimento_caixa/service.py
def registrar_movimento(session, dto: MovimentoCaixaCreate) -> MovimentoCaixa   # único ponto de escrita
def fluxo_caixa_por_periodo(session, inicio, fim, conta_id=None) -> FluxoCaixa   # regime de CAIXA
def fluxo_por_competencia(session, competencia) -> FluxoCaixa                    # regime de COMPETÊNCIA
def saldo_conta(session, conta_id, ate: date | None = None) -> Decimal
```

### 3.3 Onde entra o fechamento de competência

`fechar(session, competencia, usuario_id)`:
1. exige status ABERTA e permissão `financeiro:fechar_competencia`;
2. exige que todas as competências anteriores estejam FECHADAS (não se fecha março com fevereiro aberto);
3. roda `divergencia.detectar_na_competencia()`;
4. se houver divergência **BLOQUEIO** aberta → `CompetenciaComBloqueio`, listando as pendências;
5. congela a apuração nas colunas de totais;
6. `status='FECHADA'`, `fechada_em`, `fechada_por_usuario_id`;
7. `registrar_auditoria(acao="FECHAR_COMPETENCIA")`.

Efeito: `exigir_aberta()` passa a barrar criação de item faturável, guia, remessa e título naquela competência. Glosa e baixa de título **não** são barradas (chegam meses depois) — entram pela competência de reconhecimento.

### 3.4 Fluxo alvo ponta a ponta

```
LaboratorialService.atualizar_laudo(status=LIBERADO)      src/laboratorial/service.py:240
  └→ item_faturavel.gerar_item_faturavel(laudo.id)        [mesma transação, sem commit]
       ├─ competencia_de_lancamento(laudo.liberado_em)
       ├─ valor_tabela = obter_valor_vigente(proc, convenio, fato_gerador_em.date())
       └─ divergencia.detectar_no_item()                  SEM_PRECO / VALOR_ACIMA / VALOR_ABAIXO

Faturista (pages/faturamento_guias.py)
  └→ item_faturavel.listar_a_faturar(competencia, convenio)
  └→ guia.adicionar_itens([...])          agrupa por OS → 1 guia = 1 paciente = 1 atendimento
  └→ remessa.abrir_remessa(convenio, competencia)  /  montar_remessa_automatica()
  └→ remessa.incluir_guias([...])
  └→ remessa.pre_auditar_remessa()        consulta a TABELA DE PREÇOS (o que validar_lote nunca fez)
  └→ remessa.fechar_remessa()
       ├─ itens_faturaveis → FATURADO ; os_itens → FATURADO  (StatusOsItem.FATURADO passa a existir)
       ├─ guias → EM_REMESSA
       └─ titulo_receber.gerar_titulo_de_remessa()  venc = fechada_em + convenio.prazo_pagamento_dias
  └→ remessa.enviar_remessa()             gera xml_tiss (StatusGuiaTiss deixa de ser enum morto)

Retorno do convênio
  └→ remessa.registrar_retorno_remessa(protocolo)
  └→ glosa.registrar_glosa(guia_item, valor, motivo, codigo)
       ├─ guia_item.valor_glosado += valor      CHECK <= valor_faturado
       ├─ titulo_receber.abater_glosa()
       └─ integral → guia_item = GLOSADO_TOTAL → sai do unique parcial
  └→ glosa.abrir_recurso() → responder_recurso()
  └→ glosa.reapresentar_item() → item volta para A_FATURAR na lista de pendentes

Financeiro (pages/financeiro_contas.py)
  └→ titulo_receber.baixar_titulo(valor, forma, data)     PARCIAL
       ├─ baixas_titulo_receber (linha) + movimento_caixa (conta, categoria, competência)
       ├─ valor_pago += aplicado ; status ABERTO→PARCIAL→LIQUIDADO
       └─ divergencia.detectar_no_recebimento()

Fim do mês (pages/faturamento_competencia.py)
  └→ competencia.apurar()  → espelho do período
  └→ competencia.fechar()  → bloqueado se houver divergência BLOQUEIO
```

---

## 4. Impacto colateral

### `src/db.py` — pré-requisito (Fase 0)
`session_scope()` (linhas 18-24) não faz rollback: uma exceção no meio de um service que já deu flush deixa a transação suja até o `close()`. Com 9 migrations e services novos escrevendo em 6 tabelas por operação, isso vira bug intermitente. Adicionar `except: session.rollback(); raise` e `create_engine(..., pool_pre_ping=True, pool_recycle=1800)`. **Não** adicionar auto-commit: os services já commitam.

### Seeder
| Arquivo | O que muda |
|---|---|
| `src/seeder/cadastros.py` | `_seed_valores` gera tabela **particular** (`convenio_id=None`) e **duas vigências** por procedimento (para exercitar `vigencia_fim` e o EXCLUDE) |
| `src/seeder/laboratorial.py` | nada no código — mas passa a criar item faturável via hook; retrodatação de `liberado_em` já existente faz a competência sair correta de graça |
| `src/seeder/faturamento.py` | **reescrita**. Novo roteiro: competências → agrupar itens por (competência, convênio) → guias por OS → remessa por (convênio, competência) → fechar → enviar → retorno → glosas → recursos → reapresentações. `_retrodatar_lote` vira `_retrodatar_remessa` e precisa alcançar remessa, guias, itens, glosas, título e baixas |
| `src/seeder/financeiro.py` | conta bancária; baixas **parciais** (parte dos títulos com 2 baixas); `criar_despesa_avulsa()` no lugar do `session.add(TituloPagar(...))` direto; categorias; competência em todo movimento |
| `src/seeder/catalogo.py` | `+CODIGOS_GLOSA` (TISS), `+MOTIVOS_RECURSO`, `+CATEGORIAS_DESPESA` |
| `src/seeder/rbac.py` | 8 permissões novas. **Armadilha**: `_seed_perfis` faz early-return se já houver permissões → base existente nunca recebe as novas. Tornar idempotente por linha (upsert por `codigo`) |
| `src/seeder/__main__.py` | nenhuma ordem nova necessária (competência é criada sob demanda), mas o faturamento fecha as competências não-correntes no fim |
| `src/compras/pedido_compra/service.py:98` | `TituloPagar` precisa de `competencia`, `categoria='DESPESA_INSUMO'`, `descricao`, `fornecedor_id` |

### Páginas
| Arquivo | O que muda |
|---|---|
| `pages/faturamento_guias.py` | reescrita: seletor de competência global; abas *A Faturar* (itens agrupados por paciente/OS) / *Guias* / *Remessas*; valor read-only sem `faturamento:valor_excecao`; paginação (900 itens não cabem num loop de `st.columns`) |
| `pages/faturamento_glosas.py` | `INNER JOIN Convenio` → `LEFT JOIN` (linhas 49 e 91 do repository) para particular voltar a aparecer; abas *Registrar* / *Glosas* / *Recursos* / *Reapresentação*; filtro por competência |
| `pages/faturamento_divergencias.py` | **nova** |
| `pages/faturamento_competencia.py` | **nova** (apuração + fechar/reabrir) |
| `pages/financeiro_contas.py` | baixa parcial com saldo e histórico; aba *Conciliações* → *Divergências*; filtro por competência; botão "Nova despesa avulsa"; `_conv_label` usa `titulo.convenio_id` direto (some o dicionário de lotes) |
| `pages/financeiro_caixa.py` | filtro por conta bancária e categoria; alternância *regime de caixa* × *regime de competência* |
| `pages/cadastro_procedimentos.py` | opção "Particular" no seletor de convênio; campo vigência fim; grade da tabela vigente |
| `pages/atendimento_os.py` | exibir valor de tabela; campo bloqueado sem permissão de exceção; motivo obrigatório |
| `src/ui.py` `_MENU` | 2 entradas novas em Faturamento |
| `pages/bi_financeiro.py` | série temporal por **competência**, não por vencimento |

### BI
- `src/bi/models.py`: `FatoFaturamento` ganha `valor_liberado`, `valor_recebido`, `qtd_guias`, `sk_paciente`. `FatoFinanceiro` ganha `sk_convenio` real (hoje é sempre `None`) e separação previsto × realizado.
- `src/bi/etl.py`:
  - `_carga_fatos` linha 169-183: `GuiaItem` não tem mais `laudo_id`; unidade/convênio/competência vêm de `itens_faturaveis` (join direto, sem os 5 joins atuais). `sk_tempo` passa a ser o da **competência**, não `lote.fechado_em`.
  - linha 181: `su_consolidado` é sempre a unidade fake `0000...` — agora existe `itens_faturaveis.unidade_id`, então o fato de faturamento passa a ter unidade real. Isso conserta um indicador que hoje é inútil.
  - linhas 185-192: `TituloReceber` usa `valor_pago` (realizado) e `valor` (previsto), com `sk_convenio` preenchido.
  - `bi_dim_tempo` já tem `ano`/`mes` — nenhuma dimensão nova é necessária para competência.

### Testes
- **conftests** (`tests/faturamento/conftest.py`, `tests/financeiro/conftest.py`): adicionar às tuplas `_TABELAS` — `divergencias`, `recursos_glosa`, `baixas_titulo_receber`, `baixas_titulo_pagar`, `guias_itens`, `itens_faturaveis`, `contas_bancarias`, `competencias`; renomear `lotes_faturamento` → `remessas_faturamento`; **remover** `conciliacoes_pagamento`. `TRUNCATE ... CASCADE` já cobre a ordem, mas listar explicitamente evita surpresa. As duas listas são quase idênticas — vale extrair para `tests/_tabelas.py`.
- `tests/faturamento/_helpers.py`: `montar_base` cria competência; `criar_laudo_liberado` passa a gerar `ItemFaturavel` (ou o helper chama `gerar_item_faturavel` explicitamente, já que ele não passa por `atualizar_laudo`).
- `tests/financeiro/_helpers.py`: `Base.lote_id` → `remessa_id`; `criar_lote` → `abrir_remessa` com competência.
- Reescritos: `test_faturamento_service.py` (6), `test_glosa_service.py` (3), `test_financeiro_service.py` (10). Atenção a `test_baixar_titulo_receber_recarregado_do_banco` — o título passa a ficar **PARCIAL**, não `PAGO`, e a divergência vem de `divergencias`, não de `conciliacoes_pagamento`.
- Também afetados: `tests/atendimento/test_ordem_servico.py` (cancelamento depende de `item_faturado`), `tests/bi/test_etl.py`, `tests/atendimento/test_seeder_atendimento.py`.
- Novos: `tests/faturamento/test_competencia.py`, `test_item_faturavel.py`, `test_divergencia.py`, `test_remessa_guia.py`, `tests/financeiro/test_baixa_parcial.py`, `tests/cadastro/test_preco_vigencia.py`.

### RBAC — 8 permissões novas
`faturamento:visualizar_divergencias`, `faturamento:justificar_divergencia`, `faturamento:valor_excecao`, `faturamento:recorrer_glosa`, `faturamento:reapresentar`, `financeiro:fechar_competencia`, `financeiro:reabrir_competencia`, `financeiro:lancar_despesa`. Atualizar `_PERMISSOES`, `_ADMIN` e os perfis `faturista` / `financeiro` em `src/seeder/rbac.py`, **e** tornar o seed idempotente por linha.

---

## 5. Ordem de execução

Critério de saída de **toda** fase: `alembic upgrade head` OK · `make seeder` OK em base limpa · `make test` verde · queries de reconciliação batendo.

### Fase 0 — Fundação (sem migration)
- `src/db.py`: rollback + `pool_pre_ping`.
- `glosa/repository.py:49,91`: `INNER JOIN Convenio` → `LEFT JOIN` (particular volta às telas).
- `glosa/service.py:32`: passa a somar as glosas anteriores antes de comparar.
- `lote_faturamento/repository.py:102`: remove o `50.0`, levanta erro explícito.
- Extrair `tests/_tabelas.py`.
- *Verificação*: 3 testes de regressão novos + os 26 existentes verdes.

### Fase 1 — Preço e regra do valor (0014)
Preço particular, `vigencia_fim`, EXCLUDE, `prazo_pagamento_dias`, `os_itens.valor_tabela`, `definir_valor` encerrando vigência, `abrir_os` aplicando a regra, tela de procedimentos com "Particular", seeder de cadastros com tabela particular.
*Verificação*: `SELECT COUNT(*) FROM procedimento_valores WHERE convenio_id IS NULL > 0`; nenhuma sobreposição de vigência (o EXCLUDE prova).

### Fase 2 — Competência (0015)
Tabela, backfill, service, `pages/faturamento_competencia.py` **só com apuração** (fechamento ainda não bloqueia nada), menu, permissões.
*Verificação*: `SELECT COUNT(DISTINCT date_trunc('month', liberado_em AT TIME ZONE 'America/Recife')) FROM laudos` = número de competências com laudo.

### Fase 3 — Item faturável (0016)
Tabela, backfill, hook em `LaboratorialService.atualizar_laudo`, `listar_a_faturar` substituindo `listar_laudos_liberados_por_convenio`, `item_faturado` do OS passando a consultar `itens_faturaveis`, `StatusOsItem.FATURADO` finalmente atribuído. A tela de faturamento passa a listar itens faturáveis (ainda dentro do modelo de lote antigo).
*Verificação*: `COUNT(itens_faturaveis) = COUNT(laudos WHERE status='LIBERADO')`; nenhum `guias_itens` órfão.

### Fase 4 — Remessa (0017)
Rename, colunas, sequence, unique parcial. Pacote `lote_faturamento` → `remessa`. Páginas/BI/seeder/testes ajustados ao novo nome.
*Verificação*: `remessa.valor_apresentado = SUM(guias_itens.valor_faturado)` em todas as remessas.

### Fase 5 — Guia por paciente (0018) — **a entrega para o professor**
Explosão das guias, `item_faturavel_id`, drop de `laudo_id`, uniques parciais, pacote `guia`, reescrita de `pages/faturamento_guias.py`.
*Verificação*: `SELECT COUNT(*) FROM (SELECT guia_tiss_id FROM guias_itens gi JOIN itens_faturaveis f ON f.id=gi.item_faturavel_id GROUP BY 1 HAVING COUNT(DISTINCT f.paciente_id) > 1) x` = **0**. Nenhuma guia com mais de um paciente.

### Fase 6 — Glosa com ciclo de vida (0019)
Status, `recursos_glosa`, reapresentação, abatimento no título, `pages/faturamento_glosas.py` com 4 abas.
*Verificação*: item 100% glosado + reapresentação volta para `listar_a_faturar`; `SUM(glosas) = guias_itens.valor_glosado` para todo item.

### Fase 7 — Divergências (0020) — **o outro pedido explícito**
Tabela, 5 detectores, pré-auditoria consultando a tabela de preços, `pages/faturamento_divergencias.py`, migração e drop de `conciliacoes_pagamento`.
*Verificação*: fechar remessa com procedimento sem preço em tabela é bloqueado e a divergência aparece no painel; rodar o detector 2× não duplica linha.

### Fase 8 — Título e baixa parcial (0021)
Colunas, `baixas_titulo_receber`, baixa parcial no service e na tela, `ATRASADO` derivado, `CANCELADO` alcançável.
*Verificação*: receber R$1 de um título de R$1000 deixa o título **PARCIAL** com saldo 999 (hoje marca PAGO e gera conciliação de 999).

### Fase 9 — Caixa, contas e a pagar (0022) + fechamento com bloqueio + BI
`contas_bancarias`, categorias, CHECKs do caixa, `criar_despesa_avulsa`, baixa parcial a pagar; fechamento de competência passa a **bloquear**; `src/bi/{models,etl}.py`; seeder final; ADRs.
*Verificação*: `saldo_conta()` = `saldo_inicial + SUM(entradas) − SUM(saídas)`; `apurar(competência)` bate com o BI.

**Corte se o prazo apertar:** Fases 6 (recursos de glosa — manter só `status` + reapresentação) e 9 (contas bancárias/categorias) são as únicas dispensáveis. Fases 5 e 7 são exatamente o que o professor pediu e não podem cair.

---

## 6. Riscos e decisões que precisam de martelo

**Bloqueadores de decisão (a equipe precisa fechar antes de codar):**

1. **Fuso da competência.** `America/Recife` ou UTC? Muda a competência de todo laudo liberado entre 21h e 24h local. Uma vez escolhido, é imutável — reprocessar competência depois é caríssimo. Merece ADR.
2. **Pagamento a maior.** Capar `valor_pago` no saldo e registrar o excedente como divergência (minha proposta), ou permitir `saldo` negativo? Capar mantém o CHECK e força alguém a olhar; saldo negativo é mais simples mas volta a esconder o problema.
3. **Grão da guia = OS.** Alguns convênios aceitam guia mensal por beneficiário (várias OS numa guia). Escolhi 1 OS = 1 guia por ser o SP/SADT canônico. Se o professor esperar guia mensal, muda o índice parcial e o agrupamento — não muda o resto.
4. **Título particular por guia.** Particular paga no balcão, então o título nasce da guia, não de remessa. Alternativa: fatura mensal por paciente. Afeta o `ck_tr_origem`.
5. **Drop de `guias_itens.laudo_id`.** Limpa o MER e força tudo por `itens_faturaveis`, mas quebra 4 call sites (`glosa/repository.py`, `glosa/service.py`, `ordem_servico/repository.py:96`, `lote_faturamento/repository.py`). Manter a coluna denormalizada é mais barato e mais sujo.

**Riscos técnicos:**

6. **Alembic + rename.** `make revision` usa `--autogenerate`, que emite `drop_table` + `create_table` no lugar de `rename_table`. Se alguém rodar autogenerate depois de 0017, perde os 73 lotes. Documentar no README e no Makefile.
7. **`btree_gist` no deploy.** O `EXCLUDE` exige a extensão. No container Docker o usuário é superuser, sem problema; num Postgres gerenciado pode faltar permissão. Testar no ambiente de `DEPLOY.md` antes da Fase 1, com plano B (validar sobreposição só no service).
8. **Colunas geradas (`saldo`, `valor_liberado`, `diferenca`).** Exigem `sa.Computed(...)` no SQLAlchemy e não podem ser escritas. Se der atrito com Pydantic/`model_validate`, degradar para coluna comum mantida pelo service. Risco baixo, mas descobrir na Fase 8 seria caro — validar com um spike na Fase 2.
9. **`NULLS NOT DISTINCT`** é PG15+. O stack é PG16, OK — mas quebra qualquer tentativa de rodar em SQLite/PG14. Registrar como dependência.
10. **Base de demonstração não é comparável antes/depois.** As entidades novas consomem o RNG e mudam todos os sorteios subsequentes, mesmo com `SEED_SEMENTE` fixa. Combinar com a equipe que a base vai mudar de aparência.
11. **Volume no Streamlit.** ~900 itens faturáveis, ~400 guias, N divergências. `pages/faturamento_guias.py` hoje faz um loop de `st.columns` por laudo — com 900 a página trava. Paginação e `st.dataframe` com seleção são obrigatórios nas telas novas, não opcionais.
12. **Permissões novas em base já semeada.** `_seed_perfis` faz early-return; sem tornar idempotente, ninguém ganha acesso às telas novas numa base existente.
13. **Tamanho.** 9 migrations com backfill, 2 módulos reescritos, 4 páginas alteradas + 2 novas, seeder inteiro e ~30 testes. Para 4 pessoas isso é grande. A ordem das fases foi desenhada para paralelizar: Fase 1 (preço/cadastro) e Fase 2 (competência) não se tocam; Fases 6 e 7 podem correr em paralelo depois da 5.

---

### Arquivos críticos para a implementação

- `src/faturamento/lote_faturamento/service.py` — o `_obter_ou_criar_guia` degenerado (linha 254), o `validar_lote` que nunca olha preço (107) e o `fechar_lote` com vencimento hardcoded (144); é o arquivo que vira `remessa/service.py` + `guia/service.py`
- `src/faturamento/lote_faturamento/models.py` — origem de `LoteFaturamento`/`GuiaTiss`/`GuiaItem` e do `laudo_id UNIQUE` (linha 58)
- `src/financeiro/titulo_receber/service.py` — o `baixar_titulo` que marca PAGO em qualquer valor (linha 61) e perde o pagamento a maior (71)
- `src/cadastro/procedimento/models.py` — `convenio_id NOT NULL` (linha 34) e a ausência de `vigencia_fim`, raiz do preço particular
- `src/laboratorial/service.py` — linha 240-247, o único ponto de liberação do laudo e portanto o hook do item faturável
- `src/seeder/faturamento.py` — reescrita completa; é o teste de integração de fato do modelo novo
- `src/bi/etl.py` — linhas 169-192, o consumidor mais frágil de toda mudança de grafo