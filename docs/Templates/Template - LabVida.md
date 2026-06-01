

**UNIVERSIDADE FEDERAL DO AGRESTE DE PERNAMBUCO – UFAPE**

**BACHARELADO EM CIÊNCIA DA COMPUTAÇÃO** 

**ALINE FERNANDA SOARES SILVA**  
**CLAUDERSON BRANCO XAVIER**   
**GUSTAVO FERREIRA WANDERLEY**  
**VICTOR ALEXANDRE SARAIVA PIMENTEL**

**LabVida**  
Laboratório de Análises Clínicas

**1ª  Entrega do projeto referente à disciplina Sistemas de Informação e Tecnologias**

**Garanhuns \- PE**

**2026**

**SUMÁRIO**

[1\. Introdução e Contexto da Empresa	3](#heading=)

[2\. Estrutura Visual do ERP	4](#heading=)

[3\. Módulos do Sistema	5](#heading=)

[3.1 Módulo de Cadastro	5](#heading=)

[3.2 Módulo de Atendimento e Coleta	5](#heading=)

[3.3 Módulo de Logística de Amostras	6](#heading=)

[3.4 Módulo de Laboratorial	6](#heading=)

[3.5 Módulo de Faturamento de Convênios	7](#heading=)

[3.6 Módulo Financeiro	7](#heading=)

[3.7 Módulo de Compras	8](#3.7-módulo-de-compras)

[4\. Integração entre Módulos	9](#heading=)

[5\. Impactos Automáticos das Operações	10](#heading=)

[6\. Regras de negócio	11](#heading=)

[6.1 Cadastro	11](#heading=)

[6.2 Atendimento e Coleta	11](#heading=)

[6.3 Logística de Amostras	11](#heading=)

[6.4 Laboratorial	11](#heading=)

[6.5 Faturamento	11](#heading=)

[6.6 Financeiro	11](#heading=)

[6.7 Compras	12](#6.7-compras)

[6.8 Usuários, Segurança e Auditoria	12](#6.8-usuários,-segurança-e-auditoria)

[7\. Serviços Compartilhados	13](#heading=)

[**8\. Justificativa da Arquitetura	14**](#8.-justificativa-da-arquitetura)

# 

#  **1\. Introdução e Contexto da Empresa**

A LabVida é uma rede regional de laboratório de análises clínicas que cresceu de forma expressiva ao longo dos anos, passando de um pequeno laboratório de bairro a uma operação com laboratório central e quatro unidades de coleta distribuídas na região. Atualmente, a empresa conta com aproximadamente 95 colaboradores distribuídos entre os setores de atendimento, coleta, análises laboratoriais, logística de amostras, faturamento de convênios e setores administrativos. Apesar do crescimento consistente da demanda, a LabVida começou a enfrentar dificuldades sérias relacionadas à integração de informações, padronização de processos e eficiência operacional. Diante desse cenário, a diretoria contratou uma consultoria de gestão de TI que realizou um diagnóstico organizacional e tecnológico, identificando os seguintes problemas críticos:

**a) Gestão descentralizada:** gestores com dificuldade para acompanhar indicadores estratégicos e tomar decisões com base em dados confiáveis.

**b) Baixa integração entre sistemas:** cadastro de pacientes, exames, faturamento e controles administrativos funcionam de forma isolada, gerando retrabalho e duplicidade de dados.

**c) Gargalos no atendimento:** dados precisam ser digitados múltiplas vezes em sistemas diferentes, o que aumenta o tempo de atendimento e o risco de erros.

**d) Logística manual de amostras:** sem rastreamento em tempo real entre as unidades de coleta e o laboratório central.

**e) Faturamento de convênios críticos:** glosas frequentes, retrabalho e demora na consolidação dos faturamentos.

**f) Ausência de dashboards gerenciais:** diretoria sem visão integrada de produtividade, rentabilidade e desempenho operacional.

**g) Riscos de segurança da informação:** ausência de políticas formais de governança de dados e de controle de acesso inadequado.

Diante desse diagnóstico, o presente documento apresenta a arquitetura organizacional do ERP LabVida, demonstrando como os módulos do sistema integrarão os setores da empresa, automatizarão operações críticas e fornecerão inteligência gerencial em tempo real para sustentar o crescimento da rede.

# **2\. Estrutura Visual do ERP**

A estrutura visual do ERP LabVida deverá representar o sistema como uma arquitetura integrada, composta pelos seguintes módulos principais:

Cadastro → Atendimento e Coleta → Logística de Amostras → Laboratorial → Faturamento de Convênios → Financeiro ↳ **Módulo de Business Intelligence (BI)** *(Alimentado por todas as operações)* 

O fluxo central do sistema começa no cadastro do paciente e na abertura da Ordem de Serviço, passa pela coleta e pelo rastreamento da amostra, segue para análise laboratorial e liberação do laudo, depois avança para faturamento e, por fim, gera registros financeiros. Os indicadores gerenciais serão alimentados pelos dados registrados ao longo desse fluxo.

# **3\. Módulos do Sistema**

Cada módulo do ERP LabVida representa uma área funcional real da empresa. A seguir são detalhados o objetivo, as funcionalidades, as integrações e os impactos automáticos de cada módulo.

## **3.1 Módulo de Cadastro**

| CADASTRO |  |
| :---- | :---- |
| **Objetivo** | Controlar os cadastros essenciais da operação, como pacientes, médicos, convênios, unidades, setores e procedimentos laboratoriais. |
| **Funcionalidades** | cadastro de pacientes; registro de médicos e responsáveis técnicos; cadastro de convênios; manutenção do catálogo TUSS/TISS configuração das unidades de coleta configuração dos setores internos vinculação de procedimentos a valores contratuais criptografia de dados sensíveis dos pacientes |
| **Integrações** | Atendimento Faturamento Financeiro Laboratorial |
| **Impactos automáticos** | Quando um paciente, convênio ou procedimento é cadastrado, essas informações ficam disponíveis para abertura de OS, validação de elegibilidade, faturamento, emissão de laudos e geração de indicadores. |

## **3.2 Módulo de Atendimento e Coleta**

| COLETA |  |
| :---- | :---- |
| **Objetivo** | Organizar o atendimento ao paciente, validar os dados da OS, verificar convênios e registrar a coleta das amostras. |
| **Funcionalidades** | abertura de ordem de serviço geração de identificador único da OS emissão de etiquetas com código de barras ou QR Code validação de elegibilidade do convênio verificação de autorizações registro da coleta identificação do coletor registro de data e horário da coleta |
| **Integrações** | Cadastro Logística Faturamento Laboratorial |
| **Impactos automáticos** | A abertura da OS dispara a verificação de elegibilidade. Após a coleta, o sistema altera o status da amostra para pendência logística e envia a informação para o módulo de Logística. |

## **3.3 Módulo de Logística de Amostras**

| LOGÍSTICA DE AMOSTRAS |  |
| :---- | :---- |
| **Objetivo** | Garantir a rastreabilidade da cadeia de custódia das amostras, evitando perdas, atrasos, falhas de conferência e ausência de controle sobre o trajeto do material biológico. |
| **Funcionalidades** | gestão de malotes agrupamento de amostras por destino registro de saída da unidade acompanhamento de status da amostra controle de amostras coletadas, em trânsito e recebidas protocolo eletrônico de recebimento conferência de integridade do malote liberação da amostra para triagem técnica |
| **Integrações** | Atendimento Coleta Laboratorial |
| **Impactos automáticos** | Quando a coleta é registrada, a amostra entra no backlog logístico. Quando o recebimento é confirmado no laboratório central, o sistema desbloqueia a OS para execução técnica no módulo Laboratorial. |

## **3.4 Módulo de Laboratorial**

| LABORATORIAL |  |
| :---- | :---- |
| **Objetivo** | Controlar a execução dos exames laboratoriais, reduzir erros humanos, automatizar a comunicação com equipamentos e garantir segurança na liberação dos laudos. |
| **Funcionalidades** | triagem técnica das amostras distribuição da carga de trabalho por bancada ou equipamento interfaceamento bidirecional com analisadores clínicos envio de ordens aos equipamentos recebimento automático de resultados validação de valores de referência revisão técnica assinatura digital liberação final de laudos |
| **Integrações** | Logística Faturamento Cadastro |
| **Impactos automáticos** | Após o recebimento da amostra, o Laboratorial libera a execução técnica. Quando o resultado é importado do equipamento, o status muda para aguardando revisão técnica. Após a liberação do laudo, os dados são enviados automaticamente para o módulo de Faturamento. |

## **3.5 Módulo de Faturamento de Convênios**

| FATURAMENTO |  |
| :---- | :---- |
| **Objetivo** | Validar guias, autorizações, códigos TUSS/TISS e regras de convênio antes do fechamento do lote de faturamento. |
| **Funcionalidades** | pré-auditoria de guias; validação automática contra regras de glosa; geração de XML TISS; fechamento de lotes; monitoramento de glosas; análise por motivo de glosa; análise por operadora; análise por unidade de origem. |
| **Integrações** | Atendimento Cadastro Laboratorial Financeiro |
| **Impactos automáticos** | A liberação do laudo disponibiliza o item para pré-auditoria. O fechamento do lote gera títulos a receber no módulo Financeiro e atualiza os indicadores gerenciais. |

## **3.6 Módulo Financeiro**

| FINANCEIRO |  |
| :---- | :---- |
| **Objetivo** | Controlar o fluxo financeiro da empresa e oferecer visão consolidada da rentabilidade por exame, convênio e unidade. |
| **Funcionalidades** | contas a receber baixa automática de títulos conciliação com arquivos de pagamento controle de fluxo de caixa registro de entradas e saídas controle de repasses DRE gerencial indicadores de rentabilidade ticket médio por exame e convênio |
| **Integrações** | Faturamento Atendimento Cadastro |
| **Impactos automáticos** | Quando um lote é fechado no Faturamento, os títulos são gerados automaticamente no Contas a Receber. A partir disso, o sistema atualiza o fluxo de caixa, a DRE e os relatórios gerenciais. |

## **3.7 Módulo de Compras** {#3.7-módulo-de-compras}

| COMPRAS |  |
| :---- | :---- |
| **Objetivo** | Controlar a aquisição de insumos laboratoriais, materiais de coleta, reagentes, equipamentos e demais recursos necessários para o funcionamento das unidades e do laboratório central. |
| **Funcionalidades** | solicitação de compras; cadastro de fornecedores; controle de pedidos; registro de insumos e materiais adquiridos; acompanhamento de prazos de entrega; integração com contas a pagar. |
| **Integrações** | Financeiro Cadastro Laboratorial |
| **Impactos automáticos** | Quando uma compra é aprovada, o sistema gera uma previsão de pagamento no módulo Financeiro. Quando os insumos ou materiais são recebidos, os registros internos de materiais disponíveis são atualizados para apoiar os processos laboratoriais. |

### **3.8 Módulo de Business Intelligence (BI)**

| BI |  |
| :---- | :---- |
| **Objetivo** | Consolidar os dados gerados por todas as operações do ERP para extrair indicadores estratégicos, permitindo à diretoria e aos gestores tomar decisões baseadas em dados confiáveis em tempo real. |
| **Funcionalidades** | • Criação de dashboards interativos e gerenciais; • Monitoramento de indicadores de produtividade técnica do laboratório; • Análise de rentabilidade e ticket médio por exame, convênio e unidade; • Acompanhamento de metas operacionais e taxas de glosas em tempo real; • Relatórios preditivos de demanda de atendimento e consumo de insumos; • Painel de controle de eficiência da cadeia logística de amostras. |
| **Integrações** | Cadastro, Atendimento e Coleta, Logística, Laboratorial, Faturamento, Financeiro e Compras. |
| **Impactos automáticos** | Qualquer operação realizada nos demais módulos (como a baixa de um título ou a liberação de um laudo) atualiza os cubos de dados do BI e reflete instantaneamente nos dashboards da diretoria. |

# **4\. Integração entre Módulos**

A integração entre os módulos ocorre por meio de gatilhos automáticos que alteram o estado das informações ao longo do processo operacional.

O fluxo integrado pode ser representado da seguinte forma:

**Cadastro → Atendimento e Coleta → Logística de Amostras → Laboratorial → Faturamento de Convênios → Financeiro**

A abertura da OS no Atendimento depende de dados previamente cadastrados no módulo de Cadastro. Após a abertura, o sistema valida o convênio e, se aprovado, libera a coleta.

Quando a coleta é registrada, a amostra passa para o módulo de Logística. Após o recebimento no laboratório central, o módulo Laboratorial é desbloqueado para execução técnica. Depois da análise, o laudo é revisado e liberado. A liberação do laudo envia os dados ao Faturamento, que realiza a pré-auditoria e gera o lote. Por fim, o lote fechado alimenta o módulo Financeiro e os dados gerados ao longo do processo podem ser utilizados para relatórios e indicadores gerenciais.

# **5\. Impactos Automáticos das Operações**

| Operação de Origem | Módulo Origem | Impacto Automático | Módulo Destino |
| :---- | :---- | :---- | :---- |
| Cadastro de paciente | Cadastro | Disponibiliza dados para abertura de OS | Atendimento |
| Abertura de OS | Atendimento | Dispara validação de elegibilidade | Atendimento/Faturamento |
| Registro de coleta | Atendimento | Cria pendência de transporte | Logística |
| Recebimento de amostra | Logística | Desbloqueia execução técnica | Laboratorial |
| Importação de resultado | Laboratorial | Muda status para revisão técnica | Laboratorial |
| Liberação de laudo | Laboratorial | Envia item para pré-auditoria | Faturamento |
| Fechamento de lote | Faturamento | Gera títulos a receber | Financeiro |
| Baixa financeira | Financeiro | Atualiza fluxo de caixa | Financeiro / Relatórios Gerenciais |
| Aprovação de compra | Compras | Gera previsão de pagamento | Financeiro |
| Atualização de qualquer registro | Todos os Módulos | Alimenta os cubos de dados e atualiza os dashboards gerenciais | BI |
| Consolidação de faturamento/glosas | Faturamento | Atualiza o painel de eficiência financeira e perdas por operadora | BI |

# **6\. Regras de negócio**

## **6.1 Cadastro**

* Não permitir cadastro duplicado de paciente com o mesmo identificador.

* Dados sensíveis do paciente devem ser criptografados.

* Convênios devem estar ativos para serem usados em uma OS.

* Procedimentos devem possuir código TUSS/TISS válido.

## **6.2 Atendimento e Coleta**

* Toda OS deve possuir identificador único.

* OS de convênio só pode ser aberta com autorização válida.

* A coleta só pode ser registrada por usuário autorizado.

* Toda amostra coletada deve receber etiqueta com código de barras ou QR Code.

## **6.3 Logística de Amostras**

* Nenhuma amostra pode ser analisada sem registro de recebimento no laboratório central.

* Toda movimentação da amostra deve gerar registro de auditoria.

* Malotes devem possuir origem, destino, data, hora e responsável.

* Amostras divergentes ou danificadas devem ser bloqueadas para análise.

## **6.4 Laboratorial**

* Resultados só podem ser inseridos ou importados após recebimento logístico da amostra.

* A liberação final do laudo só pode ser feita por responsável técnico autorizado.

* Toda alteração em resultado clínico deve gerar registro em auditoria imutável.

* Resultados importados de equipamentos devem ser vinculados à OS correspondente.

## **6.5 Faturamento**

* Não permitir envio de guia sem código TUSS/TISS válido.

* Não permitir faturamento de OS sem laudo liberado.

* Guias devem passar pela pré-auditoria antes do fechamento do lote.

* Itens com inconsistência devem ser bloqueados até a correção.

## **6.6 Financeiro**

* Somente o setor financeiro pode confirmar baixa de pagamento.

* Lotes fechados no Faturamento devem gerar títulos automaticamente.

* Pagamentos recebidos devem alimentar o fluxo de caixa.

* Divergências entre valor faturado e valor recebido devem gerar alerta.


## **6.7 Compras** {#6.7-compras}

* Solicitações de compra devem ser registradas por usuário autorizado.

* Compras aprovadas devem gerar previsão de pagamento no módulo Financeiro.

* Fornecedores devem estar previamente cadastrados.

* Materiais laboratoriais devem possuir identificação, quantidade e finalidade registrada.

## **6.8 Usuários, Segurança e Auditoria** {#6.8-usuários,-segurança-e-auditoria}

* Permissões devem variar conforme o perfil do usuário.

* Apenas gestores podem cancelar operações críticas.

* Logs devem registrar alterações sensíveis.

* Dados pessoais e clínicos devem seguir diretrizes da LGPD.

* Auditorias clínicas e financeiras devem ser append-only, ou seja, sem sobrescrita dos registros anteriores.


### **6.9 Business Intelligence (BI)**

* Os dashboards estratégicos de rentabilidade e desempenho financeiro só podem ser acessados pela diretoria e usuários explicitamente autorizados.  
* Os dados apresentados no BI não devem permitir a alteração direta dos registros na base de dados operacional (visão em modo *Read-Only*).  
* O processamento e a atualização dos grandes volumes de dados (carga ETL) não devem comprometer a performance das operações em tempo real do ERP nas unidades.  
* Indicadores que envolvam dados sensíveis de pacientes devem respeitar o anonimato de acordo com as diretrizes da LGPD.

# **7\. Serviços Compartilhados**

O ERP LabVida contará com serviços comuns utilizados por todos os módulos:

* autenticação de usuários  
* controle de permissões por perfil  
* criptografia de dados sensíveis  
* logs de auditoria  
* integração com APIs de convênios  
* integração com padrão TISS  
* interfaceamento com equipamentos laboratoriais  
* geração de relatórios e indicadores gerenciais  
* notificações e alertas operacionais

# **8\. Justificativa da Arquitetura** {#8.-justificativa-da-arquitetura}

A organização em módulos separados foi escolhida para facilitar a manutenção do sistema, permitir a divisão de responsabilidades entre as áreas funcionais e reduzir o acoplamento entre os processos da LabVida. Essa arquitetura modular permite que cada área do ERP possua responsabilidades bem definidas, como cadastro, atendimento, logística, laboratório, faturamento, financeiro e compras. Dessa forma, alterações em um módulo tendem a causar menor impacto nos demais. A persistência dos dados poderá ser organizada em um banco de dados relacional, com tabelas específicas para cada área funcional e relacionamentos entre os módulos integrados. Essa estrutura facilita o controle das informações, a rastreabilidade das operações e a geração de relatórios gerenciais

