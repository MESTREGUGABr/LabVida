# LabVida — Roadmap de Execução (documento canônico)

> **Este documento é a fonte única da verdade sobre ordem, numeração de fases e numeração de migrations.**
> Onde ele divergir de [plano-evolucao-erp.md](plano-evolucao-erp.md) §8 ou de [plano-faturamento-competencia.md](plano-faturamento-competencia.md) §5, **vale este**.
> Aqueles dois documentos continuam válidos como **conteúdo técnico** (o *quê* e o *como*); este define o *quando*, o *em que ordem* e o *quem*.
> Plano de BI: [plano-bi.md](plano-bi.md).

## Por que este documento existe

Os dois planos anteriores descrevem o mesmo trabalho com **duas numerações de fase incompatíveis** — "Fase 5" significa *glosa + divergências + financeiro* num documento e *guia por paciente* no outro. Com 4 pessoas trabalhando em paralelo, isso não é detalhe editorial: é conflito de merge e retrabalho.

Além disso, a conferência do código contra a documentação encontrou **sete contradições** que precisavam de decisão antes de qualquer linha de código. Estão resolvidas na §3.

---

## Sumário

1. [Numeração canônica de fases](#1-numeração-canônica-de-fases)
2. [Numeração de migrations](#2-numeração-de-migrations)
3. [Contradições resolvidas](#3-contradições-resolvidas)
4. [Decisões que ainda precisam de martelo](#4-decisões-que-ainda-precisam-de-martelo)
5. [Divisão para 4 pessoas](#5-divisão-para-4-pessoas)
6. [Critério de pronto](#6-critério-de-pronto)
7. [Rastreabilidade: apontamento do professor → fase](#7-rastreabilidade-apontamento-do-professor--fase)
8. [Dívida de documentação](#8-dívida-de-documentação)

---

## 1. Numeração canônica de fases

| Fase | Escopo | Migration | Depende de | Paralelizável com | Detalhamento |
|:---:|---|---|:---:|:---:|---|
| **F0** | ✅ **Fundação — concluída em 02/08/2026.** `db.py` (rollback + `pool_pre_ping` + `pool_recycle`); glosa cumulativa (N3); `LEFT JOIN` do particular (N7); seed RBAC idempotente por linha (N13); fallback `50.0` removido; `tests/_tabelas.py` extraído dos **6** conftests; N19 (suíte no Windows); spike do AgGrid + 3 ADRs. **N11 já estava corrigido** pelo commit `4a07160` — o plano estava desatualizado | — | — | — | evolucao §8 |
| **F1** | ✅ **Streamlit moderno — concluída em 02/08/2026.** `renderizar_grid()` com AgGrid como fronteira única · `tratar_erros()` · `st.navigation` nativa filtrada por permissão (morreram ~140 linhas de HTML inline e ~25 de CSS de combate) · `st.dialog` no lugar dos toggles de `session_state` em Fornecedores, Compras, Glosas, Contas e Admin · grid em 12 telas · smoke das 28 telas | — | F0 | F2, F3 | evolucao §2 |
| **F2** | ✅ **BI onda 1 — concluída em 02/08/2026.** 8 bugs + 2 problemas de grão corrigidos; 7 dimensões e 6 fatos com chave natural; ETL idempotente (**35s → 1,3s**); `metricas.py`; Altair; filtro de período; 4 dashboards; 41 testes de BI | `0014` | F0 | F1, F3 | **[plano-bi.md](plano-bi.md) §10** |
| **F3** | 🔶 **Preço, catálogo e regra do valor — parcial (03/08/2026).** ✅ preço particular + vigência + EXCLUDE · regra do valor na abertura da OS · catálogo de analitos + painel + faixa por sexo/idade · exame enriquecido. ⬜ falta: tela de preços com "Particular", seeder com tabela particular. *(descrição original:)* **Preço, catálogo e regra do valor** — preço particular, `vigencia_fim`, EXCLUDE; catálogo de exames; catálogo de analitos; `ValorReferencia` por sexo/idade; regra do valor nos 3 pontos | `0015` | F0 | F1, F2 | evolucao §4 · faturamento §1.9-1.10 |
| **F4** | **Competência** — tabela, backfill, service, tela de apuração (ainda sem bloqueio) | `0017` | F3 | — | faturamento §1.1 |
| **F5** | **Item faturável** — tabela, backfill, hook na liberação do laudo, `StatusOsItem.FATURADO` finalmente atribuído | `0018` | F4 | — | faturamento §1.2 |
| **F6** | **Remessa** — rename lote→remessa, sequence, unique parcial, pacote `remessa` | `0018` | F5 | — | faturamento §1.5 |
| **F7** | ⭐ **Guia por paciente** — explosão das guias degeneradas, `item_faturavel_id`, reescrita de `faturamento_guias.py` — **a entrega visível para o professor** | `0019` | F6 | — | faturamento §1.3-1.4 |
| **F8** | **Glosa com ciclo de vida** — status, `recursos_glosa`, reapresentação, abatimento no título | `0020` | F7 | F9 | faturamento §1.6 |
| **F9** | ⭐ **Divergências** — tabela, 5 detectores, pré-auditoria consultando a tabela de preços, painel — **o outro pedido explícito** | `0021` | F7 | F8 | faturamento §1.8 |
| **F10** | **Título e baixa parcial** — `baixas_titulo_receber`, `ATRASADO` derivado, `CANCELADO` alcançável | `0022` | F9 | — | faturamento §1.7 |
| **F11** | **Caixa, contas e a pagar** + fechamento de competência **com bloqueio** | `0023` | F10 | — | faturamento §1.11 |
| **F12** | **BI onda 2** — competência como eixo, `FatoGlosa` com código TISS, DRE, previsto × realizado, divergências no BI | — | F4, F8, F10 | — | **[plano-bi.md](plano-bi.md) §10** |
| **F13** | **OMOP** — conforme decisão da equipe | a definir | F3 | qualquer | evolucao §6 |
| **F14** | **Segurança** — validação de JWT, `state` próprio, auditoria de leitura de PII, salt no hash de CPF | — | — | qualquer | evolucao §7.3 |

**Mudança de rumo mais importante em relação aos planos anteriores:** o BI saiu do fim da fila. Ele era "Fase 6, depende de tudo". A conferência do código mostrou que as datas e medidas que faltam **já existem no OLTP e simplesmente não são consultadas** ([plano-bi.md §1.6](plano-bi.md)) — cerca de 70% do BI é independente e vira **F2, em paralelo**. O que sobra vira F12.

**Corte se apertar:** F8 (manter só `status` + reapresentação, cortar recursos), F11 (contas bancárias/categorias), F13 (OMOP). **F7 e F9 não caem** — são literalmente o que o professor pediu.

---

## 2. Numeração de migrations

Head atual verificado: **`0013_bi_paciente_hash`**, cadeia única e limpa (o `0012_merge_heads_c_d` já resolveu as heads paralelas anteriores).

**Regra de sequenciamento:** `0014` (BI) entra **antes** da trilha de faturamento. Motivo: F2 e F3 rodam em paralelo, e se as duas partirem de `0013` o Alembic ganha **duas heads** e alguém vai ter que escrever outro merge. A migration de BI toca apenas tabelas `bi_*` (zero impacto no OLTP) e é pequena — então ela **entra primeiro e sozinha**, e a trilha de faturamento parte de `0014` em diante.

| Migration | Fase | Conteúdo |
|---|:---:|---|
| `0014_bi_reconstrucao` | F2 | tabelas `bi_*`: chave natural nos fatos, `bi_fato_ordem_servico`, `bi_fato_glosa`, `bi_dim_setor`, `bi_dim_motivo_glosa`, colunas novas de `bi_dim_tempo`, `bi_etl_execucao` |
| `0015_precos_comerciais` | F3 | preço particular, `vigencia_fim`, EXCLUDE, condições comerciais, rastro do valor na OS |
| `0016_catalogo_analitos` | F3 | catálogo de analitos, painel do exame, faixa por sexo/idade, exame enriquecido |
| `0017_competencias` | F4 | (era `0015`) |
| `0018_itens_faturaveis` | F5 | (era `0016`) |
| `0019_remessa` | F6 | (era `0017`) |
| `0020_guia_por_paciente` | F7 | (era `0018`) |
| `0021_glosa_ciclo_de_vida` | F8 | (era `0019`) |
| `0022_divergencias` | F9 | (era `0020`) |
| `0023_titulo_receber_baixa_parcial` | F10 | (era `0021`) |
| `0024_caixa_contas_e_pagar` | F11 | (era `0022`) |

> ⚠️ Ao ler o anexo [plano-faturamento-competencia.md](plano-faturamento-competencia.md) §2, **some 2** em todo número de migration a partir de `competencias` (a F3 consumiu 0015 e 0016). O conteúdo de cada uma está correto; só o número mudou.

**Regra obrigatória a partir daqui:** migrations **escritas à mão** (`alembic revision -m`, **sem** `--autogenerate`). O autogenerate **não detecta rename** — ele emite `drop_table` + `create_table`, o que destruiria os 73 lotes na `0018`. O alvo `make revision` do Makefile usa `--autogenerate` e **não serve** para esta remodelagem. Documentar no Makefile e no README.

---

## 3. Contradições resolvidas

Encontradas ao conferir os documentos contra o código. Cada uma tinha potencial de travar ou quebrar a execução.

| # | Contradição | Resolução |
|:---:|---|---|
| **C1** | Duas numerações de fase incompatíveis entre os dois planos | **§1 deste documento** é canônica. Os planos viram referência técnica, não roteiro |
| **C2** | A trilha Streamlit (Eixo 1) não existe no roteiro do anexo — quem seguir o anexo nunca faz AgGrid nem `st.navigation` | Virou **F1** explícita, em paralelo com F2 e F3 |
| **C3** | `guias_itens.laudo_id`: o DDL do anexo §1.4 escreve `DROP COLUMN laudo_id` como fato consumado, mas §6 item 5 lista o drop como decisão em aberto | **Decisão: dropar.** Manter a coluna denormalizada preserva 4 call sites mas mantém duas fontes de verdade para o mesmo vínculo — que é exatamente o bug N2 que estamos consertando. O drop é a última operação da `0019`, depois da explosão das guias |
| **C4** | O catálogo de analitos ([plano-evolucao-erp.md](plano-evolucao-erp.md) §4.2) substitui a decisão do [ADR 0003](adr/0003-granularizacao-analitos-laboratorial.md), sem mencioná-lo | O ADR da F3 deve **emendar explicitamente o 0003**, não nascer ao lado. A granularidade por analito do 0003 continua válida; o que muda é o analito deixar de ser texto livre |
| **C5** | Três documentos declaram o projeto pronto (README "Faturamento ✅", `revisao-final` "9.5/10, 1 bug pendente", `RESENHA` "backlog alta: vazio") contra 18 achados novos, incluindo receita que evapora | Ver §8 — dívida de documentação, com correção agendada |
| **C6** | `movimentos_caixa.competencia` criada `NOT NULL` na `0023`, mas o roteiro de backfill não menciona preenchê-la — pela regra do próprio documento ("`SET NOT NULL` falha se sobrar NULL"), a migration falha como está escrita | Backfill obrigatório na `0023`: `competencia = date_trunc('month', ocorrido_em AT TIME ZONE TZ_OPERACAO)` |
| **C7** | [plano-evolucao-erp.md](plano-evolucao-erp.md) §5.1 afirma que o bug do BI de logística "não há como corrigir sem mexer no OLTP" | **Incorreto.** `Coleta.coletada_em`, `AmostraMovimentacao.ocorrido_em`, `Malote.despachado_em` e `ProtocoloRecebimento.recebido_em` existem hoje e bastam. Nenhuma migration no OLTP. É o que permite o BI virar F2 ([plano-bi.md §1.6](plano-bi.md)) |

---

## 4. Decisões

### 4.1 Decididas — 02/08/2026

As três que bloqueavam código estão fechadas. **Nada mais impede F0, F1, F2 e F3 de começarem.**

| # | Decisão | Registro |
|:---:|---|---|
| **D1** | **Fuso da competência = `America/Recife`.** Vive em `TZ_OPERACAO` (`src/config.py`), usado por um único helper `competencia_de(instante)` e replicado literalmente em todo SQL de backfill | [ADR 0007](adr/0007-fuso-horario-da-competencia.md) · `accepted` |
| **D2** | **AgGrid — `streamlit-aggrid==1.2.1.post2`.** Spike da F0 **executado e verde**: sem conflito de dependências (Streamlit 1.60 e Altair 6.2.2 preservados), formatação pt-BR via `JsCode` funciona, frontend empacotado localmente. Fixado em `requirements.txt`; guarda permanente em `tests/test_aggrid_compat.py` (4 testes) | [ADR 0008](adr/0008-componente-unico-de-grid.md) · `accepted` |
| **D5** | **Faixa etária congelada no fato** (`sk_faixa_etaria` na linha de fato, valor vigente na data do fato gerador), não recalculada na dimensão | [ADR 0009](adr/0009-grao-chave-natural-e-medidas-derivadas-no-bi.md) · `accepted` |

### 4.2 Ainda em aberto

Nenhuma bloqueia o início. Todas podem ser decididas até a fase que as consome.

| # | Decisão | Bloqueia | Recomendação |
|:---:|---|---|---|
| **D3** | **Grão da guia = OS?** Escolhido 1 OS = 1 guia (SP/SADT canônico). Alguns convênios aceitam guia mensal por beneficiário | F7 | Manter OS. Se o professor esperava guia mensal, muda só o índice parcial e o agrupamento |
| **D4** | **Pagamento a maior** — capar no saldo e registrar divergência, ou permitir saldo negativo? | F10 | Capar. Saldo negativo volta a esconder o problema |
| **D6** | **Qual opção de OMOP** (A camada analítica / B vocabulário / C CDM completo) | F13 | B primeiro — é pré-requisito das outras duas e entrega valor real ao laboratório |

---

## 5. Divisão para 4 pessoas

A ordem das fases foi desenhada para que **três trilhas rodem em paralelo** logo depois da F0.

| Trilha | Fases | Escopo | Toca |
|---|---|---|---|
| **Frontend** | F0 (spike) → **F1** | `st.navigation`, `renderizar_grid`, `fragment`/`dialog`, `tratar_erros` | `pages/`, `src/ui*.py`, `src/ui_components/` |
| **BI** | **F2** → F12 | Modelo dimensional, ETL, métricas, Altair, 4 dashboards | `src/bi/`, `pages/bi_*.py` |
| **Modelo/Preço** | **F3** → F13 | Preço particular, vigência, catálogo de exames e analitos, regra do valor, OMOP | `src/cadastro/`, `src/laboratorial/` |
| **Faturamento** | F4 → F11 | Competência, item faturável, remessa, guia, glosa, divergências, financeiro | `src/faturamento/`, `src/financeiro/` |

- F1, F2 e F3 **não se tocam** — três pessoas em paralelo desde o primeiro dia depois da F0.
- A partir de F4 o caminho crítico do faturamento é sequencial; quem terminar sua trilha entra em F14 (segurança, independente de tudo) ou reforça o faturamento.
- F8 e F9 podem ser paralelizadas entre duas pessoas depois da F7.
- **Transversal** (mudança com aviso ao grupo): `src/db.py`, `src/ui.py`, RBAC, `alembic/`.

Donos sugeridos seguem a divisão de stacks já existente na `RESENHA` — **confirmar no grupo** (Aline, Clauderson, Gustavo, Victor).

---

## 6. Critério de pronto

Vale para **toda** fase, sem exceção:

1. `alembic upgrade head` OK em base limpa
2. `python -m src.seeder` OK em base limpa
3. `make test` verde
4. Query de reconciliação da fase batendo (tabela abaixo)
5. As telas afetadas percorridas em `docker compose up -d` sem quebrar

| Fase | Query / teste de reconciliação |
|:---:|---|
| F0 | 3 testes de regressão novos + os 165 existentes verdes |
| F1 | 26 telas percorridas; nenhum `st.rerun` global sobrando nas 6 telas de estado por linha |
| F2 | ETL rodado 2× produz **números idênticos**; `SUM(fato)` = `SUM(origem)` por fato; `DimTempo` sem buraco de mês |
| F3 | `COUNT(*) FROM procedimento_valores WHERE convenio_id IS NULL > 0`; o `EXCLUDE` prova ausência de sobreposição de vigência |
| F4 | `COUNT(DISTINCT date_trunc('month', liberado_em AT TIME ZONE TZ))` de `laudos` = nº de competências com laudo |
| F5 | `COUNT(itens_faturaveis)` = `COUNT(laudos WHERE status='LIBERADO')`; nenhum `guias_itens` órfão |
| F6 | `remessa.valor_apresentado` = `SUM(guias_itens.valor_faturado)` em todas as remessas |
| F7 | **Nenhuma guia com mais de um paciente** — a query da "explosão" retorna 0 |
| F8 | Item 100% glosado + reapresentação **volta** para `listar_a_faturar`; `SUM(glosas)` = `guias_itens.valor_glosado` |
| F9 | Fechar remessa sem preço em tabela é bloqueado e a divergência aparece no painel; detector rodado 2× não duplica linha |
| F10 | Receber R$1 de um título de R$1000 deixa **PARCIAL com saldo 999** (hoje marca PAGO) |
| F11 | `saldo_conta()` = `saldo_inicial + SUM(entradas) − SUM(saídas)` |
| F12 | `apurar(competência)` bate com o BI |

---

## 7. Rastreabilidade: apontamento do professor → fase

| Apontamento do professor | Fase | Entregável visível |
|---|:---:|---|
| Colocar mês do faturamento | F4 | Tela de apuração por competência |
| Regra de negócio do valor pelos procedimentos | F3 | Valor da tabela aplicado na OS, no laudo e na remessa |
| Tabela de exames | F3 | Catálogo enriquecido + catálogo de analitos |
| OMOP — padrão de dados de saúde | F13 | Conforme D6 |
| Por que lotes e não períodos / verificar por período | F4 + F6 | Competência é o eixo; remessa é só o envelope TISS |
| **Implementar período no BI** | **F2** | Filtro de período nas 4 páginas + série temporal correta |
| Fluxo de fechamento — por paciente — por lote | **F7** | 1 OS = 1 guia = 1 paciente; remessa agrupa guias |
| Contas — tabela separada por mês | F11 | Carteira por competência, regime caixa × competência |
| **Identificador de divergências** (lotes, valores) | **F9** | Painel de divergências, 14 tipos, 3 severidades |
| Fornecedores — grid e informações | F1 | AgGrid + cadastro completo |
| Compras — grid e produtos | F1 | AgGrid + ficha de insumo |
| IMPLEMENTAR/AJEITAR GRIDS — AgGrid | F1 | `renderizar_grid()` em todas as telas |
| Revisar UI & UX | F1 | `st.navigation` + `fragment` + `dialog` |
| **Altair melhor para BI** | **F2** | 10 gráficos migrados + drill-down |

---

## 7.1 Achado novo — N19: a suíte não roda no Windows

Descoberto ao rodar os testes durante o spike da F0. **Não estava em nenhum documento.**

[tests/test_laboratorio_page_imports.py:13,36](../tests/test_laboratorio_page_imports.py#L36) chama `Path.read_text()` **sem `encoding=`**. No Windows isso usa a codificação da locale (cp1252 em pt-BR); os arquivos do projeto são UTF-8. Dois arquivos com acento quebram a leitura:

```
src/seeder/catalogo.py    → UnicodeDecodeError na posição 4156
src/seeder/financeiro.py  → UnicodeDecodeError na posição 1526
```

`test_codebase_has_no_undefined_global_names` **falha sempre no Windows** e passa no Docker/Linux, onde a locale é UTF-8. É por isso que os documentos afirmam "165/165 passando" — a suíte só foi validada no container.

Impacto real: três das quatro pessoas da equipe desenvolvem no Windows e não conseguem rodar a suíte localmente. Correção: `read_text(encoding="utf-8")` nas duas chamadas. Entra na F0.

---

## 8. Dívida de documentação — ✅ quitada em 02/08/2026

Três documentos declaravam o projeto pronto e contradiziam os achados, então cada pessoa da equipe lia um estado diferente. Resolvido:

| Documento | O que foi feito |
|---|---|
| **[arquitetura.md](arquitetura.md)** | **Criado.** Passa a ser a referência de estado atual: fluxo, camadas, modelo de dados, módulos, BI, segurança, testes e pendências |
| [README.md](../README.md) | Tabela de status corrigida (Faturamento e Financeiro "em evolução", BI "reconstruído") + ponteiro para `arquitetura.md` |
| [CONTEXT.md](../CONTEXT.md) | Glossário atualizado com os termos de BI que passaram a existir |
| `revisao-final.md` | **Removido.** Auditoria de 28/07 que se declarava "9,5/10, 1 bug pendente" — contradita por 18 achados posteriores. As partes ainda válidas foram absorvidas por `arquitetura.md` |
| `RESENHA-E-PLANO-4-STACKS.md` | **Removido.** Declarava "backlog alta: vazio". O planejamento vive neste roadmap; o estado, em `arquitetura.md` |
| `doc.md` | **Removido.** Rascunho duplicado do README |
| `diff.patch` | **Removido.** Artefato solto na raiz |

> Os arquivos removidos continuam no histórico do git — nada foi perdido, só saiu do caminho.

### Ainda pendente

**Colisão de vocabulário na F6:** o `CONTEXT.md` define **Malote** e manda *evitar* "remessa" como sinônimo. A F6 introduz `RemessaFaturamento`, com significado completamente diferente. O glossário precisa ganhar **Competência**, **Remessa de Faturamento**, **Item Faturável**, **Divergência** e **Recurso de Glosa** **junto com as fases que os criam** — não antes, para o glossário não descrever o que não existe.
