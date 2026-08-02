---
status: accepted
---

# Grao, Chave Natural e Medidas Derivadas no BI

Quatro decisoes de modelagem do esquema estrela, tomadas junto ao [plano de BI](../plano-bi.md).

**1. Todo fato declara grao e carrega chave natural.** Cada linha de fato passa a guardar o identificador da linha de origem no OLTP (`os_item_id`, `ordem_servico_id`, `amostra_id`, `guia_item_id`, `titulo_id`, `glosa_id`). Hoje nenhum fato tem — o que torna carga incremental, deduplicacao e reconciliacao OLTP/OLAP impossiveis, e obriga o ETL a apagar tudo e recarregar. Com a chave natural, a carga vira `ON CONFLICT DO UPDATE` e passa a ser idempotente por construcao.

**2. Medida no grao errado vira fato proprio.** `tempo_ciclo_os_horas` e atributo da Ordem de Servico, mas hoje e gravado repetido em cada linha de `bi_fato_atendimento`, que tem grao de item. Qualquer media pondera a OS pelo numero de exames — uma OS com 8 exames pesa 8 vezes uma OS com 1. Criamos `bi_fato_ordem_servico` no grao de OS e o indicador sai de `bi_fato_atendimento`. A regra geral: **medida e fato so convivem quando compartilham o grao**.

**3. Medida derivada sai da tabela de fato e vira funcao na camada semantica.** `ticket_medio`, `rentabilidade` e taxa de glosa deixam de ser colunas (hoje nunca populadas) e passam a ser calculadas em `src/bi/metricas.py` sobre os aditivos. Razao pre-calculada em fato nao reagrega: a media das medias nao e a media, e o ticket medio de dois convenios nao e a media dos dois tickets. Guardar so medidas aditivas (`valor_faturado`, `valor_glosado`, `qtd_exames`) preserva a corretude sob qualquer filtro de periodo — que e exatamente o que o professor pediu ao falar em periodo no BI.

**4. Atributo que muda com o tempo e congelado no fato, nao recalculado na dimensao.** A faixa etaria do paciente passa a ser gravada como `sk_faixa_etaria` na linha de fato, com o valor vigente **na data do fato gerador**. Hoje ela vive em `bi_dim_paciente_anon` e e calculada uma unica vez, na primeira carga, e nunca mais atualizada — o que ja e um bug (B7 do plano de BI). Mas a correcao ingenua, recalcular a faixa a cada carga, cria um bug pior: um paciente que faz 19 anos migra de faixa e **some retroativamente** da faixa anterior em todo relatorio historico, mudando numeros de meses fechados. Congelar no fato preserva a historia e continua respeitando a anonimizacao — a faixa e um agregado, nao PII.

Consequencia colateral aceita: o modelo dimensional documentado na Entrega 03 muda. As colunas removidas nunca tiveram valor gravado, entao nao ha perda de dado historico.
