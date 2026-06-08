# Considerações sobre o MER

**Remetente:** ASSUERO FONSECA XIMENES <assuero.ximenes@ufape.edu.br>  
**Data:** 8 de junho de 2026 às 08:56  
**Destinatários:** Aline Fernanda Soares Silva <ALINE.FERNANDA@ufape.edu.br>, CLAUDERSON BRANCO XAVIER <CLAUDERSON.XAVIER@ufape.edu.br>, Gustavo Ferreira Wanderley <GUSTAVO.WANDERLEY@ufape.edu.br>, VICTOR ALEXANDRE SARAIVA PIMENTEL <VICTOR.SARAIVA@ufape.edu.br>

A avaliação realizada nesta atividade foi fundamentada nos princípios contemporâneos de Modelagem de Dados, Engenharia de Software e Engenharia de Requisitos, conforme discutidos por autores como Elmasri & Navathe, Connolly & Begg, Coronel & Morris, Teorey et al., Sommerville, Pressman & Maxim, além das recomendações do DAMA-DMBOK (Data Management Body of Knowledge).

O objetivo principal da análise não foi apenas verificar a presença de entidades, relacionamentos e cardinalidades, mas principalmente avaliar a capacidade do grupo em transformar o modelo organizacional do ERP em um modelo conceitual de dados capaz de representar adequadamente o domínio do negócio.

De forma geral, o trabalho demonstrou boa compreensão dos conceitos fundamentais de entidade, relacionamento e cardinalidade, além de apresentar preocupação com a integração dos processos empresariais. Entretanto, ainda existe espaço para evolução na separação entre os níveis conceitual, lógico e físico da modelagem, bem como no aprofundamento das técnicas de abstração necessárias para representar adequadamente domínios organizacionais mais complexos.

Por fim, destaca-se que a qualidade de um Modelo Entidade-Relacionamento não deve ser medida apenas pela correção técnica de suas estruturas, mas principalmente pela sua capacidade de representar fielmente a realidade organizacional da empresa estudada. Em sistemas ERP, o sucesso da modelagem depende menos da quantidade de entidades desenhadas e mais da capacidade de traduzir corretamente os processos de negócio em informações estruturadas, consistentes e integradas.

## Pontos Fortes do MER

Boa representação das entidades centrais do domínio laboratorial e boa decomposição entre Paciente, Convênio, Ordem de Serviço, Amostra, Exame, Resultado, Faturamento e Financeiro. Possui uma boa rastreabilidade da operação e o fluxo de negócio está claramente refletido nas entidades e os relacionamentos coerentes com a realidade organizacional.

## Aderência à Modelagem do ERP

A modelagem de dados representa quase integralmente a arquitetura proposta no ERP e o fluxo Cadastro - Atendimento - Coleta - Logística - Laboratório - Faturamento - Financeiro foi preservado no modelo de dados e houve bom alinhamento entre processos e persistência de dados.

## Fragilidades Conceituais do MER

Pouca utilização de abstrações mais avançadas, como generalização/especialização. Entidades como Paciente, Médico, Usuário e Responsável Técnico poderiam derivar de Pessoa e houve pouca exploração de herança conceitual.

## Fragilidades de Modelagem

Alguns elementos já aparecem excessivamente próximos do modelo lógico. Além disso existe antecipação de decisões de implementação. Poderia haver maior separação entre regras de negócio e estrutura relacional.

## Fragilidades de Aderência ao ERP

O ERP apresenta BI, auditoria corporativa e indicadores estratégicos mais ricos do que os representados no MER e a parte da camada analítica não foi refletida na modelagem conceitual.

## Análise dos Conceitos de MER

O grupo compreendeu bem os conceitos de entidade, relacionamento, cardinalidade e rastreabilidade, mas houve mistura parcialmente do Modelo Conceitual e Modelo Lógico ao utilizar identificadores e estruturas próximas das tabelas. Na prática do mercado, o modelo está muito próximo do padrão utilizado em projetos ERP reais.

---

**Dr. Assuero Fonseca Ximenes**  
Docente do Curso de Ciência da Computação  
Universidade Federal do Agreste de Pernambuco - UFAPE  
Área de Gestão de TI
