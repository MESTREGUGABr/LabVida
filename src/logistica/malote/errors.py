class LogisticaError(Exception):
    """Exceção base para o módulo de logística."""


class MaloteNaoEncontrado(LogisticaError):
    """Lançada quando um malote não é encontrado pelo ID ou código."""


class MaloteFechadoOuInvalido(LogisticaError):
    """Lançada ao tentar modificar um malote que não está em status ABERTO."""


class AmostraInvalidaParaMalote(LogisticaError):
    """Lançada ao tentar adicionar uma amostra inexistente, inativa ou que não está COLETADA."""


class UnidadeOuUsuarioInvalido(LogisticaError):
    """Lançada quando unidade de origem/destino ou usuário enviado for inválido."""
