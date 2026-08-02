---
status: accepted
---

# Fuso Horario da Competencia de Faturamento

Adotamos `America/Recife` como fuso unico de apuracao da competencia. A competencia de todo lancamento deriva do fato gerador (`laudo.liberado_em`, que e `TIMESTAMPTZ` em UTC) pela expressao `date_trunc('month', instante AT TIME ZONE 'America/Recife')`, encapsulada num unico helper `competencia_de(instante)` e replicada literalmente em todo SQL de backfill.

A alternativa seria apurar em UTC. Rejeitamos porque a competencia e eixo contabil e o laboratorio opera em horario local: um laudo liberado as 22h de 28/02 em Garanhuns e `2026-03-01T01:00Z`, e apurar em UTC o jogaria para marco — a receita apareceria no mes errado para quem assina o balanco.

A decisao e **imutavel na pratica**: reapurar competencia depois que existirem competencias fechadas exige reprocessar todo o ledger, os totais congelados e os titulos derivados. Por isso ela e registrada aqui antes de qualquer migration da trilha de faturamento (F4 em diante no [roadmap](../roadmap-execucao.md)).

O fuso vive em `TZ_OPERACAO` (`src/config.py`), nao literal espalhado pelo codigo.
