# Revisão final do módulo de BI

**Data:** 2026-08-17
**Objetivo:** revisão do módulo de BI antes do fechamento da entrega — o que corrigir e o que evoluir.

Contexto: o projeto já foi apresentado e avaliado (nota final **9,3** no parecer *"Aderência Funcional ao que foi Proposto"* do professor), com o módulo de BI marcado como **"Atendido"** (sem ressalva de parcial). Este documento não questiona essa nota — é um registro interno dos pontos que a equipe identificou numa auditoria própria, mais detalhada do que o nível de granularidade da avaliação de aderência.

## 1. Panorama — o que já está bem

O BI passou por uma reconstrução completa ("Onda 1", `plano-bi.md`, concluída em 02/08/2026, fase F2 do roadmap), que corrigiu 8 bugs de dados catalogados antes dela existir:

- Esquema estrela com **chave natural** em todo fato (`docs/adr/0009-grao-chave-natural-e-medidas-derivadas-no-bi.md`).
- ETL idempotente via `INSERT ... ON CONFLICT DO UPDATE` (`src/bi/etl.py:134-142`) e poda de linhas obsoletas (`:150`) — carga caiu de ~35s para ~1,3s.
- Gráficos em Altair (não mais o nativo do Streamlit), com tipo de gráfico adequado ao dado (linha para série temporal, barra para categórica, donut para composição).
- Filtro de período nas 4 páginas, com comparação (Δ%) contra o período anterior na Visão Executiva.
- Rodapé "dados atualizados em" em todas as páginas.

Não foram encontrados bugs de cálculo (divisão por zero, JOIN duplicando linha, timezone incorreto) nas duas passadas de revisão — os problemas abaixo são de **UX** e de **cobertura de conteúdo**, não de correção aritmética do que já existe.

## 2. Achados de UX

| Achado | Onde | Causa | Sugestão | Status |
|---|---|---|---|---|
| `st.metric` corta valor/rótulo com "..." | `src/ui_css.py:301-322` (fonte do valor fixa em 32px) + `bi_visao_executiva.py:58` e `bi_financeiro.py:52` (`st.columns(5)`) | Fonte grande + muitas colunas estreitas lado a lado + nenhuma regra de quebra de linha para telas médias (só existe breakpoint para celular) | Reduzir para 3-4 métricas por linha, ou fonte responsiva por breakpoint, ou `white-space: normal; overflow-wrap: break-word` no rótulo | ✅ **Corrigido em 2026-08-17** — fonte do valor responsiva por `cqw` (largura real do card, via `container-type: inline-size`), rótulo com quebra de linha (`!important` para vencer o CSS-in-JS do Streamlit) e quebra em 2 linhas como rede de segurança para números muito grandes |
| Rótulo mais longo do sistema estoura fácil | `bi_produtividade.py:54-57` — `"TAT medio (coleta -> laudo)"` em `st.columns(4)` | Mesmo problema acima, agravado pelo tamanho do texto | Encurtar para algo como `"TAT (coleta→laudo)"` | ✅ **Corrigido em 2026-08-17** — rótulo encurtado para `"TAT (coleta -> laudo)"` |
| Drill-down interativo criado mas nunca ligado | `src/bi/graficos.py:111` cria `alt.selection_point()`; nenhuma das 4 páginas passa `on_select="rerun"` ou lê a seleção | Funcionalidade prevista em `plano-bi.md:260` ficou pela metade | Ligar o `on_select` nas páginas, ou remover a menção do plano se não for prioridade agora | ✅ **Resolvido em 2026-08-17** — decisão do usuário foi remover em vez de implementar (cross-filter real é esforço médio-alto e toca várias páginas, não valia o custo nesta reta final). Parâmetro morto `selecao` removido de `barra_categorica`, e a promessa em `plano-bi.md:260` reescrita registrando a decisão |
| Comparação temporal (Δ%) só na Visão Executiva | `bi_financeiro.py`, `bi_logistica.py`, `bi_produtividade.py` não usam `variacao()` | Função já existe e é usada só numa página | Reaproveitar `variacao()` (já usada em `bi_visao_executiva.py`) nas outras 3 | ✅ **Resolvido em 2026-08-17** — `variacao()` replicada nas 3 páginas para os KPIs que já vêm de `metricas.kpis()` (Faturado/Glosado/Liberado/Recebido/Taxa de glosa no Financeiro; Exames/TAT no Produtividade; Amostras/Taxa de rejeição na Logística), com `delta_color="inverse"` nas métricas em que "mais" é ruim. Métricas derivadas de outros dataframes (Unidades ativas, Trânsito médio etc.) ficaram sem delta, mesmo escopo já usado na Visão Executiva |
| Gráficos sem demarcação visual entre si | Todas as 26 seções das 4 páginas — só `<h3>` + `<hr>` solto antes de cada gráfico | `renderizar_secao` nunca envolveu o conteúdo num container visual | Envolver cada seção em `st.container(border=True)` (padrão já usado em outras telas do sistema) | ✅ **Corrigido em 2026-08-17** — todas as seções agora ficam em cards com borda/sombra |
| Barras com largura inconsistente entre gráficos vizinhos | "DRE gerencial" x "Carteira a receber por faixa de atraso" (`bi_visao_executiva.py:99-121`); "Sazonalidade semanal" x "Tempo medio de atendimento por setor" (`bi_produtividade.py:111-140`) | Nenhuma das duas funções de gráfico fixava a largura da barra (`mark_bar` sem `size`) nem usava a mesma `altura`/ângulo de rótulo entre gráficos adjacentes — cada um calculava a largura/altura de forma independente, dando cards com base e espessura de barra diferentes na mesma linha | Fixar `tamanho_barra` compartilhado entre os dois gráficos, igualar a `altura` passada em ambos, e travar o ângulo do rótulo do eixo (`labelAngle=0`) | ✅ **Corrigido em 2026-08-17** — `TAMANHO_BARRA_DRE_AGING` compartilhado em `graficos.py`, alturas igualadas (240px e 200px respectivamente) e rótulo do eixo vertical fixado em `labelAngle=0` |

## 3. Achados de cobertura de conteúdo — checklist dos 8 indicadores oficiais (Entrega 3)

`docs/Entrega 3/entrega-3-corrigida.md` §11 lista 8 "Indicadores Gerenciais Gerados Pela Integração" prometidos oficialmente (documento já corrigido pelo professor). Checklist item a item contra `src/bi/`:

| # | Indicador prometido | Status | Onde |
|---|---|---|---|
| 1 | Tempo médio entre coleta e laudo | ✅ | `metricas.py:186` (`tat_por_mes`), `:209` (`tat_por_setor`) |
| 2 | Produtividade por unidade | ✅ | `metricas.py:79` (`exames_por_unidade`) |
| 3 | Taxa de glosa por convênio | ✅ | `metricas.py:469` (`taxa_glosa_por_convenio`) |
| 4 | Receita por procedimento | ✅ | `metricas.py:389` (`curva_abc_procedimentos`) |
| 5 | Inadimplência e divergências | ⚠️ parcial | inadimplência coberta (`aging_carteira`, `metricas.py:579`); **divergências não existe em nenhuma página nem em `metricas.py`** |
| 6 | Consumo de insumos por setor | ❌ **decisão: não implementar** (2026-08-17) | Bloqueador estrutural, não só um FK faltando: `_processar_consumo_estoque` (`src/atendimento/amostra/service.py:110-168`) já **soma** as quantidades de insumo de todos os procedimentos/setores de uma OS antes de gravar um único `EstoqueMovimento` — a granularidade por setor é perdida antes mesmo de persistir, e `EstoqueMovimento` (`src/compras/insumo/models.py:29-39`) não tem FK de origem (só `observacao` texto livre). Corrigir de verdade exigiria mudar o fluxo de consumo de estoque em produção + FK novo + migration. Decisão: gap documentado, não implementado nesta entrega |
| 7 | Volume de exames por período | ✅ | `metricas.py:91` (`exames_por_mes`) |
| 8 | Ocorrências de auditoria | ✅ **Implementado em 2026-08-17** | Nova página `pages/bi_auditoria.py`, consulta direta a `AuditoriaLog` (sem ETL/fato novo — log de auditoria já tinha 19 pontos de chamada cobrindo quase todos os módulos), gate por `admin:visualizar_auditoria` |

**Ponto de atenção:** os itens 6 e 8 não aparecem nem como pendência conhecida em `roadmap-execucao.md` ou `plano-bi.md` (nem na Onda 1/F2, nem na Onda 2/F12 pendente) — foram prometidos na Entrega 3 e nunca entraram no planejamento subsequente do time. O item 5 (divergências) está parcialmente coberto pela F12 já documentada como pendente.

## 4. Lacuna adicional de cobertura de negócio (visão gestor)

- **Estoque/Compras sem representação no BI** — o ERP tem o módulo (inclusive com bloqueio por saldo insuficiente na coleta), mas não existe fato/dimensão nem indicador de estoque (giro, ruptura, insumos críticos) em nenhuma das 4 páginas.
- **Sem painel de alertas/exceções** na Visão Executiva (títulos vencidos, remessas sem retorno) — previsto no desenho original (`plano-bi.md:240`), não implementado.

## 5. Nota de contexto sobre o parecer do professor

`docs/ADERÊNCIA FUNCIONAL AO QUE FOI PROPOSTO DA LABVIDA.pdf` avalia BI como **"Atendido"** (Tabela 1), diferente de Faturamento, Financeiro e Integrações externas, marcados **"Atendido parcialmente"**. A avaliação foi feita em nível macro ("existe modelo dimensional + ETL + 4 dashboards? sim") e não desceu ao nível dos 8 indicadores específicos da Entrega 3 — por isso não contradiz os achados das seções 2-4 acima, apenas indica que o risco de nota do projeto está concentrado em outros módulos, não em BI.

## 6. Documentação desatualizada

`docs/plano-evolucao-erp.md` §5.1 ("BI por período", 3 bugs) ainda descreve o diagnóstico **pré-reconstrução** do BI como se fosse o estado atual — já foi superado pela Onda 1 (`plano-bi.md`). Sugestão: marcar a seção como histórica/superada, apontando para `plano-bi.md`.

✅ **Corrigido em 2026-08-17** — adicionada uma nota no início de §5 marcando-a como diagnóstico histórico/superado (aponta para `plano-bi.md` e `revisao-bi-final.md`), e as linhas N4/N5 de §7.1 (que remetiam aos mesmos bugs) receberam o sufixo "corrigido pela reconstrução do BI".

## 7. Lista final priorizada

| Prioridade | Achado | Arquivo(s) | Esforço | Natureza | Status |
|---|---|---|---|---|---|
| 1 | `st.metric` cortando com "..." | `ui_css.py:301-322`, `bi_visao_executiva.py:58`, `bi_financeiro.py:52` | Baixo | Cosmético, mas visível e fácil de corrigir | ✅ Concluído em 2026-08-17 |
| 2 | Rótulo longo em `bi_produtividade.py` | `bi_produtividade.py:54` | Baixo | Cosmético | ✅ Concluído em 2026-08-17 |
| — | *(extra, não estava na lista original)* Gráficos sem cards + barras/alturas inconsistentes entre gráficos vizinhos | `pages/bi_*.py`, `src/bi/graficos.py` | Baixo/Médio | Cosmético, identificado pelo usuário ao validar os itens 1 e 2 | ✅ Concluído em 2026-08-17 |
| 3 | `docs/plano-evolucao-erp.md` §5.1 desatualizado | `plano-evolucao-erp.md` | Baixo | Organização de documentação | ✅ Concluído em 2026-08-17 |
| 4 | Drill-down morto (criado, não ligado) | `graficos.py:111` | Médio | Decisão de escopo: ligar ou remover do plano | ✅ Concluído em 2026-08-17 — removido (decisão do usuário) |
| 5 | Δ% ausente fora da Visão Executiva | `bi_financeiro.py`, `bi_logistica.py`, `bi_produtividade.py` | Médio | Melhoria de UX gerencial | ✅ Concluído em 2026-08-17 |
| 6a | Indicador 6 da Entrega 3 — consumo de insumos por setor | `src/atendimento/amostra/service.py`, `src/compras/insumo/models.py` | Alto | **Requisito oficial não atendido** — bloqueador estrutural (ver §3) | ✅ Decidido em 2026-08-17 — **não implementar**, gap documentado |
| 6b | Indicador 8 da Entrega 3 — ocorrências de auditoria | `pages/bi_auditoria.py` (novo), `src/bi/metricas.py` | Médio | **Requisito oficial não atendido** — infraestrutura já pronta (`AuditoriaLog`) | ✅ Concluído em 2026-08-17 |
| 7 | Estoque/Compras e painel de alertas fora do BI | `src/bi/` (novo escopo) | Alto | Evolução futura, não bloqueante | Pendente |

## Fora do escopo desta revisão

Nenhuma correção foi implementada — este documento é só o registro e a priorização, para a equipe decidir o que vale a pena atacar antes do fechamento final da entrega.
