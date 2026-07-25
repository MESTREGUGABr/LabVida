class GlosaError(Exception):
    """Exceção base para o módulo de glosa."""


class GuiaItemNaoEncontrado(GlosaError):
    """Lançada quando o guia_item não é encontrado."""


class ValorGlosaExcedeFaturado(GlosaError):
    """Lançada quando o valor da glosa excede o valor faturado."""


class ValorGlosaInvalido(GlosaError):
    """Lançada quando o valor da glosa é menor ou igual a zero."""
