class OrdemServicoNaoEncontrada(Exception):
    pass


class OsItemNaoEncontrado(Exception):
    pass


class UsuarioNaoAutorizadoParaCancelamento(Exception):
    pass


class ItemNaoPodeSerCancelado(Exception):
    pass


class OrdemServicoNaoPodeSerCancelada(Exception):
    pass


class OrdemSemItens(Exception):
    pass


class ConvenioInvalidoParaOS(Exception):
    pass


class ValorItemNaoDefinido(Exception):
    pass


class ProcedimentoInvalidoParaOS(Exception):
    pass


class PacienteInvalidoParaOS(Exception):
    pass


class MedicoInvalidoParaOS(Exception):
    pass


class UnidadeInvalidaParaOS(Exception):
    pass


class TransicaoOSInvalida(Exception):
    pass
