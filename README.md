<p align="center">
  <img src="assets/banner_labvida.png" alt="LabVida ERP" width="600">
</p>

<h1 align="center">LabVida</h1>
<p align="center"><b>ERP para Laboratório de Análises Clínicas</b></p>

<p align="center">
  Projeto acadêmico da disciplina <b>Sistemas de Informação e Tecnologias (SIT)</b><br>
  Bacharelado em Ciência da Computação, <b>UFAPE</b> (Garanhuns - PE, 2026.1)<br>
  Professor: <b>Dr. Assuero Fonseca Ximenes</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12+-blue?logo=python&logoColor=white" alt="Python 3.12+">
  <img src="https://img.shields.io/badge/Streamlit-1.60-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white" alt="PostgreSQL 16">
  <img src="https://img.shields.io/badge/Alembic-Migrations-red?logo=alembic&logoColor=white" alt="Alembic">
  <img src="https://img.shields.io/badge/Docker-Compose_v2-2496ED?logo=docker&logoColor=white" alt="Docker Compose">
  <img src="https://img.shields.io/badge/Auth0-OAuth2.0-EB5424?logo=auth0&logoColor=white" alt="Auth0">
</p>

---

## 📑 Sumário

1. [Nome do Projeto](#1-nome-do-projeto)
2. [Integrantes da Equipe](#2-integrantes-da-equipe)
3. [Descrição do Sistema](#3-descrição-do-sistema)
   - [Visão geral do ERP](#visão-geral-do-erp)
   - [Status de implementação](#status-de-implementação)
   - [Estrutura do repositório](#estrutura-do-repositório)
4. [Requisitos de Software](#4-requisitos-de-software)
5. [Versão do Python Utilizada](#5-versão-do-python-utilizada)
6. [Versão do PostgreSQL Utilizada](#6-versão-do-postgresql-utilizada)
7. [Como Instalar as Dependências](#7-como-instalar-as-dependências)
8. [Como Criar o Banco de Dados](#8-como-criar-o-banco-de-dados)
9. [Como Importar os Scripts SQL / Migrations](#9-como-importar-os-scripts-sql--migrations-alembic)
10. [Como Configurar o Arquivo `.env`](#10-como-configurar-o-arquivo-env)
11. [Comando para Executar o Streamlit](#11-comando-para-executar-o-streamlit)
12. [Usuário(s) e Senha(s) de Acesso ao Sistema](#12-usuários-e-senhas-de-acesso-ao-sistema)
13. [Observações Importantes para Execução do Projeto](#13-observações-importantes-para-execução-do-projeto)
14. [Entregas Acadêmicas](#entregas-acadêmicas)
15. [Licença](#licença)

---

## 1. Nome do Projeto

**LabVida — ERP para Laboratório de Análises Clínicas**

---

## 2. Integrantes da Equipe

<table align="center">
  <tr>
    <td align="center">
      <a href="https://github.com/alinesors">
        <img src="assets/aline-foto.png" width="110px" alt="Aline Fernanda"/><br>
        <sub><b>Aline Fernanda Soares Silva</b></sub><br>
        <sub>@alinesors</sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/ClaudersonXavier">
        <img src="assets/clauderson-foto.png" width="110px" alt="Clauderson Branco"/><br>
        <sub><b>Clauderson Branco Xavier</b></sub><br>
        <sub>@ClaudersonXavier</sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/MESTREGUGABr">
        <img src="assets/guga-foto.jpg" width="110px" alt="Gustavo Ferreira"/><br>
        <sub><b>Gustavo Ferreira Wanderley</b></sub><br>
        <sub>@MESTREGUGABr</sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/SVictor-Saraiva-P">
        <img src="assets/victor-foto.jpg" width="110px" alt="Victor Alexandre"/><br>
        <sub><b>Victor Alexandre Saraiva Pimentel</b></sub><br>
        <sub>@Victor-Saraiva-P</sub>
      </a>
    </td>
  </tr>
</table>

---

## 3. Descrição do Sistema

O **LabVida** é um ERP acadêmico desenvolvido para uma rede regional de laboratórios de análises clínicas (composta por um laboratório central e quatro unidades de coleta). O projeto parte de um diagnóstico organizacional real — caracterizado por baixa integração entre sistemas, logística manual de amostras, faturamento crítico de convênios e ausência de indicadores gerenciais — e constrói uma arquitetura de ERP totalmente integrada.

### Visão geral do ERP

O sistema é organizado em módulos especializados que refletem os setores reais do laboratório, com um fluxo operacional integrado em torno da **Ordem de Serviço (OS)**:

<p align="center">
  <img src="assets/fluxo_operacional.png" alt="Fluxo operacional do ERP LabVida" width="600">
</p>

| Módulo | Responsabilidade |
|---|---|
| **Cadastro** | Pacientes, médicos, convênios, procedimentos (TUSS/TISS), unidades e setores |
| **Atendimento e Coleta** | Abertura de OS, validação de convênio, coleta e etiquetagem de amostras |
| **Logística de Amostras** | Cadeia de custódia, malotes, rastreamento e recebimento no laboratório central |
| **Laboratorial** | Execução de exames, interfaceamento com equipamentos e liberação de laudos |
| **Faturamento** | Pré-auditoria de guias, geração de XML TISS, lotes e controle de glosas |
| **Financeiro** | Contas a receber/pagar, fluxo de caixa, conciliação e rentabilidade |
| **Compras** | Fornecedores, pedidos de compra, recebimento de insumos e controle de estoque |
| **BI** | Dashboards e indicadores gerenciais (read-only), alimentado via ETL por todos os módulos |

### Status de implementação

| Módulo | Status |
|---|:---:|
| Cadastro | ✅ Concluído |
| Atendimento e Coleta | ✅ Concluído |
| Logística de Amostras | ✅ Concluído |
| Laboratorial | ✅ Concluído |
| Faturamento | ✅ Concluído |
| Financeiro | ✅ Concluído |
| Compras | ✅ Concluído |
| BI | ⏳ Pendente |

### Estrutura do repositório

```
LabVida/
├── app.py                         → Tela de login (Google via Auth0)
├── pages/
│   ├── home.py                    → Home pós-login
│   ├── cadastro_*.py              → Cadastros (Pacientes, Convênios, Médicos, Procedimentos, Unidades)
│   ├── atendimento_*.py           → Ordens de Serviço e Coleta
│   ├── logistica_*.py             → Malotes e Recebimento
│   ├── laboratorio_*.py           → Resultados e Laudos
│   ├── faturamento_*.py           → Guias TISS e Glosas
│   ├── financeiro_*.py            → Contas a Receber/Pagar e Fluxo de Caixa
│   └── compras_*.py               → Fornecedores, Pedidos e Estoque
├── src/
│   ├── auth.py                    → Autenticação OAuth 2.0 / OIDC com Auth0
│   ├── config.py                  → Carga de configuração (.env)
│   ├── db.py                      → Engine SQLAlchemy + session_scope()
│   ├── ui.py                      → Helpers Streamlit (exigir_login)
│   ├── cadastro/                  → Pacientes, Convênios, Médicos, Procedimentos, Unidades
│   ├── atendimento/               → Ordem de Serviço, Coleta e Amostra
│   ├── logistica/                 → Malotes e Protocolo de Recebimento
│   ├── laboratorial/              → Equipamentos, Resultados e Laudos
│   ├── faturamento/               → Lotes de Faturamento, Guias TISS e Glosas
│   ├── financeiro/                → Títulos a Receber/Pagar, Caixa e Conciliação
│   ├── compras/                   → Fornecedores, Pedidos de Compra e Estoque
│   ├── usuario/                   → Identidade do Auth0
│   └── seeder/                    → Dados de exemplo (Faker)
├── alembic.ini                    → Configuração do Alembic
├── alembic/                       → Migrações do banco de dados
├── docker-compose.yml             → Serviços Docker (App Streamlit + PostgreSQL 16)
├── Dockerfile                     → Imagem Python 3.12 / Streamlit
├── Makefile                       → Comandos utilitários do projeto
├── requirements.txt               → Dependências congeladas (pip freeze)
├── .env.exemplo                   → Modelo de variáveis de ambiente
├── tests/                         → Testes automatizados (pytest)
├── CONTEXT.md                     → Glossário de domínio
├── README.md                      → Documentação principal
└── LICENSE
```

---

## 4. Requisitos de Software

Para executar o LabVida localmente (via Docker ou Python nativo), os requisitos necessários são:

| Requisito | Versão / Observação |
|---|---|
| **Python** | `3.12+` (ver [seção 5](#5-versão-do-python-utilizada)) |
| **PostgreSQL** | `16+` (imagem `postgres:16-alpine` no Docker; ver [seção 6](#6-versão-do-postgresql-utilizada)) |
| **Docker + Docker Compose** | Docker `24+` / Docker Compose `v2+` (Recomendado para subir ambiente completo) |
| **GNU Make** | Opcional, para atalhos do `Makefile` |
| **Conta Auth0** | Plano gratuito, usada para login social via Google |
| **Git** | Para clonar o repositório |

Bibliotecas Python principais (ver [`requirements.txt`](requirements.txt) para a lista completa com versões congeladas):

| Biblioteca | Finalidade |
|---|---|
| **Streamlit** | Frontend e Dashboard web interativo |
| **SQLAlchemy** | Mapeamento Objeto-Relacional (ORM) |
| **Alembic** | Gerenciamento de migrações do banco de dados |
| **Pydantic** | Validação e tipagem de modelos de dados |
| **httpx** | Requisições HTTP para verificação de tokens OAuth |
| **pytest** | Suíte de testes automatizados |

---

## 5. Versão do Python Utilizada

```
Python 3.12+
```

A versão de desenvolvimento é gerenciada nativamente e fixada no arquivo [`mise.toml`](mise.toml). Caso utilize a ferramenta [mise](https://mise.jdx.dev/), execute `mise install` na raiz do projeto.

---

## 6. Versão do PostgreSQL Utilizada

```
PostgreSQL 16 (postgres:16-alpine)
```

No ambiente Docker Compose, o serviço `postgres` utiliza a imagem oficial `postgres:16-alpine`. Para instalações locais fora do Docker, utilize qualquer instância do PostgreSQL 16+.

---

## 7. Como Instalar as Dependências

**7.1. Criar ambiente virtual Python**

```bash
python3 -m venv .venv
```

**7.2. Ativar o ambiente virtual**

* **Linux / macOS:**
  ```bash
  source .venv/bin/activate
  ```
* **Windows (PowerShell):**
  ```powershell
  .venv\Scripts\Activate.ps1
  ```
* **Windows (CMD):**
  ```cmd
  .venv\Scripts\activate.bat
  ```

**7.3. Instalar dependências congeladas**

```bash
pip install -r requirements.txt
```

---

## 8. Como Criar o Banco de Dados

O banco de dados PostgreSQL pode ser instanciado de duas formas:

### Opção A — Via Docker Compose (Recomendado)

O `docker-compose.yml` provisiona e configura automaticamente o banco PostgreSQL 16 com persistência de dados:

```bash
docker compose up --build -d
```

ou via Makefile:

```bash
make up
```

### Opção B — PostgreSQL local (Sem Docker)

Caso prefira utilizar uma instância local do PostgreSQL, crie o banco de dados e o usuário no seu gerenciador SQL:

```sql
CREATE DATABASE labvida;
CREATE USER labvida WITH PASSWORD 'labvida';
GRANT ALL PRIVILEGES ON DATABASE labvida TO labvida;
```

---

## 9. Como Importar os Scripts SQL / Migrations (Alembic)

O LabVida **não utiliza dumps estáticos (`.sql`) manuais** — a estrutura relacional é versionada e aplicada via **Alembic** (migrations em Python), e os dados iniciais de demonstração são gerados via **seeder automatizado**.

> **Por que utilizar Alembic/ORM em vez de scripts `.sql` estáticos?**
> 1. **Alinhamento Nátivo com Python/SQLAlchemy**: Garantia de sincronização entre a camada de modelos (`src/*/models.py`) e as tabelas reais do banco.
> 2. **Versionamento e Evolução**: Histórico completo de migrações (`alembic/versions/`), permitindo atualizações e rollbacks automatizados.
> 3. **Execução Automática no Docker**: Ao rodar `docker compose up`, o container executa `alembic upgrade head` no boot, construindo a base inteira sem intervenção manual.
> 4. **Dados de Demonstração (Seeder)**: Geração de registros coerentes com regras de negócio usando dados fictícios via Faker.

### 9.1. Aplicar as Migrações de Estrutura

* **Via Make / Docker:**
  ```bash
  make migrate
  ```
* **Localmente (sem Docker):**
  ```bash
  alembic upgrade head
  ```

### 9.2. Popular o Banco com Dados de Exemplo (Seed)

Para popular a base de dados com registros reais de teste (pacientes, médicos, convênios, ordens de serviço, amostras e laudos):

```bash
python -m src.seeder
```

---

## 10. Como Configurar o Arquivo `.env`

**10.1. Criar o arquivo `.env` a partir do modelo `.env.exemplo`**

* **Linux / macOS:**
  ```bash
  cp .env.exemplo .env
  ```
* **Windows:**
  ```cmd
  copy .env.exemplo .env
  ```

**10.2. Preencher as Variáveis de Ambiente**

No arquivo `.env`, preencha os parâmetros de conexão e credenciais do Auth0:

```dotenv
DATABASE_URL=postgresql+psycopg://labvida:labvida@postgres:5432/labvida
POSTGRES_USER=labvida
POSTGRES_PASSWORD=labvida
POSTGRES_DB=labvida

AUTH0_DOMAIN=SEU_DOMINIO.auth0.com
AUTH0_CLIENT_ID=SEU_CLIENT_ID
AUTH0_CLIENT_SECRET=SEU_CLIENT_SECRET

APP_BASE_URL=http://localhost:8501
PORT=8501

LGPD_ENCRYPTION_KEY=Q22r1OivohTtSBRaMi-hjLxXxrQ3SwEdOumlaNDfvw8=
```

---

## 11. Comando para Executar o Streamlit

### Opção A — Via Docker Compose (Recomendado)

```bash
docker compose up -d
```

Acesse no navegador: `http://localhost:8501`

### Opção B — Desenvolvimento Local

```bash
streamlit run app.py
```

Acesse no navegador: `http://localhost:8501`

**Fluxo de Autenticação / Login:**

```
Tela de login → "Entrar com Google" → Auth0 → Google → LabVida Home
                                                               ↓
                                                            "Sair"
```

---

## 12. Usuário(s) e Senha(s) de Acesso ao Sistema

O LabVida utiliza autenticação via **Auth0 + Login Social do Google (OAuth 2.0 / OIDC)**.

* **Ambiente com Auth0 Configurado:** Qualquer conta Google autorizada no tenant Auth0.
* **Ambiente de Desenvolvimento Local / Testes:** Caso a aplicação seja executada sem credenciais Auth0 ativas no `.env`, o sistema permite navegação no modo de desenvolvimento para testes completos de todos os módulos.
* **Dados de Teste:** O seeder automatizado (`python -m src.seeder`) popula cadastros completos de pacientes, convênios e exames para avaliação funcional.

---

## 13. Observações Importantes para Execução do Projeto

* **Suporte ao Makefile:** O `Makefile` é compatível com Linux, macOS e Windows (via GNU Make). No Windows, pode ser instalado com:
  ```cmd
  winget install GnuWin32.Make
  ```
* **Comandos Úteis do Makefile:**
  ```bash
  make help        # Exibe lista de comandos
  make up          # Sobe os containers Docker
  make down        # Encerra os containers Docker
  make build       # Reconstrói a imagem Docker
  make logs        # Visualiza os logs dos containers
  make migrate     # Aplica as migrações do banco de dados
  make test        # Executa a suíte de testes unitários com pytest
  ```
* **Suíte de Testes Automatizados:**
  ```bash
  make test
  # Ou localmente:
  pytest tests/ -v
  ```

---

## Entregas Acadêmicas

<details open>
<summary><b>Entrega 01 — Modelagem organizacional do ERP</b></summary>
<br>

Define os módulos, responsabilidades, fluxo operacional, integrações entre setores, impactos automáticos e regras de negócio. Um complemento adiciona a **arquitetura técnica** (camadas, stack, módulo core, hierarquia arquitetural e diagramas).

- [Documento da Entrega 01 (PDF)](docs/Entrega%201/-1%C2%AA%20Entrega-%20SI%20-%20LabVida.pdf)
- [Complemento — Arquitetura Técnica](docs/Entrega%201/Entrega-01-Complemento-Arquitetura-Tecnica.md)

</details>

<details open>
<summary><b>Entrega 02 — Modelagem da base de dados</b></summary>
<br>

Traduz a arquitetura organizacional em um modelo de dados relacional (PostgreSQL): modelo conceitual, modelo lógico com dicionário de dados por módulo, regras de integridade, rastreabilidade/auditoria e um modelo dimensional (esquema estrela) para o BI.

- [Documento da Entrega 02 — Modelagem de BD](docs/Entrega%202/Entrega-02-Modelagem-BD.md)
- [Planejamento da Entrega 02](docs/Entrega%202/PLANEJAMENTO-Entrega-02.md)

**Diagramas** — arquivos `.mmd` ([Mermaid](https://mermaid.js.org/)), renderizam direto no GitHub ou em [mermaid.live](https://mermaid.live):

| Diagrama | Descrição |
|---|---|
| [MER Conceitual](docs/diagramas/MER-conceitual.mmd) | Entidades e relacionamentos (alto nível) |
| [MER Lógico](docs/diagramas/MER-logico.mmd) | Tabelas, atributos, PKs, FKs e cardinalidades |
| [BI — Esquema Estrela](docs/diagramas/BI-esquema-estrela.mmd) | Modelo dimensional (fatos e dimensões) |

</details>

<details open>
<summary><b>Entrega 03 — Integração organizacional</b></summary>
<br>

Detalha como os módulos do ERP LabVida se integram por meio do fluxo operacional da Ordem de Serviço, eventos entre setores, rastreabilidade organizacional e impactos automáticos entre atendimento, coleta, logística, laboratório, faturamento, financeiro, compras, auditoria e BI.

- [Documento da Entrega 03 — Integração Organizacional](docs/Entrega%203/Entrega-03-Integracao-Organizacional.md)

</details>

---

## Licença

Distribuído sob a licença definida em [LICENSE](LICENSE).

<p align="center">
  <sub>Feito com 💙 pela equipe LabVida — UFAPE 2026</sub>
</p>
