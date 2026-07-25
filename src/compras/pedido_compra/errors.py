class PedidoError(Exception):
    """Exceção base para pedidos de compra."""


class PedidoNaoEncontrado(PedidoError):
    """Lançada quando um pedido não é encontrado."""


class PedidoNaoPodeSerAprovado(PedidoError):
    """Lançada ao tentar aprovar um pedido que não está em RASCUNHO."""


class PedidoNaoPodeSerRecebido(PedidoError):
    """Lançada ao tentar receber um pedido que não está APROVADO."""


class PedidoNaoPodeSerCancelado(PedidoError):
    """Lançada ao tentar cancelar um pedido que não está em RASCUNHO."""


class FornecedorInvalidoParaPedido(PedidoError):
    """Lançada quando o fornecedor não está ativo."""


class SolicitacaoSemItens(PedidoError):
    """Lançada ao tentar criar pedido sem itens."""
