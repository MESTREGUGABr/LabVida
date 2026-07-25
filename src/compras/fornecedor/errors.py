class FornecedorError(Exception):
    """Exceção base para fornecedores."""


class FornecedorNaoEncontrado(FornecedorError):
    """Lançada quando um fornecedor não é encontrado."""


class CnpjDuplicado(FornecedorError):
    """Lançada quando o CNPJ já está cadastrado."""


class FornecedorInativo(FornecedorError):
    """Lançada ao tentar usar um fornecedor inativo."""
