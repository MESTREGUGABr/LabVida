# LabVida — Plano de Evolução para ERP de Verdade

> Documento de **planejamento**. Nada aqui foi implementado ainda.
> Anexo técnico: [plano-faturamento-competencia.md](plano-faturamento-competencia.md).
> Documento irmão: [revisao-final.md](revisao-final.md).

## Contexto

O LabVida foi apresentado ao professor e voltou com uma lista de apontamentos. Este plano responde a **todos** eles, mais uma revisão de fluxo ponta a ponta que expôs problemas estruturais que ninguém tinha visto — inclusive receita que evapora e um dashboard de BI que mente.

**Restrição definida pelo professor:** o frontend **permanece em Streamlit**. Isso não é limitação — os dois pontos dele ("AgGrid" e "Altair melhor para BI") são exatamente bibliotecas do ecossistema Streamlit. A raiz do desconforto atual é outra: **o projeto usa Streamlit como se fosse 2022.** Está tudo em `pages/` com nav escondido via CSS, modais simulados com `session_state`, e gráficos com `st.bar_chart`. Verificado na instalação atual (Streamlit 1.60.0): `st.navigation`, `st.Page`, `st.fragment`, `st.dialog`, `st.data_editor`, `st.column_config`, `st.popover`, `st.segmented_control` e `st.altair_chart` estão **todos disponíveis e nenhum é usado**. Altair 6.2.2 já está instalado.

**Decisão de faturamento já tomada:** competência como eixo de apuração, lote vira remessa TISS, guia passa a ser por paciente/atendimento.

**Prazo:** sem prazo curto — ordem técnica, fazer certo.

`docs/revisao-final.md` já cataloga 16 bugs, 7 UX sistêmicos e 29 funcionalidades ausentes. Este plano **não duplica** aquilo; a seção 7 aqui lista só o que aquele documento **não** contém.

---

## Sumário

1. [Mapa: apontamento do professor → onde é resolvido](#1-mapa-apontamento-do-professor--onde-é-resolvido)
2. [Eixo 1 — Streamlit moderno](#2-eixo-1--streamlit-moderno)
3. [Eixo 2 — Faturamento por competência](#3-eixo-2--faturamento-por-competência)
4. [Eixo 3 — Tabela de exames e regra do valor](#4-eixo-3--tabela-de-exames-e-regra-do-valor)
5. [Eixo 4 — BI por período](#5-eixo-4--bi-por-período)
6. [Eixo 5 — OMOP: decisão da equipe](#6-eixo-5--omop--decisão-da-equipe)
7. [Achados novos: bugs e inconsistências do fluxo completo](#7-achados-novos)
8. [Ordem de execução](#8-ordem-de-execução)
9. [Decisões que precisam de martelo](#9-decisões-que-precisam-de-martelo)
10. [Verificação](#10-verificação)

---

## 1. Mapa: apontamento do professor → onde é resolvido

| Apontamento | Onde | Fase |
|---|---|---|
| Colocar mês do faturamento | Tabela `competencias` + coluna em todo lançamento | 3 |
| Regra de negócio do valor pelos procedimentos | `ProcedimentoValor` com vigência + validação em 3 pontos | 2 |
| Tabela de exames | Catálogo de exames enriquecido + catálogo de analitos | 2 |
| OMOP — padrão de dados de saúde | §6 — 3 opções, equipe decide | — |
| Por que lotes e não períodos / verifica por período | Competência é o eixo; remessa é só o envelope TISS | 3 |
| Implementar período no BI | Filtro de competência nos 3 dashboards + fatos datados corretamente | 6 |
| Fluxo de fechamento — por paciente — por lote | Guia = 1 OS = 1 paciente; remessa agrupa guias; competência fecha o período | 4 |
| Contas — tabela separada por mês | Carteira por competência + regime caixa × competência | 5 |
| Identificador de divergências (lotes, valores) | Tabela `divergencias` + painel dedicado, 14 tipos | 5 |
| Fornecedores — grid e informações | AgGrid + cadastro completo de fornecedor | 1 |
| Compras — grid e produtos | AgGrid + ficha de insumo | 1 |
| IMPLEMENTAR/AJEITAR GRIDS — AgGrid | Componente único `renderizar_grid()` em todas as 29 tabelas | 1 |
| Revisar UI & UX | `st.navigation` + `st.fragment` + `st.dialog` + padrões unificados | 1 |
| Altair melhor para BI | `st.altair_chart` substituindo `st.bar_chart` nos 10 gráficos | 6 |

---

## 2. Eixo 1 — Streamlit moderno

**Tese:** metade do que incomoda no Streamlit hoje é código legado, não limitação da ferramenta.

### 2.1 Navegação — matar o hack de CSS

Hoje: pasta `pages/` (auto-descoberta) + `src/ui_css.py:120-146` esconde o nav nativo com `display:none !important` + `src/ui.py:164-301` renderiza ~140 linhas de HTML inline como substituto.

Alvo: `st.navigation` + `st.Page` em `app.py`, construindo a lista de páginas **a partir das permissões do usuário**. O menu deixa de ser HTML inline e passa a ser navegação nativa; some o CSS de combate. `_MENU` (`src/ui.py:32-103`) vira a fonte de dados da navegação, não de um `<div>`.

Ganho colateral: hoje o menu usa `cadastro:*:escrever`, então **perfis read-only não enxergam nenhuma tela de cadastro**. A reconstrução corrige isso (visível com `:ler`, editável com `:escrever`).

### 2.2 Grids — AgGrid como componente único

Hoje: 29 `st.dataframe` espalhados, cada um com formatação própria; 1 único uso de `st.column_config` (`pages/home.py:177`); `admin_usuarios.py:81-119` simula tabela com `<div>` sobreposto a `st.columns`; `cadastro_convenios.py` e `compras_pedidos.py` não têm grid nenhum — são `st.columns` manuais por linha.

Alvo: **um** componente `src/ui_components/data_grid.py`:

```python
def renderizar_grid(
    dados: list[dict] | pd.DataFrame,
    *,
    colunas: list[ColunaGrid],       # rótulo, campo, tipo (texto|moeda|data|status|numero), largura
    selecao: Literal["nenhuma","linha","multipla"] = "nenhuma",
    acoes: list[AcaoLinha] | None = None,
    altura: int = 420,
    chave: str,
) -> ResultadoGrid:                   # .selecionados, .editados
```

Encapsula formatação pt-BR (moeda `R$ 1.234,56`, data `DD/MM/AAAA`), badge de status reaproveitando `MAPA_STATUS_POR_DOMINIO` (`src/ui_components/status_badge.py:28`, já mapeia 29 status), ordenação, filtro por coluna e paginação.

**Spike obrigatório na Fase 0:** validar `streamlit-aggrid` contra Streamlit 1.60. Se a compatibilidade não fechar, o fallback é `st.dataframe` nativo com `column_config` + `selection_mode`/`on_select` (verificado disponível) — a assinatura do componente não muda, só a implementação interna. **Decidir isso antes de reescrever 29 telas.**

### 2.3 Estado por linha — `st.fragment` mata o rerun global

Hoje: 6 telas usam `st.session_state` com chaves dinâmicas para simular formulário inline e accordion — `faturamento_guias.py` (11 acessos), `financeiro_contas.py` (8), `compras_pedidos.py` (6), `admin_usuarios.py` (4), `faturamento_glosas.py` (4), `compras_fornecedores.py` (4). Cada clique dispara `st.rerun()` da página inteira (~45 ocorrências) — daí a lentidão de `faturamento_guias.py`, que refaz 10+ queries por rerun.

Alvo:
- **`@st.fragment`** nos blocos de linha: o rerun fica confinado ao fragmento, a página não recarrega.
- **`st.dialog`** para os formulários inline (baixa de título, registrar glosa, editar fornecedor) — modal de verdade, sem `session_state[f"form_{id}"]`.
- **`st.popover`** para ações rápidas por linha.

Isso apaga a classe inteira de bug U4 do `revisao-final.md` ("apenas um formulário pode estar aberto por vez; colapsam em reruns não relacionados").

### 2.4 Padrões unificados

| Problema atual | Padrão alvo |
|---|---|
| `st.radio(horizontal=True)` fingindo de aba em 3 páginas | `st.tabs` ou `st.segmented_control` |
| Ação destrutiva com `st.checkbox` de confirmação | `st.dialog` de confirmação, um só helper |
| Traceback cru na tela (18+ páginas sem try/except) | Decorator/context `tratar_erros()` que mapeia as exceções de `errors.py` de cada módulo para `st.error` legível |
| Sem spinner em query longa | `st.spinner` no helper de listagem |
| Sem paginação (4 páginas quebram com volume real) | Paginação server-side no `renderizar_grid` (o padrão de `atendimento_os.py:207-234` já existe e funciona) |
| Lógica de domínio dentro da página (`home.py`, `laboratorio_bancada.py:79-94`, os 3 `bi_*.py`, `meu_perfil.py:89-92` mutando ORM direto) | Mover para service; página só orquestra |

### 2.5 Docker

Fica como está no essencial (já funciona: boot limpo em 54s, seed em 35s). Ajustes pontuais:
- `HEALTHCHECK` no `Dockerfile` (hoje não tem).
- Separar o seed do boot: variável `SEED_ON_BOOT=true|false` no compose, para quem só quer subir a app sem esperar 35s.
- `.dockerignore` ignorar `docs/` inteiro (hoje ignora só os PDFs).

---

## 3. Eixo 2 — Faturamento por competência

> **Detalhamento completo** — DDL, as 9 migrations com backfill, assinaturas de service e o SQL da explosão das guias: [plano-faturamento-competencia.md](plano-faturamento-competencia.md).

### 3.1 Os três princípios

1. **Competência é carimbada no fato gerador, não no ato de faturar.** Laudo liberado em março gera receita de março, mesmo que seja faturado em maio.
2. **Guia é o documento do atendimento (1 OS = 1 paciente); remessa é o envelope enviado ao convênio (N guias).** É o que o TISS realmente é, e é literalmente "fechamento por paciente — por lote".
3. **Divergência é entidade de primeira classe**, com detector idempotente e painel próprio.

### 3.2 Modelo alvo (resumo)

```
competencias (DATE PK, ABERTA|FECHADA, totais congelados no fechamento)
    ├── itens_faturaveis   1:1 com laudo — o ledger, com competência e valor de tabela
    ├── guias_tiss         1:1 com OS — paciente, data de atendimento, numeração TISS
    │     └── guias_itens  N:1 item_faturavel (SEM unique → permite reapresentação)
    │           └── glosas → recursos_glosa
    ├── remessas_faturamento  (ex-lotes_faturamento) por convênio+competência
    ├── titulos_receber    com valor_pago, saldo, baixas parciais
    └── divergencias       polimórfica, 14 tipos, 3 severidades
```

### 3.3 O que cada peça resolve

| Peça nova | Bug/limitação que mata |
|---|---|
| `itens_faturaveis` (com `laudo_id UNIQUE` migrado para cá) | Item 100% glosado hoje é **receita perdida para sempre** — `guias_itens.laudo_id` é UNIQUE e o repositório de pendentes exclui laudo já faturado. Com o UNIQUE na tabela certa, o item volta para `A_FATURAR` |
| `itens_faturaveis.valor_previsto NOT NULL` | Mata o fallback mágico `50.0` de `lote_faturamento/repository.py:102` |
| `competencias` com status | Não existe fechamento de período hoje; nada impede lançar em março depois de março fechado |
| Guia por OS + índice parcial `(ordem_servico_id, competencia) WHERE status='ABERTA'` | Hoje `_obter_ou_criar_guia` (`service.py:254`) sempre reusa `lote.guias[0]` → 1 lote = **1 guia com pacientes diferentes misturados**. A guia atual não modela nada do TISS |
| `guias_itens.valor_glosado` com `CHECK <= valor_faturado` | `glosa/service.py:32` compara cada glosa isolada → duas glosas de 60% glosam 120% de um item e ele continua `FATURADO` |
| `divergencias` | O professor pediu explicitamente. Absorve `conciliacoes_pagamento`, que hoje é beco sem saída |
| `baixas_titulo_receber` + `saldo` | Baixa parcial não existe: receber R$1 de um título de R$1000 marca **PAGO** |
| `convenios.prazo_pagamento_dias` | Vencimento é `hoje + 30` hardcoded em `fechar_lote` |

### 3.4 Catálogo de divergências (o pedido explícito)

14 tipos, detectados em 5 gatilhos, 3 severidades. Cobrem os três casos que o professor citou:

- **valor** → `SEM_PRECO_TABELA` (bloqueio), `VALOR_ACIMA_TABELA`, `VALOR_ABAIXO_TABELA`
- **lote** → `TOTAL_GUIA_DIVERGENTE`, `TOTAL_REMESSA_DIVERGENTE` (soma dos itens ≠ total gravado)
- **recebimento** → `RECEBIMENTO_MENOR`, `RECEBIMENTO_MAIOR` (recebido vs. faturado − glosado)

Mais: `TUSS_INVALIDO`, `LAUDO_NAO_LIBERADO`, `GLOSA_EXCEDE_FATURADO`, `REMESSA_SEM_RETORNO`, `COMPETENCIA_NAO_FATURADA`, `LAUDO_SEM_ITEM_FATURAVEL`, `COMPETENCIA_FECHADA_RETROATIVA`.

Regra: **registra sempre; bloqueia só severidade BLOQUEIO; avisa em ALERTA.** ALERTA pode ser fechado com justificativa por quem tem `faturamento:justificar_divergencia`.

Tela nova: `pages/faturamento_divergencias.py` — KPIs por severidade, valor em risco, filtros competência/convênio/tipo, ações justificar/corrigir/ignorar.

### 3.5 Fluxo alvo ponta a ponta

```
laudo LIBERADO ─→ gera item faturável (competência = liberado_em, valor_tabela na data do fato)
                  └→ detecta divergência de preço já na origem
faturista      ─→ agrupa itens por OS → guia do paciente
               ─→ remessa por (convênio, competência) → pré-auditoria (agora consulta a tabela de preços)
               ─→ fecha remessa → título a receber (venc. = prazo do convênio)
retorno        ─→ glosa → abate no título → recurso ou reapresentação
financeiro     ─→ baixa PARCIAL → baixa + movimento de caixa → detecta divergência
fim do mês     ─→ apurar competência → fechar (bloqueado se houver divergência BLOQUEIO)
```

---

## 4. Eixo 3 — Tabela de exames e regra do valor

### 4.1 Catálogo de exames (hoje o `Procedimento` tem 4 colunas)

`src/cadastro/procedimento/models.py:12-19` tem apenas `codigo_tuss`, `nome`, `setor` (string livre, sem FK para `setores`), `ativo`. Falta tudo que faz um catálogo de exames ser um catálogo:

| Campo a adicionar | Por quê |
|---|---|
| `tipo_material` (FK ou enum) | Hoje o material só existe *depois*, como string livre em `Amostra.tipo_material` — não é derivável do catálogo. É o que permite a coleta saber o que coletar |
| `prazo_entrega_dias` / TAT | Base do indicador de SLA que o BI não tem |
| `metodo` | Metodologia analítica (imunoturbidimetria, ELISA…) |
| `setor_id` FK → `setores` | Substitui a string livre; hoje "Bioquímica" digitado errado vira setor novo |
| `preparo_paciente` | Jejum, coleta seriada |
| `mnemonico` | Busca rápida no balcão |
| Painel/perfil (procedimento composto) | Hemograma é um painel de analitos; perfil lipídico é painel de procedimentos |

### 4.2 Catálogo de analitos — o elo que falta

Hoje `Resultado.analito` e `ValorReferencia.analito` são **duas strings livres independentes, sem FK entre si e sem tabela de analitos**. Nenhum código no repositório casa uma com a outra — a tela de resultado não sabe qual é a faixa de referência do que acabou de ser digitado. "Hemoglobina" ≠ "hemoglobina".

Alvo: tabela `analitos` (código interno, nome, unidade padrão, casa decimal, e **espaço para LOINC** — ver §6), com `procedimento_analito` ligando o painel aos seus analitos. `Resultado.analito_id` e `ValorReferencia.analito_id` viram FK.

Ganho imediato, independente de OMOP: a bancada passa a saber o que digitar, a faixa de referência passa a ser aplicável, e o laudo pode marcar resultado alterado.

Complemento: `ValorReferencia` hoje não tem faixa por **sexo** nem por **idade** (e nem unique constraint — nada impede N faixas duplicadas para o mesmo par). Adicionar `sexo`, `idade_min`, `idade_max`, `vigencia`.

### 4.3 Regra do valor — três pontos de aplicação

Hoje: se o operador digita um valor na abertura da OS, ele **sobrescreve a tabela sem nenhuma checagem** (`ordem_servico/service.py:94-100`), e a tela de faturamento expõe o valor faturado como `number_input` livremente editável (`faturamento_guias.py:172`). A "pré-auditoria" (`validar_lote`) **nunca consulta a tabela de preços**.

Alvo:
1. **Abertura da OS** — tabela é a fonte da verdade, inclusive para particular. Valor divergente exige permissão `faturamento:valor_excecao` **e** motivo; grava `origem_valor='NEGOCIADO'` + `valor_tabela` (o que a tabela dizia).
2. **Liberação do laudo** — recalcula o valor de tabela **na data do fato gerador** e registra divergência na origem, meses antes de alguém tentar faturar.
3. **Pré-auditoria da remessa** — revalida contra a tabela vigente na competência.

Pré-requisitos no modelo de preço:
- `ProcedimentoValor.convenio_id` passa a aceitar NULL → **existe tabela de preço particular** (hoje é impossível; particular é digitado à mão, sem governança nem histórico).
- `vigencia_fim` + constraint `EXCLUDE` de não-sobreposição → prova no banco de que existe exatamente um preço vigente por data.
- `definir_valor()` encerra automaticamente a vigência anterior.

---

## 5. Eixo 4 — BI por período

### 5.1 Três bugs que fazem o BI mentir hoje

| # | Bug | Onde | Efeito |
|---|---|---|---|
| B1 | `FatoLogistica.sk_tempo = date.today()` **dentro do loop** | `src/bi/etl.py:196` | **Toda a série temporal de logística é uma barra única em "hoje".** E não há como corrigir sem mexer no OLTP: `Amostra` não tem timestamp algum |
| B2 | `FatoFinanceiro` datado por `vencimento` | `src/bi/etl.py:186,191` | O gráfico rotulado "Fluxo de Caixa" plota **cronograma de vencimentos**, misturando títulos pendentes e liquidados. Não existe regime de caixa — `titulos_*` não têm data de pagamento |
| B3 | `FatoFaturamento` de lote aberto cai em `date.today()` | `src/bi/etl.py:174` | Itens migram de bucket temporal a cada execução do ETL |

Consequência: **o ETL não é idempotente.** Rodar ontem e hoje produz números diferentes para os mesmos dados de origem. E `_carga_fatos` **não tem um único teste** (`tests/bi/` só cobre dimensões e tempo de ciclo) — nada detectaria a regressão.

### 5.2 Correções

- Fatos passam a ser datados por **competência** (faturamento), **data de liquidação** (financeiro, viável depois das baixas da Fase 5) e **`AmostraMovimentacao.ocorrido_em`** (logística — a data existe, só não é consultada).
- `DimProcedimento.setor` hoje é **sempre NULL** porque `_carga_dimensoes` passa `setor=None` explicitamente (`etl.py:137`) — análise por setor não existe. Corrigir.
- `FatoFaturamento` ganha unidade real (hoje é sempre a unidade fake "consolidado", `etl.py:181`) — `itens_faturaveis.unidade_id` torna isso trivial.
- `FatoFinanceiro.sk_convenio` hoje é **sempre `None`** (`etl.py:188,192`) — passa a ser preenchido.
- **Chave natural em todo fato** (`os_item_id`, `guia_item_id`, `amostra_id`, `titulo_id`): hoje não existe nenhuma, o que torna carga incremental e reconciliação impossíveis.
- `DimTempo` ganha `ano_mes`, `semana`, `semestre`, `dia_util`. `trimestre` já existe e nunca foi usado.
- Receita **particular** passa a chegar ao BI (hoje `FatoFaturamento` vem de `GuiaItem`, que é TISS/convênio — receita de balcão é invisível).
- `bi_logistica.py:52-60` lê a tabela operacional `amostras` direto, furando o modelo dimensional. Corrigir.
- Testes de `_carga_fatos`, incluindo **idempotência** (rodar 2× produz o mesmo resultado).

### 5.3 Altair e filtro de período

Os 3 dashboards não têm **nenhum** filtro de data — todo agregado é "desde o início dos tempos", e só 2 de 11 consultas sequer tocam `bi_dim_tempo`.

- Seletor global de competência (ou intervalo) nas 3 páginas, propagado como `WHERE` sobre `bi_dim_tempo`.
- `st.bar_chart`/`st.line_chart` → `st.altair_chart` com escala de cor consistente, tooltip, rótulo em pt-BR e eixo formatado em R$. Altair 6.2.2 já está instalado — **zero dependência nova**.
- Drill-down por seleção (Altair `selection_point` + `st.altair_chart(on_select=...)`).
- Indicadores que faltam e o modelo novo destrava: ticket médio por exame/convênio, tempo médio coleta→laudo por período, taxa de glosa por convênio **por competência**, e DRE gerencial simplificado.

---

## 6. Eixo 5 — OMOP — decisão da equipe

O professor pediu "implementar essa brincadeira". Antes de escolher, o diagnóstico honesto do que existe hoje:

**Bloqueadores estruturais, em ordem de gravidade:**
1. **Não existe catálogo de analitos** — texto livre em duas tabelas desconectadas. Sem entidade estável, não há onde pendurar um `measurement_concept_id`/LOINC.
2. **`Resultado.valor` é `String(255)`** — sem valor numérico, sem unidade, sem operador (`<`, `>`), sem flag de anormalidade.
3. **Zero camada de vocabulário** — grep por LOINC/SNOMED/CID/ICD no repositório inteiro retorna **nada**. O único código é o TUSS, que é administrativo, não clínico.
4. **Sem diagnóstico/CID em lugar nenhum** → `CONDITION_OCCURRENCE` nasceria vazia.
5. `OrdemServico` não tem `fechada_em` → `visit_end_date` indefinido. `Amostra` não tem data → `specimen_date` indisponível.

### As três opções

| | **A — Camada analítica** | **B — Vocabulário no OLTP** | **C — CDM completo** |
|---|---|---|---|
| O que faz | Mantém o OLTP e cria ETL para tabelas OMOP CDM (`PERSON`, `VISIT_OCCURRENCE`, `PROCEDURE_OCCURRENCE`, `MEASUREMENT`, `SPECIMEN`) ao lado do star schema | Adota só a espinha de terminologia: tabela `concept`, catálogo de analitos com LOINC, TUSS como `source_concept`, `source_to_concept_map` | Refunda o modelo clínico no CDM |
| Pré-requisito | Catálogo de analitos (§4.2) + `Resultado` numérico + datas faltantes | Catálogo de analitos (§4.2) | Tudo do A e B + CID + `OBSERVATION_PERIOD` + `location` + `death` |
| Esforço | Médio-alto | **Baixo-médio** | Muito alto |
| Demonstrável | Sim — dá para mostrar as tabelas CDM populadas e rodar uma query OHDSI | Sim — dá para mostrar exame mapeado para LOINC | Sim, se terminar |
| Risco | Médio | **Baixo** | Alto — provavelmente não termina |
| Valor real p/ o ERP | Interoperabilidade e pesquisa | Corrige o modelo clínico de verdade (a bancada passa a ter faixa de referência aplicável) | Idem, com custo desproporcional |

**Recomendação:** **B primeiro, A depois se sobrar fôlego.** A opção B é pré-requisito das outras duas de qualquer jeito, entrega valor imediato ao laboratório (não é conformidade decorativa), e deixa a porta aberta. A opção C não cabe no escopo.

**A equipe decide.** Registrar a escolha como ADR em `docs/adr/`.

---

## 7. Achados novos

Bugs e inconsistências que **não** estão em `revisao-final.md` (aquele documento se declara "9.5/10, 1 bug pendente" — está desatualizado).

### 7.1 Críticos

| # | Achado | Onde | Impacto |
|---|---|---|---|
| N1 | **`StatusOsItem.FATURADO` nunca é atribuído em produção** | `ordem_servico/dtos.py:22` — só um teste o atribui, na mão | `repository.item_faturado` (`ordem_servico/repository.py:92`), o guarda que impede cancelar item faturado, depende dele. Funciona só pelo ramo de `GuiaItem` — e como item 100% glosado vira `GLOSADO`, ele **volta a ser cancelável** |
| N2 | **Item 100% glosado = receita perdida para sempre** | `guias_itens.laudo_id` UNIQUE + `repository.py:69,84` | Reapresentação é **estruturalmente impossível** sem alterar o schema |
| N3 | **Glosas cumulativas podem exceder 100%** | `glosa/service.py:32` compara cada glosa isolada | Duas glosas de 60% glosam R$120 de um item de R$100, e o item permanece `FATURADO` |
| N4 | **BI de logística inteiro colapsa em "hoje"** | `bi/etl.py:196` | Ver §5.1 |
| N5 | **ETL não é idempotente** | `bi/etl.py:174,196` + faixa etária congelada na 1ª carga (`etl.py:89-108`) | Mesmos dados de origem, números diferentes por dia de execução |
| N6 | **Baixa parcial não existe** | `titulo_receber/service.py:61` | Receber R$1 de R$1000 marca **PAGO** e gera conciliação de R$999 |

### 7.2 Médios

| # | Achado | Onde |
|---|---|---|
| N7 | Lotes particulares **somem** das telas de glosa — `INNER JOIN Convenio` | `glosa/repository.py:49,91` |
| N8 | `session_scope()` **não faz commit nem rollback**, só `close()` — exceção no meio de um service deixa transação suja | `src/db.py:18-24` |
| N9 | Engine sem `pool_pre_ping`/`pool_recycle` — conexão morta por timeout quebra a primeira query | `src/db.py:14` |
| N10 | Pagamento **a maior** é silenciosamente perdido (divergência só é registrada se > 0) | `titulo_receber/service.py:67` |
| N11 | `NameError` latente: usa `origem_id` definido só no ramo da outra aba | `pages/logistica_malotes.py:139` |
| N12 | RBAC é **ignorado por completo** se a tabela `perfis` estiver vazia — e o mesmo bypass está replicado em 4 lugares | `ui.py:153`, `ordem_servico/service.py:169`, `titulo_receber/service.py:50`, `titulo_pagar/service.py:41` |
| N13 | `_seed_perfis` faz early-return se já houver permissões → **base existente nunca recebe permissão nova** | `src/seeder/rbac.py` |
| N14 | Preço retroativo inserido depois **muda silenciosamente** o resultado de consultas históricas; não há como encerrar nem corrigir um preço | `procedimento/service.py:47-68` (só insere, sem update/delete) |

### 7.3 Segurança (não catalogados em lugar nenhum)

| # | Achado | Onde |
|---|---|---|
| N15 | **O `id_token` nunca é validado.** Sem verificação de assinatura JWT/JWKS, sem `nonce`, sem `aud`, sem `exp`. A autenticação é implícita: se `/userinfo` responde 200, o usuário entra | `src/auth.py:75-86`, `app.py:20-44` |
| N16 | **`state` = `code_verifier`** — o parâmetro anti-CSRF carrega o segredo do PKCE em claro, e não há checagem de CSRF | `src/auth.py:38-52` |
| N17 | Sem auditoria de **leitura** de PII — acesso a CPF descriptografado não é registrado (lacuna LGPD) | `src/auditoria/` |
| N18 | `cpf_hash` é SHA-256 **sem salt** — permite ataque de dicionário sobre o espaço de CPFs | `src/lgpd/__init__.py:18-19` |

### 7.4 Modelo — campos órfãos e estados inalcançáveis

- `StatusGuiaTiss` (4 valores) e `xml_tiss`: enum e coluna **nunca escritos**.
- `StatusTitulo.ATRASADO` e `.CANCELADO`: **inalcançáveis** (nenhum código os atribui).
- `FatoFaturamento.ticket_medio`, `FatoFinanceiro.rentabilidade`, `FatoLogistica.tempo_transito_horas`: colunas **nunca populadas**.
- `titulo_receber/repository.listar_vencidos` e `.listar_por_status`, `movimento_caixa/repository.salvar`, `errors.GuiaNaoEncontrada`, `ui_components/filter_bar.py` inteiro: **dead code**.
- `MovimentoCaixa` sem CHECK garantindo vínculo coerente → movimento órfão é permitido pelo schema.
- `LoteFaturamento` sem `unidade_id` → glosa tem unidade, faturamento não; cruzar os dois exige 5 joins.
- Dark mode (`ui_css.py:605-621`) existe e **nunca é chamado** por nenhuma página.

---

## 8. Ordem de execução

Critério de saída de **toda** fase: `alembic upgrade head` OK · `python -m src.seeder` OK em base limpa · suíte verde · queries de reconciliação batendo.

| Fase | Escopo | Depende de | Paralelizável com |
|---|---|---|---|
| **0 — Fundação** | `db.py` (rollback + `pool_pre_ping`); N3, N7, N11, N13; remove fallback `50.0`; extrai `tests/_tabelas.py`; **spike do AgGrid**; ADR do fuso da competência | — | — |
| **1 — Streamlit moderno** | `st.navigation`; componente `renderizar_grid`; `st.fragment`/`st.dialog` nas 6 telas de estado por linha; `tratar_erros()`; grids de Fornecedores e Compras (pedido explícito) | 0 (spike) | 2 |
| **2 — Preço, catálogo e regra do valor** | Preço particular + `vigencia_fim` + EXCLUDE; catálogo de exames enriquecido; catálogo de analitos; `ValorReferencia` por sexo/idade; regra do valor nos 3 pontos | 0 | 1 |
| **3 — Competência + item faturável** | Tabela `competencias` + backfill; `itens_faturaveis` (resolve N1 e N2); hook na liberação do laudo; tela de apuração | 2 | — |
| **4 — Remessa + guia por paciente** | Rename lote→remessa; explosão das guias degeneradas; reescrita de `faturamento_guias.py` — **é a entrega visível para o professor** | 3 | — |
| **5 — Glosa, divergências e financeiro** | Ciclo de vida da glosa + recurso + reapresentação; tabela `divergencias` + painel; baixa parcial; contas bancárias e categorias; fechamento de competência com bloqueio | 4 | glosa ∥ divergências |
| **6 — BI por período** | Corrige B1/B2/B3; chave natural nos fatos; filtro de competência; Altair nos 10 gráficos; indicadores novos; testes de `_carga_fatos` | 5 | — |
| **7 — OMOP** | Conforme decisão da §6 | 2 (catálogo de analitos) | 6 |
| **8 — Segurança** | N15–N18: validação de JWT, `state` próprio, auditoria de leitura de PII, salt no hash de CPF | — | qualquer |

**Divisão sugerida para 4 pessoas:** Fase 1 (frontend) e Fase 2 (modelo de preço/catálogo) não se tocam — duas duplas em paralelo. A partir da 3 o caminho crítico é sequencial no faturamento, mas Fase 6 (BI) e Fase 8 (segurança) podem correr em paralelo por quem estiver livre.

**Corte se apertar:** recursos de glosa (manter só reapresentação) e contas bancárias/categorias. **Fases 4 e 5 não podem cair** — são literalmente o que o professor pediu.

---

## 9. Decisões que precisam de martelo

Antes de codar:

1. **AgGrid ou `st.dataframe` nativo?** Depende do spike da Fase 0. Define a implementação de 29 telas.
2. **Fuso da competência** — `America/Recife` ou UTC? Muda a competência de todo laudo liberado entre 21h e meia-noite. Uma vez escolhido é imutável. **Merece ADR.**
3. **Grão da guia = OS?** Escolhemos 1 OS = 1 guia (SP/SADT canônico). Alguns convênios aceitam guia mensal por beneficiário. Se o professor esperar isso, muda o agrupamento.
4. **Pagamento a maior** — capar no saldo e registrar divergência, ou permitir saldo negativo?
5. **Qual opção de OMOP** (§6).
6. **Drop de `guias_itens.laudo_id`** — limpa o MER mas quebra 4 call sites; manter denormalizado é mais barato e mais sujo.

Riscos técnicos a monitorar: `--autogenerate` **não detecta rename** (emitiria `drop_table`+`create_table` e destruiria os dados — documentar no Makefile); `btree_gist` precisa existir no Postgres de deploy; `NULLS NOT DISTINCT` exige PG15+ (o stack é PG16, OK); colunas geradas (`Computed`) precisam de spike com Pydantic; a base de demonstração vai mudar de aparência mesmo com semente fixa.

---

## 10. Verificação

**Por fase** (além de suíte verde e seeder rodando):

| Fase | Query/teste de reconciliação |
|---|---|
| 2 | `COUNT(*) FROM procedimento_valores WHERE convenio_id IS NULL > 0`; EXCLUDE prova ausência de sobreposição |
| 3 | `COUNT(itens_faturaveis) = COUNT(laudos WHERE status='LIBERADO')`; nenhum `guias_itens` órfão |
| 4 | **Nenhuma guia com mais de um paciente** — a query que prova a "explosão" das guias degeneradas |
| 5 | Receber R$1 de um título de R$1000 deixa **PARCIAL com saldo 999** (hoje marca PAGO); item 100% glosado + reapresentação **volta** para a lista de pendentes; rodar o detector 2× não duplica divergência |
| 6 | ETL rodado 2× produz **os mesmos números**; `apurar(competência)` bate com o BI |

**Contínuo:** o seeder é o teste de integração de fato — ele atravessa 400 OS pelo fluxo real e já derrubou 3 bugs de produção. Toda mudança de modelo passa por ele antes de passar por qualquer outra coisa.

**Regressão visual:** subir com `docker compose up -d`, percorrer as 26 telas e conferir que nenhuma quebrou. Vale um checklist versionado em `docs/`.
