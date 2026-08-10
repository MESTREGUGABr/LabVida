"""Componente unico de grid e tratamento de erro de tela (fase F1).

O grid e a fronteira que isola 24 telas do AgGrid (ADR 0008). Se a normalizacao
de dados ou a leitura da selecao quebrar, quebra em todas de uma vez — por isso
essas partes sao testadas sem depender de browser.
"""

from decimal import Decimal

import pandas as pd
import pytest

from src.ui_components.data_grid import (
    ColunaGrid,
    ResultadoGrid,
    _extrair_selecionados,
    _normalizar_numericas,
    _para_dataframe,
)
from src.ui_components.erros import tratar_erros

_COLUNAS = [
    ColunaGrid("codigo", "Codigo"),
    ColunaGrid("valor", "Valor", tipo="moeda"),
    ColunaGrid("emissao", "Emissao", tipo="data"),
]


def test_projeta_e_ordena_as_colunas_declaradas() -> None:
    """A tela declara a ordem; dado extra na origem nao vaza para a tela."""
    dados = [
        {"emissao": "2026-03-01", "codigo": "A1", "valor": 10, "interno": "nao mostrar"},
    ]

    df = _para_dataframe(dados, _COLUNAS)

    assert list(df.columns) == ["codigo", "valor", "emissao"]
    assert "interno" not in df.columns


def test_coluna_ausente_falha_alto() -> None:
    """Erro de digitacao no nome do campo tem que estourar na hora, com o nome
    do campo — nao virar coluna vazia silenciosa no meio da tela."""
    with pytest.raises(KeyError, match="valor"):
        _para_dataframe([{"codigo": "A1"}], _COLUNAS)


def test_lista_vazia_produz_dataframe_com_as_colunas() -> None:
    df = _para_dataframe([], _COLUNAS)

    assert df.empty
    assert list(df.columns) == ["codigo", "valor", "emissao"]


def test_decimal_vira_numero() -> None:
    """Decimal do SQLAlchemy nao serializa para o AgGrid e chegaria como texto,
    quebrando ordenacao numerica e o formatador de moeda."""
    df = _para_dataframe(
        [{"codigo": "A1", "valor": Decimal("1234.56"), "emissao": "2026-03-01"}], _COLUNAS
    )

    df = _normalizar_numericas(df, _COLUNAS)

    assert df["valor"].iloc[0] == pytest.approx(1234.56)
    assert pd.api.types.is_numeric_dtype(df["valor"])


def test_valor_nao_numerico_vira_nulo_em_vez_de_quebrar() -> None:
    df = _para_dataframe([{"codigo": "A1", "valor": "n/d", "emissao": None}], _COLUNAS)

    df = _normalizar_numericas(df, _COLUNAS)

    assert pd.isna(df["valor"].iloc[0])


class _RespostaFalsa:
    def __init__(self, selected_rows) -> None:
        self.selected_rows = selected_rows


def test_selecao_aceita_lista_de_dicts() -> None:
    resposta = _RespostaFalsa([{"codigo": "A1"}, {"codigo": "A2"}])

    assert _extrair_selecionados(resposta) == [{"codigo": "A1"}, {"codigo": "A2"}]


def test_selecao_aceita_dataframe() -> None:
    """Versoes diferentes do componente devolvem lista ou DataFrame."""
    resposta = _RespostaFalsa(pd.DataFrame([{"codigo": "A1"}]))

    assert _extrair_selecionados(resposta) == [{"codigo": "A1"}]


def test_selecao_vazia_em_qualquer_forma() -> None:
    assert _extrair_selecionados(_RespostaFalsa(None)) == []
    assert _extrair_selecionados(_RespostaFalsa([])) == []
    assert _extrair_selecionados(_RespostaFalsa(pd.DataFrame())) == []


def test_resultado_expoe_primeiro_selecionado() -> None:
    resultado = ResultadoGrid(selecionados=[{"codigo": "A1"}, {"codigo": "A2"}])

    assert resultado.selecionado == {"codigo": "A1"}
    assert resultado.houve_selecao is True
    assert ResultadoGrid().selecionado is None
    assert ResultadoGrid().houve_selecao is False


# --------------------------------------------------------------- tratar_erros


class _ErroDeDominioFalso(Exception):
    pass


_ErroDeDominioFalso.__module__ = "src.faturamento.glosa.errors"


def test_bloco_sem_erro_reporta_sucesso() -> None:
    with tratar_erros("carregar") as resultado:
        valor = 2 + 2

    assert valor == 4
    assert resultado.ok is True
    assert bool(resultado) is True


def test_erro_de_dominio_e_capturado_e_nao_relancado() -> None:
    """A tela continua viva e decide o que fazer com resultado.ok."""
    with tratar_erros("registrar a glosa") as resultado:
        raise _ErroDeDominioFalso("Valor da glosa excede o saldo do item")

    assert resultado.ok is False
    assert isinstance(resultado.erro, _ErroDeDominioFalso)


def test_value_error_conta_como_dominio() -> None:
    """Services do laboratorial levantam ValueError com mensagem para o usuario."""
    with tratar_erros() as resultado:
        raise ValueError("Nem todos os resultados foram revisados")

    assert resultado.ok is False
    assert isinstance(resultado.erro, ValueError)


def test_erro_inesperado_tambem_e_contido() -> None:
    """Sem isso, o usuario via o traceback do Streamlit na tela."""
    with tratar_erros("listar") as resultado:
        raise RuntimeError("falha de biblioteca")

    assert resultado.ok is False
    assert isinstance(resultado.erro, RuntimeError)
