class OrdemServicoInexistente(Exception):
    pass


class ColetorInvalido(Exception):
    pass


class ColetaNaoPermitida(Exception):
    pass


class EstoqueInsuficienteError(ColetaNaoPermitida):
    pass

