class InsumoError(Exception):
    """Exceção base para insumos."""


class InsumoNaoEncontrado(InsumoError):
    """Lançada quando um insumo não é encontrado."""
