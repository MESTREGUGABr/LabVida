class TituloPagarNaoEncontrado(Exception):
    """Lançada quando um título a pagar não é encontrado."""


class TituloPagarJaBaixado(Exception):
    """Lançada ao tentar baixar um título que já foi pago."""
