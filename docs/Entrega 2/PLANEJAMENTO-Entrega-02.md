# Planejamento — Entrega 02: Modelagem da Base de Dados

**Disciplina:** Sistemas de Informação e Tecnologias (SIT)
**Projeto:** ERP LabVida — Laboratório de Análises Clínicas
**Equipe:** Aline Fernanda Soares Silva · Clauderson Branco Xavier · Gustavo Ferreira Wanderley · Victor Alexandre Saraiva Pimentel

> Este documento é o **plano de trabalho** da Entrega 02. Ele não é o entregável final em si — é o
> mapa que liga cada decisão da Entrega 01 (modelagem organizacional do ERP) ao modelo de dados que
> precisamos produzir, define o escopo, a divisão de tarefas e os critérios de avaliação a atender.

> **Pré-requisito concluído:** antes de avançar na Entrega 02, os 6 pontos avaliados como *"Atendeu
> Parcialmente"* na Entrega 01 (arquitetura técnica, camadas de código, módulo core, hierarquia
> arquitetural e estrutura visual) foram corrigidos em
> [`Entrega-01-Complemento-Arquitetura-Tecnica.md`](Entrega-01-Complemento-Arquitetura-Tecnica.md).
> A **camada de dados** ali descrita (PostgreSQL OLTP + Data Warehouse para BI) é a base que esta
> Entrega 02 detalha.

---

## 1. O que a Entrega 02 pede (e como traduzimos isso)

O enunciado pede a **modelagem inicial da base de dados** do ERP, garantindo:

| Requisito do enunciado | Como atendemos no modelo de dados |
|---|---|
| **Integração entre módulos** | Chaves estrangeiras (FKs) que conectam as tabelas dos módulos; a OS como entidade-espinha que atravessa Atendimento → Logística → Laboratorial → Faturamento → Financeiro. |
| **Consistência das informações** | Constraints (PK, FK, UNIQUE, CHECK, NOT NULL), normalização (3FN), tabelas de domínio/status em vez de texto livre. |
| **Rastreabilidade operacional** | Tabela de auditoria *append-only*, timestamps em todas as entidades operacionais, histórico de status da amostra e da OS (cadeia de custódia). |
| **Suporte às operações organizacionais** | Cada gatilho automático da Entrega 01 mapeado para uma transição de estado registrada no banco. |
| **Geração futura de indicadores e BI** | Modelagem operacional normalizada + esboço do modelo dimensional (esquema estrela) para o módulo de BI. |
| **Refletir o funcionamento da Entrega 01** | Mapeamento explícito módulo → entidades (Seção 4). Nada é inventado fora do que a Entrega 01 definiu. |

---

## 2. Decisões já tomadas

- **Profundidade:** MER **conceitual + lógico completo** — entidades, atributos, PKs, FKs, cardinalidades de todos os módulos. Sem DDL/SQL nesta etapa (foco em modelagem).
- **Entregáveis:** documento Markdown + **diagrama ER em Mermaid** em arquivo separado (renderizável/exportável).
- **SGBD de referência:** **PostgreSQL** (tipos `uuid`, `numeric`, `timestamptz`, `jsonb`; bom suporte a auditoria append-only e LGPD).

---

## 3. Entregáveis desta etapa

| # | Arquivo | Conteúdo |
|---|---|---|
| E1 | `Entrega-02-Modelagem-BD.md` | Documento principal: introdução, modelo conceitual, modelo lógico (dicionário de dados por módulo), regras de integridade, mapeamento de gatilhos, esboço BI, justificativa. |
| E2 | `diagramas/MER-conceitual.mmd` | Diagrama ER conceitual (entidades + relacionamentos, alto nível). |
| E3 | `diagramas/MER-logico.mmd` | Diagrama ER lógico completo (atributos, PKs, FKs, cardinalidades). |
| E4 | `diagramas/BI-esquema-estrela.mmd` | Esboço do modelo dimensional (fatos + dimensões) para o módulo de BI. |

> Os `.mmd` usam a sintaxe `erDiagram` do Mermaid — renderizam direto no GitHub e dá pra exportar PNG/SVG
> pelo [mermaid.live](https://mermaid.live) para colar no documento final entregue ao professor.

---

## 4. Mapeamento Módulo → Entidades (núcleo do trabalho)

Derivado diretamente das funcionalidades e regras de negócio da Entrega 01. Esta é a lista candidata de
tabelas — durante a modelagem confirmamos cada uma.

### 4.1 Cadastro
- `paciente` (dados sensíveis criptografados — LGPD)
- `medico` (solicitantes e responsáveis técnicos)
- `convenio` / `operadora`
- `plano_convenio` (vínculo convênio + regras)
- `procedimento` (catálogo, com código TUSS/TISS)
- `procedimento_valor` (vinculação procedimento ↔ valor contratual por convênio)
- `unidade` (laboratório central + 4 unidades de coleta)
- `setor`

### 4.2 Atendimento e Coleta
- `ordem_servico` (OS — identificador único; entidade-espinha do fluxo)
- `os_item` (procedimentos solicitados na OS)
- `autorizacao_convenio` (guia/autorização)
- `amostra` (etiqueta com código de barras/QR, vínculo com OS)
- `coleta` (coletor, data/hora)
- `os_status_historico` (rastreabilidade do estado da OS)

### 4.3 Logística de Amostras
- `malote` (origem, destino, data, hora, responsável)
- `malote_amostra` (associativa malote ↔ amostra)
- `amostra_movimentacao` (cadeia de custódia: coletada → trânsito → recebida)
- `protocolo_recebimento` (conferência de integridade)

### 4.4 Laboratorial
- `exame` / `os_item_resultado` (resultado vinculado ao item da OS)
- `bancada` / `equipamento` (analisadores clínicos)
- `valor_referencia` (validação de resultados)
- `laudo` (assinatura digital, liberação)
- `laudo_status_historico`
- `resultado_auditoria` (append-only — alterações em resultado clínico)

### 4.5 Faturamento
- `lote_faturamento`
- `guia_tiss` (XML TISS, pré-auditoria)
- `guia_item`
- `glosa` (motivo, operadora, unidade de origem)

### 4.6 Financeiro
- `titulo_receber` (gerado no fechamento do lote)
- `titulo_pagar` (gerado por compra aprovada)
- `movimento_caixa`
- `conciliacao_pagamento`
- `repasse`

### 4.7 Compras
- `fornecedor`
- `solicitacao_compra`
- `pedido_compra`
- `pedido_item`
- `recebimento_insumo`
- `insumo_material` (identificação, quantidade, finalidade)
- `estoque_movimento`

### 4.8 Serviços Compartilhados / Segurança (transversal)
- `usuario`
- `perfil` / `permissao` / `perfil_permissao` (controle de acesso por perfil)
- `auditoria_log` (append-only — LGPD, alterações sensíveis)

### 4.9 BI (modelo dimensional — esboço)
- Fatos: `fato_atendimento`, `fato_faturamento`, `fato_financeiro`, `fato_logistica`
- Dimensões: `dim_tempo`, `dim_unidade`, `dim_convenio`, `dim_procedimento`, `dim_paciente_anonimizado`

---

## 5. Mapeamento dos gatilhos da Entrega 01 → modelo de dados

A Seção 5 da Entrega 01 ("Impactos Automáticos") precisa estar **rastreável no banco**. Cada gatilho
vira uma transição de estado persistida:

| Gatilho (Entrega 01) | Como aparece no modelo de dados |
|---|---|
| Cadastro de paciente → disponibiliza p/ OS | FK `ordem_servico.paciente_id` |
| Abertura de OS → valida elegibilidade | `autorizacao_convenio` + status da OS |
| Registro de coleta → cria pendência logística | `amostra_movimentacao` (status `EM_TRANSITO`) |
| Recebimento de amostra → desbloqueia laboratorial | `protocolo_recebimento` + status `RECEBIDA` |
| Importação de resultado → revisão técnica | `os_item_resultado.status = AGUARDANDO_REVISAO` |
| Liberação de laudo → pré-auditoria | FK `guia_item` ← `laudo` |
| Fechamento de lote → títulos a receber | `lote_faturamento` gera `titulo_receber` |
| Baixa financeira → fluxo de caixa | `movimento_caixa` |
| Aprovação de compra → previsão de pagamento | `pedido_compra` gera `titulo_pagar` |
| Qualquer alteração → cubos de BI | tabelas-fato alimentadas via ETL |

---

## 6. Regras de integridade a refletir (da Seção 6 da Entrega 01)

- Paciente **único** por identificador → `UNIQUE` em CPF/identificador.
- Convênio precisa estar **ativo** → coluna `status` + CHECK na abertura da OS.
- Procedimento com **TUSS/TISS válido** → FK obrigatória para catálogo.
- OS com **identificador único** → PK/UNIQUE.
- Amostra só analisada **após recebimento** → status controlado por FK de movimentação.
- Laudo liberado só por **responsável técnico** → FK `usuario` + perfil.
- Auditoria **append-only / imutável** → tabelas sem UPDATE/DELETE (trigger ou convenção).
- Faturar só com **laudo liberado** → constraint lógica entre `guia_item` e `laudo`.
- Dados sensíveis **criptografados / LGPD** → colunas marcadas; anonimização no BI.

---

## 7. Divisão de tarefas sugerida (4 integrantes)

| Frente | Módulos | Responsável sugerido |
|---|---|---|
| **A — Cadastro & Atendimento** | Cadastro, Atendimento/Coleta (OS — espinha) | _(definir)_ |
| **B — Operação técnica** | Logística, Laboratorial | _(definir)_ |
| **C — Financeiro** | Faturamento, Financeiro, Compras | _(definir)_ |
| **D — Transversal & BI** | Usuários/Segurança/Auditoria, BI (estrela), consolidação do diagrama e do documento | _(definir)_ |

> Recomendação: cada um modela suas tabelas (atributos + tipos + FKs) num rascunho, e a frente D
> consolida tudo no diagrama único garantindo que as FKs entre frentes batem.

---

## 8. Critérios de avaliação a cobrir (checklist)

- [ ] Modelo **reflete fielmente** os módulos da Entrega 01 (nada inventado fora de escopo).
- [ ] Todas as **integrações** da Entrega 01 têm FK correspondente.
- [ ] Modelo **normalizado** (até 3FN) — sem redundância injustificada.
- [ ] **Rastreabilidade**: histórico de status + auditoria append-only.
- [ ] **Consistência**: constraints explícitas (PK, FK, UNIQUE, CHECK, NOT NULL).
- [ ] **LGPD**: dados sensíveis identificados e tratados.
- [ ] **BI**: caminho claro do operacional para os indicadores (esboço dimensional).
- [ ] Diagrama ER **legível** e dicionário de dados completo.
- [ ] Justificativa das decisões de modelagem.

---

## 9. Próximos passos imediatos

1. Validar este plano com a equipe (e ajustar a divisão da Seção 7).
2. Produzir `diagramas/MER-conceitual.mmd` (visão de alto nível primeiro — fecha o escopo de entidades).
3. Detalhar o modelo lógico módulo a módulo no documento principal.
4. Consolidar o `MER-logico.mmd` e validar FKs cruzadas entre frentes.
5. Esboçar o esquema estrela do BI.
6. Revisão final contra o checklist da Seção 8 e exportar diagramas para o documento entregue.
