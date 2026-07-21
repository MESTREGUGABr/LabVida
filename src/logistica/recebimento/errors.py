from src.logistica.malote.errors import LogisticaError


class MaloteJaRecebido(LogisticaError):
    """Lançada ao tentar receber um malote que já foi recebido."""


class MaloteNaoEstaEmTransito(LogisticaError):
    """Lançada ao tentar receber um malote que não está com status EM_TRANSITO."""


class UsuarioRecebedorInvalido(LogisticaError):
    """Lançada quando o usuário recebedor for inexistente ou inativo."""
