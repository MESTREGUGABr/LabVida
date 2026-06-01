# Entrega 02 — Modelagem da Base de Dados do ERP LabVida

**Disciplina:** Sistemas de Informação e Tecnologias (SIT)
**Projeto:** ERP LabVida — Laboratório de Análises Clínicas
**Equipe:** Aline Fernanda Soares Silva · Clauderson Branco Xavier · Gustavo Ferreira Wanderley · Victor Alexandre Saraiva Pimentel
**Garanhuns — PE · 2026**

---

## Sumário

1. [Introdução](#1-introdução)
2. [Objetivos da modelagem](#2-objetivos-da-modelagem)
3. [Decisões de modelagem](#3-decisões-de-modelagem)
4. [Modelo conceitual](#4-modelo-conceitual)
5. [Modelo lógico — dicionário de dados por módulo](#5-modelo-lógico--dicionário-de-dados-por-módulo)
6. [Regras de integridade e consistência](#6-regras-de-integridade-e-consistência)
7. [Rastreabilidade e auditoria](#7-rastreabilidade-e-auditoria)
8. [Mapeamento dos gatilhos da Entrega 01](#8-mapeamento-dos-gatilhos-da-entrega-01)
9. [Modelo dimensional para BI](#9-modelo-dimensional-para-bi)
10. [Justificativa da modelagem](#10-justificativa-da-modelagem)

---

## 1. Introdução

Esta entrega apresenta a **modelagem inicial da base de dados** do ERP LabVida, traduzindo em estrutura
de dados a arquitetura organizacional definida na Entrega 01. O objetivo é garantir que as informações
da rede de laboratórios sejam **organizadas, relacionadas e armazenadas** de forma a sustentar a
integração entre módulos, a consistência das informações, a rastreabilidade operacional e a futura
geração de indicadores gerenciais (BI).

A modelagem reflete fielmente os sete módulos operacionais (Cadastro, Atendimento/Coleta, Logística,
Laboratorial, Faturamento, Financeiro, Compras), os serviços compartilhados de segurança e auditoria, e
a camada analítica de BI descritos na Entrega 01 e detalhados tecnicamente no
[Complemento de Arquitetura Técnica](Entrega-01-Complemento-Arquitetura-Tecnica.md).

## 2. Objetivos da modelagem

| Objetivo da Entrega | Como o modelo atende |
|---|---|
| **Integração entre módulos** | FKs conectando as tabelas dos módulos; a Ordem de Serviço (OS) como entidade-espinha que atravessa todo o fluxo. |
| **Consistência das informações** | Constraints (PK, FK, UNIQUE, CHECK, NOT NULL), normalização até 3FN, domínios controlados por colunas `status`. |
| **Rastreabilidade operacional** | Histórico de status (OS e amostra), cadeia de custódia, auditoria *append-only*, timestamps. |
| **Suporte às operações** | Cada gatilho automático da Entrega 01 vira uma transição de estado persistida. |
| **Indicadores e BI** | Base operacional normalizada (OLTP) + modelo dimensional em esquema estrela (OLAP). |

## 3. Decisões de modelagem

- **SGBD de referência:** PostgreSQL.
- **Chaves primárias:** `uuid` em todas as entidades operacionais — evita colisões entre unidades distribuídas e não expõe volume/sequência (boa prática de segurança).
- **Tipos adotados:** `uuid`, `varchar`, `numeric` (valores monetários — nunca `float`), `date`, `timestamptz` (datas com fuso), `boolean`, `jsonb` (payload de auditoria), `text` (XML TISS).
- **Normalização:** até a 3ª Forma Normal. Tabelas associativas resolvem os relacionamentos N:N (`malote_amostra`, `perfil_permissao`, `procedimento_valor`).
- **Domínios:** estados representados por colunas `status` com valores controlados (documentados via CHECK), evitando texto livre.
- **LGPD:** dados sensíveis do paciente são criptografados na origem; no BI o paciente aparece apenas anonimizado.
- **Separação OLTP/OLAP:** a base operacional não é consultada diretamente pelo BI; um processo ETL alimenta o Data Warehouse (visão *read-only*), preservando a performance das unidades.

## 4. Modelo conceitual

O modelo conceitual apresenta as entidades principais e seus relacionamentos em alto nível, sem detalhar
atributos. Ele evidencia o fluxo central da operação — do cadastro do paciente até o registro financeiro.

> Diagrama: [`diagramas/MER-conceitual.mmd`](diagramas/MER-conceitual.mmd)

**Entidades centrais e seu papel:**

- **PACIENTE / MEDICO / CONVENIO / PROCEDIMENTO / UNIDADE** — cadastros que habilitam toda a operação.
- **ORDEM_SERVICO (OS)** — entidade-espinha; nasce no atendimento e percorre todo o ciclo de vida.
- **AMOSTRA / COLETA / MALOTE** — materializam a cadeia de custódia rastreável.
- **RESULTADO / LAUDO** — produto técnico do laboratório.
- **LOTE_FATURAMENTO / GUIA_TISS / GLOSA** — faturamento de convênios.
- **TITULO_RECEBER / TITULO_PAGAR / MOVIMENTO_CAIXA** — efeitos financeiros.
- **USUARIO / PERFIL / AUDITORIA_LOG** — segurança e rastreabilidade transversais.

## 5. Modelo lógico — dicionário de dados por módulo

Diagrama completo (atributos, PKs, FKs, cardinalidades): [`diagramas/MER-logico.mmd`](diagramas/MER-logico.mmd)

> Convenções: **PK** = chave primária · **FK** = chave estrangeira · **UK** = chave única (UNIQUE).
> Todas as entidades operacionais possuem timestamp de criação (omitido nas tabelas por concisão quando
> não relevante à regra de negócio).

### 5.1 Cadastro

| Entidade | Atributos-chave | Observações |
|---|---|---|
| `paciente` | id (PK), cpf (UK), nome, data_nascimento, sexo, contato | cpf e contato **criptografados** (LGPD) |
| `medico` | id (PK), nome, crm (UK), uf_crm, responsavel_tecnico | flag de responsável técnico habilita liberação de laudo |
| `convenio` | id (PK), nome, registro_ans, status | status `ATIVO/INATIVO` controla uso em OS |
| `procedimento` | id (PK), codigo_tuss (UK), nome, setor | TUSS/TISS obrigatório |
| `procedimento_valor` | id (PK), procedimento_id (FK), convenio_id (FK), valor, vigencia_inicio | resolve N:N procedimento↔convênio com preço contratual |
| `unidade` | id (PK), nome, tipo (CENTRAL/COLETA), endereco | 1 central + 4 unidades de coleta |
| `setor` | id (PK), unidade_id (FK), nome | setores internos por unidade |

### 5.2 Atendimento e Coleta

| Entidade | Atributos-chave | Observações |
|---|---|---|
| `ordem_servico` | id (PK), codigo_os (UK), paciente_id (FK), medico_id (FK), convenio_id (FK), unidade_id (FK), status | **entidade-espinha**; codigo_os é o identificador único |
| `os_item` | id (PK), ordem_servico_id (FK), procedimento_id (FK), valor_negociado, status | um procedimento solicitado por linha |
| `autorizacao_convenio` | id (PK), ordem_servico_id (FK), numero_guia, status, validade | OS de convênio exige autorização válida |
| `amostra` | id (PK), ordem_servico_id (FK), codigo_barras (UK), tipo_material, status | etiqueta com código de barras/QR |
| `coleta` | id (PK), amostra_id (FK), coletor_id (FK), coletada_em | coletor = usuário autorizado |
| `os_status_historico` | id (PK), ordem_servico_id (FK), status, ocorrido_em, usuario_id (FK) | histórico de transições da OS |

### 5.3 Logística de Amostras

| Entidade | Atributos-chave | Observações |
|---|---|---|
| `malote` | id (PK), unidade_origem_id (FK), unidade_destino_id (FK), responsavel_id (FK), saida_em, status | origem, destino, data/hora e responsável obrigatórios |
| `malote_amostra` | id (PK), malote_id (FK), amostra_id (FK) | associativa N:N |
| `amostra_movimentacao` | id (PK), amostra_id (FK), status (COLETADA/EM_TRANSITO/RECEBIDA), ocorrido_em | **cadeia de custódia** |
| `protocolo_recebimento` | id (PK), malote_id (FK), recebedor_id (FK), integridade_ok, recebido_em | conferência de integridade no laboratório central |

### 5.4 Laboratorial

| Entidade | Atributos-chave | Observações |
|---|---|---|
| `equipamento` | id (PK), setor_id (FK), nome, protocolo (HL7/ASTM) | analisadores com interfaceamento |
| `valor_referencia` | id (PK), procedimento_id (FK), minimo, maximo, unidade_medida | validação de resultados |
| `resultado` | id (PK), os_item_id (FK), equipamento_id (FK), valor, status, importado_em | importado do equipamento → `AGUARDANDO_REVISAO` |
| `laudo` | id (PK), os_item_id (FK), responsavel_tecnico_id (FK), status, liberado_em, assinatura_digital | liberação só por responsável técnico |
| `resultado_auditoria` | id (PK), laudo_id (FK), usuario_id (FK), valor_anterior, valor_novo, ocorrido_em | **append-only** — toda alteração de resultado clínico |

### 5.5 Faturamento

| Entidade | Atributos-chave | Observações |
|---|---|---|
| `lote_faturamento` | id (PK), convenio_id (FK), status (ABERTO/FECHADO), fechado_em | fechamento gera títulos |
| `guia_tiss` | id (PK), lote_faturamento_id (FK), numero, status_pre_auditoria, xml_tiss | XML padrão TISS |
| `guia_item` | id (PK), guia_tiss_id (FK), laudo_id (FK), procedimento_id (FK), valor_faturado | só faturável com laudo liberado |
| `glosa` | id (PK), guia_item_id (FK), motivo, valor_glosado, unidade_origem_id (FK) | análise por motivo/operadora/unidade |

### 5.6 Financeiro

| Entidade | Atributos-chave | Observações |
|---|---|---|
| `titulo_receber` | id (PK), lote_faturamento_id (FK), valor, vencimento, status | gerado no fechamento do lote |
| `titulo_pagar` | id (PK), pedido_compra_id (FK), valor, vencimento, status | gerado por compra aprovada |
| `movimento_caixa` | id (PK), titulo_receber_id (FK), titulo_pagar_id (FK), tipo (ENTRADA/SAIDA), valor, ocorrido_em | alimenta fluxo de caixa |
| `conciliacao_pagamento` | id (PK), titulo_receber_id (FK), valor_recebido, divergencia | divergência faturado×recebido gera alerta |

### 5.7 Compras

| Entidade | Atributos-chave | Observações |
|---|---|---|
| `fornecedor` | id (PK), nome, cnpj (UK), status | cadastro prévio obrigatório |
| `solicitacao_compra` | id (PK), solicitante_id (FK), status, criada_em | registrada por usuário autorizado |
| `pedido_compra` | id (PK), solicitacao_compra_id (FK), fornecedor_id (FK), status, valor_total | aprovação gera previsão de pagamento |
| `pedido_item` | id (PK), pedido_compra_id (FK), insumo_material_id (FK), quantidade, valor_unitario | itens do pedido |
| `recebimento_insumo` | id (PK), pedido_compra_id (FK), recebido_em, conferido | recebimento atualiza estoque |
| `insumo_material` | id (PK), nome, finalidade, quantidade_estoque | identificação, quantidade e finalidade |
| `estoque_movimento` | id (PK), insumo_material_id (FK), tipo (ENTRADA/SAIDA), quantidade, ocorrido_em | apoia processos laboratoriais |

### 5.8 Segurança e Auditoria (transversal)

| Entidade | Atributos-chave | Observações |
|---|---|---|
| `usuario` | id (PK), perfil_id (FK), login (UK), senha_hash, ativo | autenticação |
| `perfil` | id (PK), nome | papéis (RBAC) |
| `permissao` | id (PK), codigo (UK), descricao | permissões atômicas |
| `perfil_permissao` | id (PK), perfil_id (FK), permissao_id (FK) | associativa N:N |
| `auditoria_log` | id (PK), usuario_id (FK), entidade, acao, dados (jsonb), ocorrido_em | **append-only** — alterações sensíveis (LGPD) |

## 6. Regras de integridade e consistência

Traduzindo as regras de negócio da Entrega 01 em mecanismos do banco:

| Regra de negócio (Entrega 01) | Mecanismo no modelo |
|---|---|
| Paciente único por identificador | `UNIQUE (paciente.cpf)` |
| Convênio precisa estar ativo na OS | `CHECK` lógico via `convenio.status = 'ATIVO'` na abertura |
| Procedimento com TUSS/TISS válido | `UNIQUE (procedimento.codigo_tuss)` + FK obrigatória em `os_item` |
| OS com identificador único | `UNIQUE (ordem_servico.codigo_os)` |
| Coleta só por usuário autorizado | FK `coleta.coletor_id → usuario` + verificação de permissão |
| Amostra só analisada após recebimento | status controlado por `amostra_movimentacao` |
| Laudo liberado só por responsável técnico | FK `laudo.responsavel_tecnico_id` + flag `medico.responsavel_tecnico` |
| Não faturar OS sem laudo liberado | FK obrigatória `guia_item.laudo_id` (laudo `LIBERADO`) |
| Lote fechado gera títulos | relação `lote_faturamento → titulo_receber` |
| Divergência faturado×recebido gera alerta | `conciliacao_pagamento.divergencia` |
| Auditoria imutável | tabelas `*_auditoria` e `auditoria_log` **append-only** (sem UPDATE/DELETE) |
| Dados sensíveis / LGPD | colunas criptografadas + anonimização no BI |

## 7. Rastreabilidade e auditoria

A rastreabilidade é garantida por três mecanismos:

1. **Histórico de status** — `os_status_historico` e `amostra_movimentacao` registram cada transição com data/hora e responsável, permitindo reconstruir todo o ciclo de vida da OS e a cadeia de custódia da amostra.
2. **Auditoria clínica append-only** — `resultado_auditoria` registra valor anterior e novo a cada alteração de resultado, sem sobrescrita (exigência regulatória).
3. **Auditoria geral append-only** — `auditoria_log` (jsonb) captura ações sensíveis de qualquer entidade, atendendo à LGPD e à governança da Entrega 01.

## 8. Mapeamento dos gatilhos da Entrega 01

Cada "impacto automático" da Seção 5 da Entrega 01 corresponde a uma operação rastreável no banco:

| Gatilho | Efeito no modelo de dados |
|---|---|
| Cadastro de paciente → OS | habilita FK `ordem_servico.paciente_id` |
| Abertura de OS → valida elegibilidade | cria `autorizacao_convenio` |
| Registro de coleta → pendência logística | insere `amostra_movimentacao (EM_TRANSITO)` |
| Recebimento de amostra → libera laboratorial | `protocolo_recebimento` + `amostra_movimentacao (RECEBIDA)` |
| Importação de resultado → revisão técnica | `resultado.status = AGUARDANDO_REVISAO` |
| Liberação de laudo → pré-auditoria | `laudo.status = LIBERADO` habilita `guia_item` |
| Fechamento de lote → títulos a receber | `lote_faturamento (FECHADO)` gera `titulo_receber` |
| Baixa financeira → fluxo de caixa | insere `movimento_caixa` |
| Aprovação de compra → previsão de pagamento | `pedido_compra (APROVADO)` gera `titulo_pagar` |
| Qualquer alteração → BI | replicação via ETL para as tabelas-fato |

## 9. Modelo dimensional para BI

Para suportar indicadores sem comprometer a performance operacional, o BI usa um **esquema estrela**
separado (OLAP), alimentado por ETL a partir da base operacional. O paciente aparece **anonimizado**
(LGPD), e o acesso é *read-only*.

> Diagrama: [`diagramas/BI-esquema-estrela.mmd`](diagramas/BI-esquema-estrela.mmd)

**Tabelas-fato** (métricas): `fato_atendimento`, `fato_faturamento`, `fato_financeiro`, `fato_logistica`.
**Dimensões** (contexto): `dim_tempo`, `dim_unidade`, `dim_convenio`, `dim_procedimento`, `dim_paciente_anon`.

Indicadores suportados (conforme módulo BI da Entrega 01): produtividade técnica, ticket médio por
exame/convênio/unidade, taxa de glosas, rentabilidade, eficiência da cadeia logística e demanda preditiva.

## 10. Justificativa da modelagem

A modelagem proposta reflete diretamente a arquitetura organizacional da Entrega 01: cada módulo
funcional corresponde a um conjunto coeso de tabelas, e as integrações entre setores se materializam como
chaves estrangeiras. A escolha de um **banco relacional normalizado** (até 3FN) garante consistência e
elimina a duplicidade de dados — um dos problemas centrais do diagnóstico da LabVida.

A **Ordem de Serviço como entidade-espinha** assegura a integração ponta a ponta do fluxo operacional,
enquanto as estruturas de **histórico de status e auditoria append-only** entregam a rastreabilidade
clínica e regulatória exigida. A separação entre base operacional (OLTP) e camada analítica (OLAP via
esquema estrela) viabiliza os indicadores gerenciais e o BI sem impactar as operações em tempo real das
unidades, respeitando a LGPD pela anonimização dos dados sensíveis. Em conjunto, a modelagem sustenta a
integração, a consistência, a rastreabilidade e a inteligência gerencial que motivaram a adoção do ERP.
