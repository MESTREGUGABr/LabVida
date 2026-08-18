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

| Achado | Onde | Causa | Sugestão |
|---|---|---|---|
| `st.metric` corta valor/rótulo com "..." | `src/ui_css.py:301-322` (fonte do valor fixa em 32px) + `bi_visao_executiva.py:58` e `bi_financeiro.py:52` (`st.columns(5)`) | Fonte grande + muitas colunas estreitas lado a lado + nenhuma regra de quebra de linha para telas médias (só existe breakpoint para celular) | Reduzir para 3-4 métricas por linha, ou fonte responsiva por breakpoint, ou `white-space: normal; overflow-wrap: break-word` no rótulo |
| Rótulo mais longo do sistema estoura fácil | `bi_produtividade.py:54-57` — `"TAT medio (coleta -> laudo)"` em `st.columns(4)` | Mesmo problema acima, agravado pelo tamanho do texto | Encurtar para algo como `"TAT (coleta→laudo)"` |
| Drill-down interativo criado mas nunca ligado | `src/bi/graficos.py:111` cria `alt.selection_point()`; nenhuma das 4 páginas passa `on_select="rerun"` ou lê a seleção | Funcionalidade prevista em `plano-bi.md:260` ficou pela metade | Ligar o `on_select` nas páginas, ou remover a menção do plano se não for prioridade agora |
| Comparação temporal (Δ%) só na Visão Executiva | `bi_financeiro.py`, `bi_logistica.py`, `bi_produtividade.py` não usam `variacao()` | Função já existe e é usada só numa página | Reaproveitar `variacao()` (já usada em `bi_visao_executiva.py`) nas outras 3 |

## 3. Achados de cobertura de conteúdo — checklist dos 8 indicadores oficiais (Entrega 3)

`docs/Entrega 3/entrega-3-corrigida.md` §11 lista 8 "Indicadores Gerenciais Gerados Pela Integração" prometidos oficialmente (documento já corrigido pelo professor). Checklist item a item contra `src/bi/`:

| # | Indicador prometido | Status | Onde |
|---|---|---|---|
| 1 | Tempo médio entre coleta e laudo | ✅ | `metricas.py:186` (`tat_por_mes`), `:209` (`tat_por_setor`) |
| 2 | Produtividade por unidade | ✅ | `metricas.py:79` (`exames_por_unidade`) |
| 3 | Taxa de glosa por convênio | ✅ | `metricas.py:469` (`taxa_glosa_por_convenio`) |
| 4 | Receita por procedimento | ✅ | `metricas.py:389` (`curva_abc_procedimentos`) |
| 5 | Inadimplência e divergências | ⚠️ parcial | inadimplência coberta (`aging_carteira`, `metricas.py:579`); **divergências não existe em nenhuma página nem em `metricas.py`** |
| 6 | Consumo de insumos por setor | ❌ ausente | zero menção a "insumo" em `src/bi/` |
| 7 | Volume de exames por período | ✅ | `metricas.py:91` (`exames_por_mes`) |
| 8 | Ocorrências de auditoria | ❌ ausente | zero menção a "auditoria" em `src/bi/` |

**Ponto de atenção:** os itens 6 e 8 não aparecem nem como pendência conhecida em `roadmap-execucao.md` ou `plano-bi.md` (nem na Onda 1/F2, nem na Onda 2/F12 pendente) — foram prometidos na Entrega 3 e nunca entraram no planejamento subsequente do time. O item 5 (divergências) está parcialmente coberto pela F12 já documentada como pendente.

## 4. Lacuna adicional de cobertura de negócio (visão gestor)

- **Estoque/Compras sem representação no BI** — o ERP tem o módulo (inclusive com bloqueio por saldo insuficiente na coleta), mas não existe fato/dimensão nem indicador de estoque (giro, ruptura, insumos críticos) em nenhuma das 4 páginas.
- **Sem painel de alertas/exceções** na Visão Executiva (títulos vencidos, remessas sem retorno) — previsto no desenho original (`plano-bi.md:240`), não implementado.

## 5. Nota de contexto sobre o parecer do professor

`docs/ADERÊNCIA FUNCIONAL AO QUE FOI PROPOSTO DA LABVIDA.pdf` avalia BI como **"Atendido"** (Tabela 1), diferente de Faturamento, Financeiro e Integrações externas, marcados **"Atendido parcialmente"**. A avaliação foi feita em nível macro ("existe modelo dimensional + ETL + 4 dashboards? sim") e não desceu ao nível dos 8 indicadores específicos da Entrega 3 — por isso não contradiz os achados das seções 2-4 acima, apenas indica que o risco de nota do projeto está concentrado em outros módulos, não em BI.

## 6. Documentação desatualizada

`docs/plano-evolucao-erp.md` §5.1 ("BI por período", 3 bugs) ainda descreve o diagnóstico **pré-reconstrução** do BI como se fosse o estado atual — já foi superado pela Onda 1 (`plano-bi.md`). Sugestão: marcar a seção como histórica/superada, apontando para `plano-bi.md`.

## 7. Lista final priorizada

| Prioridade | Achado | Arquivo(s) | Esforço | Natureza |
|---|---|---|---|---|
| 1 | `st.metric` cortando com "..." | `ui_css.py:301-322`, `bi_visao_executiva.py:58`, `bi_financeiro.py:52` | Baixo | Cosmético, mas visível e fácil de corrigir |
| 2 | Rótulo longo em `bi_produtividade.py` | `bi_produtividade.py:54` | Baixo | Cosmético |
| 3 | `docs/plano-evolucao-erp.md` §5.1 desatualizado | `plano-evolucao-erp.md` | Baixo | Organização de documentação |
| 4 | Drill-down morto (criado, não ligado) | `graficos.py:111` | Médio | Decisão de escopo: ligar ou remover do plano |
| 5 | Δ% ausente fora da Visão Executiva | `bi_financeiro.py`, `bi_logistica.py`, `bi_produtividade.py` | Médio | Melhoria de UX gerencial |
| 6 | Indicadores 6 e 8 da Entrega 3 ausentes (insumos por setor, ocorrências de auditoria) | `src/bi/metricas.py` (novo código) | Alto | **Requisito oficial não atendido** — decisão de escopo com a equipe |
| 7 | Estoque/Compras e painel de alertas fora do BI | `src/bi/` (novo escopo) | Alto | Evolução futura, não bloqueante |

## Fora do escopo desta revisão

Nenhuma correção foi implementada — este documento é só o registro e a priorização, para a equipe decidir o que vale a pena atacar antes do fechamento final da entrega.
