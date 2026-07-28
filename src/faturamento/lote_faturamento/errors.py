class FaturamentoError(Exception):
    """Exceção base para o módulo de faturamento."""


class LoteNaoEncontrado(FaturamentoError):
    """Lançada quando um lote de faturamento não é encontrado."""


class GuiaNaoEncontrada(FaturamentoError):
    """Lançada quando uma guia TISS não é encontrada."""


class LaudoJaFaturado(FaturamentoError):
    """Lançada ao tentar faturar um laudo que já possui guia_item."""


class LaudoNaoLiberado(FaturamentoError):
    """Lançada ao tentar faturar um laudo com status diferente de LIBERADO."""


class LoteJaFechado(FaturamentoError):
    """Lançada ao tentar modificar um lote que não está ABERTO."""


class LoteSemItens(FaturamentoError):
    """Lançada ao tentar fechar um lote sem guias ou itens."""


class ConvenioInvalidoParaLote(FaturamentoError):
    """Lançada quando o convênio informado não está ativo ou não existe."""


class ConvenioNaoConfereComLaudo(FaturamentoError):
    """Lançada quando o convênio do laudo não confere com o convênio do lote."""


class ValorFaturadoInvalido(FaturamentoError):
    """Lançada quando o valor faturado é menor ou igual a zero."""


class LoteReprovadoPreAuditoria(FaturamentoError):
    """Lançada quando o lote não passa na pré-auditoria antes do fechamento."""
