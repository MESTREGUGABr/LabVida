# Protecao contra cancelamento integral de OS com itens concluidos

O cancelamento integral de uma Ordem de Servico deve ser bloqueado quando algum item ja tiver Laudo liberado ou estiver faturado. Nessa situacao, o gestor pode cancelar apenas itens ainda ativos; a regra agregada dos itens determina se a OS permanece em andamento ou se torna `CONCLUIDA`, enquanto `CANCELADA` fica reservado para OSs sem itens concluidos.
