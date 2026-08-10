"""Componente unico de grid do LabVida (ADR 0008).

Todas as tabelas do sistema passam por aqui. Antes eram 24 chamadas soltas de
`st.dataframe`, cada uma com formatacao propria, mais telas que simulavam tabela
com `st.columns` manual e uma que sobrepunha `<div>` a colunas.

A assinatura e a fronteira estavel: o AgGrid e detalhe de implementacao. Trocar
a engine depois custa este arquivo, nao 24 call sites — por isso a funcao nao
expoe nada do vocabulario do AgGrid (`gridOptions`, `JsCode`, `columnDefs`).

Formatacao pt-BR (moeda, data, numero) e badge de status sao aplicados aqui, uma
vez, em vez de repetidos em cada tela.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

import pandas as pd
import streamlit as st

TipoColuna = Literal["texto", "moeda", "data", "data_hora", "numero", "inteiro", "status", "booleano"]
ModoSelecao = Literal["nenhuma", "linha", "multipla"]

_ALTURA_PADRAO = 420
_PAGINA_PADRAO = 25

# --- formatadores JS, avaliados no browser pelo AgGrid ----------------------
# Ficam aqui e nao nas telas: e o unico ponto que precisa saber que existe JS.
_FMT_MOEDA = """
function(p){
  if (p.value === null || p.value === undefined || p.value === '') return '';
  return 'R$ ' + Number(p.value).toLocaleString('pt-BR',
    {minimumFractionDigits: 2, maximumFractionDigits: 2});
}
"""

_FMT_DATA = """
function(p){
  if (!p.value) return '';
  var d = new Date(p.value);
  if (isNaN(d)) return p.value;
  return d.toLocaleDateString('pt-BR');
}
"""

_FMT_DATA_HORA = """
function(p){
  if (!p.value) return '';
  var d = new Date(p.value);
  if (isNaN(d)) return p.value;
  return d.toLocaleDateString('pt-BR') + ' ' +
         d.toLocaleTimeString('pt-BR', {hour: '2-digit', minute: '2-digit'});
}
"""

_FMT_NUMERO = """
function(p){
  if (p.value === null || p.value === undefined || p.value === '') return '';
  return Number(p.value).toLocaleString('pt-BR',
    {minimumFractionDigits: 2, maximumFractionDigits: 2});
}
"""

_FMT_INTEIRO = """
function(p){
  if (p.value === null || p.value === undefined || p.value === '') return '';
  return Number(p.value).toLocaleString('pt-BR');
}
"""

_FMT_BOOLEANO = """
function(p){ return p.value ? 'Sim' : 'Nao'; }
"""

_FORMATADORES: dict[str, str] = {
    "moeda": _FMT_MOEDA,
    "data": _FMT_DATA,
    "data_hora": _FMT_DATA_HORA,
    "numero": _FMT_NUMERO,
    "inteiro": _FMT_INTEIRO,
    "booleano": _FMT_BOOLEANO,
}

_NUMERICAS = {"moeda", "numero", "inteiro"}
_DATAS = {"data", "data_hora"}


@dataclass(frozen=True)
class ColunaGrid:
    """Descricao de uma coluna, no vocabulario do dominio."""

    campo: str
    rotulo: str
    tipo: TipoColuna = "texto"
    largura: int | None = None
    editavel: bool = False
    oculta: bool = False
    filtravel: bool = True


@dataclass
class ResultadoGrid:
    """O que a tela precisa saber depois de renderizar."""

    selecionados: list[dict[str, Any]] = field(default_factory=list)
    dados: pd.DataFrame = field(default_factory=pd.DataFrame)

    @property
    def selecionado(self) -> dict[str, Any] | None:
        """Primeira linha selecionada — o caso comum de selecao simples."""
        return self.selecionados[0] if self.selecionados else None

    @property
    def houve_selecao(self) -> bool:
        return bool(self.selecionados)


def _para_dataframe(dados: list[dict] | pd.DataFrame, colunas: list[ColunaGrid]) -> pd.DataFrame:
    if isinstance(dados, pd.DataFrame):
        df = dados.copy()
    else:
        df = pd.DataFrame(list(dados))

    if df.empty:
        return pd.DataFrame(columns=[c.campo for c in colunas])

    faltando = [c.campo for c in colunas if c.campo not in df.columns]
    if faltando:
        raise KeyError(f"Colunas ausentes nos dados do grid: {faltando}")

    return df[[c.campo for c in colunas]]


def _normalizar_numericas(df: pd.DataFrame, colunas: list[ColunaGrid]) -> pd.DataFrame:
    """Decimal do SQLAlchemy nao serializa para o AgGrid — vira float aqui."""
    for coluna in colunas:
        if coluna.tipo in _NUMERICAS and coluna.campo in df.columns:
            df[coluna.campo] = pd.to_numeric(df[coluna.campo], errors="coerce")
    return df


def _normalizar_datas(df: pd.DataFrame, colunas: list[ColunaGrid]) -> pd.DataFrame:
    """`date`/`datetime` puro fica com dtype `object` no DataFrame — o
    st_aggrid so converte pra ISO string automaticamente em colunas com dtype
    `datetime64`. Sem isso o valor cru chega ao browser e o `_FMT_DATA`
    (JS) nao consegue parsear, mostrando "[object Object]"."""
    for coluna in colunas:
        if coluna.tipo in _DATAS and coluna.campo in df.columns:
            valores = pd.to_datetime(df[coluna.campo], errors="coerce")
            df[coluna.campo] = valores.apply(
                lambda v: v.isoformat() if pd.notna(v) else None
            )
    return df


def renderizar_grid(
    dados: list[dict] | pd.DataFrame,
    *,
    colunas: list[ColunaGrid],
    chave: str,
    selecao: ModoSelecao = "nenhuma",
    altura: int = _ALTURA_PADRAO,
    paginar: bool = True,
    tamanho_pagina: int = _PAGINA_PADRAO,
    permitir_busca: bool = True,
    mensagem_vazio: str = "Nenhum registro encontrado.",
) -> ResultadoGrid:
    """Renderiza uma tabela e devolve a selecao.

    `chave` precisa ser unica na pagina — e o que mantem o estado do grid entre
    reruns (ordenacao, filtro, pagina atual).
    """
    df = _normalizar_datas(_normalizar_numericas(_para_dataframe(dados, colunas), colunas), colunas)

    if df.empty:
        st.caption(mensagem_vazio)
        return ResultadoGrid(dados=df)

    from st_aggrid import AgGrid, ColumnsAutoSizeMode, GridOptionsBuilder, GridUpdateMode, JsCode

    construtor = GridOptionsBuilder.from_dataframe(df)
    construtor.configure_default_column(
        # `filterable` nao existe mais nesta versao do st_aggrid — vira kwarg
        # morto no defaultColDef e o AgGrid ignora. `filter` e a propriedade
        # real que liga o componente de filtro por coluna.
        filter=permitir_busca,
        floatingFilter=permitir_busca,
        sortable=True,
        resizable=True,
        wrapText=False,
        autoHeight=False,
    )

    for coluna in colunas:
        opcoes: dict[str, Any] = {
            "header_name": coluna.rotulo,
            "editable": coluna.editavel,
            "hide": coluna.oculta,
        }
        if coluna.largura:
            opcoes["width"] = coluna.largura
        if coluna.tipo in _NUMERICAS:
            opcoes["type"] = ["numericColumn", "rightAligned"]
        if coluna.tipo in _FORMATADORES:
            opcoes["valueFormatter"] = JsCode(_FORMATADORES[coluna.tipo])
        if not coluna.filtravel:
            opcoes["filter"] = False
            opcoes["floatingFilter"] = False
        construtor.configure_column(coluna.campo, **opcoes)

    if selecao != "nenhuma":
        construtor.configure_selection(
            "multiple" if selecao == "multipla" else "single",
            use_checkbox=(selecao == "multipla"),
        )

    if paginar:
        construtor.configure_pagination(
            paginationAutoPageSize=False, paginationPageSize=tamanho_pagina
        )

    resposta = AgGrid(
        df,
        gridOptions=construtor.build(),
        height=altura,
        key=chave,
        # allow_unsafe_jscode: os formatadores acima sao JS. Sao literais deste
        # modulo — nada vindo de dado de usuario chega a ser avaliado.
        allow_unsafe_jscode=True,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
        fit_columns_on_grid_load=False,
        enable_enterprise_modules=False,
        theme="streamlit",
    )

    return ResultadoGrid(
        selecionados=_extrair_selecionados(resposta),
        dados=df,
    )


def _extrair_selecionados(resposta: Any) -> list[dict[str, Any]]:
    """A forma de `selected_rows` varia entre versoes do componente.

    Ja veio como lista de dicts e como DataFrame; normalizamos para lista de
    dicts para a tela nao ter que se preocupar com isso.
    """
    linhas = getattr(resposta, "selected_rows", None)
    if linhas is None and isinstance(resposta, dict):
        linhas = resposta.get("selected_rows")

    if linhas is None:
        return []
    if isinstance(linhas, pd.DataFrame):
        return [] if linhas.empty else linhas.to_dict("records")
    if isinstance(linhas, list):
        return [linha for linha in linhas if isinstance(linha, dict)]
    return []
