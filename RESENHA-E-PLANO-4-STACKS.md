# LabVida — Resenha do Projeto + Plano de Desenvolvimento em 4 Stacks

> Documento-base para a equipe. Lê de cima pra baixo: primeiro **o que é** e **por que é diferente**,
> depois **como já está**, depois **como a gente desenvolve** e, no fim, **a divisão das 4 trilhas
> (stacks)** com dono, escopo e itens a fazer. Pode copiar e mandar no grupo.
>
> **Última atualização:** 2026-07-26 (2) — **Stacks A, B e C concluídas** e **Stack D em grande parte
> implementada**: RBAC efetivo (gate no shell), **auditoria append-only plugada nos services**, **LGPD
> aplicada** (CPF criptografado), BI com ETL + 3 dashboards, navegação unificada + design system.
> **Suíte completa verde: 138 testes.** ✅ Heads paralelas do Alembic **resolvidas** (merge `0012`).
> Ver §4 (estado atual) e §10.
>
> Fontes vivas no repo: `README.md` (visão + como rodar), `CONTEXT.md` (glossário de domínio),
> `docs/Entrega 1/Entrega-01-Complemento-Arquitetura-Tecnica.md` (camadas/arquitetura técnica),
> `docs/Entrega 2/Entrega-02-Modelagem-BD.md` (modelo de dados), `docs/Entrega 3/Entrega-03-Integracao-Organizacional.md`
> (integração/eventos), `docs/Entrega 2/diagramas/*.mmd` (MER + esquema estrela), `docs/adr/` (decisões).

---

## 0. TL;DR (resumo executivo)

- **O que é:** LabVida é um **ERP acadêmico para uma rede regional de laboratórios de análises
  clínicas** (1 laboratório central + 4 unidades de coleta), cobrindo o ciclo completo
  **Cadastro → Atendimento/Coleta → Logística → Laboratorial → Faturamento → Financeiro**, com **BI**
  alimentado por todos os módulos.
- **Diferencial:** não é um "CRUD de laboratório". Ele nasce de uma **engenharia de ERP de verdade** —
  a **Ordem de Serviço (OS) como entidade-espinha**, impactos automáticos por eventos entre setores,
  camadas Controller → Service → Repository, auditoria *append-only*, rastreabilidade clínica (cadeia de
  custódia), RBAC e separação operacional/analítica (OLTP/OLAP). Isso dá **consistência e
  rastreabilidade ponta a ponta** num protótipo acadêmico.
- **Onde está:** **fundação + Stacks A, B e C funcionais + Stack D em grande parte implementada.** Login
  Google (Auth0/PKCE), infra Docker + Alembic + pytest, **modelagem completa no papel** (Entregas 02 e 03),
  **fundação de dados** (`src/db.py`), **Stack A** (cadastros, atendimento/coleta e OS), **Stack B**
  (malotes, cadeia de custódia, recebimento, equipamentos, valores de referência, resultados e laudos +
  esteira de bancada + cancelamento coerente de OS/itens), **Stack C** (faturamento com guias/lotes e
  glosas, financeiro com títulos a receber/pagar, caixa e conciliação, compras com fornecedores, pedidos e
  estoque) e boa parte da **Stack D** (RBAC efetivo com gate por permissão no shell + gestão de usuários,
  auditoria *append-only* **plugada nos services**, **LGPD com CPF criptografado (Fernet) + hash**, BI com
  esquema estrela, ETL e 3 dashboards, navegação unificada + design system). Tudo em fatias verticais
  (migration → model → repository → service → DTO/validação → tela → testes), com **suíte completa verde:
  138 testes**. Restam apenas evoluções (ETL incremental do BI, rotação automatizada da chave LGPD,
  fluxo de caixa) e a **execução** do deploy — o roteiro está no `DEPLOY.md` (§4.3/§8).
- **Contexto:** projeto da disciplina **Sistemas de Informação e Tecnologias (SIT)** — Ciência da
  Computação, **UFAPE** (Garanhuns-PE, 2026). Equipe de 4.
- **O plano:** evoluir o produto dividindo o trabalho em **4 stacks verticais** (cada pessoa dona de um
  conjunto de módulos, do banco à tela), com processo de desenvolvimento comum.

---

## 1. Visão do produto — o que é o LabVida

O LabVida parte de um **diagnóstico organizacional real** de uma rede de laboratórios: baixa integração
entre sistemas, logística manual de amostras sem rastreamento, faturamento de convênios crítico (glosas)
e ausência de indicadores gerenciais. A resposta é um **ERP integrado** em que o dado nasce uma vez e
circula por todos os setores, organizado em torno da **Ordem de Serviço (OS)**:

```
Cadastro → Atendimento e Coleta → Logística de Amostras → Laboratorial → Faturamento → Financeiro
                                                                                          ↳ BI (alimentado por todos)
                                                              Compras → (insumos / contas a pagar)
```

- **Multi-unidade:** uma central + quatro unidades de coleta. Toda entidade operacional sabe **em que
  unidade** ocorreu; a gestão enxerga o consolidado e unidade a unidade.
- **Domínio clínico-regulatório:** códigos **TUSS/TISS**, **guias** e **glosas** de convênio, **laudo**
  liberado só por responsável técnico, **cadeia de custódia** da amostra e **LGPD** sobre dados do paciente.

**Público-alvo (cenário do projeto):** rede de laboratórios de pequeno/médio porte que precisa integrar
atendimento, logística entre unidades, processo técnico, faturamento de convênios e indicadores — sem
controles paralelos em planilhas.

**Fora de escopo (proposital, por ser protótipo acadêmico):** interfaceamento real com analisadores
(HL7/ASTM) e envio real de XML TISS a operadoras ficam como **modelados, não integrados**; o foco da
implementação é o fluxo de dados ponta a ponta dentro do ERP.

---

## 2. Por que o LabVida não é um CRUD — o DNA arquitetural

O LabVida foi **modelado com padrões de ERP** antes de virar código (Entregas 01–03). É isso que separa
o produto de um amontoado de telas com `INSERT`/`UPDATE`. Cada padrão abaixo **já está definido nas docs**
e é o que as stacks devem **preservar** ao implementar:

| Padrão arquitetural | Como aparece no LabVida | Por que importa |
|---|---|---|
| **Entidade-espinha** | A **Ordem de Serviço (OS)** atravessa atendimento → coleta → logística → laboratório → faturamento → financeiro | Tudo gira em torno de um fato central, único e rastreável (`codigo_os`) |
| **Camadas** Controller → Service → Repository | UI (Streamlit `pages/`) → **services** (regra) → **repositories** (SQLAlchemy) | Regra de negócio isolada e testável, sem SQL espalhado na tela |
| **Impactos automáticos por eventos** | OS aberta → demanda de coleta; coleta → pendência logística; laudo liberado → item faturável; lote fechado → título a receber | Consistência: um setor reage ao outro sem redigitação |
| **Transições de estado persistidas** | `os_status_historico`, `amostra_movimentacao` (cadeia de custódia) | Dá pra reconstruir todo o ciclo de vida da OS e da amostra |
| **Auditoria append-only** | `auditoria_log` (jsonb) e `resultado_auditoria` (valor anterior/novo) — sem UPDATE/DELETE | Rastreabilidade clínica e regulatória; exigência de governança/LGPD |
| **RBAC** (perfil → permissão) | `usuario`/`perfil`/`permissao`/`perfil_permissao`; páginas gated por permissão no `shell()` | Cada um faz só o que pode (**efetivo**; acesso plano só como fallback p/ usuário sem perfil — ver §2.1) |
| **Escopo por unidade** | Entidades operacionais carregam `unidade_id` | Base para segregar acesso e medir desempenho por unidade |
| **Separação OLTP/OLAP** | Base operacional normalizada + **esquema estrela** (fatos/dimensões) alimentado por ETL; BI *read-only* | Dashboards não pesam na operação das unidades |
| **Boas práticas de dado** | PK `uuid` · `numeric` p/ dinheiro (nunca `float`) · `timestamptz` · domínios via colunas `status` | Sem colisão entre unidades, sem bug de centavo, sem fuso quebrado |
| **LGPD por design** | Dados sensíveis do paciente criptografados na origem; paciente **anonimizado** no BI | Privacidade tratada no modelo, não como remendo |

> **Resumo do diferencial:** integração por entidade-espinha + rastreabilidade (status histórico + cadeia
> de custódia + auditoria imutável) + separação OLTP/OLAP + LGPD, tudo já desenhado na modelagem. O
> trabalho das stacks é **implementar mantendo esses padrões** — não atalhar com CRUD solto.

### 2.1 Onde a engenharia ainda é "no papel" (ser honesto)

- **RBAC:** agora **efetivo** — perfil→permissão implementados (`src/rbac/`), com **gate no `shell()`**
  (`permissao=...` por página) e tela de gestão de usuários/perfis (`pages/admin_usuarios.py`). O acesso
  plano do ADR 0002 virou **fallback**: usuário **sem perfil atribuído** ainda entra com acesso amplo
  (compatibilidade), mas assim que ganha um perfil os gates valem. Falta atribuir perfis por padrão e
  revisar a granularidade das permissões por página.
- **Auditoria append-only:** `auditoria_log` (jsonb) + helper `registrar_auditoria` (`src/auditoria/`)
  **plugados nas operações sensíveis**: abertura/cancelamento de OS e de item, registro de coleta,
  liberação de laudo e fechamento de lote de faturamento. O laboratorial mantém também sua auditoria de
  valores (`resultado_auditoria`). Ampliar para os demais movimentos financeiros é evolução natural.
- **LGPD:** **implementada** — o CPF do paciente **deixou de ser texto puro**: agora é `cpf_encrypted`
  (Fernet) + `cpf_hash` (SHA-256, único) com property que descriptografa (`src/lgpd/`). Depende da env
  **`LGPD_ENCRYPTION_KEY`**. Anonimização do paciente no BI ainda a confirmar.
- **BI:** **implementado** — esquema estrela (fatos/dimensões em `src/bi/models.py`), **ETL**
  (`src/bi/etl.py`) e **3 dashboards** (produtividade, logística, financeiro). Profundidade/atualização do
  ETL segue evoluindo.
- **Eventos/impactos automáticos:** a Entrega 03 descreve o barramento de eventos; na implementação
  atual eles são **transições de estado em service + persistência** (não há fila/mensageria no protótipo).
- **Integrações externas TISS/HL7/ASTM:** seguem **modeladas, não integradas** — a integração real com
  analisadores e operadoras está fora do escopo do protótipo.

---

## 3. Arquitetura técnica

**Stack (decisão obrigatória da disciplina — `docs/adr/0001`):** **Python 3.12** · **Streamlit**
(frontend) · **PostgreSQL** · **SQLAlchemy** + **Alembic** (ORM/migrations) · **Pydantic** (validação) ·
**Auth0** (login Google, OAuth2/OIDC + PKCE) · **httpx** · **Docker Compose** · **pytest**.

> ⚠️ **Particularidades do Streamlit** (diferente de um framework web "tradicional"): a página
> **re-executa de cima a baixo a cada interação** (rerun); estado de sessão vive em `st.session_state`;
> multipage é por arquivos em `pages/`. **Não** coloque regra de negócio na página — a página só lê
> entrada, chama o **service** e renderiza. Nada de SQL na tela.

### 3.1 Camadas (alvo de organização do código)

A Entrega 01 (complemento) define Controller → Service → Repository. Traduzido para a stack atual:

A organização real ficou **por pacote de módulo (fatia vertical)**, não camada-primeiro — isso casa melhor
com a divisão em 4 stacks (cada dono é dono de um pacote `src/<modulo>/`). O Cadastro de Pacientes é o
**template de referência** que B/C/D devem seguir:

```
app.py                  # entrada: tela de login (Auth0/Google) + roteamento pós-login  -> JÁ EXISTE
pages/                  # telas por módulo (UI = "controllers" do Streamlit)
  home.py               # home pós-login + links de navegação                            -> JÁ EXISTE
  cadastro_pacientes.py # CRUD de Paciente (cadastrar/listar/editar/inativar)            -> JÁ EXISTE
src/
  auth.py               # OAuth2/OIDC + PKCE (Auth0)                                      -> JÁ EXISTE
  config.py             # carga de env/config (get_auth_config, get_database_url)         -> JÁ EXISTE
  db.py                 # engine + sessionmaker + session_scope() + Base (DeclarativeBase)-> JÁ EXISTE
  rbac.py               # (a criar) papéis/permissões — espelho tipado das tabelas
  cadastro/             # FATIA VERTICAL (template): pacote do módulo                      -> JÁ EXISTE
    models.py           #   modelo SQLAlchemy (Paciente)
    repository.py       #   acesso a dados (queries SQLAlchemy isoladas; nada de regra)
    service.py          #   regra de negócio (criar/atualizar/inativar; checa CPF duplicado)
    dtos.py             #   DTOs Pydantic (Create/Update/Read) + enum SexoPaciente
    validators.py       #   normalização/validação (CPF c/ dígito verificador, telefone, nome)
    errors.py           #   exceções de domínio (CpfPacienteDuplicado, PacienteNaoEncontrado)
  seeder/               # geração de dados de exemplo (Faker)                             -> JÁ EXISTE
alembic/versions/       # toda mudança de schema é uma migration versionada
  0003_criar_tabela_pacientes.py   # 1ª migration (base, down_revision=None)             -> JÁ EXISTE
tests/                  # pytest (AppTest do Streamlit + testes de dtos/validators/service)
docs/                   # Entregas 01–03, ADRs, diagramas (fontes da modelagem)
```

> **Convenção firmada (seguir em B/C/D):** módulo = pacote `src/<modulo>/`; cada **entidade** é um
> **sub-pacote** `src/<modulo>/<entidade>/` com `models · repository · service · dtos · (validators) ·
> errors` (ex.: `src/cadastro/medico/`, `src/atendimento/ordem_servico/`). Camada Streamlit fica em
> `pages/`. Operações multi-entidade rodam numa transação no service (ex.: `abrir_os`, `registrar_coleta`).
> **Não** usar layout camada-primeiro (`src/models/`, `src/repositories/`). Exceção histórica: o
> **Paciente** é flat em `src/cadastro/` (protótipo original) — pode ser migrado para `src/cadastro/paciente/`
> depois, sem urgência.

**Fluxo de uma operação (como já roda no Cadastro):** página (Streamlit) abre `session_scope()`, monta o
**DTO Pydantic** (que normaliza/valida a entrada) → chama o **service** (regra) → service usa o
**repository** (dados via SQLAlchemy) e dá `commit`. Operações que afetam vários módulos devem rodar
dentro de **uma transação** (atomicidade) e registrar **transição de estado + auditoria**.

### 3.2 Multi-unidade & segurança

- Toda entidade **operacional** carrega `unidade_id` (OS, amostra, malote, lote, título…).
- **Cadastros são compartilhados** (paciente/médico/convênio/procedimento são globais); o que é por
  unidade é a **operação** (qual unidade abriu a OS, coletou, recebeu o malote).
- **Auth 100% server-side** via Auth0; sessão em `st.session_state`. Login com Google identifica **quem**
  executou cada ação (rastreabilidade) — base para a auditoria e para o RBAC futuro.
- **LGPD:** dados sensíveis do paciente (CPF, contato) **criptografados na origem**; no BI, paciente entra
  **anonimizado**.

### 3.3 Eventos / impactos automáticos

| Origem | Impacto automático | Onde (na implementação) |
|---|---|---|
| OS aberta | cria itens da OS + valida convênio/autorização + gera demanda de coleta | service `atendimento` + status da OS |
| Coleta registrada | amostra → `COLETADA` + abre `amostra_movimentacao` (pendência logística) | service `coleta` (transição + auditoria) |
| Amostra recebida no central | `protocolo_recebimento` + amostra → `RECEBIDA` (desbloqueia laboratório) | service `logistica` |
| Laudo liberado (resp. técnico) | item vira **faturável** (habilita `guia_item`) + auditoria | service `laboratorial` |
| Lote de faturamento fechado | gera **título a receber** no financeiro | service `faturamento` (transação) |
| Compra aprovada | gera **título a pagar** + previsão de recebimento de insumo | service `compras` |
| Qualquer evento operacional | alimenta os fatos do BI | ETL/agregação (futuro) |

Regra de ouro: **transacional → uma transação no banco (service)**; **analítico/pesado → ETL/BI separado**.

---

## 4. Estado atual — o que JÁ está pronto

**Fundação concretizada + Stacks A, B e C implementadas + Stack D em grande parte implementada. Permanecem
acabamentos transversais (auditoria plugada nos services, deploy/hardening), a correção das heads paralelas
do Alembic (§8) e melhorias pontuais.**

### 4.1 Já funciona (código)

| Item | O que faz | Onde |
|---|---|---|
| **Login Google** | OAuth2/OIDC com **PKCE** via Auth0, troca de código, `userinfo`, logout | `src/auth.py`, `app.py` |
| **Carga de config** | lê `.env` (Auth0 + `DATABASE_URL`); `get_auth_config`/`get_database_url` | `src/config.py` |
| **Home pós-login** | guarda de sessão, saudação, **link p/ Cadastro de Pacientes**, "Sair" | `pages/home.py` |
| **Fundação de dados** ⭐ | `engine` + `sessionmaker` + **`session_scope()`** (context manager) + `Base` (DeclarativeBase) | `src/db.py` |
| **Cadastro de Pacientes** ⭐ | **fatia vertical completa**: model → repository → service → DTO/validação → tela (CRUD: cadastrar / listar ativos / editar / inativar com *soft-delete*) | `src/cadastro/*`, `pages/cadastro_pacientes.py` |
| **Cadastros Stack A** ⭐⭐ | médico (flag responsável técnico, CRM+UF único), convênio (status ATIVO/INATIVO), procedimento (TUSS único) + valor por convênio, unidade (CENTRAL/COLETA) + setor — cada um fatia vertical + tela | `src/cadastro/{medico,convenio,procedimento,unidade}/*`, `pages/cadastro_*.py` |
| **Atendimento / OS** ⭐⭐ | **abertura da Ordem de Serviço** (espinha): `codigo_os` único, itens, validação de paciente/unidade/médico/convênio ativo e valor; `os_status_historico`; autorização de convênio | `src/atendimento/ordem_servico/*`, `src/atendimento/autorizacao/*`, `pages/atendimento_os.py` |
| **Coleta / cadeia de custódia** ⭐⭐ | registro de coleta gera **amostra** (código de barras, status COLETADA) + vincula coletor + transiciona a OS — tudo numa transação | `src/atendimento/amostra/*`, `pages/atendimento_coleta.py` |
| **`usuario` mínima** ⭐⭐ | identidade do Auth0 sincronizada em `usuarios` no login (ator de coleta/histórico) — base enxuta que a Stack D estende | `src/usuario/*`, `app.py` |
| **Logística / cadeia de custódia** ⭐⭐⭐ | malote, associação de amostras, despacho, movimentações `COLETADA → EM_TRANSITO → RECEBIDA/REJEITADA`, protocolo de recebimento e transição da OS para `EM_ANALISE` | `src/logistica/*`, `pages/logistica_*.py` |
| **Laboratorial** ⭐⭐⭐ | cadastro de equipamentos e valores de referência; registro/auditoria de resultados; criação e liberação de laudos; **esteira de bancada** | `src/laboratorial/*`, `pages/laboratorio_*.py` |
| **Cancelamento de OS** ⭐⭐⭐ | cancelamento coerente de OS inteira ou item a item, com regras de estado + conclusão automática da OS ao liberar o último laudo | `src/atendimento/ordem_servico/*`, `pages/atendimento_os.py` |
| **Faturamento** 🟧 | guias/itens **a partir de laudo liberado**, agrupamento em lote, fechamento do lote → **título a receber**; glosas por motivo/operadora | `src/faturamento/{lote_faturamento,glosa}/*`, `pages/faturamento_*.py` |
| **Financeiro** 🟧 | títulos a receber e a pagar, movimento de caixa e conciliação de pagamento (faturado × recebido) | `src/financeiro/{titulo_receber,titulo_pagar,movimento_caixa,conciliacao_pagamento}/*`, `pages/financeiro_*.py` |
| **Compras & Estoque** 🟧 | fornecedores, pedidos de compra (→ **título a pagar**), insumos e movimento de estoque | `src/compras/{fornecedor,pedido_compra,insumo}/*`, `pages/compras_*.py` |
| **RBAC efetivo** 🟪 | perfil→permissão + **gate por página no `shell()`** (`permissao=...`) + tela de gestão de usuários/perfis e "meu perfil"; seeder de perfis | `src/rbac/*`, `pages/admin_usuarios.py`, `pages/meu_perfil.py`, `src/seeder/rbac.py` |
| **Auditoria append-only** 🟪 | tabela `auditoria_log` (jsonb) + helper `registrar_auditoria`, **plugado** nas operações sensíveis (abrir/cancelar OS e item, coleta, liberar laudo, fechar lote) | `src/auditoria/*` + services de `atendimento`/`laboratorial`/`faturamento` |
| **LGPD (CPF criptografado)** 🟪 | CPF do paciente agora `cpf_encrypted` (Fernet) + `cpf_hash` (SHA-256, único); property descriptografa; máscara na UI | `src/lgpd/__init__.py`, `src/cadastro/models.py` |
| **BI (OLAP)** 🟪 | esquema estrela (fatos/dimensões), **ETL** a partir do operacional e **3 dashboards** (produtividade, logística, financeiro) | `src/bi/*`, `pages/bi_*.py` |
| **Navegação unificada + design system** 🟪 | `shell()` (login gate + page config + CSS + RBAC), menu lateral, tema institucional, componentes reutilizáveis (cabeçalho, seção, empty state, KPI card, badge…) | `src/ui.py`, `src/ui_components/*`, `src/ui_theme.py`, `src/ui_icons.py`, `src/ui_css.py` |
| **Migration Stack C** 🟧 | tabelas de faturamento/financeiro/compras + ajustes (`titulos_pagar` nullable, lote sem convênio) | `alembic/versions/0006_stack_c_faturamento.py`, `0007_*`, `0008_*` |
| **Migration Stack D** 🟪 | RBAC/auditoria, CPF criptografado (LGPD) e esquema estrela (BI) | `alembic/versions/0009_rbac_auditoria.py`, `0010_lgpd_cpf_encrypted.py`, `0011_bi_esquema_estrela.py` |
| **Migration `0004`** ⭐⭐ | 13 tabelas da Stack A encadeadas na head `0003` (CHECK de domínios de status, FKs, índices únicos) | `alembic/versions/0004_*.py` |
| **Migration Stack B** ⭐⭐⭐ | tabelas de logística e laboratorial encadeadas após Stack A | `alembic/versions/0005_stack_b_logistica.py`, `alembic/versions/f6ccac7706b1_add_laboratorial_models.py` |
| **Seeder de cadastros** ⭐⭐ | popula unidades/convênios/procedimentos+valores/médicos (insere se vazio) p/ abrir OS na demo | `src/seeder/cadastros.py` |
| **Guarda de sessão** ⭐⭐ | helper `exigir_login()` — agora encapsulado pelo `shell()` da Stack D (login gate + RBAC + CSS) | `src/ui.py` |
| **1ª migration** ⭐ | cria tabela `pacientes` (PK `uuid`, CPF `unique`, enum `sexo_paciente`, flag `ativo`) | `alembic/versions/0003_*.py` |
| **Seeder de pacientes** ⭐ | popula Pacientes de exemplo com **Faker** (CPF válido, telefone, sexo) — `make seeder` | `src/seeder/*` |
| **Infra Docker** | `docker-compose` (app + Postgres 16 + serviços de teste), `Dockerfile` (Python 3.12-slim, não-root) | `docker-compose.yml`, `Dockerfile` |
| **Migrations** | Alembic configurado, **autogenerate ligado** (`env.py` lê `Base.metadata`); aplica no boot | `alembic/`, `alembic.ini` |
| **Testes** | pytest: `AppTest` (login/home) + DTOs/validators (unit) + services (integração via Postgres de teste); cobre cadastros, atendimento, logística, laboratorial, faturamento, financeiro, compras, RBAC, LGPD, auditoria e BI — **138 testes (suíte verde)** | `tests/` (subpasta por módulo) |
| **Automação** | `Makefile` (`up/down/test/migrate/revision/seeder/clean`) | `Makefile` |

> ⭐ = fundação/Cadastro de Pacientes. ⭐⭐ = Stack A. ⭐⭐⭐ = Stack B. 🟧 = Stack C. 🟪 = Stack D.

### 4.2 Já modelado (papel — base para implementar)

- **Modelagem de dados completa** (Entrega 02): dicionário de dados dos 8 módulos + transversal, MER
  conceitual e lógico (`.mmd`), regras de integridade, mapeamento dos gatilhos e **esquema estrela** do BI.
- **Integração organizacional** (Entrega 03): eventos entre setores, rastreabilidade ponta a ponta,
  cenário integrado demonstrativo, indicadores gerenciais.
- **Arquitetura técnica** (Entrega 01 — complemento): camadas, módulo *core* (ciclo da OS), hierarquia
  arquitetural (operacional/analítica/estratégica/compartilhada).
- **Glossário de domínio** (`CONTEXT.md`) e **3 ADRs** (stack; autenticação/RBAC mínimo; granularidade de
  analitos laboratoriais).

### 4.3 Ainda NÃO existe / pendente (o que falta)

- ✅ **Heads paralelas no Alembic — RESOLVIDO:** criada a migration de merge `0012_merge_heads_c_d`
  (mergepoint de `0009_cancelamento_item` + `0011_bi_esquema_estrela`). `alembic upgrade head` aplica a
  cadeia completa em banco limpo (validado na suíte).
- ✅ **Auditoria plugada — RESOLVIDO:** `registrar_auditoria` é chamado em abrir/cancelar OS e item,
  registro de coleta, liberação de laudo e fechamento de lote. Cobertura por testes de wiring.
- ✅ **LGPD_ENCRYPTION_KEY — RESOLVIDO:** adicionada ao `.env.example`; corrigida a chave de teste inválida
  no `docker-compose`; `tests/conftest.py` garante uma chave Fernet válida. (Bug: a chave de teste anterior
  não era um Fernet válido e quebrava a suíte que cria paciente.)
- ✅ **Anonimização no BI — REFORÇADA:** o BI já não carregava PII; agora o `id_origem` do paciente é um
  **hash SHA-256** (não o UUID cru), impedindo join trivial de volta a `pacientes` (migração `0013` + ETL).
- ✅ **RBAC — perfil por padrão:** novo usuário recebe perfil no login (bootstrap: 1º vira `admin`, demais
  `visualizador`), encerrando o acesso amplo por ausência de perfil. Coberto por testes.
- ✅ **Auditoria financeira:** `registrar_auditoria` também em baixa de título (receber/pagar) e registro
  de glosa, com testes.
- ✅ **Busca/paginação:** telas de Pacientes e de OS ganharam busca (nome/código) + filtro de status (OS)
  e limite de exibição.
- ✅ **Deploy — guia + template:** `DEPLOY.md` e `.env.production.example` com passo a passo e checklist de
  hardening (Auth0 leaked password, segredos, chave LGPD). Execução do deploy depende de alvo/credenciais.
- 🟡 **BI — profundidade do ETL**: agendamento/atualização incremental e mais indicadores.
- 🟡 **Rotação da `LGPD_ENCRYPTION_KEY`** (re-criptografia dos CPFs) — documentada, ainda não automatizada.
- 🟢 Conciliação/fluxo de caixa mais completos.
- ℹ️ **Integrações externas** (TISS real, HL7/ASTM): **fora do escopo** do protótipo (modeladas).

> Em uma frase: **as quatro alas estão de pé e a suíte está verde (138 testes)** — A, B e C completas e D
> em grande parte pronta. Restam acabamentos (RBAC por padrão, ampliar auditoria, ETL) e o hardening/deploy.

---

## 5. Processo de desenvolvimento (vale para as 4 stacks)

### 5.1 Workflow Git
- Trabalhar na **`main`** (equipe pequena). Commits **pequenos e frequentes**, um por passo concluído,
  mensagem em **português** (segue o padrão dos commits atuais: `feat:`, `fix:`, `docs:`).
- **Validar antes de commitar:** `make test` (ou `pytest`) verde + `alembic upgrade head` aplica sem erro
  + o app sobe (`make up`/`streamlit run`).
- `git pull --rebase` antes do push pra evitar conflito (4 pessoas na mesma branch). Se começar a doer,
  migrar pra **PRs curtos** (o repo já usou PR uma vez — ver histórico).

### 5.2 Comandos
```bash
make up            # sobe app + Postgres (Docker)        -> http://localhost:8501
make down          # para tudo (mantém volume)
make logs          # acompanha logs do app
make test          # sobe Postgres de teste, roda pytest, derruba o banco de teste
make migrate       # alembic upgrade head no banco principal
make revision msg="criar tabela paciente"   # cria migration vazia

# Sem Docker (local):
.venv\Scripts\streamlit run app.py
.venv\Scripts\pytest tests/ -v
```
> Windows: pra derrubar o `streamlit` use **PowerShell** (`Stop-Process` filtrando `python`/`streamlit`),
> não empilhe vários `streamlit run` na mesma porta. `make` no Windows: `winget install GnuWin32.Make`.

### 5.3 Banco de dados (Alembic + PostgreSQL)
- **Toda** mudança de schema é uma **migration nova** (`make revision msg="..."`), preenchida à mão
  (`upgrade`/`downgrade`) ou via autogenerate quando os models existirem. **Nunca editar migration já
  aplicada/compartilhada.**
- **Combinar a numeração/ordem no grupo** antes de gerar migration (evita duas pessoas criando heads
  paralelas). Quem cria a migration roda `alembic upgrade head` e confere o `downgrade`.
- Seguir o **dicionário de dados da Entrega 02**: tipos `uuid` (PK), `numeric` (dinheiro), `timestamptz`,
  `jsonb` (auditoria); constraints `PK/FK/UNIQUE/CHECK/NOT NULL`; normalização até 3FN.
- **Tabelas de auditoria são append-only** — não emitir `UPDATE`/`DELETE` (garantir por convenção/trigger).

### 5.4 Definition of Done (DoD) — por item
1. **Migration** criada/aplicada conforme o dicionário da Entrega 02 (com `downgrade`).
2. **Camadas:** model (SQLAlchemy) + repository (dados) + service (regra) + página (UI). Sem SQL na tela,
   sem regra no repository.
3. **Validação Pydantic** na entrada; **transição de estado + auditoria** onde a operação for sensível.
4. **Rastreabilidade/segurança** conferidas (ação fica logada com identidade; quando houver RBAC, o gate).
5. `pytest` verde (teste de service/repo onde fizer sentido) + app sobe sem erro + migration aplica limpo.
6. **Linguagem de domínio** do `CONTEXT.md` respeitada (ex.: "Ordem de Serviço", não "pedido"; "amostra",
   não "material"; "laudo", não "resultado").
7. Commit em PT + push. Marcar ✅ no backlog (§7) / atualizar este doc.

### 5.5 Convenções de código
- Repository = só query (SQLAlchemy), **sem regra**. Service = regra, **sem Streamlit**. Página = **sem SQL**.
- Dinheiro = `numeric` no banco / formatação BRL na UI. Datas = `timestamptz`. PK = `uuid`. Nada de `float`
  pra dinheiro.
- Domínio falado na língua do `CONTEXT.md` (e os sinônimos a **evitar** listados lá).
- Streamlit: estado em `st.session_state`; nada de regra/efeito colateral pesado no corpo da página —
  delega ao service. Reaproveitar helpers comuns (`src/db.py`, formatação) em vez de duplicar.

---

## 6. Divisão em 4 stacks (as 4 trilhas)

**Conceito:** cada pessoa é dona de um **domínio vertical** — do **banco (migration) à tela**, passando
por model → repository → service → página. Assim as quatro trabalham em **paralelo** com pouco pisar no pé
uma da outra. O que é **transversal** (auth, `db.py`, RBAC, navegação/layout, migrations base) é
**compartilhado** e mudado com aviso no grupo. A divisão segue a sugerida na Entrega 02 (§7).

> Cada stack tem: **Dono · Escopo · Pastas/arquivos · O que já existe · Itens a desenvolver (prioridade
> 🔴 alta / 🟡 média / 🟢 baixa) · Dependências.** Donos sugeridos abaixo — **confirmar no grupo.**

### 🟦 Stack A — Cadastro & Atendimento/Coleta  *(o núcleo / a espinha)*
**Dono sugerido:** Aline

- **Escopo:** os cadastros que habilitam tudo + a **entidade-espinha (OS)**. Paciente, médico, convênio,
  procedimento (TUSS), unidade/setor; abertura de OS, itens da OS, autorização de convênio, coleta de
  amostra e histórico de status da OS.
- **Pastas/arquivos:** `pages/cadastro*`, `pages/atendimento*`, `pages/coleta*` · `src/models/{paciente,
  medico,convenio,procedimento,unidade,ordem_servico,amostra,coleta}` · repositories/services
  correspondentes · migrations das tabelas 5.1 e 5.2 da Entrega 02.
- **Já existe:** ✅ **Cadastro de Paciente completo** (CRUD: cadastrar/listar ativos/editar/inativar com
  *soft-delete*; CPF validado por dígito verificador e único; tela + service + repository + DTO + seeder +
  testes) — é o **template vertical** que o resto da stack replica. Restante modelado na Entrega 02
  (§5.1, §5.2) e Entrega 03.
- **Itens concluídos:** **✅ Stack A concluída (47 testes da própria stack).**
  - ✅ **Paciente** — migration + CRUD + validação + seeder + testes (`src/cadastro/`).
  - ✅ **Demais cadastros**: médico (flag responsável técnico, CRM+UF único), convênio (`status`),
    procedimento (`codigo_tuss` único) + `procedimento_valor` por convênio, unidade (CENTRAL/COLETA) + setor.
  - ✅ **Abertura de OS** (`codigo_os` único) com itens, validando paciente/unidade/médico ativos, **convênio
    ATIVO** e procedimento válido; valor por item explícito ou **derivado do valor de tabela** do convênio;
    primeiro `os_status_historico`.
  - ✅ **Registro de coleta** → amostra com código de barras (status `COLETADA`), vínculo do coletor
    (`usuario`), transição da OS para `COLETADA` + histórico, numa transação. Deixa a amostra `COLETADA`
    como gancho da pendência logística (Stack B).
  - ✅ **Autorização de convênio** (guia/status/validade) registrada e vinculada à OS (+ helper
    `possui_autorizacao_valida`).
  - ✅ **CPF criptografado na origem** (LGPD) — **feito na Stack D** (`cpf_encrypted`/Fernet + `cpf_hash`).
  - 🟢 Busca/listagem paginada de pacientes e OS (hoje lista simples / últimas 100 OS).
- **Dependências:** consumiu uma `usuario` **mínima** criada nesta leva (terreno da Stack D, alinhado);
  produz amostras `COLETADA` consumidas pela Stack B.

### 🟩 Stack B — Logística & Laboratorial  *(operação técnica)*
**Dono sugerido:** Clauderson

- **Escopo:** a cadeia de custódia e o produto técnico. Malotes, movimentação de amostra, recebimento no
  central; equipamento, valor de referência, resultado, revisão, **laudo** e auditoria de resultado.
- **Pastas/arquivos:** `pages/logistica*`, `pages/laboratorio*` · `src/models/{malote,malote_amostra,
  amostra_movimentacao,protocolo_recebimento,equipamento,resultado,laudo,resultado_auditoria}` ·
  repositories/services · migrations das tabelas 5.3 e 5.4.
- **Já existe:** ✅ implementada nos commits `a51a75d` (logística) e `d4acede`/`09a289b` (laboratorial),
  com ajustes posteriores de migration, UI e relacionamentos.
- **Itens concluídos:**
  - ✅ **Malote + movimentação de amostra** (`COLETADA → EM_TRANSITO → RECEBIDA`) = cadeia de custódia; `protocolo_recebimento` com conferência de integridade + transição da OS para `EM_ANALISE`.
  - ✅ **Resultado** (registro/importação simulada) → `AGUARDANDO_REVISAO`; liberação de laudo com exigência de responsável técnico e `resultado_auditoria` append-only.
  - ✅ **Cadastro de valores de referência** para os analitos.
  - ✅ **Esteira de bancada** e telas de logística, cadastros laboratoriais, resultados e laudos.
  - ✅ **Cancelamento coerente de OS/itens** com conclusão automática da OS ao liberar o último laudo.
- **Melhorias pendentes:** validação de vínculo do responsável técnico com cadastro de médico/RBAC (o gate
  por perfil já existe; falta amarrar ao cadastro), mais testes específicos do service laboratorial.
- **Dependências:** recebe amostras da Stack A; o laudo liberado é o ponto de integração com a Stack C;
  a autorização por perfil ainda será consolidada pela Stack D.

### 🟧 Stack C — Faturamento, Financeiro & Compras
**Dono sugerido:** Victor

- **Escopo:** transformar laudo em receita e fechar o ciclo econômico. Guias/lotes TISS e glosas; títulos
  a receber/pagar, caixa e conciliação; fornecedores, pedidos, recebimento de insumo e estoque.
- **Pastas/arquivos:** `pages/faturamento*`, `pages/financeiro*`, `pages/compras*` · `src/models/{lote_
  faturamento,guia_tiss,guia_item,glosa,titulo_receber,titulo_pagar,movimento_caixa,conciliacao_pagamento,
  fornecedor,pedido_compra,recebimento_insumo,insumo_material,estoque_movimento}` · migrations 5.5–5.7.
- **Já existe:** ✅ **implementada** (PR #10 `feat/modulo-financeiro` + commits de faturamento/glosa),
  em fatias verticais por entidade (`src/faturamento/*`, `src/financeiro/*`, `src/compras/*`) + telas +
  migrations `0006`–`0008` + 19 testes.
- **Itens concluídos:**
  - ✅ **Faturamento:** `guia_item` **a partir de laudo liberado**, agrupamento em `lote_faturamento`,
    fechamento do lote → **`titulo_receber`** (transação); lote sem convênio tratado.
  - ✅ **Glosa** (motivo/operadora) registrada e vinculada ao faturamento.
  - ✅ **Financeiro:** `titulo_receber`/`titulo_pagar`, `movimento_caixa` e **conciliação** de pagamento.
  - ✅ **Compras:** fornecedor, pedido de compra (→ **`titulo_pagar`**), insumo e movimento de estoque.
- **Melhorias pendentes:** 🟡 alertas de divergência mais ricos na conciliação, fluxo de caixa
  consolidado por período, e instrumentar a **auditoria** nas operações financeiras (Stack D).
- **Dependências:** consome o **laudo liberado** (Stack B); abastece o BI (Stack D) com receita/glosa.

### 🟪 Stack D — Transversal: Segurança/RBAC, Auditoria, BI & Plataforma
**Dono sugerido:** Gustavo

- **Escopo:** o que atravessa todo mundo. Persistência de usuário + RBAC, auditoria append-only, LGPD,
  o **BI** (ETL + esquema estrela), navegação/layout, fundação de banco (`db.py`) e deploy.
- **Pastas/arquivos:** `src/auth.py`, `src/config.py` (já existem), `src/db.py`, `src/rbac.py` ·
  `src/models/{usuario,perfil,permissao,perfil_permissao,auditoria_log}` + dimensões/fatos do BI ·
  `pages/` (shell de navegação, BI/dashboards) · migrations 5.8 e 9 (BI).
- **Já existe:** ✅ **em grande parte implementada** (PR #17 "Frontend v2" + commits de RBAC/LGPD/BI).
  Fundação (`src/db.py`, 1ª migration, convenção de pacote), login Google, `usuario` sincronizada do Auth0,
  **RBAC efetivo** (`src/rbac/` + gate no `shell()`), **auditoria** modelada (`src/auditoria/`), **LGPD**
  (`src/lgpd/` — CPF criptografado), **BI** (`src/bi/` — estrela + ETL + 3 dashboards) e **navegação
  unificada + design system** (`src/ui*`, `src/ui_components/`).
- **Itens concluídos:**
  - ✅ **Fundação de dados:** `src/db.py` + 1ª migration + convenção de pacote vertical (herdada por A/B/C).
  - ✅ **`usuario` + RBAC:** perfil/permissão (`perfil`, `permissao`, `perfil_permissao`), gate por página
    (`shell(permissao=...)`), gestão de usuários (`admin_usuarios.py`) e "meu perfil"; seeder de perfis.
  - ✅ **Navegação unificada:** `shell()` (login gate + page config + CSS global + RBAC) e menu lateral —
    substitui o antigo *meta-refresh* repetido em cada página.
  - ✅ **Design system:** tema institucional + componentes (`renderizar_cabecalho/secao/empty_state`,
    `kpi_card`, `status_badge`, `filter_bar`, `action_bar`) e ícones SVG (FontAwesome/currentColor).
  - ✅ **LGPD:** CPF em repouso criptografado (Fernet) + hash SHA-256 + máscara na UI.
  - ✅ **BI:** esquema estrela + ETL + dashboards de produtividade, logística e financeiro.
- **Itens a desenvolver / acabamento:**
  - 🔴 **Corrigir heads paralelas do Alembic** (merge migration — ver §8).
  - 🔴 **Plugar a auditoria nos services:** chamar `registrar_auditoria` nas operações sensíveis
    (OS/coleta/laudo/faturamento/financeiro) — o helper existe, mas ainda não é invocado.
  - 🟡 **RBAC:** atribuir perfis por padrão e revisar granularidade + testes de gate.
  - 🟡 **BI/LGPD:** anonimização do paciente no BI; profundidade/atualização do ETL; gestão da
    `LGPD_ENCRYPTION_KEY`.
  - 🟢 **Deploy** (definir alvo) + envs de produção; *leaked password* / hardening do Auth0.
- **Dependências:** **transversal** — `db.py`, RBAC e auditoria tocam todas as stacks; alinhar no grupo
  antes de mudar. O BI consome eventos/dados de A, B e C.

### 6.1 Matriz de quem-toca-o-quê (evitar pisão de pé)

| Área compartilhada | Dono natural | Regra |
|---|---|---|
| `src/auth.py`, `src/config.py` (login) | Stack D | Mudou? avisar no grupo |
| `src/db.py`, convenção repository/service base | Stack D | Define o padrão; mudança = aviso |
| `src/rbac.py` + tabelas `usuario/perfil/permissao` | Stack D | Novo perfil/permissão = aviso + migration |
| `alembic/versions/` (ordem das migrations) | quem cria a migration | Combinar a ordem/head **antes** de gerar |
| `pages/` (shell de navegação/menu) | Stack D | Cada stack pede o link da sua tela |
| Helpers comuns (formatação, validação Pydantic base) | qualquer | Não duplicar; centralizar |
| `CONTEXT.md` / `README.md` / este doc / backlog | todos | Manter linguagem de domínio; marcar ✅ ao concluir |

---

## 7. Backlog consolidado por prioridade

**✅ Concluído**
- Fundação de dados: `src/db.py` + migration base + convenção de pacote vertical — **Stack D**.
- **Stack A inteira**: cadastros (paciente/médico/convênio/procedimento+valor/unidade+setor), **abertura de
  OS** (espinha, com validações e histórico), **autorização de convênio** e **coleta** (amostra + cadeia de
  custódia inicial + transição da OS). `usuario` sincronizada do Auth0 — **Stack A**.
- **Stack B inteira**: logística (malote, movimentação, recebimento e transição da OS), laboratorial
  (equipamentos, valores de referência, resultados, auditoria de resultados, laudos, esteira de bancada) e
  **cancelamento coerente de OS/itens** — **Stack B**.
- **Stack C inteira**: faturamento (guia/lote → título a receber) + glosa; financeiro (títulos a
  receber/pagar, caixa, conciliação); compras (fornecedor, pedido → título a pagar, insumo, estoque) — **Stack C**.
- **Stack D (grande parte)**: RBAC efetivo (perfil→permissão + gate no shell + gestão de usuários), LGPD
  (CPF criptografado), BI (estrela + ETL + 3 dashboards), navegação unificada + design system — **Stack D**.
- **Heads paralelas do Alembic resolvidas** (merge `0012_merge_heads_c_d`) — **Stack D**.
- **Auditoria append-only plugada** nas operações sensíveis (OS, coleta, laudo, lote, **baixa de título e
  glosa**) — **Stack C/D**.
- **LGPD_ENCRYPTION_KEY** no `.env.example`/`docker-compose`/`conftest` + correção da chave de teste inválida — **Stack D**.
- **RBAC com perfil por padrão** (bootstrap admin + `visualizador`) encerrando o acesso plano — **Stack D**.
- **BI com `id_origem` anonimizado por hash** (migração `0013`) — **Stack D**.
- **Busca/paginação** em Pacientes e OS — **Stack A**.
- **`DEPLOY.md` + `.env.production.example`** (guia + hardening) — **Stack D**.
- **Issues #8/#9 (hardening laboratorial):** service bloqueia laudo com resultado não revisado e valida
  responsável técnico ativo — **Stack B**.
- **138 testes — suíte completa verde** (validada em banco limpo via docker).

**🔴 Alta (destrava/consolida)**
- _(vazio — resolvidos nesta leva.)_

**🟡 Média**
- Profundidade/atualização do ETL do BI (incremental, mais indicadores) — **Stack D**.
- **Rotação automatizada** da `LGPD_ENCRYPTION_KEY` (re-criptografia) — **Stack D**.
- Alertas de divergência na conciliação; fluxo de caixa consolidado — **Stack C**.

**🟢 Baixa / oportunístico**
- Executar o **deploy** de fato (definir alvo/credenciais) seguindo o `DEPLOY.md` — **Stack D**.

---

## 8. Riscos & pendências (ler antes de apresentar/entregar)

- ✅ **Heads paralelas no Alembic — RESOLVIDO:** `0008_lote_sem_convenio` tinha dois filhos
  (`0009_cancelamento_item` e `0009_rbac_auditoria`→`0010`→`0011`). Criado o mergepoint
  **`0012_merge_heads_c_d`**; `alembic upgrade head` aplica a cadeia inteira em banco limpo (validado).
- ⚠️ **Ordem das migrations:** com várias pessoas gerando migration na `main`, **combinar a head antes** —
  a bifurcação acima foi exatamente esse risco; usar branch/PR curto ajuda a evitar repetição.
- ✅ **Banco com schema:** as migrations `0003`…`0013` cobrem cadastros, Stack A/B/C e a transversal D
  (RBAC/auditoria, LGPD, BI), com **head única**.
- ✅ **RBAC efetivo + perfil por padrão:** perfil→permissão com gate no `shell()`. Novo usuário recebe
  perfil no login (bootstrap: 1º = `admin`, demais = `visualizador`) — o acesso amplo por ausência de perfil
  só ocorre se o RBAC **não** tiver sido semeado (`python -m src.seeder`).
- ✅ **LGPD — CPF criptografado:** dívida do texto puro **quitada** (`cpf_encrypted`/Fernet + `cpf_hash`).
  **`LGPD_ENCRYPTION_KEY`** documentada (`.env.example`/`.env.production.example`), provida ao serviço de
  teste e blindada no `conftest`. No BI, `id_origem` do paciente vira **hash** (não o UUID). Pendente:
  **rotação automatizada** da chave (re-criptografia) — procedimento descrito no `DEPLOY.md`.
- ✅ **Auditoria plugada:** `registrar_auditoria` em abrir/cancelar OS e item, coleta, liberação de laudo,
  fechamento de lote, **baixa de título (receber/pagar) e glosa** (com testes). Pendente: caixa/conciliação.
- ⚠️ **Auth0/segredos:** `.env` com `AUTH0_CLIENT_SECRET` e `LGPD_ENCRYPTION_KEY` **nunca** vão pro git;
  signup público e proteção de senha vazada a revisar antes de qualquer deploy (checklist no `DEPLOY.md`).
- ℹ️ **Integrações externas (TISS real, HL7/ASTM)** ficam **simuladas** no protótipo — deixar claro na
  apresentação o que é fluxo interno vs. integração real.

---

## 9. Glossário rápido

- **Ordem de Serviço (OS):** entidade-espinha — o atendimento de um paciente que agrupa os exames; tudo
  deriva dela (ver `CONTEXT.md`).
- **Amostra / cadeia de custódia:** material biológico rastreado de `COLETADA` → `EM_TRANSITO` → `RECEBIDA`.
- **Laudo:** documento final do exame, liberado **só por responsável técnico**; habilita o faturamento.
- **TUSS/TISS · guia · glosa:** padrão de procedimentos/faturamento de convênio; glosa = recusa de
  pagamento pelo convênio.
- **RBAC:** controle por perfil → permissão (**efetivo**, com gate no `shell()`; acesso plano só como
  fallback para usuário sem perfil atribuído).
- **Auditoria append-only:** log imutável de ações sensíveis (`auditoria_log`, `resultado_auditoria`) — só
  insere, nunca altera/apaga.
- **OLTP/OLAP:** base operacional (dia a dia das unidades) vs. analítica (esquema estrela do BI,
  *read-only*, paciente anonimizado).
- **Multi-unidade:** 1 laboratório central + 4 unidades de coleta; entidades operacionais carregam
  `unidade_id`.

---

> **Próximo passo sugerido:** as quatro stacks estão implementadas e a **suíte está verde (138 testes)**.
> Os itens de operação/acabamento e o backlog médio/baixo foram resolvidos (RBAC com perfil padrão,
> auditoria financeira, anonimização por hash no BI, busca/paginação, guia de deploy). O que resta é
> **evolução e execução**: **(1)** aprofundar o ETL do BI (incremental + indicadores); **(2)** automatizar a
> rotação da `LGPD_ENCRYPTION_KEY`; **(3)** enriquecer conciliação/fluxo de caixa; **(4)** **executar** o
> deploy conforme o `DEPLOY.md`. A head atual do Alembic é **`0013_bi_paciente_hash`** — nova migration
> deve partir dela.

---

## 10. Changelog da resenha

- **2026-07-26 (4)** — Backlog médio/baixo resolvido, **suíte verde (138 testes)**: **RBAC com perfil por
  padrão** (bootstrap: 1º usuário = `admin`, demais = `visualizador`), encerrando o acesso plano; **auditoria
  financeira** (baixa de título a receber/pagar e glosa); **BI com `id_origem` anonimizado por hash SHA-256**
  (migração `0013` + ETL); **busca/paginação** nas telas de Pacientes e OS; **`DEPLOY.md` +
  `.env.production.example`** (guia de deploy + checklist de hardening Auth0/segredos/LGPD). Head do Alembic:
  `0013_bi_paciente_hash`.
- **2026-07-26 (3)** — Resolvidas issues abertas do repositório (backend + UX), **suíte verde (132 testes)**:
  **#8** o service bloqueia liberação de laudo com resultado não revisado; **#9** valida responsável técnico
  (médico ativo + `responsavel_tecnico`) no service, com testes; **#16** recebimento de malote permite
  **recusar amostras individualmente** (service + tela) + teste; **#15** tela de coleta mostra os exames
  solicitados da OS; **#13** removida a seção "Autorizações de convênio" da tela de OS (não consumida por
  nenhuma regra — módulo backend preservado); **#5** tela de malotes mostra o conteúdo do malote antes de
  despachar. Tabelas de conferência/malote passam a exibir código de barras em vez de UUID cru.
- **2026-07-26 (2)** — Resolvidos os itens pendentes de operação/acabamento e **suíte completa verde (127
  testes)**, validada em banco limpo via docker. (1) **Heads paralelas do Alembic** unidas pelo mergepoint
  `0012_merge_heads_c_d`. (2) **Auditoria append-only plugada** nos services (`registrar_auditoria` em
  abrir/cancelar OS e item, coleta, liberar laudo, fechar lote) + testes de wiring. (3) **LGPD_ENCRYPTION_KEY**
  adicionada ao `.env.example`, provida ao serviço de teste e blindada no `tests/conftest.py`; **corrigida a
  chave de teste inválida** do `docker-compose` (não era Fernet válido — quebrava a suíte que cria paciente).
  (4) **Anonimização no BI verificada** (sem PII; só faixa etária/sexo/id pseudonimizado). Também corrigidos
  2 testes de `test_app.py` que quebravam com o novo `shell()`/menu do PR #17 (contrato `user["id"]` +
  `st.page_link` no `AppTest`).
- **2026-07-26** — Grande atualização de estado após o merge do **PR #17 "Frontend v2"** (Stack D) na `main`.
  Refletido: **Stack C concluída** (faturamento/glosa, financeiro/títulos/caixa/conciliação, compras/
  estoque — PR #10 + commits; migrations `0006`–`0008`) e **Stack D em grande parte implementada** — RBAC
  efetivo (perfil→permissão + gate no `shell()` + `admin_usuarios`/`meu_perfil` + seeder), auditoria
  modelada (`auditoria_log` + helper, ainda não plugado), **LGPD** (CPF `cpf_encrypted`/Fernet + `cpf_hash`),
  **BI** (esquema estrela + ETL + 3 dashboards) e **navegação unificada + design system** (`shell`, menu,
  `ui_components`, tema). Também na Stack B: **esteira de bancada** e **cancelamento coerente de OS/itens**
  (PR #14). Total de testes atualizado para **116**. **Novo risco crítico:** o merge deixou **heads
  paralelas no Alembic** (`0009_cancelamento_item` × `0009_rbac_auditoria`→`0011`) — `upgrade head` quebra
  até mesclar (§8). Dívida de **CPF em texto puro marcada como quitada**; RBAC deixou de ser "plano".
- **2026-07-24** — Atualização para refletir o estado real do repositório: Stack B marcada como concluída,
  incluídos logística e laboratorial no estado atual, head do Alembic atualizada para `f6ccac7706b1`,
  total de testes atualizado para 72 e backlog reorganizado. A versão anterior afirmava incorretamente
  que a Stack B ainda não existia.
- **2026-07-21** — Implementada a logística da Stack B: malote, associação de amostras, cadeia de custódia,
  recebimento central e transição da OS para `EM_ANALISE` (`a51a75d`). Implementado o módulo laboratorial:
  equipamentos, valores de referência, resultados, auditoria e laudos (`d4acede`, `09a289b`), com correções
  de migration e UI posteriores.

- **2026-06-30 (2)** — **Stack A concluída.** Cadastros completos (médico/convênio/procedimento+valor/
  unidade+setor) e **atendimento/coleta** com a **OS como entidade-espinha**: abertura com validações
  (paciente/unidade/médico ativos, convênio ATIVO, procedimento válido, valor explícito ou derivado de
  tabela), itens, `os_status_historico`, autorização de convênio, e **registro de coleta** gerando amostra
  (cadeia de custódia) + vínculo do coletor + transição da OS, tudo transacional. Criada `usuario` mínima
  sincronizada do Auth0 no login; helper de guarda `src/ui.py`; navegação na home; seeder de cadastros;
  migration `0004` (13 tabelas, encadeada em `0003`). **47 testes verdes** via `make test`. Convenção de
  estrutura refinada para **sub-pacote por entidade** (§3.1).
- **2026-06-30 (1)** — Atualização pós-primeira-entrega de módulo. Refletido: fundação de dados (`src/db.py`,
  `session_scope`, `Base`); **Cadastro de Pacientes** ponta a ponta (migration `0003`, pacote
  `src/cadastro/` com model/repository/service/dtos/validators/errors, tela CRUD, seeder Faker, testes
  unit + integração); `make seeder` e autogenerate do Alembic. Convenção de layout ajustada para
  **pacote vertical por módulo** (§3.1). Novos riscos: numeração de migration (base é `0003`) e **CPF em
  texto puro** (LGPD pendente). Backlog e Stacks A/D remarcados.
- **(versão inicial)** — Resenha-base: visão, DNA arquitetural, fundação auth+infra, modelagem no papel,
  divisão em 4 stacks.
