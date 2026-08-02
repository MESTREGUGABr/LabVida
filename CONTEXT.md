# LabVida

Glossario de dominio do ERP LabVida. Define linguagem comum para o laboratorio, sem detalhes de implementacao.

## Linguagem

**LabVida**:
ERP academico para uma rede regional de laboratorios de analises clinicas, composta por laboratorio central e unidades de coleta.
_Evitar_: sistema, plataforma, app.

**Cadastro**:
Area do LabVida que mantem dados basicos e referenciais necessarios para iniciar e sustentar o fluxo operacional.
_Evitar_: modulo inicial, base de dados, tela de cadastro.

**Ordem de Servico (OS)**:
Entidade central do fluxo operacional; representa o atendimento de um paciente e agrupa os exames solicitados.
_Evitar_: pedido, atendimento, ordem.

**Item ativo da OS**:
Item de uma Ordem de Servico que ainda participa do atendimento e pode exigir a liberacao de um Laudo; um item cancelado nao e ativo.
_Evitar_: item pendente, exame ativo.

**Conclusao da OS**:
Estado da Ordem de Servico alcancado quando todos os seus itens ativos possuem Laudos liberados. Itens cancelados nao impedem a conclusao.
_Evitar_: fechamento, finalizacao do pedido.

**Cancelamento da OS**:
Estado da Ordem de Servico alcancado quando todos os seus itens estao cancelados. O cancelamento de um ou mais itens nao cancela a OS enquanto houver trabalho ativo.
_Evitar_: cancelamento parcial da ordem, exclusao da OS.

**Paciente**:
Pessoa de qualquer idade atendida pelo laboratorio e vinculada a uma ou mais Ordens de Servico.
_Evitar_: cliente, usuario.

**Data de Nascimento do Paciente**:
Data civil em que o Paciente nasceu; pode ser a data atual, mas nunca uma data futura.
_Evitar_: idade, aniversario.

**CPF do Paciente**:
Identificador civil usado pelo laboratorio para reconhecer um paciente de forma unica no Cadastro.
_Evitar_: documento, identificador generico.

**Telefone do Paciente**:
Meio de contato telefonico usado pelo laboratorio para comunicacoes operacionais com o paciente.
_Evitar_: contato.

**Amostra**:
Material biologico coletado de um paciente para realizacao de exames, rastreado durante coleta, transporte e processamento.
_Evitar_: material, item.

**Coleta**:
Evento em que uma amostra e obtida de um paciente por colaborador autorizado.
_Evitar_: retirada, recebimento.

**Malote**:
Agrupamento logistico de amostras transportadas entre unidade de coleta e laboratorio central.
_Evitar_: pacote, remessa.

**Cadeia de Custódia**:
Registro ordenado e auditavel das movimentacoes, responsaveis e localizacoes de uma Amostra desde a Coleta ate a analise e liberacao do Laudo.
_Evitar_: historico de rastreio, rastro.

**Protocolo de Recebimento**:
Registro formal de conferencia fisica e de integridade de um Malote e de suas Amostras na entrada do laboratorio central.
_Evitar_: checagem, recebimento simples.

**Laudo**:
Documento final de resultado de exame, validado e liberado por responsavel tecnico.
_Evitar_: resultado, relatorio.

**Convenio**:
Entidade pagadora ou intermediadora vinculada a Ordens de Servico para identificar quem autoriza ou remunera exames. Um convenio pode estar ativo ou inativo; convenios inativos permanecem reconheciveis pelo laboratorio para preservar historico.
_Evitar_: plano, seguradora.

**Guia TISS**:
Registro padronizado usado na comunicacao de faturamento entre laboratorio e convenio.
_Evitar_: guia, fatura.

**Glosa**:
Recusa total ou parcial de pagamento feita por convenio sobre item faturado.
_Evitar_: erro de pagamento, desconto.

**BI**:
Camada analitica que consolida dados operacionais em indicadores, dashboards e relatorios gerenciais.
_Evitar_: relatorio, dashboard.

**Dimensao**:
Tabela do BI que descreve o contexto de um fato — quem, o que, onde e quando. E por ela que se filtra e agrupa (tempo, unidade, convenio, procedimento, setor, faixa etaria, motivo de glosa).
_Evitar_: tabela auxiliar, lookup.

**Fato**:
Tabela do BI que guarda as medidas de um evento do negocio, sempre num unico grao e sempre com a chave natural da linha de origem.
_Evitar_: tabela de dados, agregado.

**Grao**:
O que exatamente uma linha de fato representa (uma Ordem de Servico, um item, uma amostra, uma glosa). Medida so convive com o fato que compartilha seu grao.
_Evitar_: nivel, granularidade generica.

**Chave Natural**:
Identificador da linha de origem no operacional guardado no fato. E o que torna a carga do BI reexecutavel e permite reconciliar BI com a base operacional.
_Evitar_: id, chave primaria.

**Medida Aditiva**:
Valor que pode ser somado em qualquer combinacao de dimensoes (valor faturado, quantidade de exames). Indicador de razao — ticket medio, taxa de glosa — e sempre calculado a partir delas, nunca armazenado.
_Evitar_: metrica, indicador armazenado.

**Regime de Caixa**:
Reconhecimento do valor na data em que o dinheiro entrou ou saiu de fato, apurado a partir dos movimentos de caixa.
_Evitar_: realizado, pago.

**Regime de Competencia**:
Reconhecimento do valor na data do fato gerador, independentemente de quando o dinheiro circula. No faturamento e a data em que o laudo foi liberado.
_Evitar_: previsto, provisionado.

**Tempo de Atendimento (TAT)**:
Intervalo entre a coleta da Amostra e a liberacao do ultimo Laudo da Ordem de Servico. Medido no grao da OS, nunca no grao do item.
_Evitar_: tempo de ciclo, lead time.

**Resultado**:
Valor bruto ou interpretacao tecnica inicial importada de um equipamento laboratorial referente a um parametro de exame.
_Evitar_: laudo, exame.

**Analito**:
Componente especifico ou grandeza medida individualmente dentro de um exame maior (ex: Leucocitos dentro de um Hemograma). Possui valor de referencia e resultado proprios.
_Evitar_: parametro, sub-exame, item.
