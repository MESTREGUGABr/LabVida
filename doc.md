<p align="center">
  <img src="assets/banner_labvida.png" alt="LabVida" width="600">
</p>

<h1 align="center">LabVida</h1>
<p align="center"><b>ERP para Laboratório de Análises Clínicas</b></p>

<p align="center">
  Projeto acadêmico da disciplina <b>Sistemas de Informação e Tecnologias (SIT)</b><br>
  Bacharelado em Ciência da Computação, <b>UFAPE</b> (Garanhuns - PE, 2026)
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12+-blue?logo=python&logoColor=white" alt="Python 3.12+">
  <img src="https://img.shields.io/badge/Streamlit-frontend-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/PostgreSQL-database-4169E1?logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white" alt="Docker Compose">
  <img src="https://img.shields.io/badge/Auth0-login-EB5424?logo=auth0&logoColor=white" alt="Auth0">
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
9. [Como Importar os Scripts SQL / Migrations](#9-como-importar-os-scripts-sql--restaurar-o-backup-migrations)
10. [Como Configurar o Arquivo `.env`](#10-como-configurar-o-arquivo-env)
11. [Comando para Executar o Streamlit](#11-comando-para-executar-o-streamlit)
12. [Usuário(s) e Senha(s) de Acesso](#12-usuários-e-senhas-de-acesso-ao-sistema)
13. [Observações Importantes](#13-observações-importantes-para-execução-do-projeto)
14. [Entregas Acadêmicas](#entregas-acadêmicas)
15. [Licença](#licença)

---

## 1. Nome do Projeto

**LabVida - ERP para Laboratório de Análises Clínicas**

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

O **LabVida** é um ERP acadêmico para uma rede regional de laboratórios de análises clínicas
(um laboratório central + quatro unidades de coleta). O projeto parte de um diagnóstico organizacional
real, baixa integração entre sistemas, logística manual de amostras, faturamento de convênios crítico,
ausência de indicadores gerenciais e propõe uma arquitetura de ERP integrada para resolvê-lo.

### Visão geral do ERP

O sistema é organizado em módulos especializados que refletem os setores reais do laboratório, com
um fluxo operacional integrado em torno da **Ordem de Serviço (OS)**:

<p align="center">
  <img src="assets/fluxo_operacional.png" alt="Fluxo operacional do ERP LabVida" width="600">
</p>

| Módulo | Responsabilidade |
|---|---|
| **Cadastro** | Pacientes, médicos, convênios, procedimentos (TUSS/TISS), unidades, setores |
| **Atendimento e Coleta** | Abertura de OS, validação de convênio, coleta e etiquetagem de amostras |
| **Logística de Amostras** | Cadeia de custódia, malotes, rastreamento e recebimento no laboratório central |
| **Laboratorial** | Execução de exames, interfaceamento com equipamentos, liberação de laudos |
| **Faturamento** | Pré-auditoria de guias, geração de XML TISS, lotes e controle de glosas |
| **Financeiro** | Contas a receber/pagar, fluxo de caixa, conciliação, rentabilidade |
| **Compras** | Fornecedores, pedidos, recebimento de insumos, estoque |
| **BI** | Dashboards e indicadores (read-only), alimentado por todos os módulos via ETL |

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
atualizar
```

---

## 4. Requisitos de Software

Para executar o LabVida localmente (com ou sem Docker), são necessários:

| Requisito | Observação |
|---|---|
| **Python** | 3.12+ (ver [seção 5](#5-versão-do-python-utilizada)) |
| **PostgreSQL** | `[PREENCHER: ex. PostgreSQL 16]` (ver [seção 6](#6-versão-do-postgresql-utilizada)) |
| **Docker + Docker Compose** | Recomendado para subir app + banco de forma integrada |
| **GNU Make** | Opcional, para usar os atalhos do `Makefile` |
| **Conta Auth0** | Plano gratuito (até 7.000 usuários), usada para login com Google |
| **Git** | Para clonar o repositório |

Bibliotecas Python principais (ver `requirements.txt` para a lista completa e versões travadas):

| Biblioteca | Finalidade |
|---|---|
| **Streamlit** | Frontend da aplicação |
| **httpx** | Requisições HTTP para OAuth |
| **SQLAlchemy** | ORM |
| **Alembic** | Migrations do banco |
| **Pydantic** | Validação de dados |
| **pytest** | Testes automatizados |

---

## 5. Versão do Python Utilizada

```
Python 3.12+
```

A versão exata usada em desenvolvimento é fixada no arquivo [`mise.toml`](mise.toml). Caso utilize
[mise](https://mise.jdx.dev/) para gerenciar versões locais, basta rodar `mise install` na raiz do projeto.

---

## 6. Versão do PostgreSQL Utilizada

```
[PREENCHER: ex. PostgreSQL 16]
```

> ℹ️ A versão exata da imagem do PostgreSQL utilizada em Docker está definida no serviço `db` do
> [`docker-compose.yml`](docker-compose.yml). Verifique o campo `image:` (ex. `postgres:16-alpine`) e
> substitua o placeholder acima pela versão correspondente.

---

## 7. Como Instalar as Dependências

**7.1. Criar ambiente virtual**

```bash
python -m venv .venv
```

**7.2. Instalar dependências**

```bash
.venv\Scripts\pip install -r requirements.txt
```

> Em ambientes Unix/Linux/Mac, utilize `source .venv/bin/activate` e depois `pip install -r requirements.txt`.

---

## 8. Como Criar o Banco de Dados

O banco de dados PostgreSQL pode ser criado de duas formas:

**Opção A — Via Docker Compose (recomendado)**

O `docker-compose.yml` já provisiona automaticamente um container PostgreSQL configurado para o projeto:

```bash
docker compose up -d
```

ou, usando o Makefile:

```bash
make up
```

**Opção B — PostgreSQL local (sem Docker)**

Caso prefira usar uma instância local do PostgreSQL, crie manualmente o banco e o usuário indicados no `.env`:

```sql
CREATE DATABASE labvida;
CREATE USER labvida_user WITH PASSWORD 'SENHA_AQUI';
GRANT ALL PRIVILEGES ON DATABASE labvida TO labvida_user;
```

> `[PREENCHER: confirmar nome exato do banco/usuário/senha padrão definidos em config.py ou docker-compose.yml]`

---

## 9. Como Importar os Scripts SQL / Restaurar o Backup (Migrations)

O LabVida **não utiliza dump/backup `.sql` manual** — o schema do banco é versionado e aplicado via
**Alembic** (migrations). Os dados de exemplo são gerados via **seeder** (Faker).

**9.1. Aplicar as migrations**

Via Docker/Make:

```bash
make migrate
```

Localmente (sem Docker):

```bash
.venv\Scripts\alembic upgrade head
```

**9.2. Criar uma nova migration (quando alterar modelos)**

```bash
make revision msg="criar tabela paciente"
```

**9.3. Popular o banco com dados de exemplo (seed)**

```
[PREENCHER: comando exato do seeder, ex. .venv\Scripts\python -m src.seeder.run]
```

> ℹ️ Ao subir o ambiente via `docker compose up -d` ou `make up`, as migrations podem já ser aplicadas
> automaticamente pelo entrypoint do container — confirme esse comportamento no `Dockerfile` /
> `docker-compose.yml` do projeto.

---

## 10. Como Configurar o Arquivo `.env`

O login do LabVida usa **Auth0** (plano gratuito, até 7.000 usuários) como intermediário para login com Google.

**10.1. Configurar o Auth0**

a) Crie uma conta gratuita em [auth0.com](https://auth0.com)

b) No Dashboard, crie uma aplicação do tipo **Regular Web Application**

c) Em **Settings**, configure:
   - **Allowed Callback URLs**: `http://localhost:8501`
   - **Allowed Logout URLs**: `http://localhost:8501`

d) Em **Connections**, desative `Username-Password-Authentication` e mantenha apenas `google-oauth2` ativo

e) Copie **Domain**, **Client ID** e **Client Secret**

**10.2. Criar o arquivo `.env`**

```bash
copy .env.example .env
```

> Em Unix/Linux/Mac: `cp .env.example .env`

**10.3. Preencher as variáveis no `.env`**

```dotenv
AUTH0_DOMAIN=SEU_DOMINIO.auth0.com
AUTH0_CLIENT_ID=SEU_CLIENT_ID
AUTH0_CLIENT_SECRET=SEU_CLIENT_SECRET
APP_BASE_URL=http://localhost:8501

# Configuração do banco de dados
DATABASE_URL=[PREENCHER: ex. postgresql://labvida_user:senha@localhost:5432/labvida]
```

> O mesmo `.env` é usado no desenvolvimento local e pelo Docker Compose. Variáveis de ambiente do
> shell sobrescrevem valores do `.env`.

---

## 11. Comando para Executar o Streamlit

**Opção A — Desenvolvimento local (sem Docker)**

```bash
.venv\Scripts\streamlit run app.py
```

Acesse: `http://localhost:8501`

**Opção B — Via Docker Compose**

```bash
docker compose up -d
```

ou:

```bash
make up
```

Acesse: `http://localhost:8501`

**Fluxo de login**

```
Tela de login → "Entrar com Google" → Auth0 → Google → LabVida Home
                                                              ↓
                                                           "Sair"
```

---

## 12. Usuário(s) e Senha(s) de Acesso ao Sistema

O LabVida **não utiliza usuário/senha próprios** — a autenticação é feita exclusivamente via
**Auth0 + login social do Google (OAuth 2.0 / OIDC)**. Não há credenciais internas cadastradas na
aplicação.

Para testar o sistema, utilize uma conta Google válida configurada no seu tenant Auth0
(dependendo da configuração do Auth0, pode ser necessário liberar o e-mail de teste em
**Auth0 → Authentication → Social → Google** ou adicioná-lo como usuário de teste).

> `[PREENCHER: caso exista algum usuário de teste específico (ex. conta de professor/avaliador
> pré-cadastrada no Auth0), listar aqui e-mail e instruções de acesso]`

Dados de exemplo (pacientes, convênios, OS, etc.) são gerados automaticamente pelo **seeder** (Faker),
não exigindo login manual de dados para testes funcionais dos módulos.

---

## 13. Observações Importantes para Execução do Projeto

- O Makefile funciona tanto no **Windows** quanto no **Unix** (usa apenas recursos nativos do GNU Make + Docker CLI). No Windows, instale via Winget:

  ```bash
  winget install GnuWin32.Make
  ```

  Após a instalação, reinicie o terminal.

- **Comandos comuns** disponíveis via Makefile:

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

- **Testes automatizados**:

  ```bash
  # Via Make (com Docker):
  make test

  # Ou localmente (sem Docker):
  .venv\Scripts\pytest tests/ -v
  ```

  O comando `make test` sobe um PostgreSQL de teste, aplica as migrations, executa o pytest e remove
  o banco de teste ao final.

- O módulo **BI** ainda está **pendente** de implementação (ver [seção 3 — Status de implementação](#status-de-implementação)).

- O `docker-compose.yml` lê o `.env` automaticamente; não é necessário exportar variáveis manualmente
  ao usar Docker.

---

## Entregas Acadêmicas

<details open>
<summary><b>Entrega 01 — Modelagem organizacional do ERP</b></summary>
<br>

Define os módulos, responsabilidades, fluxo operacional, integrações entre setores, impactos automáticos
e regras de negócio. Um complemento adiciona a **arquitetura técnica** (camadas, stack, módulo core,
hierarquia arquitetural e diagramas).

- [Documento da Entrega 01 (PDF)](docs/Entrega%201/-1%C2%AA%20Entrega-%20SI%20-%20LabVida.pdf)
- [Complemento — Arquitetura Técnica](docs/Entrega%201/Entrega-01-Complemento-Arquitetura-Tecnica.md)

</details>

<details open>
<summary><b>Entrega 02 — Modelagem da base de dados</b></summary>
<br>

Traduz a arquitetura organizacional em um modelo de dados relacional (PostgreSQL): modelo conceitual,
modelo lógico com dicionário de dados por módulo, regras de integridade, rastreabilidade/auditoria e
um modelo dimensional (esquema estrela) para o BI.

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

Detalha como os módulos do ERP LabVida se integram por meio do fluxo operacional da Ordem de Serviço,
eventos entre setores, rastreabilidade organizacional e impactos automáticos entre atendimento, coleta,
logística, laboratório, faturamento, financeiro, compras, auditoria e BI.

- [Documento da Entrega 03 — Integração Organizacional](docs/Entrega%203/Entrega-03-Integracao-Organizacional.md)

</details>

---

## Licença

Distribuído sob a licença definida em [LICENSE](LICENSE).

<p align="center">
  <sub>Feito com 💙 pela equipe LabVida — UFAPE 2026</sub>
</p>