# Entrega 02 Corrigida - Modelagem da Base de Dados do ERP LabVida

**Disciplina:** Sistemas de Informação e Tecnologias (SIT)  
**Projeto:** ERP LabVida - Laboratório de Análises Clínicas  
**Equipe:** Aline Fernanda Soares Silva · Clauderson Branco Xavier · Gustavo Ferreira Wanderley · Victor Alexandre Saraiva Pimentel  
**Garanhuns - PE · 2026**

---

## 1. Introdução

Esta versão corrigida da Entrega 02 revisa a modelagem da base de dados do ERP LabVida a partir do feedback recebido. A versão anterior representava bem as entidades centrais do laboratório e o fluxo operacional do ERP, porém misturava parcialmente elementos do modelo conceitual com decisões próprias do modelo lógico e explorava pouco técnicas de abstração, como generalização e especialização.

As principais correções realizadas foram:

- Separação mais explícita entre modelo conceitual, modelo lógico e decisões físicas.
- Inclusão de generalização/especialização com a entidade conceitual **Pessoa**.
- Reorganização das entidades humanas do domínio, evitando repetição conceitual entre Paciente, Médico, Usuário e Responsável Técnico.
- Maior distinção entre regras de negócio e estruturas relacionais.
- Inclusão conceitual mais clara da camada analítica, BI, auditoria corporativa e indicadores estratégicos.
- Preservação da aderência ao fluxo do ERP: Cadastro - Atendimento - Coleta - Logística - Laboratório - Faturamento - Financeiro.

---

## 2. Objetivos da Modelagem Corrigida

| Objetivo | Como a versão corrigida atende |
|---|---|
| Representar o domínio do negócio | O modelo parte dos conceitos organizacionais do laboratório antes de detalhar tabelas e chaves. |
| Separar níveis de modelagem | O documento diferencia modelo conceitual, modelo lógico e decisões físicas de implementação. |
| Usar abstração conceitual | A entidade Pessoa generaliza Paciente, Profissional de Saúde e Colaborador/Usuário. |
| Preservar o fluxo ERP | A Ordem de Serviço continua sendo a entidade central que integra atendimento, coleta, logística, laboratório, faturamento e financeiro. |
| Incluir BI e auditoria corporativa | A camada analítica passa a ser tratada como parte relevante do domínio informacional do ERP. |
| Manter rastreabilidade | Amostras, laudos, resultados, faturamento e ações sensíveis permanecem auditáveis. |

---

## 3. Separação dos Níveis de Modelagem

Uma das fragilidades apontadas no feedback foi a proximidade excessiva entre modelo conceitual e modelo lógico. Por isso, a modelagem corrigida adota a seguinte separação:

| Nível | Finalidade | O que aparece neste nível | O que não deve aparecer neste nível |
|---|---|---|---|
| Conceitual | Representar o domínio do negócio | Entidades, relacionamentos, especializações e cardinalidades | Tipos SQL, UUID, índices, constraints físicas e nomes técnicos de tabela |
| Lógico | Organizar a estrutura relacional | Entidades convertidas em relações, atributos, identificadores, chaves e normalização | Detalhes de SGBD e comandos SQL específicos |
| Físico | Definir implementação no banco | Tipos PostgreSQL, índices, criptografia, triggers, particionamento e permissões | Reinterpretação do negócio |

Assim, o MER conceitual passa a representar primeiro os conceitos do ERP LabVida, enquanto o modelo lógico traduz esses conceitos para uma estrutura relacional consistente.

---

## 4. Modelo Conceitual Corrigido

O modelo conceitual corrigido representa o domínio do ERP em alto nível, com foco nas entidades do negócio e em seus relacionamentos. Nesta seção não são usados tipos de dados, chaves primárias, UUIDs, nomes de colunas técnicas ou decisões específicas de PostgreSQL.

### 4.1 Generalização e Especialização de Pessoa

A entidade **Pessoa** representa qualquer indivíduo relevante para o ERP LabVida. Essa abstração evita duplicidade conceitual de dados comuns, como nome, documento, contato e endereço.

Especializações de **Pessoa**:

- **Paciente:** pessoa atendida pelo laboratório e vinculada a ordens de serviço.
- **Profissional de Saúde:** pessoa que solicita exames ou assume responsabilidade técnica por laudos.
- **Colaborador:** pessoa que trabalha na organização e executa atividades internas do ERP.
- **Usuário do Sistema:** colaborador com credenciais e permissões para operar o sistema.
- **Responsável Técnico:** especialização de Profissional de Saúde autorizada a validar e liberar laudos.

A especialização não elimina as entidades específicas; ela apenas organiza melhor o domínio. Um médico, por exemplo, é uma pessoa com registro profissional e pode ou não atuar como responsável técnico. Um usuário do sistema é uma pessoa vinculada à operação interna e a um perfil de acesso.

### 4.2 Entidades Conceituais Principais

| Entidade Conceitual | Papel no domínio |
|---|---|
| Pessoa | Generaliza indivíduos envolvidos no ERP. |
| Paciente | Recebe atendimento, realiza exames e possui dados sensíveis protegidos pela LGPD. |
| Profissional de Saúde | Solicita exames ou atua tecnicamente sobre laudos. |
| Responsável Técnico | Libera laudos e responde tecnicamente por resultados. |
| Colaborador | Atua em processos internos como atendimento, coleta, logística, laboratório, financeiro ou compras. |
| Usuário do Sistema | Acessa o ERP conforme perfil e permissões. |
| Convênio | Entidade pagadora ou intermediadora de atendimento. |
| Procedimento/Exame | Serviço laboratorial solicitado e executado. |
| Unidade | Laboratório central ou unidade de coleta. |
| Ordem de Serviço | Entidade integradora do fluxo operacional. |
| Amostra | Material biológico coletado do paciente. |
| Coleta | Evento de obtenção da amostra. |
| Malote | Agrupamento logístico de amostras entre unidades. |
| Resultado | Registro técnico produzido a partir da análise laboratorial. |
| Laudo | Documento final validado por responsável técnico. |
| Lote de Faturamento | Agrupa guias e itens faturáveis. |
| Guia TISS | Representa o padrão de comunicação com convênios. |
| Título Financeiro | Representa obrigação a receber ou a pagar. |
| Movimento Financeiro | Registra entradas e saídas financeiras. |
| Fornecedor | Entidade externa associada a compras e suprimentos. |
| Insumo | Material utilizado nas atividades laboratoriais. |
| Auditoria Corporativa | Registro institucional de ações sensíveis e eventos críticos. |
| Indicador Estratégico | Informação consolidada para gestão e BI. |

### 4.3 Relacionamentos Conceituais Centrais

| Relacionamento | Cardinalidade Conceitual | Interpretação |
|---|---|---|
| Pessoa especializa-se em Paciente | 1:0..1 | Uma pessoa pode ser paciente. |
| Pessoa especializa-se em Profissional de Saúde | 1:0..1 | Uma pessoa pode ser médico ou responsável técnico. |
| Pessoa especializa-se em Colaborador | 1:0..1 | Uma pessoa pode trabalhar na organização. |
| Colaborador especializa-se em Usuário do Sistema | 1:0..1 | Nem todo colaborador precisa acessar o ERP. |
| Profissional de Saúde especializa-se em Responsável Técnico | 1:0..1 | Apenas profissionais habilitados liberam laudos. |
| Paciente possui Ordem de Serviço | 1:N | Um paciente pode ter várias ordens de serviço. |
| Ordem de Serviço contém Procedimentos/Exames | 1:N | Uma OS pode solicitar vários exames. |
| Convênio autoriza Ordem de Serviço | 0..1:N | Uma OS pode ser particular ou vinculada a convênio. |
| Unidade registra Ordem de Serviço | 1:N | A OS nasce em uma unidade de atendimento/coleta. |
| Ordem de Serviço gera Amostras | 1:N | Uma OS pode exigir uma ou mais amostras. |
| Colaborador realiza Coleta | 1:N | A coleta é feita por colaborador autorizado. |
| Amostra percorre Malotes | N:N | Uma amostra pode ser transportada em malote e um malote contém várias amostras. |
| Amostra produz Resultado | 1:N | Uma amostra pode gerar resultados de exames diferentes. |
| Resultado compõe Laudo | N:1 | Um laudo consolida resultados validados. |
| Responsável Técnico libera Laudo | 1:N | Cada laudo liberado deve ter responsável técnico. |
| Laudo habilita Faturamento | 1:0..N | Apenas laudos liberados entram no faturamento. |
| Lote de Faturamento gera Título a Receber | 1:1..N | O fechamento do lote gera efeitos financeiros. |
| Compra gera Título a Pagar | 1:0..N | Compras aprovadas geram obrigações financeiras. |
| Eventos operacionais alimentam Auditoria Corporativa | N:N | Alterações sensíveis são registradas institucionalmente. |
| Eventos operacionais alimentam Indicadores Estratégicos | N:N | Dados consolidados sustentam BI e gestão. |

---

## 5. Modelo Lógico Corrigido

O modelo lógico traduz o modelo conceitual para uma estrutura relacional normalizada. Diferente do modelo conceitual, aqui já aparecem entidades relacionais, atributos principais, identificadores e vínculos.

### 5.1 Núcleo de Pessoas e Acessos

| Relação | Atributos principais | Observação |
|---|---|---|
| pessoa | identificador, nome, documento, contato, endereco | Dados comuns a indivíduos do domínio. |
| paciente | pessoa, data_nascimento, sexo, dados_sensiveis | Especialização de pessoa, com proteção LGPD. |
| profissional_saude | pessoa, conselho_profissional, numero_registro, uf_registro | Representa médicos e profissionais habilitados. |
| responsavel_tecnico | profissional_saude, habilitacao, status | Subtipo de profissional autorizado a liberar laudos. |
| colaborador | pessoa, unidade, setor, cargo, status | Pessoa vinculada à operação interna. |
| usuario_sistema | colaborador, login, senha_hash, ativo | Acesso ao ERP. |
| perfil | nome, descricao | Papel de acesso. |
| permissao | codigo, descricao | Permissão individual. |
| perfil_permissao | perfil, permissao | Associação N:N entre perfis e permissões. |

### 5.2 Cadastro Operacional

| Relação | Atributos principais | Observação |
|---|---|---|
| convenio | nome, registro_ans, status | Controla atendimento por operadora/convênio. |
| plano_convenio | convenio, nome, regras_cobertura, status | Detalha regras específicas de cobertura. |
| procedimento | codigo_tuss, nome, setor, material_requerido | Catálogo de exames/procedimentos. |
| procedimento_valor | procedimento, convenio, valor, vigencia | Valor contratado por convênio. |
| unidade | nome, tipo, endereco | Laboratório central e unidades de coleta. |
| setor | unidade, nome | Setores internos. |

### 5.3 Atendimento, Coleta e Logística

| Relação | Atributos principais | Observação |
|---|---|---|
| ordem_servico | codigo, paciente, profissional_solicitante, convenio, unidade, status | Entidade central do fluxo. |
| os_item | ordem_servico, procedimento, status, valor_negociado | Procedimentos solicitados. |
| autorizacao_convenio | ordem_servico, numero_guia, status, validade | Autorização associada ao convênio. |
| amostra | ordem_servico, codigo_barras, tipo_material, status | Material biológico rastreável. |
| coleta | amostra, colaborador_coletor, data_hora | Evento de coleta. |
| malote | unidade_origem, unidade_destino, responsavel, status | Transporte entre unidades. |
| malote_amostra | malote, amostra | Associação entre malotes e amostras. |
| amostra_movimentacao | amostra, status, data_hora, responsavel | Cadeia de custódia. |
| protocolo_recebimento | malote, recebedor, integridade_ok, data_hora | Conferência no recebimento. |

### 5.4 Laboratório e Laudos

| Relação | Atributos principais | Observação |
|---|---|---|
| equipamento | setor, nome, protocolo_integracao | Equipamentos laboratoriais. |
| valor_referencia | procedimento, minimo, maximo, unidade_medida, faixa | Apoia validação técnica. |
| resultado | os_item, equipamento, valor, status, data_importacao | Resultado produzido ou importado. |
| resultado_revisao | resultado, profissional_revisor, parecer, data_hora | Revisão técnica antes do laudo. |
| laudo | os_item, responsavel_tecnico, status, data_liberacao, assinatura_digital | Documento final. |
| resultado_auditoria | resultado, usuario_sistema, valor_anterior, valor_novo, data_hora | Histórico imutável de alterações clínicas. |

### 5.5 Faturamento e Financeiro

| Relação | Atributos principais | Observação |
|---|---|---|
| lote_faturamento | convenio, periodo, status, data_fechamento | Agrupa guias para cobrança. |
| guia_tiss | lote_faturamento, numero, status_pre_auditoria, xml_tiss | Padrão TISS. |
| guia_item | guia_tiss, laudo, procedimento, valor_faturado | Item faturável após laudo liberado. |
| glosa | guia_item, motivo, valor_glosado, unidade_origem | Controle de recusas de pagamento. |
| titulo_receber | lote_faturamento, valor, vencimento, status | Efeito financeiro de cobrança. |
| titulo_pagar | pedido_compra, valor, vencimento, status | Obrigação financeira de compras. |
| movimento_financeiro | titulo, tipo, valor, data_hora | Entrada ou saída financeira. |
| conciliacao_pagamento | titulo_receber, valor_recebido, divergencia | Confronto entre faturado e recebido. |

### 5.6 Compras e Estoque

| Relação | Atributos principais | Observação |
|---|---|---|
| fornecedor | nome, cnpj, status | Cadastro de fornecedores. |
| solicitacao_compra | solicitante, status, data_criacao | Solicitação interna. |
| pedido_compra | solicitacao_compra, fornecedor, status, valor_total | Pedido aprovado ou pendente. |
| pedido_item | pedido_compra, insumo, quantidade, valor_unitario | Itens do pedido. |
| recebimento_insumo | pedido_compra, data_recebimento, conferido | Entrada física de materiais. |
| insumo | nome, finalidade, quantidade_estoque | Material usado pelo laboratório. |
| estoque_movimento | insumo, tipo, quantidade, data_hora | Controle de entrada e saída. |

---

## 6. Regras de Negócio Separadas da Estrutura Relacional

Outra correção importante é separar claramente regras de negócio das estruturas relacionais. As tabelas representam dados; as regras indicam restrições e comportamentos do ERP.

| Regra de negócio | Entidades envolvidas | Interpretação |
|---|---|---|
| Paciente deve ser identificável de forma única | Pessoa, Paciente | Evita duplicidade de cadastro. |
| Convênio precisa estar ativo para autorizar atendimento | Convênio, Plano, Ordem de Serviço | Uma OS de convênio depende de elegibilidade. |
| Procedimento deve existir no catálogo | Procedimento, OS Item | Não há exame fora do catálogo. |
| Amostra só pode ser analisada após recebimento | Amostra, Movimentação, Protocolo de Recebimento | Garante cadeia de custódia. |
| Resultado alterado deve ser auditado | Resultado, Resultado Auditoria | Preserva rastreabilidade clínica. |
| Laudo só pode ser liberado por responsável técnico | Laudo, Responsável Técnico | Garante responsabilidade técnica. |
| Laudo liberado habilita faturamento | Laudo, Guia Item, Lote de Faturamento | Impede cobrança antes da conclusão técnica. |
| Fechamento de lote gera título financeiro | Lote de Faturamento, Título a Receber | Integra faturamento e financeiro. |
| Compra aprovada gera obrigação financeira | Pedido de Compra, Título a Pagar | Integra compras e financeiro. |
| Alterações sensíveis devem compor auditoria corporativa | Usuário, Auditoria Corporativa | Atende governança, LGPD e controle interno. |

---

## 7. Auditoria Corporativa Corrigida

Na versão anterior, a auditoria estava presente, mas muito associada a tabelas técnicas. A correção amplia a auditoria como conceito corporativo do ERP.

A **Auditoria Corporativa** registra eventos relevantes para governança, segurança, LGPD, rastreabilidade operacional e responsabilização institucional.

Eventos auditáveis:

- Cadastro, alteração ou inativação de paciente.
- Abertura, cancelamento ou alteração de ordem de serviço.
- Coleta, transporte e recebimento de amostras.
- Importação, revisão e alteração de resultados.
- Liberação, retificação ou cancelamento de laudos.
- Fechamento de lotes de faturamento.
- Registro de glosas e conciliações financeiras.
- Aprovação de compras e movimentações de estoque.
- Acesso a dados sensíveis de pacientes.
- Alteração de perfis e permissões de usuários.

Conceitualmente, a auditoria se relaciona com Usuário do Sistema, Evento Operacional, Entidade Afetada e Momento da Ação. No modelo lógico, esse conceito pode ser implementado por registros imutáveis, mas a decisão de usar JSON, trigger ou mecanismo específico pertence ao nível físico.

---

## 8. Camada Analítica e BI Corrigidos

O feedback apontou que o ERP apresenta BI, auditoria corporativa e indicadores estratégicos mais ricos do que os representados no MER. Por isso, a versão corrigida inclui a camada analítica como parte explícita do domínio informacional.

### 8.1 Entidades Analíticas Conceituais

| Entidade Analítica | Papel |
|---|---|
| Indicador Estratégico | Representa métricas utilizadas pela gestão. |
| Painel Gerencial | Agrupa indicadores por área de decisão. |
| Evento Operacional Consolidado | Representa eventos do ERP preparados para análise. |
| Dimensão de Análise | Contextualiza indicadores por tempo, unidade, convênio, procedimento, paciente anonimizado ou setor. |
| Fato Analítico | Consolida ocorrências mensuráveis como atendimentos, faturamentos, glosas e movimentações logísticas. |

### 8.2 Indicadores Estratégicos Representados

| Indicador | Origem no ERP | Uso gerencial |
|---|---|---|
| Produtividade por unidade | Ordem de Serviço, Coleta, Laudo | Avaliar desempenho das unidades. |
| Tempo médio entre coleta e laudo | Coleta, Amostra, Resultado, Laudo | Medir eficiência operacional. |
| Taxa de glosa por convênio | Guia TISS, Guia Item, Glosa | Negociar com operadoras e corrigir falhas. |
| Receita por procedimento | Procedimento, Guia Item, Título a Receber | Analisar rentabilidade. |
| Inadimplência e divergências | Título a Receber, Conciliação | Apoiar gestão financeira. |
| Consumo de insumos por setor | Estoque, Insumo, Setor | Planejar compras e reduzir desperdícios. |
| Volume de exames por período | OS Item, Procedimento, Tempo | Prever demanda. |
| Ocorrências de auditoria | Auditoria Corporativa, Usuário | Monitorar riscos e conformidade. |

### 8.3 Modelo Dimensional Lógico

| Tipo | Estrutura | Métricas ou contexto |
|---|---|---|
| Fato | fato_atendimento | quantidade de OS, quantidade de exames, tempo de atendimento |
| Fato | fato_logistica | tempo de transporte, amostras transportadas, ocorrências de integridade |
| Fato | fato_laboratorial | tempo de processamento, quantidade de laudos, revisões técnicas |
| Fato | fato_faturamento | valor faturado, valor glosado, taxa de glosa |
| Fato | fato_financeiro | valor recebido, valor pendente, divergência financeira |
| Fato | fato_auditoria | quantidade de eventos, tipo de ação, criticidade |
| Dimensão | dim_tempo | dia, mês, trimestre, ano |
| Dimensão | dim_unidade | unidade, tipo de unidade, localização |
| Dimensão | dim_convenio | convênio, plano, status |
| Dimensão | dim_procedimento | exame, setor, código TUSS |
| Dimensão | dim_paciente_anonimizado | faixa etária, sexo, região sem identificação direta |
| Dimensão | dim_usuario | perfil, setor, unidade, sem exposição indevida de dados pessoais |

Essa camada permanece separada da base operacional. O modelo operacional registra os eventos; o modelo analítico consolida informações para tomada de decisão.

---

## 9. Rastreabilidade do Fluxo ERP

O fluxo principal do ERP LabVida permanece preservado e mais claramente conectado ao domínio:

| Etapa do ERP | Entidades envolvidas | Resultado informacional |
|---|---|---|
| Cadastro | Pessoa, Paciente, Convênio, Procedimento, Unidade | Base cadastral confiável. |
| Atendimento | Ordem de Serviço, Paciente, Profissional de Saúde, Convênio | Solicitação formal de exames. |
| Coleta | Amostra, Coleta, Colaborador | Material biológico identificado. |
| Logística | Malote, Amostra, Movimentação, Protocolo | Cadeia de custódia rastreável. |
| Laboratório | Resultado, Revisão, Laudo, Responsável Técnico | Produção e validação técnica. |
| Faturamento | Guia TISS, Guia Item, Lote, Glosa | Cobrança estruturada. |
| Financeiro | Títulos, Movimentos, Conciliação | Controle econômico-financeiro. |
| Compras | Solicitação, Pedido, Fornecedor, Insumo, Estoque | Suprimento da operação. |
| Auditoria | Usuário, Evento, Entidade Afetada | Governança e conformidade. |
| BI | Fatos, Dimensões, Indicadores | Gestão estratégica. |

---

## 10. Justificativa da Modelagem Corrigida

A modelagem corrigida mantém os pontos fortes da versão original, especialmente a boa representação das entidades centrais do laboratório e a rastreabilidade do fluxo operacional. Ao mesmo tempo, responde às fragilidades apontadas no feedback.

A introdução da entidade **Pessoa** melhora o nível de abstração do MER, pois evita que Paciente, Médico, Usuário e Responsável Técnico sejam tratados como conceitos totalmente independentes quando, na realidade, compartilham características comuns. Essa generalização torna o modelo mais aderente a práticas de modelagem conceitual e permite representar melhor papéis diferentes exercidos por indivíduos dentro do ERP.

A separação entre modelo conceitual, lógico e físico evita a antecipação de decisões de implementação. O documento passa a distinguir o que pertence ao domínio do negócio, o que pertence à organização relacional dos dados e o que seria decisão técnica de banco de dados.

A ampliação da auditoria corporativa e do BI corrige a lacuna de aderência ao ERP, pois o sistema proposto não serve apenas para registrar operações laboratoriais, mas também para apoiar governança, conformidade, gestão financeira, análise estratégica e tomada de decisão.

Portanto, esta versão corrigida representa de forma mais completa o domínio organizacional da LabVida, preservando a integração operacional do ERP e acrescentando os elementos conceituais solicitados na avaliação: abstração, separação de níveis de modelagem, auditoria corporativa e camada analítica.

---

## 11. Resumo das Correções Solicitadas e Atendidas

| Feedback do professor | Correção realizada |
|---|---|
| Pouca generalização/especialização | Criada a entidade Pessoa e suas especializações. |
| Paciente, Médico, Usuário e Responsável Técnico poderiam derivar de Pessoa | Reorganizado o núcleo de pessoas com Paciente, Profissional de Saúde, Colaborador, Usuário e Responsável Técnico. |
| Modelo muito próximo do lógico | Criada seção separando modelo conceitual, lógico e físico. |
| Antecipação de decisões de implementação | Removidas decisões físicas do modelo conceitual e mantidas apenas no nível adequado. |
| Separar regras de negócio e estrutura relacional | Criada seção própria para regras de negócio. |
| BI e indicadores estratégicos pouco refletidos | Incluída camada analítica com fatos, dimensões e indicadores. |
| Auditoria corporativa pouco explorada | Criada seção conceitual específica de auditoria corporativa. |
