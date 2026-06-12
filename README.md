# LabVida — ERP para Laboratório de Análises Clínicas

Projeto acadêmico da disciplina **Sistemas de Informação e Tecnologias (SIT)** —
Bacharelado em Ciência da Computação, **UFAPE** (Garanhuns - PE, 2026).

O **LabVida** é um ERP acadêmico para uma rede regional de laboratórios de análises clínicas
(um laboratório central + quatro unidades de coleta). O projeto parte de um diagnóstico organizacional
real — baixa integração entre sistemas, logística manual de amostras, faturamento de convênios crítico,
ausência de indicadores gerenciais — e propõe uma arquitetura de ERP integrada para resolvê-lo.

## Equipe

- Aline Fernanda Soares Silva
- Clauderson Branco Xavier
- Gustavo Ferreira Wanderley
- Victor Alexandre Saraiva Pimentel

## Visão geral do ERP

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

## Estrutura do repositório

```
LabVida/
├── app.py                         → Página inicial do Streamlit
├── alembic.ini                    → Configuração do Alembic
├── alembic/                       → Migrations do banco
├── docker-compose.yml             → App, PostgreSQL e serviços de teste
├── Dockerfile                     → Imagem Python/Streamlit
├── Makefile                       → Comandos comuns do projeto
├── mise.toml                      → Versão Python para desenvolvimento local
├── requirements.txt               → Dependências Python
├── tests/                         → Testes automatizados
├── CONTEXT.md                     → Glossário de domínio
├── README.md
├── LICENSE
└── docs/
    ├── adr/                       → Decisões arquiteturais
    ├── Entrega 1/                  → Modelagem organizacional do ERP
    │   ├── -1ª Entrega- SI - LabVida.pdf
    │   └── Entrega-01-Complemento-Arquitetura-Tecnica.md
    ├── Entrega 2/                  → Modelagem da base de dados
    │   ├── Entrega-02-Modelagem-BD.md
    │   └── PLANEJAMENTO-Entrega-02.md
    ├── Entrega 3/                  → Integração organizacional
    │   └── Entrega-03-Integracao-Organizacional.md
    ├── diagramas/                  → Diagramas Mermaid (.mmd) da modelagem de dados
    │   ├── MER-conceitual.mmd
    │   ├── MER-logico.mmd
    │   ├── MER(usado no relatorio).mmd
    │   └── BI-esquema-estrela.mmd
    └── Templates/                  → Template padrão dos documentos da equipe
```

## Stack de implementação

- **Python 3.12**
- **Streamlit**
- **PostgreSQL**
- **Docker Compose**
- **SQLAlchemy**
- **Alembic**
- **Pydantic**
- **pytest**

## Como executar

Suba o LabVida com Docker Compose:

```bash
docker compose up -d
```

Acesse:

```text
http://localhost:8501
```

Também é possível usar o Makefile:

```bash
make up
```

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
make test
```

Esse comando sobe um PostgreSQL de teste, aplica as migrations, executa o pytest e remove o banco de teste ao final.

## Entregas

### Entrega 01 — Modelagem organizacional do ERP
Define os módulos, responsabilidades, fluxo operacional, integrações entre setores, impactos automáticos
e regras de negócio. Um complemento adiciona a **arquitetura técnica** (camadas, stack, módulo core,
hierarquia arquitetural e diagramas).

- [Documento da Entrega 01 (PDF)](docs/Entrega%201/-1%C2%AA%20Entrega-%20SI%20-%20LabVida.pdf)
- [Complemento — Arquitetura Técnica](docs/Entrega%201/Entrega-01-Complemento-Arquitetura-Tecnica.md)

### Entrega 02 — Modelagem da base de dados
Traduz a arquitetura organizacional em um modelo de dados relacional (PostgreSQL): modelo conceitual,
modelo lógico com dicionário de dados por módulo, regras de integridade, rastreabilidade/auditoria e
um modelo dimensional (esquema estrela) para o BI.

- [Documento da Entrega 02 — Modelagem de BD](docs/Entrega%202/Entrega-02-Modelagem-BD.md)
- [Planejamento da Entrega 02](docs/Entrega%202/PLANEJAMENTO-Entrega-02.md)

#### Diagramas
Arquivos `.mmd` ([Mermaid](https://mermaid.js.org/)) — renderizam direto no GitHub ou em [mermaid.live](https://mermaid.live):

- [MER Conceitual](docs/diagramas/MER-conceitual.mmd) — entidades e relacionamentos (alto nível)
- [MER Lógico](docs/diagramas/MER-logico.mmd) — tabelas, atributos, PKs, FKs e cardinalidades
- [BI — Esquema Estrela](docs/diagramas/BI-esquema-estrela.mmd) — modelo dimensional (fatos e dimensões)

### Entrega 03 — Integração organizacional
Detalha como os módulos do ERP LabVida se integram por meio do fluxo operacional da Ordem de Serviço,
eventos entre setores, rastreabilidade organizacional e impactos automáticos entre atendimento, coleta,
logística, laboratório, faturamento, financeiro, compras, auditoria e BI.

- [Documento da Entrega 03 — Integração Organizacional](docs/Entrega%203/Entrega-03-Integracao-Organizacional.md)

## Licença

Distribuído sob a licença definida em [LICENSE](LICENSE).
