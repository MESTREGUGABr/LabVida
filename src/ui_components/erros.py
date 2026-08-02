"""Tratamento uniforme de erro nas telas.

Antes, 18+ paginas chamavam service e repository sem `try/except`: banco fora do
ar ou regra de negocio violada num ponto nao previsto jogavam o traceback do
Streamlit na cara do usuario.

A classificacao nao importa uma lista de excecoes de dominio — seriam ~10
imports e risco de ciclo. Ela olha de ONDE a excecao veio: o que nasce em
`src.*` e erro de dominio e tem mensagem escrita para ser lida; o resto e falha
tecnica e vira mensagem generica, com o detalhe escondido num expander.
"""

from __future__ import annotations

from contextlib import contextmanager
from collections.abc import Iterator

import streamlit as st


class _Resultado:
    """Deixa a tela saber se o bloco passou, sem precisar de flag externa."""

    def __init__(self) -> None:
        self.ok = True
        self.erro: Exception | None = None

    def __bool__(self) -> bool:
        return self.ok


def _e_erro_de_dominio(excecao: Exception) -> bool:
    """Erro nosso, com mensagem destinada ao usuario."""
    if isinstance(excecao, (ValueError, PermissionError)):
        return True
    return type(excecao).__module__.startswith("src.")


def _e_erro_de_banco(excecao: Exception) -> bool:
    modulo = type(excecao).__module__
    return modulo.startswith("sqlalchemy") or modulo.startswith("psycopg")


@contextmanager
def tratar_erros(acao: str = "", *, mostrar_detalhe: bool = True) -> Iterator[_Resultado]:
    """Envolve uma operacao de tela e converte falha em mensagem legivel.

        with tratar_erros("carregar os fornecedores") as resultado:
            fornecedores = listar_fornecedores(session)
        if not resultado:
            return

    Nao relanca: a tela continua e decide o que fazer com `resultado.ok`.
    """
    resultado = _Resultado()
    contexto = f" ao {acao}" if acao else ""

    try:
        yield resultado
    except Exception as excecao:  # noqa: BLE001 - fronteira de UI, e o objetivo
        resultado.ok = False
        resultado.erro = excecao

        if _e_erro_de_dominio(excecao):
            st.error(str(excecao) or f"Operacao nao permitida{contexto}.")
        elif _e_erro_de_banco(excecao):
            st.error(
                f"Nao foi possivel comunicar com o banco de dados{contexto}. "
                "Tente novamente em instantes."
            )
            if mostrar_detalhe:
                with st.expander("Detalhe tecnico"):
                    st.code(f"{type(excecao).__name__}: {excecao}")
        else:
            st.error(f"Ocorreu um erro inesperado{contexto}.")
            if mostrar_detalhe:
                with st.expander("Detalhe tecnico"):
                    st.code(f"{type(excecao).__name__}: {excecao}")
