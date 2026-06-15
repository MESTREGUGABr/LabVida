# LabVida — ERP para Laboratorio de Analises Clinicas

Projeto academico da disciplina **Sistemas de Informacao e Tecnologias (SIT)** —
Bacharelado em Ciencia da Computacao, **UFAPE** (Garanhuns - PE, 2026).

O **LabVida** e um ERP academico para uma rede regional de laboratorios de analises clinicas
(um laboratorio central + quatro unidades de coleta). O projeto parte de um diagnostico organizacional
real — baixa integracao entre sistemas, logistica manual de amostras, faturamento de convenios critico,
ausencia de indicadores gerenciais — e propoe uma arquitetura de ERP integrada para resolve-lo.

## Equipe

- Aline Fernanda Soares Silva
- Clauderson Branco Xavier
- Gustavo Ferreira Wanderley
- Victor Alexandre Saraiva Pimentel

## Visao geral do ERP

O sistema e organizado em modulos especializados que refletem os setores reais do laboratorio, com
um fluxo operacional integrado em torno da **Ordem de Servico (OS)**:

```
Cadastro → Atendimento e Coleta → Logistica de Amostras → Laboratorial → Faturamento → Financeiro
                                                                                          ↳ BI (alimentado por todos)
                                                              Compras → (insumos / contas a pagar)
```

| Modulo | Responsabilidade |
|---|---|
| **Cadastro** | Pacientes, medicos, convenios, procedimentos (TUSS/TISS), unidades, setores |
| **Atendimento e Coleta** | Abertura de OS, validacao de convenio, coleta e etiquetagem de amostras |
| **Logistica de Amostras** | Cadeia de custodia, malotes, rastreamento e recebimento no laboratorio central |
| **Laboratorial** | Execucao de exames, interfaceamento com equipamentos, liberacao de laudos |
| **Faturamento** | Pre-auditoria de guias, geracao de XML TISS, lotes e controle de glosas |
| **Financeiro** | Contas a receber/pagar, fluxo de caixa, conciliacao, rentabilidade |
| **Compras** | Fornecedores, pedidos, recebimento de insumos, estoque |
| **BI** | Dashboards e indicadores (read-only), alimentado por todos os modulos via ETL |

## Estrutura do repositorio

```
LabVida/
├── app.py                         → Tela de login (Google via Auth0)
├── pages/
│   └── home.py                    → Home pos-login
├── src/
│   ├── __init__.py
│   └── auth.py                    → Autenticacao OAuth 2.0 / OIDC com Auth0
├── alembic.ini                    → Configuracao do Alembic
├── alembic/                       → Migrations do banco
├── docker-compose.yml             → App, PostgreSQL e servicos de teste
├── Dockerfile                     → Imagem Python/Streamlit
├── Makefile                       → Comandos comuns do projeto
├── mise.toml                      → Versao Python para desenvolvimento local
├── requirements.txt               → Dependencias Python
├── tests/                         → Testes automatizados
├── CONTEXT.md                     → Glossario de dominio
├── README.md
├── LICENSE
└── docs/
    ├── adr/                       → Decisoes arquiteturais
    ├── Entrega 1/                  → Modelagem organizacional do ERP
    ├── Entrega 2/                  → Modelagem da base de dados
    ├── Entrega 3/                  → Integracao organizacional
    ├── diagramas/                  → Diagramas Mermaid (.mmd) da modelagem de dados
    └── Templates/                  → Template padrao dos documentos da equipe
```

## Stack de implementacao

- **Python 3.12**+
- **Streamlit** (frontend)
- **Auth0** (login com Google, sem custo)
- **httpx** (requisicoes HTTP para OAuth)
- **PostgreSQL**
- **Docker Compose**
- **SQLAlchemy**
- **Alembic**
- **Pydantic**
- **pytest**

## Como executar (desenvolvimento local)

### 1. Configurar Auth0

O login usa **Auth0** (plano gratuito, ate 7.000 usuarios) como intermediario para login com Google.

a) Crie uma conta gratuita em [auth0.com](https://auth0.com)

b) No Dashboard, crie uma aplicacao do tipo **Regular Web Application**

c) Em **Settings**, configure:
   - **Allowed Callback URLs**: `http://localhost:8501`
   - **Allowed Logout URLs**: `http://localhost:8501`

d) Em **Connections**, desative `Username-Password-Authentication` e mantenha apenas `google-oauth2` ativo

e) Copie **Domain**, **Client ID** e **Client Secret**

f) Copie `.env.example` para `.env`:

```bash
copy .env.example .env
```

g) Preencha as variaveis de Auth0 no `.env`:

```dotenv
AUTH0_DOMAIN=SEU_DOMINIO.auth0.com
AUTH0_CLIENT_ID=SEU_CLIENT_ID
AUTH0_CLIENT_SECRET=SEU_CLIENT_SECRET
APP_BASE_URL=http://localhost:8501
```

O mesmo `.env` e usado no desenvolvimento local e pelo Docker Compose. Variaveis de ambiente do shell sobrescrevem valores do `.env`.

### 2. Criar ambiente virtual e instalar dependencias

```bash
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```

### 3. Executar o app

```bash
.venv\Scripts\streamlit run app.py
```

Acesse: `http://localhost:8501`

### 4. Fluxo de login

```
Tela de login → "Entrar com Google" → Auth0 → Google → LabVida Home
                                                              ↓
                                                           "Sair"
```

## Como executar (Docker)

Suba o LabVida com Docker Compose:

```bash
docker compose up -d
```

O Docker Compose le o `.env` automaticamente.

Acesse:

```text
http://localhost:8501
```

Tambem e possivel usar o Makefile:

```bash
make up
```

## Makefile

O Makefile funciona tanto no **Windows** quanto no **Unix** (usa apenas recursos nativos do GNU Make + Docker CLI). No Windows, instale via Winget:

```bash
winget install GnuWin32.Make
```

Apos a instalacao, reinicie o terminal.

## Comandos comuns

```bash
make help
make up
make down
make restart
make build
make logs
make test
make migrate
make revision msg="criar tabela paciente"
make clean
```

## Testes

Execute todos os testes com:

```bash
# Via Make (com Docker):
make test

# Ou localmente (sem Docker):
.venv\Scripts\pytest tests/ -v
```

O comando `make test` sobe um PostgreSQL de teste, aplica as migrations, executa o pytest e remove o banco de teste ao final.

## Entregas

### Entrega 01 — Modelagem organizacional do ERP
Define os modulos, responsabilidades, fluxo operacional, integracoes entre setores, impactos automaticos
e regras de negocio. Um complemento adiciona a **arquitetura tecnica** (camadas, stack, modulo core,
hierarquia arquitetural e diagramas).

- [Documento da Entrega 01 (PDF)](docs/Entrega%201/-1%C2%AA%20Entrega-%20SI%20-%20LabVida.pdf)
- [Complemento — Arquitetura Tecnica](docs/Entrega%201/Entrega-01-Complemento-Arquitetura-Tecnica.md)

### Entrega 02 — Modelagem da base de dados
Traduz a arquitetura organizacional em um modelo de dados relacional (PostgreSQL): modelo conceitual,
modelo logico com dicionario de dados por modulo, regras de integridade, rastreabilidade/auditoria e
um modelo dimensional (esquema estrela) para o BI.

- [Documento da Entrega 02 — Modelagem de BD](docs/Entrega%202/Entrega-02-Modelagem-BD.md)
- [Planejamento da Entrega 02](docs/Entrega%202/PLANEJAMENTO-Entrega-02.md)

#### Diagramas
Arquivos `.mmd` ([Mermaid](https://mermaid.js.org/)) — renderizam direto no GitHub ou em [mermaid.live](https://mermaid.live):

- [MER Conceitual](docs/diagramas/MER-conceitual.mmd) — entidades e relacionamentos (alto nivel)
- [MER Logico](docs/diagramas/MER-logico.mmd) — tabelas, atributos, PKs, FKs e cardinalidades
- [BI — Esquema Estrela](docs/diagramas/BI-esquema-estrela.mmd) — modelo dimensional (fatos e dimensoes)

### Entrega 03 — Integracao organizacional
Detalha como os modulos do ERP LabVida se integram por meio do fluxo operacional da Ordem de Servico,
eventos entre setores, rastreabilidade organizacional e impactos automaticos entre atendimento, coleta,
logistica, laboratorio, faturamento, financeiro, compras, auditoria e BI.

- [Documento da Entrega 03 — Integracao Organizacional](docs/Entrega%203/Entrega-03-Integracao-Organizacional.md)

## Licenca

Distribuido sob a licenca definida em [LICENSE](LICENSE).
