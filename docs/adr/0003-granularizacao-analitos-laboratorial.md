---
status: accepted
---

# Granularizacao de Analitos no Modulo Laboratorial

Decidimos modelar os resultados laboratoriais com granularidade de **Analito** (multiplas linhas na tabela `resultado` para um unico `os_item_id`) em vez de consolida-los em um unico payload JSON. Alem disso, adicionamos a coluna `valor_esperado_texto` (varchar) na tabela `valor_referencia` para dar suporte pleno a testes qualitativos (ex: "Nao Reagente").

Isso desvia da arquitetura inicial (Entrega 02) que sugeria uma relacao mais simples e agrupada entre o resultado e o exame. O *trade-off* de adicionar essa complexidade no banco de dados e justificado pela obrigatoriedade de permitir auditoria clinica *append-only* (tabela `resultado_auditoria`) restrita exatamente ao parametro especifico que o medico retificou, alem de permitir regras de negocio distintas (matematicas vs. textuais) na avaliacao de cada componente do exame.
