# LabVida — Arquitetura e Estado do Sistema

> **Documento de referência do estado atual.** Descreve o que existe hoje no código:
> fluxo, camadas, modelo de dados, módulos e o que já foi implementado.
> Atualizado em **02/08/2026** · branch `evolucao-erp` · head do Alembic `0014_bi_reconstrucao`.
>
> Para *o que vem a seguir*, veja [roadmap-execucao.md](roadmap-execucao.md).
> Para a linguagem de domínio, [CONTEXT.md](../CONTEXT.md).

---

## Sumário

1. [O que é o LabVida](#1-o-que-é-o-labvida)
2. [Arquitetura de código](#2-arquitetura-de-código)
3. [Fluxo ponta a ponta](#3-fluxo-ponta-a-ponta)
4. [Módulos implementados](#4-módulos-implementados)
5. [Business Intelligence](#5-business-intelligence)
6. [Segurança, RBAC, LGPD e auditoria](#6-segurança-rbac-lgpd-e-auditoria)
7. [Modelo de dados](#7-modelo-de-dados)
8. [Testes](#8-testes)
9. [Migrations](#9-migrations)
10. [Como rodar](#10-como-rodar)
11. [Estado por fase e pendências](#11-estado-por-fase-e-pendências)
12. [Mapa da documentação](#12-mapa-da-documentação)

---

## 1. O que é o LabVida

ERP para uma rede regional de laboratórios de análises clínicas — laboratório central mais unidades de coleta. Projeto acadêmico da disciplina **Sistemas de Informação e Tecnologias**, UFAPE, 2026.1.

O sistema cobre o ciclo completo: cadastro → abertura de OS → coleta → transporte em malote → recebimento → bancada → laudo → faturamento TISS → título → caixa, com compras e BI ao lado.

**Stack:** Python 3.12 · Streamlit 1.60 · PostgreSQL 16 · SQLAlchemy 2.0 · Alembic · Pydantic 2 · Altair 6 · Auth0 (OAuth2/OIDC) · Docker Compose.

**O que torna o projeto não-CRUD:** a Ordem de Serviço é uma entidade-espinha com máquina de estados e histórico auditável; a amostra tem cadeia de custódia rastreada; o faturamento tem pré-auditoria e ciclo de glosa; e o BI é um star schema separado, alimentado por ETL a partir do operacional.

---

## 2. Arquitetura de código

### 2.1 Pacote vertical por domínio

Cada domínio é um pacote com a mesma anatomia, do banco à tela:

```
src/<dominio>/<subdominio>/
├── models.py       SQLAlchemy — tabela e relacionamentos
├── dtos.py         Pydantic — contratos de entrada/saída e enums de status
├── repository.py   Consultas. Sem regra de negócio.
├── service.py      Regra de negócio, validação, permissão e auditoria
└── errors.py       Exceções do domínio
```

A página em `pages/` **orquestra**: chama service, trata erro, renderiza. Não decide regra.

### 2.2 Camadas

```
pages/*.py                  Streamlit — 27 telas, montadas por st.navigation
   │  (só chama service; a partir da F2, BI não tem SQL em página)
   ▼
src/<dominio>/service.py    Regra de negócio · RBAC · auditoria · transação
   ▼
src/<dominio>/repository.py Consulta pura
   ▼
src/db.py                   Engine, Session, Base
   ▼
PostgreSQL
```

### 2.3 Transação

`session_scope()` ([src/db.py](../src/db.py)) entrega a sessão, faz **rollback em exceção** e fecha. O `commit` é responsabilidade do service — não há auto-commit. O engine usa `pool_pre_ping` e `pool_recycle=1800` para não quebrar na primeira query após conexão ociosa.

### 2.4 Camada de UI (fase F1)

| Peça | Papel |
|---|---|
| `app.py` | **Entrypoint e roteador.** Decide entre login e aplicação, e monta `st.navigation` a partir das permissões. Única chamada de `set_page_config` |
| [ui.py](../src/ui.py) `paginas_permitidas()` | Regra de visibilidade do menu — função pura, testável |
| [ui_components/data_grid.py](../src/ui_components/data_grid.py) | `renderizar_grid()` — **fronteira única** com o AgGrid. Formatação pt-BR, ordenação, filtro, paginação e seleção num só lugar |
| [ui_components/erros.py](../src/ui_components/erros.py) | `tratar_erros()` — converte falha em mensagem legível, classificando pela origem da exceção |
| [ui_components/](../src/ui_components/) | Cabeçalho, seção, KPI, badge de status, estado vazio |

**Regra:** a página orquestra (chama service → renderiza componente). Não monta SQL, não monta HTML e não fala com o AgGrid diretamente.

### 2.5 Transversais

| Módulo | Papel |
|---|---|
| [src/auth.py](../src/auth.py) | OAuth2/PKCE com Auth0 |
| [src/rbac/](../src/rbac/) | Perfil → Permissão (N:N), gate por tela |
| [src/lgpd/](../src/lgpd/) | Fernet + SHA-256 no CPF, rotação de chave |
| [src/auditoria/](../src/auditoria/) | Trilha append-only |
| [src/ui.py](../src/ui.py), [ui_css.py](../src/ui_css.py), [ui_components/](../src/ui_components/) | Shell, menu, design system |
| [src/seeder/](../src/seeder/) | Base de demonstração idempotente |

---

## 3. Fluxo ponta a ponta

```
CADASTRO           paciente · convênio · médico · procedimento(+valor) · unidade/setor
   │
   ▼
ATENDIMENTO        abrir_os()  →  ORDEM DE SERVIÇO (a espinha)
   │               ├─ valida convênio ATIVO
   │               ├─ cria AutorizacaoConvenio PENDENTE
   │               ├─ gera codigo_os  OS-{ano}-{6 hex}
   │               └─ registra transição em os_status_historico
   ▼
COLETA             registrar_coleta()  →  AMOSTRA + código de barras
   │               ├─ exige permissão atendimento:coletar
   │               └─ exige autorização VALIDA quando há convênio
   ▼
LOGÍSTICA          malote → despachar → protocolo de recebimento
   │               ├─ cadeia de custódia em amostras_movimentacoes
   │               └─ amostra divergente vai para REJEITADA
   ▼
LABORATORIAL       resultado por ANALITO → revisão → LAUDO
   │               ├─ bloqueia resultado sem amostra RECEBIDA
   │               ├─ liberação exige responsável técnico ativo
   │               └─ alteração de resultado gera auditoria imutável
   ▼
FATURAMENTO        lote → guia TISS → item  →  pré-auditoria  →  fechar
   │               ├─ só laudo LIBERADO entra
   │               ├─ validar_lote() checa TUSS, valor e laudo
   │               └─ glosa abate o item (validação CUMULATIVA)
   ▼
FINANCEIRO         título a receber → baixa → movimento de caixa
   │
   ▼
BI                 ETL → star schema → 4 dashboards
```

**Compras** roda em paralelo: solicitação → aprovação → título a pagar → recebimento → estoque.

### 3.1 Máquina de estados da OS

`ABERTA → EM_ANALISE → CONCLUIDA`, com `CANCELADA` como terminal. As regras de agregação são o ponto mais bem coberto do sistema (12/12 histórias testadas):

- Cancelar item individual não cancela a OS enquanto houver item ativo.
- OS vira `CONCLUIDA` quando **todos os itens ativos** têm laudo liberado — itens cancelados não impedem.
- OS vira `CANCELADA` só quando **todos** os itens estão cancelados.
- Item com laudo liberado ou já faturado **não pode** ser cancelado.
- Toda transição grava `usuario_id` em `os_status_historico`.

Decisões em [ADR 0004](adr/0004-ator-da-conclusao-da-os.md), [0005](adr/0005-semantica-de-cancelamento-da-os.md) e [0006](adr/0006-protecao-contra-cancelamento-de-os-concluida-parcialmente.md).

---

## 4. Módulos implementados

### 4.1 Cadastro

| Entidade | Telas | Regras aplicadas |
|---|---|---|
| Paciente | [cadastro_pacientes.py](../pages/cadastro_pacientes.py) | CPF único (dígito verificador + hash), criptografado em repouso, busca e paginação server-side, soft-delete |
| Convênio | [cadastro_convenios.py](../pages/cadastro_convenios.py) | Nome e CNPJ únicos (casefold), status ATIVO/INATIVO |
| Médico | [cadastro_medicos.py](../pages/cadastro_medicos.py) | CRM+UF único, flag `responsavel_tecnico` |
| Procedimento | [cadastro_procedimentos.py](../pages/cadastro_procedimentos.py) | `codigo_tuss` com 8 dígitos exatos; **tabela de preço por convênio e particular, com vigência fechada por EXCLUDE**; material, método, prazo e mnemônico |
| Unidade / Setor | [cadastro_unidades.py](../pages/cadastro_unidades.py) | Tipo CENTRAL ou COLETA |

### 4.2 Atendimento e coleta

[atendimento_os.py](../pages/atendimento_os.py) e [atendimento_coleta.py](../pages/atendimento_coleta.py). Abertura de OS com itens, autorização de convênio, cancelamento com RBAC, coleta com etiqueta de código de barras, paginação server-side.

### 4.3 Logística

[logistica_malotes.py](../pages/logistica_malotes.py) e [logistica_recebimento.py](../pages/logistica_recebimento.py). Malote com origem, destino, responsável e datas de criação/despacho; protocolo de recebimento com conferência de integridade e **rejeição individual** de amostra; cadeia de custódia completa em `amostras_movimentacoes`.

### 4.4 Laboratorial

[laboratorio_cadastros.py](../pages/laboratorio_cadastros.py), [laboratorio_bancada.py](../pages/laboratorio_bancada.py), [laboratorio_resultados.py](../pages/laboratorio_resultados.py), [laboratorio_laudos.py](../pages/laboratorio_laudos.py).

Granularidade por **analito** ([ADR 0003](adr/0003-granularizacao-analitos-laboratorial.md)): uma linha de `resultados` por parâmetro, o que permite auditoria clínica restrita ao parâmetro retificado e regras distintas para valor numérico e textual. `valores_referencia` suporta faixa numérica e valor esperado textual.

### 4.5 Faturamento

[faturamento_guias.py](../pages/faturamento_guias.py) e [faturamento_glosas.py](../pages/faturamento_glosas.py).

Lote → guia TISS → item, com `validar_lote()` fazendo pré-auditoria (TUSS de 8 dígitos, valor positivo, laudo liberado) e bloqueando o fechamento se reprovar. O fechamento gera título a receber. Glosa com **validação cumulativa** — duas glosas parciais que somem mais que o faturado são recusadas, e o item só vira `GLOSADO` quando o acumulado fecha o valor.

Lote particular (`convenio_id IS NULL`) aparece nas telas de glosa, rotulado "Particular".

### 4.6 Financeiro

[financeiro_contas.py](../pages/financeiro_contas.py) e [financeiro_caixa.py](../pages/financeiro_caixa.py). Títulos a receber e a pagar, baixa com permissão `financeiro:baixar_titulo`, movimento de caixa por período, conciliação com alerta de divergência.

### 4.7 Compras

[compras_fornecedores.py](../pages/compras_fornecedores.py), [compras_pedidos.py](../pages/compras_pedidos.py), [compras_estoque.py](../pages/compras_estoque.py). Segregação de funções: solicitante, aprovador e almoxarife são permissões distintas. Aprovação gera título a pagar; recebimento movimenta estoque.

---

## 5. Business Intelligence

Reconstruído na fase F2 ([plano-bi.md](plano-bi.md)). Star schema em tabelas `bi_*`, isolado do OLTP.

### 5.1 Camadas

```
OLTP → src/bi/etl.py       carga idempotente, incremental-ready, observável
     → src/bi/models.py    7 dimensões · 6 fatos · registro de execução
     → src/bi/metricas.py  camada semântica: 1 função = 1 indicador
     → src/bi/graficos.py  specs Altair + paleta única
     → src/bi/filtros.py   filtro de período compartilhado
     → pages/bi_*.py       4 dashboards — SEM SQL
```

### 5.2 Dimensões e fatos

| Dimensão | Observação |
|---|---|
| `bi_dim_tempo` | **Densa** — dia a dia, com `ano_mes`, `semana_iso`, `semestre`, `dia_util`, `competencia` |
| `bi_dim_unidade` · `bi_dim_convenio` · `bi_dim_procedimento` | Upsert com atualização de atributos |
| `bi_dim_setor` · `bi_dim_faixa_etaria` · `bi_dim_motivo_glosa` | Criadas na F2 |
| `bi_dim_paciente_anon` | Pseudônimo SHA-256; só sexo é atributo |

| Fato | Grão | Chave natural |
|---|---|---|
| `bi_fato_ordem_servico` | 1 OS | `ordem_servico_id` |
| `bi_fato_atendimento` | 1 item de OS | `os_item_id` |
| `bi_fato_faturamento` | 1 item de guia | `guia_item_id` |
| `bi_fato_financeiro` | 1 lançamento por regime | `regime`+`origem_tabela`+`origem_id` |
| `bi_fato_logistica` | 1 amostra | `amostra_id` |
| `bi_fato_glosa` | 1 glosa | `glosa_id` |

**Três regras de modelagem** ([ADR 0009](adr/0009-grao-chave-natural-e-medidas-derivadas-no-bi.md)): todo fato declara grão e chave natural; medida só convive com o fato do seu grão; medida derivada (ticket médio, taxa de glosa) é calculada em `metricas.py`, nunca guardada em coluna — razão pré-calculada não reagrega.

### 5.3 Regimes financeiros

`bi_fato_financeiro` separa **PREVISTO** (título, datado pelo vencimento) de **CAIXA** (movimento, datado por `ocorrido_em`). Título em aberto entra como previsto e **não** como recebido.

### 5.4 Dashboards

| Tela | Conteúdo |
|---|---|
| [bi_visao_executiva.py](../pages/bi_visao_executiva.py) | KPIs com variação vs período anterior, receita mensal, previsto × recebido, DRE gerencial, aging da carteira, taxa de glosa |
| [bi_produtividade.py](../pages/bi_produtividade.py) | Volume por unidade/convênio/setor/faixa etária, TAT por mês e por setor, sazonalidade semanal |
| [bi_financeiro.py](../pages/bi_financeiro.py) | Faturado × glosado, receita e ticket médio por convênio, curva ABC, glosa por motivo, fluxo de caixa realizado |
| [bi_logistica.py](../pages/bi_logistica.py) | Amostras por mês e unidade, tempo de trânsito, rejeições, situação atual |

Todas com filtro de período (presets + intervalo), gráficos Altair com tooltip em pt-BR, e rodapé "dados atualizados em".

### 5.5 ETL

Idempotente por construção: zero `date.today()` na carga de fatos, upsert por chave natural e poda do que sumiu da origem. Agregação no banco, sem N+1 — **1,3 s** para a base de demonstração de ~400 OS. Cada execução vira uma linha em `bi_etl_execucao` com duração e contagem por fato.

Roda pelo seeder, por `python -m src.bi.etl`, ou pelo botão **Atualizar dados do BI** em qualquer dashboard.

---

## 6. Segurança, RBAC, LGPD e auditoria

### 6.1 Autenticação

Auth0 via OAuth2 com PKCE ([src/auth.py](../src/auth.py)). O usuário é sincronizado em `usuarios` no primeiro login.

### 6.2 RBAC

`Perfil → PerfilPermissao → Permissao`. **11 perfis** e **34 permissões** semeados. O gate está em `shell(permissao=...)` de cada página e, para operações sensíveis, também no service.

Perfis: `admin`, `atendente`, `coletador`, `tecnico_laboratorio`, `responsavel_tecnico`, `faturista`, `financeiro`, `requisitante_compras`, `aprovador_compras`, `almoxarife`, `visualizador`.

O seed é **idempotente linha a linha**: permissão, perfil e vínculo são conferidos um a um, então base já semeada recebe o que for adicionado depois.

**Bootstrap** ([ADR 0002](adr/0002-autenticacao-google-usuario-rbac-minimo.md)): o primeiro usuário vira `admin`, os demais `visualizador`.

### 6.3 LGPD

CPF criptografado com Fernet e indexado por SHA-256 (`cpf_hash`) — o setter do model faz as duas coisas, transparente para o service. No BI o paciente é pseudonimizado por hash e só `sexo` e faixa etária são expostos. Rotação de chave em `python -m src.lgpd.rotacao`.

### 6.4 Auditoria

`auditoria_log` (corporativa) e `resultados_auditoria` (clínica) são **append-only**. Cobrem CRUDs de cadastro, abertura e cancelamento de OS, coleta, despacho e recebimento de malote, liberação de laudo, alteração de resultado, fechamento de lote, glosa e baixa de título.

---

## 7. Modelo de dados

**57 tabelas** — 42 operacionais e 15 analíticas.

| Domínio | Tabelas |
|---|---|
| Cadastro | `pacientes` `convenios` `medicos` `procedimentos` `procedimento_valores` `unidades` `setores` |
| Atendimento | `ordens_servico` `os_itens` `os_status_historico` `autorizacoes_convenio` `amostras` `coletas` |
| Logística | `malotes` `malotes_amostras` `protocolos_recebimento` `amostras_movimentacoes` |
| Laboratorial | `equipamentos` `valores_referencia` `resultados` `resultados_auditoria` `laudos` |
| Faturamento | `lotes_faturamento` `guias_tiss` `guias_itens` `glosas` |
| Financeiro | `titulos_receber` `titulos_pagar` `movimentos_caixa` `conciliacoes_pagamento` |
| Compras | `fornecedores` `solicitacoes_compra` `pedidos_compra` `pedidos_itens` `recebimentos_insumo` `insumos_materiais` `estoque_movimentos` |
| Acesso | `usuarios` `perfis` `permissoes` `perfil_permissao` `auditoria_log` |
| BI | 8 dimensões + 6 fatos + `bi_etl_execucao` |

**Convenções:** PK `UUID` · dinheiro em `Numeric(12,2)` · tempo em `TIMESTAMPTZ` · status como `String` com enum no DTO · soft-delete por `ativo` onde há histórico a preservar.

---

## 8. Testes

**274 testes passando, zero skips.** Rodam em Windows e Linux.

> `make test` roda com `--build`. Sem isso o compose reusa a imagem antiga e uma
> dependência nova em `requirements.txt` não entra — já aconteceu com o
> `streamlit-aggrid`, e os testes que dependiam dele foram pulados em silêncio.

| Área | Cobertura |
|---|---|
| `tests/bi/` (5 arquivos) | Idempotência do ETL, reconciliação OLTP↔OLAP, grão sem duplicação, regressão dos 8 bugs de BI, camada de métricas, **renderização dos 4 dashboards via `AppTest`** |
| `tests/atendimento/` (6) | Abertura de OS, autorização, coleta, cancelamento coerente (12 histórias) |
| `tests/faturamento/` (5) | Lote, guia, glosa cumulativa, particular nas telas, valor do item |
| `tests/cadastro/` (5) | CRUD, unicidade, validadores de CPF/CNPJ/TUSS |
| `tests/rbac/` (3) | Gate, granularidade, perfil padrão, idempotência do seed |
| `tests/financeiro/` (3) · `tests/compras/` (2) · `tests/laboratorial/` (2) · `tests/logistica/` (2) · `tests/lgpd/` (2) · `tests/auditoria/` (1) | Regras de cada domínio |
| Raiz | Sessão e rollback, compatibilidade do AgGrid, componente de grid, navegação por permissão, config, **smoke das 28 telas** |

`tests/_tabelas.py` centraliza os conjuntos de tabelas truncadas entre testes, por domínio.

O **seeder é o teste de integração de fato**: atravessa ~400 OS pelo fluxo real e já derrubou bugs que a suíte unitária não pegava.

---

## 9. Migrations

15 arquivos, head **`0014_bi_reconstrucao`**, cadeia única.

| Revisão | Conteúdo |
|---|---|
| `0003`–`0005` | Pacientes, convênios, atendimento, logística |
| `f6ccac7706b1` | Laboratorial |
| `0006`–`0008` | Faturamento, ajuste de títulos, lote sem convênio |
| `0009` (×2) | RBAC + auditoria · auditoria de cancelamento |
| `0010` | LGPD — CPF criptografado |
| `0011` | BI — esquema estrela |
| `0012` | Merge das heads paralelas |
| `0013` | BI — paciente por hash |
| `0014` | **BI — reconstrução** (grão, chave natural, calendário denso) |

> ⚠️ A partir daqui, migrations são **escritas à mão**. `alembic revision --autogenerate` **não detecta rename** — emite `drop_table` + `create_table`, o que destruiria dados na remodelagem de faturamento. O alvo `make revision` usa autogenerate e **não serve** para as fases F4–F11.

---

## 10. Como rodar

```bash
cp .env.exemplo .env        # preencher AUTH0_* e LGPD_ENCRYPTION_KEY
docker compose up --build -d
docker compose logs -f app
```

O container executa `alembic upgrade head` → `python -m src.seeder` → `streamlit run`. Acesse **http://localhost:8501**.

| Comando | Efeito |
|---|---|
| `make up` / `make down` / `make logs` | Ciclo de vida |
| `make test` | Banco de teste isolado + suíte + limpeza |
| `make seeder` | Repopula a base de demonstração |
| `make clean` | Derruba **e apaga o volume** |
| `docker compose exec app python -m src.bi.etl` | Recarrega só o BI |

Base de demonstração: ~400 OS, ~1600 itens, ~960 laudos, ~76 lotes, glosas, carteira parcialmente liquidada e compras com estoque movimentado. Semente fixa (`SEED_SEMENTE`), escala ajustável por `--escala`.

---

## 11. Estado por fase e pendências

| Fase | Escopo | Estado |
|:---:|---|:---:|
| **F0** | Fundação — rollback, glosa cumulativa, particular na glosa, seed RBAC, suíte no Windows | ✅ |
| **F2** | BI onda 1 | ✅ |
| **F1** | Streamlit moderno — grid, navegação nativa, dialogs | ✅ |
| **F3** | Preço particular, vigência, catálogo de analitos, regra do valor | ✅ |
| **F4** | Competência como eixo de apuração, com fechamento | ✅ |
| F5–F11 | Item faturável → remessa → guia por paciente → glosa → divergências → baixa parcial → caixa | ⬜ |
| F12 | BI onda 2 | ⬜ |
| F13 | OMOP | ⬜ |
| F14 | Segurança (JWT, `state`, auditoria de PII, salt no CPF) | ⬜ |

### Pendências conhecidas

**Estruturais** — resolvidas nas fases F3–F11, detalhadas em [plano-evolucao-erp.md](plano-evolucao-erp.md) §7:

- Item 100% glosado é **receita perdida**: `guias_itens.laudo_id` é UNIQUE, então reapresentação é estruturalmente impossível (F5).
- Não existe fechamento de período — nada impede lançar em março depois de março fechado (F4).
- Baixa parcial não existe: receber R$1 de um título de R$1000 marca PAGO (F10).
- Vencimento é `hoje + 30` hardcoded; não há prazo por convênio (F3).
- Não existe tabela de preço **particular** nem `vigencia_fim` (F3).
- `Resultado.analito` e `ValorReferencia.analito` são textos livres desconectados — a bancada não sabe a faixa de referência do que digitou (F3).
- `StatusOsItem.FATURADO`, `StatusGuiaTiss` e `xml_tiss` são estados inalcançáveis ou colunas nunca escritas (F5/F7).

**Segurança** (F14): `id_token` não é validado (sem JWKS, `nonce`, `aud`, `exp`); `state` carrega o `code_verifier` do PKCE; leitura de PII não é auditada; `cpf_hash` é SHA-256 sem salt.

**Vocabulário**: a F6 introduz `RemessaFaturamento`, mas o [CONTEXT.md](../CONTEXT.md) hoje manda *evitar* "remessa" como sinônimo de malote. Precisa ser resolvido junto com a fase.

---

## 12. Mapa da documentação

| Documento | Papel |
|---|---|
| **[arquitetura.md](arquitetura.md)** | **Este documento — estado atual do sistema** |
| [diagramas/bi-esquema-estrela.mmd](diagramas/bi-esquema-estrela.mmd) | Modelo dimensional em vigor (Mermaid) |
| [roadmap-execucao.md](roadmap-execucao.md) | **Canônico** — ordem das fases, migrations, decisões, divisão do time |
| [plano-bi.md](plano-bi.md) | Reconstrução do BI (F2 feita, F12 pendente) |
| [plano-evolucao-erp.md](plano-evolucao-erp.md) | Conteúdo técnico dos 5 eixos + catálogo de achados |
| [plano-faturamento-competencia.md](plano-faturamento-competencia.md) | DDL, migrations e serviços das fases F4–F11 |
| [adr/](adr/) | 9 decisões arquiteturais |
| [specs/](specs/) | Especificação do cancelamento coerente da OS |
| [Entrega 1/](Entrega%201/) · [Entrega 2/](Entrega%202/) · [Entrega 3/](Entrega%203/) | Entregas acadêmicas (histórico) |
| [../README.md](../README.md) | Instruções de instalação e execução |
| [../CONTEXT.md](../CONTEXT.md) | Glossário de domínio |
| [../DEPLOY.md](../DEPLOY.md) | Deploy em produção |
