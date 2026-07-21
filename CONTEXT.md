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

**Paciente**:
Pessoa atendida pelo laboratorio e vinculada a uma ou mais Ordens de Servico.
_Evitar_: cliente, usuario.

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

**Resultado**:
Valor bruto ou interpretacao tecnica inicial importada de um equipamento laboratorial referente a um parametro de exame.
_Evitar_: laudo, exame.

**Analito**:
Componente especifico ou grandeza medida individualmente dentro de um exame maior (ex: Leucocitos dentro de um Hemograma). Possui valor de referencia e resultado proprios.
_Evitar_: parametro, sub-exame, item.
