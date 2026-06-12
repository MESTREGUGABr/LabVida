# LabVida

Glossario de dominio do ERP LabVida. Define linguagem comum para o laboratorio, sem detalhes de implementacao.

## Linguagem

**LabVida**:
ERP academico para uma rede regional de laboratorios de analises clinicas, composta por laboratorio central e unidades de coleta.
_Evitar_: sistema, plataforma, app.

**Ordem de Servico (OS)**:
Entidade central do fluxo operacional; representa o atendimento de um paciente e agrupa os exames solicitados.
_Evitar_: pedido, atendimento, ordem.

**Paciente**:
Pessoa atendida pelo laboratorio e vinculada a uma ou mais Ordens de Servico.
_Evitar_: cliente, usuario.

**Amostra**:
Material biologico coletado de um paciente para realizacao de exames, rastreado durante coleta, transporte e processamento.
_Evitar_: material, item.

**Coleta**:
Evento em que uma amostra e obtida de um paciente por colaborador autorizado.
_Evitar_: retirada, recebimento.

**Malote**:
Agrupamento logistico de amostras transportadas entre unidade de coleta e laboratorio central.
_Evitar_: pacote, remessa.

**Laudo**:
Documento final de resultado de exame, validado e liberado por responsavel tecnico.
_Evitar_: resultado, relatorio.

**Convenio**:
Entidade pagadora ou intermediadora que autoriza e remunera atendimentos conforme regras contratadas.
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
