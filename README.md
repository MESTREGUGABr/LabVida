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
  <img src="https://img.shields.io/badge/Auth-Local_(email%2Fsenha)-2E7D32?logo=lock&logoColor=white" alt="Autenticação local">
</p>

---

## 📑 Sumário

0. [⚡ Início Rápido (Docker)](#-início-rápido-docker)
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

## ⚡ Início Rápido (Docker)

Caminho mais curto para ter o sistema completo rodando (app + PostgreSQL + migrações + dados de exemplo). **A ordem importa:** o `.env` precisa existir e estar preenchido *antes* do `docker compose up`.

```bash
# 1. Criar o .env a partir do modelo  (Windows:  copy .env.exemplo .env)
cp .env.exemplo .env

# 2. Preencher LGPD_ENCRYPTION_KEY no .env (ver seção 10 — obrigatória)

# 3. Subir tudo
docker compose up --build -d
```

Acesse **<http://localhost:8501>**. Na tela de login, use a aba **"Criar conta"** (qualquer conta criada já entra como admin) ou entre com um usuário do seeder — ver [seção 12](#12-usuários-e-senhas-de-acesso-ao-sistema).

> ⏳ **Nota sobre a inicialização:** A primeira subida do container pode levar de **30 a 60 segundos** para liberar o acesso na porta 8501. Isso ocorre porque o boot executa automaticamente o build/instalação das dependências, as migrações do banco (`alembic upgrade head`) e a geração da base de dados de demonstração (`python -m src.seeder`), simulando ~3 meses de operação real do laboratório.
>
> **Não é preciso criar `venv`, instalar dependências nem rodar `make migrate` para usar o sistema via Docker.**

Acompanhar o boot em tempo real: `docker compose logs -f app` · Encerrar: `docker compose down`

As seções [7](#7-como-instalar-as-dependências) (venv) e [9](#9-como-importar-os-scripts-sql--migrations-alembic) (migrações manuais) são necessárias apenas para execução **sem Docker** ou para rodar a suíte de testes na máquina local.

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
| --- | --- |
| **Cadastro** | Pacientes, médicos, convênios, procedimentos (TUSS/TISS), unidades e setores |
| **Atendimento e Coleta** | Abertura de OS, validação de convênio, coleta e etiquetagem de amostras |
| **Logística de Amostras** | Cadeia de custódia, malotes, rastreamento e recebimento no laboratório central |
| **Laboratorial** | Execução de exames, interfaceamento com equipamentos e liberação de laudos |
| **Faturamento** | Pré-auditoria de guias, geração de XML TISS, lotes e controle de glosas |
| **Financeiro** | Contas a receber/pagar, fluxo de caixa, conciliação e rentabilidade |
| **Compras** | Fornecedores, pedidos de compra, recebimento de insumos e controle de estoque |
| **BI** | Dashboards e indicadores gerenciais (read-only), alimentado via ETL por todos os módulos |

### Status de implementação

> Estado detalhado, com fluxo, modelo de dados e pendências por módulo:
> **[docs/arquitetura.md](docs/arquitetura.md)**. Próximos passos: [docs/roadmap-execucao.md](docs/roadmap-execucao.md).

| Módulo | Status | Observação |
| --- | :---: | --- |
| Cadastro | ✅ Operacional | Falta tabela de preço particular e vigência de fim (fase F3) |
| Atendimento e Coleta | ✅ Operacional | Fluxo completo, cancelamento coerente 100% testado |
| Logística de Amostras | ✅ Operacional | Cadeia de custódia completa |
| Laboratorial | ✅ Operacional | Falta catálogo de analitos ligando resultado a faixa de referência (F3) |
| Faturamento | 🔶 Em evolução | Lote/guia/glosa funcionam; competência, guia por paciente e divergências são as fases F4–F9 |
| Financeiro | 🔶 Em evolução | Títulos e caixa funcionam; baixa parcial é a fase F10 |
| Compras | ✅ Operacional | Segregação de funções aplicada |
| BI | ✅ Reconstruído | Star schema com grão e chave natural, ETL idempotente, 4 dashboards em Altair com filtro de período |

**223 testes passando.** A suíte roda em Windows e Linux.

### Estrutura do repositório

```
LabVida/
├── app.py                         → Tela de login local (e-mail/senha) com abas Entrar/Criar conta
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
│   ├── usuario/                   → Identidade, hash de senha (bcrypt) e autenticação local
│   ├── bi/                        → Esquema estrela e ETL de carga dos fatos
│   └── seeder/                    → Base de demonstração (~3 meses de operação)
│       ├── catalogo.py            → Procedimentos, convênios, insumos e equipe
│       ├── config.py              → Volume (escala), janela temporal e RNG
│       └── <modulo>.py            → Um seeder por módulo, idempotente
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
| --- | --- |
| **Python** | `3.12+` (ver [seção 5](#5-versão-do-python-utilizada)) |
| **PostgreSQL** | `16+` (imagem `postgres:16-alpine` no Docker; ver [seção 6](#6-versão-do-postgresql-utilizada)) |
| **Docker + Docker Compose** | Docker `24+` / Docker Compose `v2+` (Recomendado para subir ambiente completo) |
| **GNU Make** | Opcional, para atalhos do `Makefile` |
| **Git** | Para clonar o repositório |

Bibliotecas Python principais (ver [`requirements.txt`](requirements.txt) para a lista completa com versões congeladas):

| Biblioteca | Finalidade |
| --- | --- |
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

> ⚠️ **Python 3.12 é o mínimo real, não uma recomendação.** O `requirements.txt` fixa `numpy==2.5.1`, que não publica distribuição para versões anteriores. Em Python 3.11 ou inferior o `pip install -r requirements.txt` falha com:
>
> ```
> ERROR: Could not find a version that satisfies the requirement numpy==2.5.1
> ```
>
> Isso vale apenas para a execução local — a imagem Docker já usa `python:3.12-slim`.

---

## 6. Versão do PostgreSQL Utilizada

```
PostgreSQL 16 (postgres:16-alpine)
```

No ambiente Docker Compose, o serviço `postgres` utiliza a imagem oficial `postgres:16-alpine`. Para instalações locais fora do Docker, utilize qualquer instância do PostgreSQL 16+.

---

## 7. Como Instalar as Dependências

> Necessário apenas para execução **sem Docker** ou para rodar `pytest` localmente. Pelo [Início Rápido](#-início-rápido-docker), as dependências já são instaladas dentro da imagem.

**7.1. Criar ambiente virtual Python (com 3.12+)**

- **Linux / macOS:**

  ```bash
  python3 --version          # precisa ser 3.12 ou superior
  python3 -m venv .venv
  ```
- **Windows (PowerShell / CMD):** o comando `python3` **não existe no Windows** — o alias apenas abre a Microsoft Store (`Python não foi encontrado; executar sem argumentos para instalar do Microsoft Store...`). Use o *Python Launcher* (`py`) apontando explicitamente a versão:

  ```powershell
  py -0p                     # lista as versões instaladas e seus caminhos
  py -3.12 -m venv .venv     # ou py -3.13, se for a versão instalada
  ```

  > Evite `python -m venv .venv` sem indicar a versão: o `python` do PATH pode ser uma versão antiga (ex.: 3.11) e o ambiente criado quebra na instalação (ver [seção 5](#5-versão-do-python-utilizada)).

**7.2. Ativar o ambiente virtual**

- **Linux / macOS:**

  ```bash
  source .venv/bin/activate
  ```
- **Windows (PowerShell):**

  ```powershell
  .venv\Scripts\Activate.ps1
  ```
- **Windows (CMD):**

  ```cmd
  .venv\Scripts\activate.bat
  ```

**7.3. Instalar dependências congeladas**

```bash
python --version             # confirme que o venv ativo é 3.12+
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

> O `.env` precisa estar preenchido antes deste comando — ver [seção 10](#10-como-configurar-o-arquivo-env).

### Opção B — PostgreSQL local (Sem Docker)

Caso prefira utilizar uma instância local do PostgreSQL, crie o banco de dados e o usuário no seu gerenciador SQL:

```sql
CREATE DATABASE labvida;
CREATE USER labvida WITH PASSWORD 'labvida';
GRANT ALL PRIVILEGES ON DATABASE labvida TO labvida;
```

E ajuste o `DATABASE_URL` do `.env` para apontar ao host local:

```dotenv
DATABASE_URL=postgresql+psycopg://labvida:labvida@localhost:5432/labvida
```

> O valor padrão do `.env.exemplo` usa `@postgres:5432` — `postgres` é o nome do serviço **na rede interna do Docker** e não resolve fora dela. Rodar `alembic`/`streamlit` na máquina host com esse valor falha com `failed to resolve host 'postgres'`.
>
> O contêiner do Compose publica a porta `5432`, então `localhost:5432` também funciona para acessar da máquina host o banco que está rodando no Docker.

---

## 9. Como Importar os Scripts SQL / Migrations (Alembic)

O LabVida suporta a reconstrução do banco de dados tanto via **scripts SQL diretos (`schema.sql`, `dados.sql`, `banco.backup`)** quanto via **migrações automatizadas (Alembic)**.

### 9.1. Restauração via Scripts SQL (`schema.sql` / `dados.sql` / `banco.backup`)

Para importar diretamente os arquivos SQL fornecidos na raiz do projeto:

- **Restaurar Estrutura e Dados via `schema.sql` e `dados.sql`:**

  ```bash
  psql -U labvida -d labvida -f schema.sql
  psql -U labvida -d labvida -f dados.sql
  ```

  *(Ou via Docker)*:

  ```bash
  docker compose exec -T postgres psql -U labvida -d labvida < schema.sql
  docker compose exec -T postgres psql -U labvida -d labvida < dados.sql
  ```

- **Restaurar via Backup Completo (`banco.backup`):**

  ```bash
  pg_restore -U labvida -d labvida -c banco.backup
  ```

  *(Ou via Docker)*:

  ```bash
  docker compose exec -T postgres pg_restore -U labvida -d labvida -c < banco.backup
  ```

---

### 9.2. Aplicar as Migrações de Estrutura (Alembic)

> **Ao subir por Docker, as migrações já são aplicadas automaticamente** no boot do container (item 3 da caixa acima). Os comandos abaixo servem para reaplicá-las manualmente ou para uso sem Docker. Confira o resultado com `docker compose logs app | grep "Running upgrade"`.

- **Via Docker:**

  ```bash
  docker compose run --rm app alembic upgrade head
  ```

  Com GNU Make instalado, o atalho equivalente é `make migrate`.
- **Localmente (sem Docker):**

  ```bash
  alembic upgrade head
  ```

  > Exige o venv da [seção 7](#7-como-instalar-as-dependências) **ativado** e `DATABASE_URL` apontando para `localhost` (ver [seção 8, Opção B](#opção-b--postgresql-local-sem-docker)).

### 9.2. Popular o Banco com Dados de Exemplo (Seed)

> Também executado automaticamente no boot do container Docker (leva ~35s na primeira vez; nas seguintes é ignorado, pois cada módulo é idempotente).

O seeder não gera registros soltos: ele **simula ~3 meses de operação do laboratório**, atravessando o fluxo ponta a ponta pelos mesmos services da aplicação. Ou seja, as regras de negócio são validadas de verdade — OS de convênio só coleta com autorização, resultado só entra com amostra recebida no central, laudo só é liberado por responsável técnico com resultados revisados, lote só fecha se passar na pré-auditoria TISS.

- **Via Docker:**

  ```bash
  docker compose run --rm app python -m src.seeder
  ```
- **Localmente (sem Docker):**

  ```bash
  python -m src.seeder
  ```

**O que é gerado (volume padrão):**

| Módulo | Conteúdo |
| --- | --- |
| **RBAC** | 11 perfis, 33 permissões e 16 usuários — um por função (recepção, coleta, bancada, RT, faturista, financeiro, compras, almoxarifado) |
| **Cadastro** | 5 unidades e 15 setores, 8 convênios, 30 procedimentos com analitos e faixas de referência, 240 preços negociados, 12 médicos (5 responsáveis técnicos), 220 pacientes |
| **Atendimento** | ~400 OS distribuídas em dias de movimento por unidade, com ~1.600 exames, em **todos os estágios**: aberta, coletada, em trânsito, em análise, concluída e cancelada |
| **Logística** | ~100 malotes (despachados e recebidos), com amostras rejeitadas por avaria e cadeia de custódia completa |
| **Laboratorial** | 6 equipamentos, 34 valores de referência, ~1.300 resultados (dentro e fora da faixa) e ~950 laudos entre rascunho e liberado |
| **Faturamento** | ~70 lotes (abertos e fechados), guias TISS e ~80 glosas parciais e integrais |
| **Financeiro** | Títulos a receber vindos do fechamento de lote, despesas fixas mensais, baixas com movimento de caixa e conciliações de pagamento divergente |
| **Compras** | 8 fornecedores, 24 insumos com preço de tabela, ~18 pedidos em todos os status e estoque com entradas e saídas |
| **BI** | Carga do esquema estrela (dimensões + fatos de atendimento, faturamento, financeiro e logística) |

**Ajustar o volume:** todo o volume é escalável, útil para gerar uma base menor (demonstração rápida) ou maior (teste de carga):

```bash
python -m src.seeder --escala 0.2   # ~1/5 do volume
SEED_ESCALA=3 python -m src.seeder  # 3x o volume
```

| Variável | Padrão | Efeito |
| --- | :---: | --- |
| `SEED_ESCALA` | `1.0` | Multiplicador de volume de todos os módulos |
| `SEED_JANELA_DIAS` | `90` | Período de operação simulado (afeta a série temporal do BI) |
| `SEED_INICIO` | — | Data ISO de início da operação simulada (ex.: `2022-01-01`); tem precedência sobre `SEED_JANELA_DIAS` |
| `SEED_SEMENTE` | `20261` | Semente do gerador aleatório |

**Estender a série temporal (ex.: operação de 2022 até hoje):** a janela inteira sai da data definida em `SEED_INICIO`, e os volumes padrão (OS, pacientes, pedidos) crescem proporcionalmente para manter a densidade por mês — com `2022-01-01` a base fica com ~7.5k OS e ~56 competências.

A série não é uniforme: `src/seeder/trajetoria.py` molda a **evolução real da empresa** — crescimento ~2%/mês (≈27% ao ano), sazonalidade local (pico de inverno, vales em dez-jan, domingo residual), e o catálogo define o ciclo de vida da rede: a Unidade São José abre em jul/2023 e a Boa Vista em fev/2024, os convênios Hapvida, SulAmérica, NotreDame, Cassi e Golden Cross entram na carteira ao longo dos anos, o mix particular cai de ~30% para ~12%, o TAT da bancada melhora e a rejeição de amostras cai de ~8% para ~4%. O resultado no BI: faturamento, volume de exames e custos fixos crescem juntos, mês a mês.

Como cada módulo do seeder é idempotente, a base atual precisa ser recriada antes:

```bash
# 1. Apaga o volume do Postgres (perde os dados atuais — tudo dummy)
docker compose down -v

# 2. Sobe com a janela longa definida (o boot aplica migrations e roda o seeder)
SEED_INICIO=2022-01-01 docker compose up -d
```

> Deixe `SEED_INICIO=2022-01-01` no `.env` se quiser que a base longa vire o padrão do projeto (o compose repassa a variável ao container).

> ⏳ O seed com a janela de 2022 até hoje gera ~7.5k OS e pode levar de **20 a 60 minutos** na primeira subida; o app só responde na porta 8501 depois do seeder concluir. Acompanhe com `docker compose logs -f app`. Alternativamente, suba só o banco e rode o seeder à parte:
>
> ```bash
> docker compose up -d postgres
> SEED_INICIO=2022-01-01 docker compose run --rm app python -m src.seeder
> docker compose up -d
> ```
>
> (A segunda subida do `app` reusa os dados já semeados: os módulos detectam as tabelas cheias e não duplicam nada.)

---

## 10. Como Configurar o Arquivo `.env`

**10.1. Criar o arquivo `.env` a partir do modelo `.env.exemplo`**

- **Linux / macOS:**

  ```bash
  cp .env.exemplo .env
  ```
- **Windows:**

  ```cmd
  copy .env.exemplo .env
  ```

**10.2. Preencher as Variáveis de Ambiente**

No arquivo `.env`, preencha os parâmetros de conexão e a chave de criptografia:

```dotenv
DATABASE_URL=postgresql+psycopg://labvida:labvida@postgres:5432/labvida
POSTGRES_USER=labvida
POSTGRES_PASSWORD=labvida
POSTGRES_DB=labvida

APP_BASE_URL=http://localhost:8501
PORT=8501

# Login local (F15) — senha de todos os usuários do seeder de demo. Opcional,
# default "labvida123" se ausente. Ver seção 12.
SENHA_PADRAO_SEED=labvida123

LGPD_ENCRYPTION_KEY=Q22r1OivohTtSBRaMi-hjLxXxrQ3SwEdOumlaNDfvw8=
```

> ⚠️ **`LGPD_ENCRYPTION_KEY` é obrigatória e precisa estar preenchida antes de `docker compose up`** — o Compose interrompe a subida logo no início se estiver vazia:
>
> ```
> error while interpolating services.app.environment.LGPD_ENCRYPTION_KEY:
> required variable LGPD_ENCRYPTION_KEY is missing a value
> ```
>
> Sobre o `DATABASE_URL`: use `@postgres:5432` para executar **via Docker** (nome do serviço na rede do Compose) e `@localhost:5432` para executar **na máquina host** (ver [seção 8, Opção B](#opção-b--postgresql-local-sem-docker)).

---

## 11. Comando para Executar o Streamlit

### Opção A — Via Docker Compose (Recomendado)

```bash
docker compose up -d
```

Acesse no navegador: `http://localhost:8501` *(Nota: na primeira execução, o container leva de 30 a 60 segundos para concluir as migrações e o seeder de dados inicial antes da aplicação responder).*

### Opção B — Desenvolvimento Local

Com o venv da [seção 7](#7-como-instalar-as-dependências) ativado, um PostgreSQL acessível e `DATABASE_URL` apontando para `localhost`:

```bash
streamlit run app.py
```

Acesse no navegador: `http://localhost:8501`

**Fluxo de Autenticação / Login:**

```
Tela de login (abas "Entrar" / "Criar conta") → LabVida Home
                                                       ↓
                                                    "Sair"
```

---

## 12. Usuário(s) e Senha(s) de Acesso ao Sistema

O LabVida usa **autenticação local por e-mail e senha** (fase F15 — correção pedida pelo professor na apresentação de 09/08/2026, substituindo o login social por Google/Auth0; ver [ADR 0010](docs/adr/0010-substituir-login-google-por-email-senha.md)). A tela de login tem duas abas, sempre visíveis:

- **Entrar** — e-mail e senha de uma conta já existente.
- **Criar conta** — nome, e-mail e senha. **Toda conta criada aqui recebe automaticamente o perfil `admin`** — decisão aceitável só porque o projeto é acadêmico e não vai a produção real; simplifica testes, já que qualquer conta nova já administra o sistema (rebaixar para outro perfil é feito depois em *Administração → Usuários*, se quiser).

**Dados de Teste:** o seeder automatizado (`python -m src.seeder`) popula ~3 meses de operação completa — ver [seção 9.2](#92-popular-o-banco-com-dados-de-exemplo-seed) — e cria toda a equipe de demonstração **já com senha definida**, pronta para logar. A senha de todos eles é a variável `SENHA_PADRAO_SEED` do `.env` (default `labvida123` se não for definida). Exemplo, com o admin de demonstração:

| Campo | Valor |
|---|---|
| E-mail | `direcao@labvida.com.br` |
| Senha | valor de `SENHA_PADRAO_SEED` (default `labvida123`) |

Qualquer outro e-mail da lista em [`src/seeder/catalogo.py`](src/seeder/catalogo.py) (`USUARIOS`) usa a mesma senha. Trocar `SENHA_PADRAO_SEED` no `.env` só afeta usuários criados ou re-semeados **depois** da troca — não redefine a senha de quem já tem uma.

---

## 13. Observações Importantes para Execução do Projeto

- **Suporte ao Makefile:** O `Makefile` é apenas um conjunto de atalhos — **nenhum comando do projeto depende dele**. Windows não traz GNU Make por padrão (`O termo 'make' não é reconhecido...`); instale-o com `winget install GnuWin32.Make` ou use diretamente o comando `docker compose` equivalente:

  | Atalho Make | Comando equivalente |
  | --- | --- |
  | `make up` | `docker compose up -d` |
  | `make down` | `docker compose down` |
  | `make build` | `docker compose build` |
  | `make logs` | `docker compose logs -f app` |
  | `make migrate` | `docker compose run --rm app alembic upgrade head` |
  | `make seeder` | `docker compose run --rm app python -m src.seeder` |
  | `make test` | `docker compose --profile test run --rm app_test` |
  | `make clean` | `docker compose down -v` |

- **Suíte de Testes Automatizados:**

  ```bash
  make test
  # Ou via Docker, sem Make:
  docker compose --profile test run --rm app_test
  # Ou localmente (venv 3.12+ ativado, banco acessível em localhost):
  pytest tests/ -v
  ```

### 13.1. Problemas Comuns

| Erro | Causa | Solução |
| --- | --- | --- |
| `Python não foi encontrado; executar sem argumentos para instalar do Microsoft Store` | `python3` não existe no Windows — é um alias da Store | Use `py -3.12 -m venv .venv` ([seção 7.1](#7-como-instalar-as-dependências)) |
| `ERROR: Could not find a version that satisfies the requirement numpy==2.5.1` | O venv foi criado com Python 3.11 ou inferior | Recrie o venv com Python 3.12+ ([seção 5](#5-versão-do-python-utilizada)) |
| `required variable LGPD_ENCRYPTION_KEY is missing a value` | `.env` ausente ou com `LGPD_ENCRYPTION_KEY` vazia | Preencha o `.env` antes de subir ([seção 10](#10-como-configurar-o-arquivo-env)) |
| `E-mail ou senha inválidos` ao logar com usuário do seeder | `SENHA_PADRAO_SEED` foi trocada depois que o seeder já tinha criado o usuário | Use a senha com a qual o usuário foi criado, ou redefina a senha dele em *Administração → Usuários* |
| `O termo 'make' não é reconhecido...` | GNU Make não instalado (padrão no Windows) | Use o comando `docker compose` equivalente da tabela acima |
| `failed to resolve host 'postgres'` | `DATABASE_URL` com host da rede interna do Docker sendo usado na máquina host | Use `@localhost:5432` para rodar fora do Docker ([seção 8, Opção B](#opção-b--postgresql-local-sem-docker)) |
| `docker compose up` conclui mas a porta 8501 não responde | Migrações/seed ainda executando no boot | Acompanhe com `docker compose logs -f app` |

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
| --- | --- |
| [MER Conceitual](docs/Entrega%202/diagramas/MER-conceitual.mmd) | Entidades e relacionamentos (alto nível) |
| [MER Lógico](docs/Entrega%202/diagramas/MER-logico.mmd) | Tabelas, atributos, PKs, FKs e cardinalidades |
| [BI — Esquema Estrela](docs/Entrega%202/diagramas/BI-esquema-estrela.mmd) | Modelo dimensional **como entregue na Entrega 02** |

> O esquema estrela foi reconstruído depois da Entrega 02. O modelo **em vigor** está em
> [docs/diagramas/bi-esquema-estrela.mmd](docs/diagramas/bi-esquema-estrela.mmd).

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
