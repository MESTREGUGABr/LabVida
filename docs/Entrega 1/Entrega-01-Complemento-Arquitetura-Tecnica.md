# Complemento da Entrega 01 — Arquitetura Técnica do ERP LabVida

**Disciplina:** Sistemas de Informação e Tecnologias (SIT)
**Projeto:** ERP LabVida — Laboratório de Análises Clínicas
**Equipe:** Aline Fernanda Soares Silva · Clauderson Branco Xavier · Gustavo Ferreira Wanderley · Victor Alexandre Saraiva Pimentel

> Este documento **complementa a 1ª Entrega**, atendendo aos pontos avaliados como *"Atendeu Parcialmente"*.
> A Entrega 01 cobriu com profundidade a **arquitetura organizacional** (módulos, fluxos, regras,
> integrações). Aqui detalhamos a **arquitetura técnica**: organização em camadas, stack tecnológica,
> destaque do módulo *core*, hierarquia arquitetural e a representação **visual** do sistema.

---

## Pontos atendidos por este complemento

| # | Critério (avaliação do professor) | Lacuna apontada | Seção que resolve |
|---|---|---|---|
| 1 | Arquitetura técnica do sistema | Faltou detalhamento explícito da arquitetura tecnológica completa | §1, §2 |
| 2 | Organização de código e camadas | Faltou backend, frontend, services, controllers, APIs, filas, camadas | §2, §3 |
| 3 | Clareza do módulo *core* | O núcleo operacional não foi destacado arquiteturalmente como "core do ERP" | §4 |
| 4 | Hierarquia arquitetural | Faltou divisão entre camadas operacionais, estratégicas, analíticas e serviços compartilhados | §5 |
| 5 | Estrutura visual do ERP | Faltou um diagrama visual completo | §6 (e diagramas §2, §4, §5) |

---

## 1. Visão geral da arquitetura tecnológica

O ERP LabVida adota uma **arquitetura em camadas (layered)** com **módulos de domínio** desacoplados,
combinada a um **barramento de eventos** que materializa os "impactos automáticos" descritos na Entrega 01.
A escolha responde diretamente aos problemas do diagnóstico organizacional:

| Decisão técnica | Problema do diagnóstico que resolve |
|---|---|
| Banco de dados relacional único e integrado | (b) Baixa integração entre sistemas; duplicidade de dados |
| Barramento de eventos / filas assíncronas | (d) Logística manual sem rastreamento em tempo real |
| API Gateway + serviços compartilhados | (c) Gargalos no atendimento (redigitação em vários sistemas) |
| Camada analítica (ETL + Data Warehouse) | (a) Gestão descentralizada; (f) Ausência de dashboards |
| Camada de segurança transversal (IAM, criptografia, auditoria) | (g) Riscos de segurança da informação |
| Integrações TISS e interfaceamento de equipamentos | (e) Faturamento crítico; processo laboratorial manual |

**Stack tecnológica de referência:**

| Camada | Tecnologias de referência |
|---|---|
| Frontend (Apresentação) | Aplicação web SPA (React/Angular) + app responsivo para coleta nas unidades |
| Backend (Aplicação) | API REST (Node.js/NestJS ou Java/Spring Boot), organizada em controllers → services → repositories |
| Mensageria / Eventos | Fila de mensagens (RabbitMQ/Kafka) para propagação assíncrona de eventos entre módulos |
| Persistência operacional | Banco relacional **PostgreSQL** (OLTP) |
| Persistência analítica | Data Warehouse + processo ETL para o módulo de BI (OLAP) |
| Integrações externas | APIs de convênios, padrão **TISS** (XML), interfaceamento HL7/ASTM com analisadores clínicos |
| Segurança | IAM/Auth (JWT + RBAC), criptografia de dados sensíveis, logs de auditoria append-only |

---

## 2. Arquitetura em camadas (organização de código)

A organização lógica do sistema separa responsabilidades técnicas em camadas bem definidas. Cada
requisição percorre as camadas de cima para baixo; os eventos automáticos trafegam pelo barramento.

```mermaid
flowchart TB
    subgraph FE["🖥️ Camada de Apresentação (Frontend)"]
        WEB["Portal Web (SPA)<br/>Atendimento · Gestão"]
        MOBILE["App de Coleta<br/>(unidades)"]
        DASH["Dashboards BI<br/>(diretoria)"]
    end

    subgraph GW["🚪 API Gateway"]
        GATEWAY["Roteamento · Rate limit · Auth"]
    end

    subgraph APP["⚙️ Camada de Aplicação (Backend)"]
        direction TB
        CTRL["Controllers (REST API)"]
        SVC["Services (regras de negócio)"]
        REPO["Repositories (acesso a dados)"]
        CTRL --> SVC --> REPO
    end

    subgraph DOM["📦 Módulos de Domínio"]
        M1["Cadastro"]
        M2["Atendimento/Coleta"]
        M3["Logística"]
        M4["Laboratorial"]
        M5["Faturamento"]
        M6["Financeiro"]
        M7["Compras"]
    end

    subgraph SHARED["🔧 Serviços Compartilhados (transversais)"]
        AUTH["Auth/IAM · RBAC"]
        CRYPTO["Criptografia"]
        AUDIT["Auditoria append-only"]
        NOTIF["Notificações"]
        TISS["Integração TISS / Convênios"]
        EQUIP["Interfaceamento de Equipamentos"]
    end

    subgraph BUS["📨 Barramento de Eventos / Filas"]
        QUEUE["Mensageria assíncrona<br/>(impactos automáticos)"]
    end

    subgraph DATA["🗄️ Camada de Dados"]
        OLTP[("PostgreSQL<br/>Base Operacional (OLTP)")]
        ETL["ETL"]
        DW[("Data Warehouse<br/>(OLAP / BI)")]
    end

    FE --> GW --> APP
    APP --> DOM
    DOM --> SHARED
    DOM --> QUEUE
    QUEUE --> DOM
    REPO --> OLTP
    OLTP --> ETL --> DW
    DASH --> DW
```

**Leitura da camada de aplicação (padrão por módulo):**
- **Controller** — expõe os endpoints REST, valida entrada, traduz HTTP ↔ domínio.
- **Service** — concentra as **regras de negócio** da Entrega 01 (ex.: "não faturar OS sem laudo liberado").
- **Repository** — isola o acesso ao PostgreSQL, garantindo que regras não conheçam detalhes de SQL.
- **Eventos** — após uma operação, o service publica um evento na fila; outros módulos reagem (assíncrono).

---

## 3. Comunicação assíncrona — os "impactos automáticos" como eventos

A Seção 5 da Entrega 01 ("Impactos Automáticos das Operações") é implementada tecnicamente via
**barramento de eventos**. Cada gatilho organizacional vira uma mensagem publicada/consumida:

```mermaid
sequenceDiagram
    participant AT as Atendimento
    participant BUS as Barramento de Eventos
    participant LOG as Logística
    participant LAB as Laboratorial
    participant FAT as Faturamento
    participant FIN as Financeiro
    participant BI as BI (ETL)

    AT->>BUS: ColetaRegistrada
    BUS->>LOG: cria pendência de transporte
    LOG->>BUS: AmostraRecebida
    BUS->>LAB: desbloqueia execução técnica
    LAB->>BUS: LaudoLiberado
    BUS->>FAT: envia item p/ pré-auditoria
    FAT->>BUS: LoteFechado
    BUS->>FIN: gera títulos a receber
    Note over BUS,BI: Todo evento também alimenta o ETL → cubos do BI
    BUS-->>BI: evento replicado para análise
```

Esse desacoplamento por eventos é o que garante baixo acoplamento entre módulos (justificativa
arquitetural da Entrega 01) e resolve a logística manual sem rastreamento em tempo real.

---

## 4. Módulo *core* do ERP (núcleo operacional)

O **core do ERP LabVida** é o eixo **Atendimento → Ordem de Serviço (OS) → Laboratorial**, organizado
em torno da **Ordem de Serviço como entidade-espinha** que atravessa todo o ciclo de vida operacional.
Todos os demais módulos orbitam e dependem desse núcleo.

```mermaid
flowchart LR
    subgraph CORE["⭐ CORE DO ERP — Ciclo de Vida da Ordem de Serviço"]
        direction LR
        OS["📋 Ordem de Serviço (OS)<br/><b>entidade-espinha</b>"]
        AT["Atendimento<br/>e Coleta"]
        LAB["Laboratorial"]
        AT --> OS --> LAB
    end

    CAD["Cadastro<br/>(habilita o core)"]
    LOG["Logística<br/>(transporta a amostra)"]
    FAT["Faturamento"]
    FIN["Financeiro"]
    COM["Compras<br/>(abastece insumos)"]
    BI["BI"]

    CAD -.fornece dados.-> CORE
    CORE -.amostra.-> LOG
    LOG -.devolve ao fluxo.-> CORE
    CORE -.laudo liberado.-> FAT
    FAT --> FIN
    COM -.insumos.-> LAB
    CORE -.eventos.-> BI
    FAT -.eventos.-> BI
    FIN -.eventos.-> BI

    classDef core fill:#1f6feb,stroke:#0d419d,color:#fff;
    class OS,AT,LAB,CORE core;
```

**Por que esse é o core:**
- É onde a **OS nasce, percorre seu ciclo de vida e gera o laudo** — o produto final do laboratório.
- Sem ele, nenhum outro módulo tem o que processar: Faturamento depende do laudo, Financeiro depende do faturamento, BI depende de todos os eventos gerados aqui.
- Concentra as **regras de negócio mais críticas** (clínicas e de rastreabilidade): identificador único da OS, vínculo amostra↔OS, liberação de laudo por responsável técnico, auditoria imutável de resultados.
- Cadastro é **pré-condição** (habilita), Compras é **suporte** (abastece), e Faturamento/Financeiro/BI são **consumidores a jusante** do que o core produz.

---

## 5. Hierarquia arquitetural (camadas estratégicas)

Os módulos do ERP se organizam em uma **hierarquia de quatro camadas**, conforme seu papel na operação
e na tomada de decisão — do chão de operação até a estratégia da diretoria.

```mermaid
flowchart TB
    subgraph L4["🎯 Camada Estratégica (Diretoria)"]
        BI["Business Intelligence<br/>dashboards · indicadores · metas"]
    end

    subgraph L3["📊 Camada Analítica (Gestão)"]
        ETL["ETL · Data Warehouse"]
        REL["Relatórios gerenciais · DRE · rentabilidade"]
    end

    subgraph L2["⚙️ Camada Operacional (Núcleo do negócio)"]
        CORE["Atendimento/OS · Logística · Laboratorial"]
        FAT["Faturamento"]
        FIN["Financeiro"]
        COM["Compras"]
        CAD["Cadastro"]
    end

    subgraph L1["🔧 Camada de Serviços Compartilhados (Transversal)"]
        AUTH["Autenticação · RBAC"]
        CRYPTO["Criptografia · LGPD"]
        AUDIT["Auditoria append-only"]
        NOTIF["Notificações"]
        INT["Integrações TISS · Equipamentos"]
    end

    L2 --> L3 --> L4
    L1 -.suporta todas.-> L2
    L1 -.suporta todas.-> L3
    L1 -.suporta todas.-> L4

    classDef strat fill:#8250df,stroke:#6639ba,color:#fff;
    classDef anal fill:#bf8700,stroke:#9e6a03,color:#fff;
    classDef op fill:#1a7f37,stroke:#116329,color:#fff;
    classDef shared fill:#6e7781,stroke:#424a53,color:#fff;
    class BI strat;
    class ETL,REL anal;
    class CORE,FAT,FIN,COM,CAD op;
    class AUTH,CRYPTO,AUDIT,NOTIF,INT shared;
```

| Camada | Papel | Módulos / componentes |
|---|---|---|
| **Estratégica** | Decisão da diretoria baseada em dados | BI (dashboards, metas, preditivos) |
| **Analítica** | Consolidação e geração de indicadores | ETL, Data Warehouse, relatórios gerenciais, DRE |
| **Operacional** | Execução do dia a dia do laboratório | Cadastro, Atendimento/OS, Logística, Laboratorial, Faturamento, Financeiro, Compras |
| **Serviços Compartilhados** | Recursos transversais reutilizáveis | Auth/RBAC, criptografia, auditoria, notificações, integrações |

A camada analítica é **alimentada** pela operacional (sem interferir nela — BI é *read-only*, respeitando
a regra da Entrega 01), e a camada de serviços compartilhados **atravessa** todas as demais.

---

## 6. Estrutura visual completa do ERP

Diagrama macro que substitui a descrição puramente textual da Seção 2 da Entrega 01, mostrando os
módulos, o fluxo central e a alimentação do BI por todas as operações.

```mermaid
flowchart LR
    CAD["📇 Cadastro"] --> AT["🩸 Atendimento<br/>e Coleta"]
    AT --> LOG["🚚 Logística<br/>de Amostras"]
    LOG --> LAB["🔬 Laboratorial"]
    LAB --> FAT["🧾 Faturamento<br/>de Convênios"]
    FAT --> FIN["💰 Financeiro"]
    COM["🛒 Compras"] -.insumos.-> LAB
    COM -.contas a pagar.-> FIN

    CAD -.-> BI["📊 Business Intelligence"]
    AT -.-> BI
    LOG -.-> BI
    LAB -.-> BI
    FAT -.-> BI
    FIN -.-> BI
    COM -.-> BI

    classDef flow fill:#0969da,stroke:#0a3069,color:#fff;
    classDef support fill:#1a7f37,stroke:#116329,color:#fff;
    classDef bi fill:#8250df,stroke:#6639ba,color:#fff;
    class CAD,AT,LOG,LAB,FAT,FIN flow;
    class COM support;
    class BI bi;
```

**Legenda:** linha cheia = fluxo operacional principal (ciclo da OS); linha tracejada = alimentação do BI
e suporte de Compras. O BI é alimentado por **todos** os módulos, conforme a Entrega 01.

---

## 7. Síntese

Com este complemento, a Entrega 01 passa a apresentar — além da já consolidada arquitetura
organizacional — a **arquitetura técnica completa**: organização em camadas (frontend, backend com
controllers/services/repositories, mensageria, dados), stack tecnológica explícita, comunicação
assíncrona por eventos, destaque do **core** operacional (ciclo da OS), **hierarquia arquitetural** em
quatro camadas e a **representação visual** do sistema por diagramas. Esses elementos servem de base
direta para a Entrega 02 (modelagem da base de dados), onde a camada de dados aqui descrita é detalhada.
