# Semantica de cancelamento da OS

Uma Ordem de Servico so pode assumir o estado `CANCELADA` quando todos os seus itens estiverem cancelados. O cancelamento parcial de itens nao anula a OS: se restarem itens ativos pendentes, ela continua no fluxo; se todos os itens ativos tiverem Laudos liberados, ela assume `CONCLUIDA`. Essa regra preserva na OS o trabalho que ainda existe e permite concluir com sucesso os itens que nao foram cancelados.
