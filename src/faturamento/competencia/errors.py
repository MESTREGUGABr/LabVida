class CompetenciaError(Exception):
    """Excecao base do modulo de competencia."""


class CompetenciaNaoEncontrada(CompetenciaError):
    pass


class CompetenciaFechada(CompetenciaError):
    """Tentativa de lancar em competencia ja fechada."""


class CompetenciaJaFechada(CompetenciaError):
    pass


class CompetenciaAnteriorAberta(CompetenciaError):
    """Nao se fecha marco com fevereiro aberto."""


class JustificativaObrigatoria(CompetenciaError):
    pass
