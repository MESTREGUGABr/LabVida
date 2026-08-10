class UsuarioNaoEncontrado(Exception):
    pass


class CredenciaisInvalidas(Exception):
    """E-mail ou senha incorretos, conta sem senha, ou conta inativa.

    Deliberadamente uma única exceção para os quatro casos — nunca dar pistas
    diferentes ao chamador sobre qual foi o motivo (evita enumeração de contas).
    """


class SenhaFraca(Exception):
    pass


class EmailJaCadastrado(Exception):
    pass


class EmailInvalido(Exception):
    pass
