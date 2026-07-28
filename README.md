# LabVida — ERP para Laboratório de Análises Clínicas

Projeto acadêmico da disciplina **Sistemas de Informação e Tecnologias (SIT)** —
Bacharelado em Ciência da Computação, **UFAPE** (Garanhuns - PE, 2026.1).
Professor: **Dr. Assuero Fonseca Ximenes**

O **LabVida** é um ERP acadêmico para uma rede regional de laboratórios de análises clínicas
(um laboratório central + quatro unidades de coleta). O projeto parte de um diagnóstico organizacional
real — baixa integração entre sistemas, logística manual de amostras, faturamento de convênios crítico,
ausência de indicadores gerenciais — e propõe uma arquitetura de ERP integrada para resolvê-lo.

## Equipe

- Aline Fernanda Soares Silva
- Clauderson Branco Xavier
- Gustavo Ferreira Wanderley
- Victor Alexandre Saraiva Pimentel

---

## Requisitos de Software e Versões Utilizadas

Para a execução e avaliação do sistema, assegure-se de que os softwares abaixo estejam instalados:

| Software / Tecnologia | Versão Mínima / Utilizada | Finalidade |
|---|---|---|
| **Python** | `3.12+` | Linguagem base da aplicação |
| **PostgreSQL** | `16+` | Banco de Dados Relacional |
| **Streamlit** | `1.60.0` (congelada no `requirements.txt`) | Interface de usuário (Frontend/Dashboard) |
| **Docker** | `24+` | Containerização da aplicação |
| **Docker Compose** | `v2+` | Orquestração de contêineres (App + PostgreSQL) |

---

## Visão Geral do ERP

O sistema é organizado em módulos especializados que refletem os setores reais do laboratório, com
um fluxo operacional integrado em torno da **Ordem de Serviço (OS)**:

```
Cadastro → Atendimento e Coleta → Logística de Amostras → Laboratorial → Faturamento → Financeiro
                                                                                          ↳ BI (alimentado por todos)
                                                              Compras → (insumos / contas a pagar)
```

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

---

## Status de Implementação

| Módulo | Status |
|---|---|
| **Cadastro** | ✅ Concluído |
| **Atendimento e Coleta** | ✅ Concluído |
| **Logística de Amostras** | ✅ Concluído |
| **Laboratorial** | ✅ Concluído |
| **Faturamento** | ✅ Concluído  |
| **Financeiro** | ✅ Concluído  |
| **Compras** | ✅ Concluído  |
| **BI** | ⏳ Pendente |

---

## Arquitetura do Banco de Dados e Migrações (Alembic)

> **Nota sobre o gerenciamento de banco de dados:**
> O projeto utiliza o **Alembic** integrado ao **SQLAlchemy** para o controle de migrações e criação do esquema relacional, em vez de scripts SQL estáticos (`.sql`). 
> 
> **Por que utilizar Alembic/ORM em vez de `.sql` estático?**
> 1. **Alinhamento com Python e ORM**: As migrações são escritas e versionadas em Python nativo (`alembic/versions/`), garantindo sincronização direta com as entidades do SQLAlchemy.
> 2. **Rastreabilidade e Evolução**: Permite controle de versão histórico do banco de dados, migrações incrementais e reversão (*rollback*) automatizada.
> 3. **Inicialização Automática**: Ao subir o container Docker ou executar a aplicação, o Alembic aplica automaticamente todas as migrações até a revisão mais recente (`alembic upgrade head`), garantindo reconstrução total do banco em qualquer ambiente sem necessidade de importação manual de scripts SQL.
> 4. **Povoamento Automatizado (Seeder)**: Para geração de dados de teste e demonstração funcional, o projeto inclui um módulo de geração de dados reais (`python -m src.seeder`).

---

## Estrutura do Repositório

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

## Como Executar (Opção 1: Utilizando Docker — Recomendado)

Suba toda a aplicação (Streamlit + Banco PostgreSQL) de forma totalmente automatizada:

### 1. Configurar variáveis de ambiente

Copie o arquivo de exemplo `.env.exemplo` para `.env`:

```bash
# Linux / macOS:
cp .env.exemplo .env

# Windows (CMD):
copy .env.exemplo .env
```

### 2. Construir e Iniciar os Containers

Execute o comando do Docker Compose:

```bash
docker compose up --build -d
```

> **O que acontece ao rodar o comando acima:**
> - O PostgreSQL 16 é iniciado e configurado automaticamente.
> - O contêiner da aplicação Python aguarda o banco ficar saudável (*healthcheck*).
> - As migrações do banco são aplicadas automaticamente (`alembic upgrade head`).
> - O servidor Streamlit é iniciado na porta 8501.

### 3. Acessar a Aplicação

Abra o navegador no endereço:

```text
http://localhost:8501
```

### 4. Parar os Containers

Para interromper os serviços:

```bash
docker compose down
```

---

## Como Executar (Opção 2: Desenvolvimento Local sem Docker)

### 1. Configurar Variáveis de Ambiente e Auth0

O login utiliza **Auth0** (plano gratuito, até 7.000 usuários) para login social com o Google.

a) Copie `.env.exemplo` para `.env`:

```bash
cp .env.exemplo .env
```

b) Preencha as credenciais do Auth0 no `.env` (caso deseje autenticação remota):

```dotenv
AUTH0_DOMAIN=SEU_DOMINIO.auth0.com
AUTH0_CLIENT_ID=SEU_CLIENT_ID
AUTH0_CLIENT_SECRET=SEU_CLIENT_SECRET
APP_BASE_URL=http://localhost:8501
DATABASE_URL=postgresql+psycopg://labvida:labvida@localhost:5432/labvida
```

### 2. Criar Ambiente Virtual e Instalar Dependências

```bash
python3 -m venv .venv

# Linux / macOS:
source .venv/bin/activate

# Windows (PowerShell):
.venv\Scripts\Activate.ps1

# Instalar dependências congeladas:
pip install -r requirements.txt
```

### 3. Criar Banco de Dados e Aplicar Migrações

Garantindo que o servidor PostgreSQL esteja em execução localmente:

```bash
# Aplica a estrutura de tabelas via Alembic:
alembic upgrade head

# Opcional: popula o banco com dados de exemplo/demonstração:
python -m src.seeder
```

### 4. Executar o Streamlit

```bash
streamlit run app.py
```

Acesse no navegador: `http://localhost:8501`

---

## Usuários e Autenticação de Acesso

O sistema utiliza autenticação segura via **OAuth 2.0 / OpenID Connect (Auth0)** integrada à conta Google. 

* **Usuário Padrão:** Qualquer conta Google válida cadastrada/autorizada no Auth0.
* **Usuário em Modo de Teste / Dev:** No ambiente local/Docker sem credenciais Auth0 configuradas, o sistema permite navegação no modo de desenvolvimento para testes de módulos.

---

## Comandos Úteis (Makefile)

Caso possua a ferramenta `make` instalada:

```bash
make help        # Lista todos os comandos disponíveis
make up          # Sobe os containers Docker
make down        # Para os containers Docker
make build       # Reconstrói as imagens Docker
make logs        # Exibe os logs dos containers
make migrate     # Executa migrações do banco (alembic upgrade head)
make test        # Executa a suíte de testes com pytest
```

---

## Testes Automatizados

Para executar os testes da aplicação:

```bash
# Via Make (com Docker):
make test

# Localmente:
pytest tests/ -v
```

---

## Documentação das Entregas

* **Entrega 01 — Modelagem Organizacional do ERP:** [docs/Entrega 1/](docs/Entrega%201/)
* **Entrega 02 — Modelagem da Base de Dados:** [docs/Entrega 2/](docs/Entrega%202/)
* **Entrega 03 — Integração Organizacional:** [docs/Entrega 3/](docs/Entrega%203/)

---

## Licença

Distribuído sob a licença definida em [LICENSE](LICENSE).
