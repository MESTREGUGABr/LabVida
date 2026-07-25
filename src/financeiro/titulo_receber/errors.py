class FinanceiroError(Exception):
    """Exceção base para o módulo financeiro."""


class TituloReceberNaoEncontrado(FinanceiroError):
    """Lançada quando um título a receber não é encontrado."""


class TituloReceberJaBaixado(FinanceiroError):
    """Lançada ao tentar baixar um título que já foi pago."""
