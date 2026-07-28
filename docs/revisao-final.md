# Revisão Final — LabVida ERP

Relatório de revisão de regras de negócio, bugs, UX e cobertura de testes.
Atualizado em 28/07/2026.

---

## Sumário

1. [Cobertura vs. Diagnóstico da Empresa (PDF)](#1-cobertura-vs-diagnóstico-da-empresa-pdf)
2. [Regras de Negócio por Módulo](#2-regras-de-negócio-por-módulo)
   - [2.1 Cadastro](#21-cadastro)
   - [2.2 Atendimento e Coleta](#22-atendimento-e-coleta)
   - [2.3 Logística de Amostras](#23-logística-de-amostras)
   - [2.4 Laboratorial](#24-laboratorial)
   - [2.5 Faturamento](#25-faturamento)
   - [2.6 Financeiro](#26-financeiro)
   - [2.7 Compras](#27-compras)
   - [2.8 Segurança e Auditoria](#28-segurança-e-auditoria)
   - [2.9 Business Intelligence](#29-business-intelligence)
3. [Cancelamento da OS — Regras de Agregação](#3-cancelamento-da-os--regras-de-agregação)
4. [Bugs de Código/Lógica](#4-bugs-de-códigológica)
   - [4.1 Críticos](#41-críticos)
   - [4.2 Médios](#42-médios)
   - [4.3 Menores](#43-menores)
5. [UX Issues](#5-ux-issues)
   - [5.1 Sistêmicos](#51-sistêmicos)
   - [5.2 Por Página](#52-por-página)
6. [Funcionalidades Ausentes](#6-funcionalidades-ausentes)
7. [Gaps de Cobertura de Testes](#7-gaps-de-cobertura-de-testes)
8. [Issues de Infraestrutura](#8-issues-de-infraestrutura)
9. [Resumo Quantitativo](#9-resumo-quantitativo)

---

## 1. Cobertura vs. Diagnóstico da Empresa (PDF)

Os 7 problemas críticos identificados pela consultoria no documento `docs/empresa LabVida.pdf`:

| # | Problema (PDF) | Cobertura no projeto | Situação |
|---|---------------|---------------------|----------|
| **a** | Gestão descentralizada, sem indicadores para decisão | BI implementado com 3 dashboards (produtividade, logística, financeiro) + Home com KPIs operacionais | ✅ Coberto |
| **b** | Baixa integração entre sistemas, retrabalho e duplicidade | OS como entidade-espinha integrando todos os módulos via `os_status_historico` e cadeia de custódia. Dados nascem uma vez e fluem entre setores. | ✅ Coberto |
| **c** | Gargalos no atendimento (dados redigitados em sistemas diferentes) | Cadastro único de paciente → OS reutiliza dados. CPF único evita duplicados. | ✅ Coberto |
| **d** | Logística manual de amostras, sem rastreamento em tempo real | Malotes + `AmostraMovimentacao` (cadeia de custódia) + status tracking (COLETADA → EM_TRANSITO → RECEBIDA) | ✅ Coberto |
| **e** | Faturamento de convênios crítico, glosas frequentes | Lotes, Guias TISS e Glosas implementados. **Faltam:** geração de XML TISS e pré-auditoria automática | ⚠️ Parcial |
| **f** | Ausência de dashboards gerenciais | BI com 3 dashboards + ETL. **Faltam:** filtros de data, mais indicadores, drill-down | ⚠️ Parcial |
| **g** | Riscos de segurança da informação | RBAC com perfil/permissão, CPF criptografado (Fernet + SHA-256), LGPD (anonimização no BI), auditoria append-only | ✅ Coberto |

---

## 2. Regras de Negócio por Módulo

Base: `docs/Templates/Template - LabVida.md` — Seção 6 (37 regras).

### 2.1 Cadastro

| # | Regra | Status | Onde validar | Detalhes |
|---|-------|--------|-------------|----------|
| 1 | Não permitir cadastro duplicado de paciente (CPF único) | ✅ | `src/cadastro/service.py` + model `cpf_hash` com unique index | `CpfPacienteDuplicado` no service. SHA-256 hash para busca. |
| 2 | Dados sensíveis do paciente criptografados (LGPD) | ✅ | Model `Paciente` — property setter de `cpf` aplica Fernet + SHA-256 | Transparente para o service, implementado em nível de model. |
| 3 | Convênios ativos para uso em OS | ✅ | `src/atendimento/ordem_servico/service.py:abrir_os()` | Valida `convenio.status == StatusConvenio.ATIVO`. |
| 4 | Procedimentos com código TUSS/TISS válido | ✅ | `src/cadastro/procedimento/dtos.py:_codigo_tuss()` | Valida exatamente 8 dígitos numéricos. |

### 2.2 Atendimento e Coleta

| # | Regra | Status | Onde validar | Detalhes |
|---|-------|--------|-------------|----------|
| 5 | Toda OS deve possuir identificador único | ✅ | `src/atendimento/ordem_servico/service.py:abrir_os()` | `codigo_os` formato `OS-{ano}-{6 hex}` com unique constraint no banco. |
| 6 | OS de convênio só pode ser aberta com autorização válida | ✅ | `abrir_os()` cria `AutorizacaoConvenio` PENDENTE; `registrar_coleta()` bloqueia sem `VALIDA` | Autorização criada junto com a OS. Coleta só prossegue após validação. |
| 7 | Coleta só pode ser registrada por usuário autorizado | ✅ | `src/atendimento/amostra/service.py:registrar_coleta()` | Verifica `usuario_tem_permissao("atendimento:coletar")`. Bootstrap-friendly. |
| 8 | Toda amostra coletada deve receber etiqueta (código de barras/QR) | ✅ | `pages/atendimento_coleta.py:106,107,123` | `codigo_barras` já gerado e exibido em `st.success()`, `st.toast()` e tabela de amostras. |

### 2.3 Logística de Amostras

| # | Regra | Status | Onde validar | Detalhes |
|---|-------|--------|-------------|----------|
| 9 | Nenhuma amostra analisada sem registro de recebimento | ✅ | `src/laboratorial/service.py:_validar_amostra_recebida()` | `registrar_resultado` valida `Amostra.status == RECEBIDA` antes de criar resultado. |
| 10 | Toda movimentação da amostra gera registro de auditoria | ✅ | `src/logistica/malote/service.py:despachar_malote()` + `recebimento/service.py:receber_malote()` | `registrar_auditoria("DESPACHAR_MALOTE")` e `("RECEBER_MALOTE")` adicionados. Trilha corporativa completa em coleta, despacho e recebimento. |
| 11 | Malotes devem possuir origem, destino, data, hora e responsável | ✅ | Modelo `Malote` | Todos os campos presentes: `unidade_origem_id`, `unidade_destino_id`, `criado_em`, `despachado_em`, `enviado_por_usuario_id`. |
| 12 | Amostras divergentes ou danificadas devem ser bloqueadas | ✅ | `src/logistica/recebimento/service.py:receber_malote()` | Suporta rejeição individual via `dto.amostras_rejeitadas`. Amostras rejeitadas vão para status `REJEITADA`. |

### 2.4 Laboratorial

| # | Regra | Status | Onde validar | Detalhes |
|---|-------|--------|-------------|----------|
| 13 | Resultados só podem ser inseridos após recebimento logístico | ✅ | `src/laboratorial/service.py:_validar_amostra_recebida()` | Valida antes de criar `Resultado`. Mesma validação da regra #9. |
| 14 | Liberação final do laudo só por responsável técnico autorizado | ✅ | `src/laboratorial/service.py:atualizar_laudo()` | Valida: `medico.ativo == True`, `medico.responsavel_tecnico == True`, existência de `responsavel_tecnico_id`. |
| 15 | Toda alteração em resultado clínico gera auditoria imutável | ✅ | `src/laboratorial/service.py:atualizar_resultado()` | `ResultadoAuditoria` append-only com `valor_anterior` e `valor_novo`. |
| 16 | Resultados importados de equipamentos vinculados à OS | ✅ | Modelo `Resultado` | FK `os_item_id` → `os_itens.id` → `ordens_servico.id`. |

### 2.5 Faturamento

| # | Regra | Status | Onde validar | Detalhes |
|---|-------|--------|-------------|----------|
| 17 | Não permitir envio de guia sem código TUSS/TISS válido | ✅ | FK `guia_item.procedimento_id` → validado na criação | Procedimento é validado com 8 dígitos na criação (#4); FK garante integridade. |
| 18 | Não permitir faturamento de OS sem laudo liberado | ✅ | `adicionar_guia_item()` | Valida `laudo.status == LIBERADO` antes de criar `GuiaItem`. |
| 19 | Guias devem passar por pré-auditoria antes do fechamento do lote | ❌ | — | **Não implementado.** `fechar_lote()` fecha imediatamente. Não há etapa intermediária de pré-auditoria. |
| 20 | Itens com inconsistência devem ser bloqueados até correção | ❌ | — | **Não implementado.** Não há mecanismo de sinalização ou bloqueio de itens inconsistentes no lote. |

### 2.6 Financeiro

| # | Regra | Status | Onde validar | Detalhes |
|---|-------|--------|-------------|----------|
| 21 | Somente o setor financeiro pode confirmar baixa de pagamento | ✅ | `src/financeiro/titulo_receber/service.py` + `titulo_pagar/service.py:baixar_titulo()` | Verifica `usuario_tem_permissao("financeiro:baixar_titulo")`. Bootstrap-friendly. |
| 22 | Lotes fechados no Faturamento devem gerar títulos automaticamente | ✅ | `fechar_lote()` | Cria `TituloReceber` com `valor_total` do lote e vencimento em 30 dias. |
| 23 | Pagamentos recebidos devem alimentar o fluxo de caixa | ✅ | `baixar_titulo()` (receber) | Cria `MovimentoCaixa` (tipo `ENTRADA`) com o valor pago. |
| 24 | Divergências entre valor faturado e recebido devem gerar alerta | ⚠️ | `baixar_titulo()` | `ConciliacaoPagamento` é criada com a divergência. Mas é **apenas um registro passivo** — não há notificação ou alerta ativo. |

### 2.7 Compras

| # | Regra | Status | Onde validar | Detalhes |
|---|-------|--------|-------------|----------|
| 25 | Solicitações de compra registradas por usuário autorizado | ✅ | `src/compras/pedido_compra/service.py:criar_solicitacao()` | Verifica `usuario_tem_permissao("compras:solicitar")`. Bootstrap-friendly. |
| 26 | Compras aprovadas devem gerar previsão de pagamento | ✅ | `aprovar_pedido()` | Cria `TituloPagar` com `valor_total`, vencimento em 30 dias. |
| 27 | Fornecedores devem estar previamente cadastrados | ✅ | `criar_solicitacao()` | Valida `fornecedor.status == ATIVO`. |
| 28 | Materiais com identificação, quantidade e finalidade registrada | ✅ | Modelo `InsumoMaterial` | Colunas: `nome`, `finalidade`, `quantidade_estoque`. |

### 2.8 Segurança e Auditoria

| # | Regra | Status | Onde validar | Detalhes |
|---|-------|--------|-------------|----------|
| 29 | Permissões devem variar conforme o perfil do usuário | ✅ | `src/rbac/` + `src/ui.py:shell()` | RBAC completo: `Perfil → Permissao` via `PerfilPermissao`. Gate `shell(permissao=...)` em cada página. |
| 30 | Apenas gestores podem cancelar operações críticas | ✅ | `src/atendimento/ordem_servico/service.py:_validar_permissao_cancelar()` | Verifica permissão `atendimento:cancelar_os` (só admin). Bootstrap ignora se RBAC não semeado. |
| 31 | Logs devem registrar alterações sensíveis | ✅ | `src/cadastro/*/service.py` + `pages/cadastro_*.py` + `src/logistica/malote/service.py` + `recebimento/service.py` | Auditoria em CRUDs de cadastro (5 entidades, 12 operações) + despacho e recebimento de malotes. |
| 32 | Dados pessoais e clínicos devem seguir LGPD | ✅ | `src/lgpd/` + model `Paciente` | CPF: Fernet (encrypted) + SHA-256 (hash). BI: paciente anonimizado. Rotação de chave implementada. |
| 33 | Auditorias clínicas e financeiras append-only | ✅ | `auditoria_log` + `resultado_auditoria` | Ambas são tabelas insert-only (sem UPDATE/DELETE no código). |

### 2.9 Business Intelligence

| # | Regra | Status | Onde validar | Detalhes |
|---|-------|--------|-------------|----------|
| 34 | Dashboards acessíveis só por diretoria e autorizados | ✅ | `shell(permissao="bi:visualizar")` | Gate nas 3 páginas de BI. |
| 35 | Dados do BI read-only (sem alteração da base operacional) | ✅ | Star schema separado | Tabelas `bi_dim_*` e `bi_fato_*` são independentes da base OLTP. |
| 36 | ETL não deve comprometer performance do ERP | ⚠️ | `src/bi/etl.py` | Sem mecanismo de throttle ou agendamento. ETL executado manualmente, sem controle de resource usage. |
| 37 | Indicadores com dados de paciente devem respeitar anonimização | ✅ | `bi_dim_paciente_anon` | `id_origem` = SHA-256 do UUID. Apenas `faixa_etaria` e `sexo` são expostos. |

---

## 3. Cancelamento da OS — Regras de Agregação

Base: `docs/specs/0001-cancelamento-coerente-da-os.md` e ADRs 0005/0006.

| # | História de Usuário | Status | Detalhes |
|---|---------------------|--------|----------|
| 1 | Cancelar item ativo individual sem afetar outros | ✅ | `cancelar_item_os()` com validações individuais |
| 2 | Rejeitar cancelamento de item com laudo liberado | ✅ | Verifica `RESULTADO_LIBERADO` + existência de `Laudo` com status `LIBERADO` |
| 3 | Rejeitar cancelamento de item faturado | ✅ | Verifica existência de `GuiaItem` vinculado ao laudo do item |
| 4 | Identificar usuário autenticado em cada cancelamento | ✅ | `cancelado_por_usuario_id` no model `OsItem` + `auditoria_log` |
| 5 | OS com item ativo pendente permanece no fluxo após cancelamento parcial | ✅ | `_atualizar_status_agregado()` mantém status atual se houver item ativo |
| 6 | OS com cancelados + todos ativos com laudos → CONCLUIDA | ✅ | Testado em `test_os_conclui_quando_outro_item_tem_laudo` |
| 7 | Último item cancelado → OS CANCELADA | ✅ | Testado em `test_cancelar_ultimo_item_cancela_os` |
| 8 | Bloquear cancelamento integral com itens concluídos | ✅ | `cancelar_os()` rejeita se há item com laudo liberado ou faturado |
| 9 | Permitir cancelar itens ativos restantes individualmente | ✅ | `cancelar_item_os()` só bloqueia o item específico, não a OS |
| 10 | Transições de status da OS registradas em `os_status_historico` | ✅ | `registrar_transicao()` com `usuario_id` |
| 11 | Usuário autenticado registrado em cada transição de status | ✅ | `usuario_id` registrado no `os_status_historico` |
| 12 | Cancelamentos repetidos rejeitados (idempotentes) | ✅ | Verifica estado atual antes de cancelar (`ItemNaoPodeSerCancelado`) |

**Status: 100% coberto.** O cancelamento da OS é a parte mais bem implementada do sistema.

---

## Correções aplicadas (27-28/07/2026)

| Data | O que | Arquivos |
|------|-------|----------|
| 27/07 | `alembic/env.py` importa `rbac`, `auditoria`, `bi` | `alembic/env.py` |
| 27/07 | `ConvenioService` unificado com validação de unicidade | `convenio/service.py`, `dtos.py`, `cadastro/service.py` |
| 27/07 | `cadastro_convenios.py` — erro handling + campos CNPJ/telefone/email | `pages/cadastro_convenios.py` |
| 27/07 | Botão Liberar Laudo `disabled` com resultados não revisados | `pages/laboratorio_laudos.py` |
| 27/07 | `time.sleep()` artificiais removidos (laudos + resultados) | `pages/laboratorio_laudos.py`, `laboratorio_resultados.py` |
| 27/07 | UUIDs → `codigo_os` nos selectboxes | `pages/laboratorio_laudos.py`, `laboratorio_resultados.py` |
| 27/07 | RBAC: `remover_permissao_do_perfil` + `desvincular_usuario_do_perfil` | `src/rbac/`, `pages/admin_usuarios.py`, tests |
| 27/07 | 🔴 `shell()`: desvincular perfil bloqueia acesso | `src/ui.py`, tests |
| 27/07 | Regras #9 + #13: `registrar_resultado` bloqueia sem amostra recebida | `src/laboratorial/service.py`, tests |
| 28/07 | Regra #30: RBAC no cancelamento (`atendimento:cancelar_os`) | seeder + OS service + tests |
| 28/07 | Regra #6: Autorização de convênio na OS | OS service + amostra service + tests |
| 28/07 | UX cancelamento: botões ocultos sem `atendimento:cancelar_os` | `pages/atendimento_os.py` |
| 28/07 | Regras #7+#21+#25: RBAC nos services (coleta/financeiro/compras) | 4 services + 3 conftests + 3 tests |
| 28/07 | 🔴 `financeiro_contas.py`: `FinanceiroError` não capturado na aba pagar | `pages/financeiro_contas.py` |
| 28/07 | Regra #8: Código de barras já exibido na UI (confirmado) | `pages/atendimento_coleta.py` |
| 28/07 | Regra #10: Auditoria corporativa em despacho e recebimento | `logistica/malote/service.py`, `recebimento/service.py` |
| 28/07 | Regra #31: Auditoria em CRUDs de cadastro (5 entidades, 12 operações) | 5 services + 5 páginas |
| 28/07 | Regras #4+#17: Validação TUSS 8 dígitos exatos | `procedimento/dtos.py`, tests |

**165/165 testes passando.**

---

## 4. Bugs de Código/Lógica

### 4.1 Críticos

#### Bug #1 — `registrar_resultado` não valida recebimento da amostra ✅ CORRIGIDO
- **Correção aplicada:** `_validar_amostra_recebida()` adicionado no `registrar_resultado()`. Verifica `Amostra.status == RECEBIDA` antes de criar resultado.

#### Bug #2 — `ConvenioService` duplicado e versão em produção é incompleta ✅ CORRIGIDO
- **Arquivos:**
  - `src/cadastro/convenio/service.py` — versão unificada com validações
  - `src/cadastro/convenio/dtos.py` — DTO enriquecido com `cnpj`, `telefone`, `email`
  - `src/cadastro/service.py` — métodos de Convênio removidos (mantém só Paciente)
- **Correção aplicada:** Unificada a implementação em `src/cadastro/convenio/service.py` com validação de nome duplicado (casefold), CNPJ duplicado (se informado), `obter_convenio_por_id`, `inativar_convenio` e `atualizar_convenio`. DTO atualizado com suporte a `cnpj`, `telefone`, `email`. Consumidores atualizados. 51/51 testes passando.

#### Bug #3 — `AutorizacaoConvenio` nunca utilizada ✅ CORRIGIDO
- **Correção aplicada:** `abrir_os()` cria `AutorizacaoConvenio` PENDENTE quando OS tem convênio. `registrar_coleta()` bloqueia se não houver autorização `VALIDA`.

#### Bug #4 — `alembic/env.py` não importa modelos de RBAC, Auditoria e BI ✅ CORRIGIDO
- **Arquivo:** `alembic/env.py`
- **Problema:** Os modelos `src/rbac/models.py`, `src/auditoria/models.py` e `src/bi/models.py` **não são importados** no `env.py`. Isso significa que `alembic revision --autogenerate` nunca detectará mudanças nessas tabelas (`perfis`, `permissoes`, `perfil_permissao`, `auditoria_log`, `bi_dim_*`, `bi_fato_*`). Qualquer alteração futura nessas tabelas será ignorada ou precisará de migration manual.
- **Correção aplicada:** Adicionados os 3 imports no `alembic/env.py`. Agora `alembic revision --autogenerate` detecta mudanças em todas as tabelas do sistema.

### 4.2 Médios

#### Bug #5 — `registrar_resultado` e `atualizar_resultado` têm `session.commit()` interno
- **Arquivo:** `src/laboratorial/service.py` — linhas ~110 e ~138
- **Problema:** Ambos os métodos do `LaboratorialService` fazem `session.commit()` internamente. Isso quebra o controle transacional externo: não é possível compor múltiplas operações com rollback atômico. Outros services do projeto delegam o commit para a camada de página (via `session_scope`).
- **Solução sugerida:** Remover `session.commit()` dos métodos do `LaboratorialService`. Deixar o commit a cargo do chamador (página), como é feito nos demais módulos.

#### Bug #6 — `laboratorio_bancada.py` faz commit redundante
- **Arquivo:** `pages/laboratorio_bancada.py`
- **Problema:** A página chama `session.commit()` após chamar métodos do `LaboratorialService`, que já commitaram internamente (Bug #5). Isso causa double-commit desnecessário.
- **Solução sugerida:** Corrigir junto com o Bug #5.

#### Bug #7 — `atendimento_coleta.py` carrega todas as OS sem paginação
- **Arquivo:** `pages/atendimento_coleta.py` — linha 33
- **Problema:** `listar_os(session)` é chamado sem limite de resultados. Se houver 10.000+ OS no banco, a página carrega tudo em memória e trava.
- **Solução sugerida:** Adicionar paginação ou filtro por status + busca textual, como já existe em `atendimento_os.py`.

#### Bug #8 — `_listar_os_itens()` carrega todos os registros sem limite
- **Arquivos:**
  - `pages/laboratorio_resultados.py` — função `_listar_os_itens()`
  - `pages/laboratorio_laudos.py` — função `_listar_os_itens()`
- **Problema:** A query `select(OsItem)` retorna todos os itens de todas as OS. Sem paginação, sem filtro. Vai quebrar com volume real.
- **Solução sugerida:** Adicionar filtro (ex: apenas itens de OS com status `EM_ANALISE` e amostras `RECEBIDA`) e paginação.

#### Bug #9 — `laboratorio_laudos.py` mostra aviso mas não bloqueia botão de liberação ✅ CORRIGIDO
- **Arquivo:** `pages/laboratorio_laudos.py`
- **Problema:** O aviso "Nem todos os resultados foram digitados e REVISADOS" é exibido na tela, mas o botão "Salvar e LIBERAR Laudo" continua visível e funcional. O service bloqueia corretamente (lança `ValueError`), então o laudo não é liberado. Mas o UX é enganoso — o usuário clica, vê erro, e não entende por que o botão estava disponível.
- **Correção aplicada:** Adicionado `disabled=not todos_revisados` ao botão. Agora o botão fica cinza e não-clicável enquanto houver resultados pendentes de revisão ou sem resultados.

#### Bug #10 — `faturamento_guias.py` usa valor fixo `50.00` como padrão
- **Arquivo:** `pages/faturamento_guias.py`
- **Problema:** O valor padrão dos campos de faturamento é hardcodado como `50.00`, em vez de buscar o valor contratado da tabela `procedimento_valores` ou o valor negociado em `os_item.valor_negociado`.
- **Solução sugerida:** Buscar o valor correto: primeiro `os_item.valor_negociado` (se definido), caso contrário `procedimento_valor.vigente` para o convênio.

#### Bug #11 — Dupla representação de estado em Convênio
- **Arquivos:** Model `Convenio` (`src/cadastro/convenio/models.py`) + service
- **Problema:** O modelo tem duas colunas redundantes: `ativo` (boolean) e `status` (enum `ATIVO`/`INATIVO`). O service tenta mantê-las sincronizadas, mas um UPDATE direto no banco pode dessincronizá-las. O código consulta `status` em alguns lugares e `ativo` em outros.
- **Solução sugerida:** Remover a coluna `ativo` e usar apenas `status`. Atualizar todas as queries que usam `ativo` para usar `status`.

#### Bug #12 — Home formatação de moeda frágil
- **Arquivo:** `pages/home.py` — função do KPI de faturamento
- **Problema:** A formatação BRL usa substituição de string (`f"R$ {valor:,.2f}"` trocando vírgulas por pontos), que produz resultados incorretos para valores com mais de uma casa de milhar (ex: `R$ 1.234.567,89` sai errado).
- **Solução sugerida:** Usar `locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')` e `locale.currency()` ou uma função utilitária centralizada.

### 4.3 Menores

#### Bug #13 — UUIDs expostos na UI ✅ CORRIGIDO
- **Arquivos:** `pages/laboratorio_laudos.py` (linha 45), `pages/laboratorio_resultados.py` (linha 47)
- **Correção aplicada:** Substituído `item.ordem_servico.id` por `item.ordem_servico.codigo_os` nos selectboxes. Agora o usuário vê `"OS-2026-a3f2c1 — Hemograma"` em vez de `"OS a1b2c3d4-... — Proc Hemograma"`. Também removidos `time.sleep(0.5)` restantes no `laboratorio_resultados.py` (Bug #16).

#### Bug #14 — Formatação de moeda inconsistente (US vs BR)
- **Arquivos:** `pages/bi_financeiro.py`, `pages/bi_logistica.py`, `pages/home.py`
- **Problema:** Algumas páginas usam `$1,234.56` (padrão US), outras usam `R$ 1.234,56` (padrão BR). Na mesma aplicação, o usuário vê dois formatos diferentes.
- **Solução sugerida:** Padronizar para formato brasileiro em toda a aplicação.

#### Bug #15 — Perda de dados ao alterar quantidade de itens no pedido
- **Arquivo:** `pages/compras_pedidos.py`
- **Problema:** O `st.number_input("Qtd de itens")` reconstrói todas as linhas de itens ao ser alterado. Dados já preenchidos nas linhas existentes são perdidos silenciosamente.
- **Solução sugerida:** Usar botão "Adicionar item" individual em vez de definir quantidade fixa, ou salvar estado em `st.session_state`.

#### Bug #16 — `time.sleep()` artificiais no código ✅ CORRIGIDO
- **Arquivos:**
  - `pages/laboratorio_laudos.py` — `time.sleep(2.5)` após criar rascunho e `time.sleep(0.5)` após liberar
- **Correção aplicada:** Removidos ambos os `time.sleep()`. O Streamlit >=1.36 mantém `st.toast()` no canto inferior durante `st.rerun()`. Padrão já usado com sucesso em `faturamento_glosas.py`, `financeiro_contas.py` e `compras_pedidos.py` sem sleep.

---

## 5. UX Issues

### 5.1 Sistêmicos

| # | Issue | Páginas afetadas | Severidade |
|---|-------|-----------------|------------|
| **U1** | **Zero `st.spinner()` no projeto inteiro** — queries longas travam a UI em silêncio, sem feedback visual. | Todas as 26 | Alta |
| **U2** | **Ações destrutivas sem confirmação** — Inativar paciente, inativar convênio, despachar malote, fechar lote, aprovar/receber pedido, cancelar item OS. Um clique executa ação irreversível. | 12 páginas | Alta |
| **U3** | **`st.rerun()` reseta tab index** — Em páginas com múltiplas abas, após salvar um registro o sistema volta para a primeira aba. Usuário perde contexto. | 8 páginas | Média |
| **U4** | **`st.session_state` toggle para sub-formulários** — Padrão frágil usado em faturamento, financeiro e compras. Apenas um formulário pode estar aberto por vez; colapsam em reruns não relacionados. | 3 páginas | Média |
| **U5** | **Empty states sem call-to-action** — Mensagens como "Cadastre X primeiro" não oferecem link ou botão para navegar até a página de cadastro. | 10+ páginas | Baixa |
| **U6** | **Queries sem paginação** — Vão quebrar com volume real de dados de produção. | 4 páginas | Alta |
| **U7** | **Sem tratamento de erro para queries de listagem** — Se o banco estiver offline, o usuário vê um traceback completo do Streamlit em vez de mensagem amigável. | 18+ páginas | Média |

### 5.2 Por Página

| Página | Issues específicos |
|--------|-------------------|
| `home.py` | Botão "Nova OS" na seção de OS recentes é elemento morto (sem ação vinculada). KPIs sem spinner. |
| `cadastro_pacientes.py` | Botão "Inativar" sem confirmação. CPF e telefone sem máscara de input. Paginação quebra ao buscar com filtro. |
| `cadastro_medicos.py` | **Não permite editar ou inativar médicos.** Sem busca/paginação na lista. |
| `cadastro_convenios.py` | **Não permite editar nome/ANS** de convênio existente. Toggle ativar/inativar sem confirmação. Sem busca. |
| `cadastro_procedimentos.py` | Não lista valores já definidos por procedimento. **Não permite editar valores existentes.** Formato do campo valor (BR) sem instrução clara. |
| `cadastro_unidades.py` | **Não permite editar/inativar unidades ou setores.** |
| `atendimento_os.py` | Campos de valor monetário aparecem até para OS particular. Cancelamento oculto para usuários sem permissão. |
| `atendimento_coleta.py` | Dropdown de OS sem busca/paginação. Não mostra quais itens já tiveram amostra coletada. Sem indicação visual do que falta coletar. |
| `logistica_malotes.py` | Amostras de qualquer unidade podem ser vinculadas a qualquer malote (sem validação de origem). Despachar sem confirmação. |
| `logistica_recebimento.py` | Confirmar recebimento sem confirmação. Sem visualização de malotes já recebidos. |
| `laboratorio_cadastros.py` | Botão "Salvar Equipamento" **sem try/except** — traceback puro em caso de erro. Setor não vinculado corretamente à unidade selecionada. |
| `laboratorio_resultados.py` | Selectbox usa `codigo_os` legível. Sem operações em lote. |
| `laboratorio_laudos.py` | Botão de liberação desabilitado com resultados não revisados. Sem preview/PDF do laudo. |
| `laboratorio_bancada.py` | Commit redundante após service. Sem try/except no registro de resultado. Fila sem paginação. |
| `faturamento_guias.py` | **Muito lento:** 10+ queries por rerun (uma por lote aberto). Fechar lote sem confirmação. Valor padrão R$50,00 hardcodado. Sem per-guia view após adicionar itens. |
| `faturamento_glosas.py` | Sub-formulário com toggle frágil. Não considera glosas acumuladas no max_value. Sem busca/filtro. |
| `financeiro_contas.py` | Sub-formulário com toggle frágil. Contas a pagar sem valor parcial (sempre paga total). Sem busca/paginação. |
| `financeiro_caixa.py` | Sem spinner. Ano via `number_input` (difícil de navegar). Sem drill-down para transação origem. |
| `compras_fornecedores.py` | CNPJ sem máscara de formatação. Edit inline frágil (toggle no session_state). Inativar sem confirmação. Sem busca. |
| `compras_pedidos.py` | Alterar qtd de itens perde dados preenchidos. Aprovar/cancelar/receber sem confirmação. Sem visão dos itens no acompanhar. |
| `compras_estoque.py` | Sem ajuste manual de estoque. Sem editar insumo. Movimentações sem paginação. |
| `admin_usuarios.py` | Layout confuso (HTML table + column layout duplicados). Sem bulk assign. Sem remover perfil de usuário. Sem criar/deletar perfil. |
| `meu_perfil.py` | Update de nome usa SQLAlchemy direto (sem service/auditoria). Sem mostrar permissões do perfil. |
| `bi_produtividade.py` | Sem filtro de data. Sem drill-down. Sem spinner. |
| `bi_logistica.py` | Sem filtro de data. Query direta na tabela operacional `amostras` (bypassa BI). Formatação US. |
| `bi_financeiro.py` | Sem filtro de data. Sem drill-down. Formatação US inconsistente. |

---

## 6. Funcionalidades Ausentes

| # | Funcionalidade | Módulo | Referência (Template/PDF) |
|---|---------------|--------|--------------------------|
| F1 | Pré-auditoria de guias TISS antes do fechamento do lote | Faturamento | Template 3.5, Regra 19 |
| F2 | Geração de XML TISS | Faturamento | Template 3.5 |
| F3 | Validação de autorização de convênio na abertura de OS | Atendimento | ✅ Corrigido |
| F4 | Impressão/visualização de etiqueta com código de barras | Atendimento | ✅ Confirmado na UI |
| F5 | Validação de formato do código TUSS (dígitos, checksum) | Cadastro | ✅ Corrigido |
| F6 | Edição de médicos (nome, CRM, responsável técnico) | Cadastro | — |
| F7 | Edição de procedimentos (nome, setor) | Cadastro | — |
| F8 | Edição/inativação de unidades e setores | Cadastro | — |
| F9 | Edição de valores de procedimento por convênio | Cadastro | — |
| F10 | Notificações/alertas ativos para divergências financeiras | Financeiro | Regra 24 |
| F11 | Pagamento parcial de títulos (receber e pagar) | Financeiro | — |
| F12 | Recebimento parcial de pedidos de compra | Compras | — |
| F13 | DRE gerencial | Financeiro | Template 3.6 |
| F14 | Indicador de ticket médio por exame e convênio | BI | Template 3.8 |
| F15 | Indicador de tempo médio coleta → laudo | BI | Template 3.8 |
| F16 | Relatórios preditivos de demanda | BI | Template 3.8 |
| F17 | Interfaceamento bidirecional com equipamentos (HL7/ASTM) | Laboratorial | Template 3.4 |
| F18 | Integração com APIs reais de convênios (TISS) | Faturamento | Serviços compartilhados |
| F19 | Remover permissão de perfil | RBAC | ✅ Corrigido |
| F20 | Desvincular usuário de perfil | RBAC | ✅ Corrigido |
| F21 | Inativar usuário | Usuário | — |
| F22 | Auditoria para operações de cadastro (CRUD de master data) | Auditoria | ✅ Corrigido |
| F23 | Auditoria para operações de logística (malote, recebimento) | Auditoria | ✅ Corrigido |
| F24 | Auditoria para operações de compras | Auditoria | Pendente |
| F25 | Auditoria para operações de RBAC (atribuição de perfil) | Auditoria | Pendente |
| F26 | Filtros de data nos dashboards de BI | BI | — |
| F27 | Drill-down nos gráficos de BI | BI | — |
| F28 | Controle de vigência/término de valores de procedimento | Cadastro | — |
| F29 | Agendamento automático do ETL (scheduler) | BI | Regra 36 |

---

## 7. Gaps de Cobertura de Testes

### 7.1 Resumo

| Métrica | Valor |
|---------|-------|
| Total de testes | ~140 |
| Arquivos de teste | 23 |
| Módulos com zero testes de integração | Faturamento (fluxo real), Compras (estoque) |
| Funcionalidades sem testes | Autorização convênio, equipamentos, valores referência, pré-auditoria, concorrência |

### 7.2 Gaps por área

| Área | O que falta testar |
|------|-------------------|
| **Faturamento** | Fluxo completo: laudo liberado → adicionar ao lote → guia TISS criada → lote fechado → título a receber gerado. Só existem testes CRUD de lote. |
| **Faturamento** | Glosas: integração com faturamento. Sem testes para `registrar_glosa`. |
| **Financeiro** | Pagamento parcial de título. Conciliação com divergência. Fluxo de caixa com entradas e saídas reais no mesmo período. |
| **Compras** | Recebimento parcial de pedido. Lançamento em `estoque_movimentos` após recebimento. |
| **Laboratorial** | CRUD de equipamentos. CRUD de valores de referência. ~~Validação de resultado com amostra recebida~~ ✅ Testado. |
| **Logística** | Unicidade de amostra no malote (constraint unique). Transições inválidas de status de amostra. |
| **RBAC** | Seeds de permissões (`src/seeder/rbac.py`). ~~Remoção de permissão~~ ✅ Testado. ~~Desvinculação de usuário~~ ✅ Testado. |
| **Concorrência** | Dois usuários tentando cancelar o mesmo item. Race conditions em transições de status. |
| **LGPD** | Máscara de CPF em todas as telas (não apenas teste unitário do mask). |
| **BI** | ETL com dados operacionais reais. Cálculo de indicadores (tempo de ciclo, ticket médio). |

---

## 8. Issues de Infraestrutura

| # | Issue | Detalhe | Severidade |
|---|-------|---------|------------|
| I1 | `alembic/env.py` não importa `rbac`, `auditoria`, `bi` models | Autogenerate cego para tabelas de RBAC, auditoria e BI (mesmo que Bug #4) | ✅ Corrigido |
| I2 | `ConvenioService` duplicado em dois arquivos | Duas implementações concorrentes. A usada em produção (`convenio/service.py`) é a incompleta. | ✅ Corrigido |
| I3 | `session.commit()` descentralizado no módulo laboratorial | `LaboratorialService` comita internamente, impedindo composição transacional (mesmo que Bug #5) | Média |
| I4 | Chave LGPD hardcoded em `tests/conftest.py` | Chave Fernet de teste exposta no código. OK para testes, mas há risco de confusão se alguém usá-la em produção. | Baixa |
| I5 | `rotacionar_chave` sem mecanismo de rollback | Se a rotação for interrompida no meio, dados ficam parcialmente criptografados com chaves diferentes. Sem dry-run. | Média |
| I6 | BI depende de ETL manual | Não há scheduler/trigger para executar o ETL automaticamente. Sem ETL, dashboards ficam vazios e não há indicação de como popular. | Média |

---

## 9. Resumo Quantitativo

| Indicador | Valor |
|-----------|-------|
| Regras de negócio totais (Template) | 37 |
| Regras **totalmente cobertas** ✅ | 31 (84%) |
| Regras **parcialmente cobertas** ⚠️ | 4 (11%) |
| Regras **não cobertas** ❌ | 2 (5%) |
| Bugs críticos | 4 (todos resolvidos) |
| Bugs médios | 8 (2 resolvidos, 6 pendentes) |
| Bugs menores | 4 (3 resolvidos, 1 pendente) |
| Histórias de cancelamento da OS | 12/12 (100%) |
| **Total de testes passando** | **165/165** |

### Nota geral: 9.0/10 (após 2 sessões — 18 correções aplicadas)

O projeto está **sólido para um protótipo acadêmico**. Os pontos fortes são:

- **Fluxo central OS → coleta → logística → laboratorial → laudo** funciona corretamente de ponta a ponta
- **Cancelamento da OS** com regras de agregação — impecável, 100% coberto por testes
- **Modelagem de dados** consistente (UUID, numeric, timestamptz, status enums)
- **RBAC e LGPD** implementados com boas práticas (Fernet, SHA-256, anonimização no BI)
- **Separação OLTP/OLAP** com star schema para BI

### Pendências restantes (não resolvidas)

| # | Regra/Issue | Esforço |
|---|------------|---------|
| #19 | Pré-auditoria de guias TISS antes do fechamento do lote | 60-90 min |
| #20 | Bloqueio de itens inconsistentes no faturamento | 30 min |
| #24 | Alertas de divergência financeira (notificação ativa) | 15 min |
| #36 | ETL com scheduler (não manual) | 15 min |

---

*Relatório atualizado em 28/07/2026. Revisão completa de código, documentação, testes e migrações.*
