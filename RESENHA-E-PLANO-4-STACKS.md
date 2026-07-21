# LabVida — Resenha do Projeto + Plano de Desenvolvimento em 4 Stacks

> Documento-base para a equipe. Lê de cima pra baixo: primeiro **o que é** e **por que é diferente**,
> depois **como já está**, depois **como a gente desenvolve** e, no fim, **a divisão das 4 trilhas
> (stacks)** com dono, escopo e itens a fazer. Pode copiar e mandar no grupo.
>
> **Última atualização:** 2026-06-30 — **Stack A concluída** (cadastros completos + atendimento/coleta com
> a OS como espinha) sobre a fundação de dados. 47 testes verdes. Ver §4 (estado atual) e §10 (changelog).
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
- **Onde está:** **fundação + Stack A inteira no ar.** Login Google (Auth0/PKCE), infra Docker + Alembic +
  pytest, **modelagem completa no papel** (Entregas 02 e 03), **fundação de dados** (`src/db.py`) e a
  **Stack A completa**: cadastros (paciente, médico, convênio, procedimento + valor, unidade + setor) e
  **atendimento/coleta** com a **Ordem de Serviço como entidade-espinha** (abertura com validações, itens,
  autorização de convênio, registro de coleta gerando amostra/cadeia de custódia e transição de status).
  Tudo em fatias verticais (migration → model → repository → service → DTO/validação → tela → testes), com
  **47 testes verdes**. Falta implementar as Stacks **B** (logística/laboratorial), **C** (faturamento/
  financeiro/compras) e o transversal pleno da **D** (RBAC/auditoria/BI).
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
| **RBAC** (perfil → permissão) | `usuario`/`perfil`/`permissao`/`perfil_permissao`; coleta e liberação de laudo gated por perfil | Cada um faz só o que pode (modelado; v1 com acesso plano — ver §2.1) |
| **Escopo por unidade** | Entidades operacionais carregam `unidade_id` | Base para segregar acesso e medir desempenho por unidade |
| **Separação OLTP/OLAP** | Base operacional normalizada + **esquema estrela** (fatos/dimensões) alimentado por ETL; BI *read-only* | Dashboards não pesam na operação das unidades |
| **Boas práticas de dado** | PK `uuid` · `numeric` p/ dinheiro (nunca `float`) · `timestamptz` · domínios via colunas `status` | Sem colisão entre unidades, sem bug de centavo, sem fuso quebrado |
| **LGPD por design** | Dados sensíveis do paciente criptografados na origem; paciente **anonimizado** no BI | Privacidade tratada no modelo, não como remendo |

> **Resumo do diferencial:** integração por entidade-espinha + rastreabilidade (status histórico + cadeia
> de custódia + auditoria imutável) + separação OLTP/OLAP + LGPD, tudo já desenhado na modelagem. O
> trabalho das stacks é **implementar mantendo esses padrões** — não atalhar com CRUD solto.

### 2.1 Onde a engenharia ainda é "no papel" (ser honesto)

- **RBAC:** modelado por completo, mas a **v1 usa acesso plano** — todo usuário autenticado tem o mesmo
  nível funcional (decisão registrada em `docs/adr/0002`). O valor atual do login é **rastreabilidade**
  (associar cada ação a uma identidade). Ligar perfil→permissão é item de backlog (Stack D).
- **Eventos/impactos automáticos:** a Entrega 03 descreve o barramento de eventos; na implementação
  atual eles serão **transições de estado em service + persistência** (não há fila/mensageria no protótipo).
- **ETL/BI, criptografia LGPD, integrações TISS/equipamentos:** desenhados, ainda não implementados.

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

**Fundação concretizada + 1ª fatia vertical (Cadastro de Pacientes) no ar; os outros 7 módulos a construir.**

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
| **Migration `0004`** ⭐⭐ | 13 tabelas da Stack A encadeadas na head `0003` (CHECK de domínios de status, FKs, índices únicos) | `alembic/versions/0004_*.py` |
| **Seeder de cadastros** ⭐⭐ | popula unidades/convênios/procedimentos+valores/médicos (insere se vazio) p/ abrir OS na demo | `src/seeder/cadastros.py` |
| **Guarda de sessão** ⭐⭐ | helper `exigir_login()` reutilizado pelas telas novas (provisório até o shell da Stack D) | `src/ui.py` |
| **1ª migration** ⭐ | cria tabela `pacientes` (PK `uuid`, CPF `unique`, enum `sexo_paciente`, flag `ativo`) | `alembic/versions/0003_*.py` |
| **Seeder de pacientes** ⭐ | popula Pacientes de exemplo com **Faker** (CPF válido, telefone, sexo) — `make seeder` | `src/seeder/*` |
| **Infra Docker** | `docker-compose` (app + Postgres 16 + serviços de teste), `Dockerfile` (Python 3.12-slim, não-root) | `docker-compose.yml`, `Dockerfile` |
| **Migrations** | Alembic configurado, **autogenerate ligado** (`env.py` lê `Base.metadata`); aplica no boot | `alembic/`, `alembic.ini` |
| **Testes** | pytest: `AppTest` (login/home) + **dtos/validators (unit)** + **service (integração via Postgres de teste)** | `tests/`, `tests/cadastro/*` |
| **Automação** | `Makefile` (`up/down/test/migrate/revision/seeder/clean`) | `Makefile` |

> ⭐ = entregue na leva da fundação + Cadastro de Pacientes. ⭐⭐ = entregue agora, na **Stack A completa**.

### 4.2 Já modelado (papel — base para implementar)

- **Modelagem de dados completa** (Entrega 02): dicionário de dados dos 8 módulos + transversal, MER
  conceitual e lógico (`.mmd`), regras de integridade, mapeamento dos gatilhos e **esquema estrela** do BI.
- **Integração organizacional** (Entrega 03): eventos entre setores, rastreabilidade ponta a ponta,
  cenário integrado demonstrativo, indicadores gerenciais.
- **Arquitetura técnica** (Entrega 01 — complemento): camadas, módulo *core* (ciclo da OS), hierarquia
  arquitetural (operacional/analítica/estratégica/compartilhada).
- **Glossário de domínio** (`CONTEXT.md`) e **2 ADRs** (stack; autenticação/RBAC mínimo).

### 4.3 Ainda NÃO existe (é o trabalho das stacks)

- **Stack B — Logística & Laboratorial:** malote, `amostra_movimentacao` (cadeia de custódia completa),
  `protocolo_recebimento`, equipamento, resultado, **laudo** e `resultado_auditoria`. A coleta da Stack A
  já deixa a amostra em `COLETADA` como **ponto de integração** para a Stack B abrir a pendência logística.
- **Stack C — Faturamento, Financeiro & Compras:** nada implementado.
- **RBAC efetivo + auditoria (Stack D):** existe `usuario` **mínima** (e-mail/nome do Auth0), mas **sem
  perfil/permissão** (RBAC ainda **plano**) e **sem `auditoria_log`**. A guarda de sessão é o helper
  provisório `exigir_login()`; o shell de navegação definitivo é da Stack D.
- **Criptografia LGPD:** o **CPF segue em texto puro** (`String(11)`) — a criptografia na origem prevista
  no §3.2 continua pendente (decisão de adiar para a Stack D — ver risco em §8).
- **BI/ETL** e **deploy**.

> Em uma frase: **a fundação está no chão e a primeira ala completa (Stack A: cadastros + atendimento/
> coleta com a OS) está de pé e testada. Faltam as alas B e C e o acabamento transversal da D.**

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
- **Itens a desenvolver:** **✅ Stack A concluída (47 testes verdes).**
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
  - 🟡 **CPF criptografado na origem** (LGPD) — **adiado para a Stack D** (segue texto puro; ver §8).
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
- **Já existe:** **nada implementado** — modelado na Entrega 02 (§5.3, §5.4) e Entrega 03 (processamento
  operacional e técnico).
- **Itens a desenvolver:**
  - ✅ **Malote + movimentação de amostra** (`COLETADA → EM_TRANSITO → RECEBIDA`) = cadeia de custódia; `protocolo_recebimento` com conferência de integridade + transição da OS para `EM_ANALISE`.
  - 🔴 **Resultado** (registro/importação simulada) → `AGUARDANDO_REVISAO`; **liberação de laudo** apenas por responsável técnico (gate por perfil) + `resultado_auditoria` **append-only**.
  - 🟡 **Valor de referência** para validar resultado fora da faixa.
  - 🟢 Tela de "esteira" da bancada (fila de amostras recebidas a processar).
- **Dependências:** recebe amostras da Stack A; ao liberar laudo, **destrava o faturável** da Stack C;
  consome perfil "responsável técnico" do RBAC (Stack D).

### 🟧 Stack C — Faturamento, Financeiro & Compras
**Dono sugerido:** Victor

- **Escopo:** transformar laudo em receita e fechar o ciclo econômico. Guias/lotes TISS e glosas; títulos
  a receber/pagar, caixa e conciliação; fornecedores, pedidos, recebimento de insumo e estoque.
- **Pastas/arquivos:** `pages/faturamento*`, `pages/financeiro*`, `pages/compras*` · `src/models/{lote_
  faturamento,guia_tiss,guia_item,glosa,titulo_receber,titulo_pagar,movimento_caixa,conciliacao_pagamento,
  fornecedor,pedido_compra,recebimento_insumo,insumo_material,estoque_movimento}` · migrations 5.5–5.7.
- **Já existe:** **nada implementado** — modelado na Entrega 02 (§5.5–5.7) e Entrega 03 (cobrança e
  controle econômico).
- **Itens a desenvolver:**
  - 🔴 **Faturamento:** montar `guia_item` **só a partir de laudo liberado**, agrupar em `lote_faturamento`,
    fechar lote → **gerar `titulo_receber`** (transação atômica).
  - 🟡 **Glosa** (motivo/operadora/unidade) e **conciliação** faturado×recebido com alerta de divergência.
  - 🟡 **Compras:** pedido → aprovação **gera `titulo_pagar`**; recebimento de insumo **dá entrada no
    estoque** (`estoque_movimento`).
  - 🟢 `movimento_caixa` consolidando entradas/saídas (fluxo de caixa).
- **Dependências:** depende do **laudo liberado** (Stack B); abastece o BI (Stack D) com receita/glosa.

### 🟪 Stack D — Transversal: Segurança/RBAC, Auditoria, BI & Plataforma
**Dono sugerido:** Gustavo

- **Escopo:** o que atravessa todo mundo. Persistência de usuário + RBAC, auditoria append-only, LGPD,
  o **BI** (ETL + esquema estrela), navegação/layout, fundação de banco (`db.py`) e deploy.
- **Pastas/arquivos:** `src/auth.py`, `src/config.py` (já existem), `src/db.py`, `src/rbac.py` ·
  `src/models/{usuario,perfil,permissao,perfil_permissao,auditoria_log}` + dimensões/fatos do BI ·
  `pages/` (shell de navegação, BI/dashboards) · migrations 5.8 e 9 (BI).
- **Já existe:** **login Google (Auth0/PKCE), config e home pós-login** funcionando; infra Docker/Alembic/
  pytest. ✅ **`src/db.py`** (engine/sessão/`Base`/`session_scope`) e a **1ª migration** já no ar; a
  **convenção repository/service** está firmada pelo pacote `src/cadastro/`. RBAC e BI **modelados**
  (Entrega 02 §5.8 e §9), ainda não implementados.
- **Itens a desenvolver:**
  - ✅ **Fundação de dados:** `src/db.py` + 1ª migration + convenção de pacote vertical (herdada por A/B/C).
  - 🔴 **`usuario` + auditoria:** ligar a identidade do Auth0 a uma tabela `usuario`; `auditoria_log`
    (jsonb) **append-only** com helper que os services chamam (ainda não existe).
  - 🔴 **Navegação por módulo** (shell do `pages/`, menu, guarda de sessão reutilizável — hoje cada página
    repete o *meta-refresh* de redirecionamento; centralizar).
  - 🟡 **RBAC efetivo** (perfil→permissão, gates) — sucede o acesso plano do ADR 0002.
  - 🟡 **BI:** esquema estrela (fatos/dimensões) + ETL simples a partir do operacional; primeiros
    dashboards (produtividade por unidade, tempo coleta→laudo, glosa por convênio, receita por procedimento).
  - 🟡 **Criptografia em repouso** dos campos sensíveis do paciente (LGPD) + anonimização no BI.
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
  custódia inicial + transição da OS). `usuario` **mínima** sincronizada do Auth0. 47 testes — **Stack A**.

**🔴 Alta (destrava todo o resto)**
- `usuario` completo (perfil) + `auditoria_log` append-only ligados ao login Auth0 — **Stack D**.
- **Logística**: malote + `amostra_movimentacao` (recebe a amostra `COLETADA` da Stack A) — **Stack B**.
- **Liberação de laudo** (gate responsável técnico) + auditoria de resultado — **Stack B**.
- **Faturamento**: laudo liberado → guia/lote → título a receber — **Stack C**.

**🟡 Média**
- RBAC efetivo (perfil→permissão) sucedendo o acesso plano — **Stack D**.
- Glosa + conciliação faturado×recebido — **Stack C**.
- Compras: pedido→título a pagar; recebimento→estoque — **Stack C**.
- Valor de referência / validação de resultado — **Stack B**.
- BI (esquema estrela + ETL simples + primeiros dashboards) — **Stack D**.
- Criptografia LGPD + anonimização no BI — **Stack D**.

**🟢 Baixa / oportunístico**
- Autorização de convênio detalhada; busca/paginação de OS e pacientes — **Stack A**.
- Esteira de bancada; fluxo de caixa consolidado — **Stack B/C**.
- Deploy + hardening de produção — **Stack D**.

---

## 8. Riscos & pendências (ler antes de apresentar/entregar)

- ✅ **Banco com schema inicial:** a 1ª migration (`pacientes`) já existe e aplica — o bloqueio de
  "banco vazio" da versão anterior **caiu**. A fundação (`db.py` + convenção) está disponível para A/B/C.
- ✅ **Cadeia de migrations linear:** `0003` (base, pacientes) → `0004_stack_a_atendimento` (13 tabelas da
  Stack A). A head atual é **`0004_stack_a_atendimento`** — a **próxima** migration (Stack B/C/D) deve
  apontar `down_revision = "0004_stack_a_atendimento"`.
- ⚠️ **Ordem das migrations:** com várias pessoas gerando migration na `main`, **combinar a head antes** —
  heads paralelas no Alembic dão dor de cabeça pra mesclar.
- ℹ️ **`usuario` mínima invadiu a Stack D (combinado):** a Stack A criou `usuarios` (e-mail/nome do Auth0)
  para amarrar coleta/histórico a um ator. A Stack D deve **estender** essa tabela (perfil, RBAC) em vez de
  recriá-la, e ligar o `auditoria_log` aos mesmos `usuario_id`.
- ⚠️ **RBAC é plano na v1** (ADR 0002): gates de "responsável técnico" e afins precisam ser tratados como
  **convenção/regra de service** até o RBAC efetivo entrar; não confundir "logado" com "autorizado".
- ⚠️ **LGPD — CPF em texto puro (dívida aberta):** a tabela `pacientes` já existe com **CPF sem
  criptografia** (`String(11)`). A criptografia na origem prevista no §3.2 ficou pendente — **decidir a
  estratégia agora**, antes de espalhar mais cadastros sensíveis, para não acumular migração dolorosa.
- ⚠️ **Auth0/segredos:** `.env` com `AUTH0_CLIENT_SECRET` **nunca** vai pro git; signup público e proteção
  de senha vazada a revisar antes de qualquer deploy.
- ℹ️ **Integrações externas (TISS real, HL7/ASTM) e ETL pesado** ficam **simulados** no protótipo — deixar
  claro na apresentação o que é fluxo interno vs. integração real.

---

## 9. Glossário rápido

- **Ordem de Serviço (OS):** entidade-espinha — o atendimento de um paciente que agrupa os exames; tudo
  deriva dela (ver `CONTEXT.md`).
- **Amostra / cadeia de custódia:** material biológico rastreado de `COLETADA` → `EM_TRANSITO` → `RECEBIDA`.
- **Laudo:** documento final do exame, liberado **só por responsável técnico**; habilita o faturamento.
- **TUSS/TISS · guia · glosa:** padrão de procedimentos/faturamento de convênio; glosa = recusa de
  pagamento pelo convênio.
- **RBAC:** controle por perfil → permissão (modelado; v1 com acesso plano).
- **Auditoria append-only:** log imutável de ações sensíveis (`auditoria_log`, `resultado_auditoria`) — só
  insere, nunca altera/apaga.
- **OLTP/OLAP:** base operacional (dia a dia das unidades) vs. analítica (esquema estrela do BI,
  *read-only*, paciente anonimizado).
- **Multi-unidade:** 1 laboratório central + 4 unidades de coleta; entidades operacionais carregam
  `unidade_id`.

---

> **Próximo passo sugerido:** com a **Stack A pronta** (cadastros + OS + coleta), o caminho crítico agora é a
> **Stack B**: receber a amostra `COLETADA` (malote + `amostra_movimentacao` + `protocolo_recebimento`),
> registrar resultado e **liberar laudo** (gate de responsável técnico) — o que destrava a **Stack C**
> (faturamento). Em paralelo, a **Stack D** estende a `usuario` mínima (perfil/RBAC), adiciona o
> `auditoria_log` e decide a **cripto do CPF (LGPD)**. Toda nova migration parte de
> `down_revision = "0004_stack_a_atendimento"`.

---

## 10. Changelog da resenha

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
