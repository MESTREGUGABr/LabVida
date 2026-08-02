"""Specs Altair reutilizaveis do BI.

As paginas nao montam grafico na mao: pedem uma spec daqui. Assim os 4
dashboards compartilham paleta, tooltip em pt-BR e formatacao de eixo, em vez de
cada `st.bar_chart` decidir sozinho — que era o estado anterior (10 graficos sem
tooltip, sem escala de cor e sem formatacao brasileira).

Sobre formatacao monetaria: o eixo usa notacao compacta (`20k`), que le igual em
qualquer locale, e o TOOLTIP traz o valor por extenso ja formatado em pt-BR por
`formatar_brl`. Depender do locale do Vega para o separador decimal seria fragil.
"""

from typing import Literal

import altair as alt
import pandas as pd

from src.ui import formatar_brl

# Paleta categorica de 8 tons — suficiente para convenios, setores e unidades.
PALETA = [
    "#2563eb", "#0891b2", "#7c3aed", "#db2777",
    "#ea580c", "#65a30d", "#0d9488", "#4f46e5",
]
COR_POSITIVA = "#16a34a"
COR_NEGATIVA = "#dc2626"
COR_NEUTRA = "#2563eb"
COR_ALERTA = "#ea580c"

_ALTURA_PADRAO = 300


def _tema(grafico: alt.Chart) -> alt.Chart:
    """Configuracao comum. Nao fixa cor de texto: quebraria o modo escuro."""
    return (
        grafico.configure_view(strokeWidth=0)
        .configure_axis(grid=True, gridOpacity=0.15, labelFontSize=11, titleFontSize=11)
        .configure_legend(labelFontSize=11, titleFontSize=11, orient="bottom")
    )


def _coluna_formatada(dados: pd.DataFrame, campo: str, formato: str) -> tuple[pd.DataFrame, str]:
    """Cria a coluna de tooltip ja formatada em pt-BR."""
    copia = dados.copy()
    rotulo = f"_{campo}_fmt"
    if formato == "moeda":
        copia[rotulo] = copia[campo].astype(float).map(formatar_brl)
    elif formato == "horas":
        copia[rotulo] = copia[campo].astype(float).map(lambda v: f"{v:.1f} h".replace(".", ","))
    elif formato == "percentual":
        copia[rotulo] = copia[campo].astype(float).map(lambda v: f"{v:.1f}%".replace(".", ","))
    else:
        copia[rotulo] = copia[campo].map(lambda v: f"{int(v):,}".replace(",", "."))
    return copia, rotulo


def _eixo_quantitativo(campo: str, titulo: str, formato: str) -> alt.Y:
    especificador = "~s" if formato == "moeda" else ",.0f"
    return alt.Y(f"{campo}:Q", title=titulo, axis=alt.Axis(format=especificador))


def barra_categorica(
    dados: pd.DataFrame,
    *,
    categoria: str,
    valor: str,
    titulo: str = "",
    rotulo_categoria: str = "",
    rotulo_valor: str = "",
    formato: Literal["moeda", "quantidade", "horas", "percentual"] = "quantidade",
    horizontal: bool = True,
    cor_unica: str | None = None,
    altura: int = _ALTURA_PADRAO,
    selecao: str | None = None,
) -> alt.Chart:
    """Ranking por categoria. Horizontal por padrao: nome de convenio nao cabe
    em rotulo de eixo X vertical sem virar diagonal ilegivel."""
    dados, fmt = _coluna_formatada(dados, valor, formato)
    rotulo_categoria = rotulo_categoria or categoria.replace("_", " ").capitalize()
    rotulo_valor = rotulo_valor or valor.replace("_", " ").capitalize()

    quantitativo = _eixo_quantitativo(valor, rotulo_valor, formato)
    nominal = alt.Y(f"{categoria}:N", title=rotulo_categoria, sort="-x") if horizontal else alt.X(
        f"{categoria}:N", title=rotulo_categoria, sort="-y"
    )

    codificacao = (
        {"x": quantitativo, "y": nominal} if horizontal else {"x": nominal, "y": quantitativo}
    )

    if cor_unica:
        cor = alt.value(cor_unica)
    else:
        cor = alt.Color(f"{categoria}:N", scale=alt.Scale(range=PALETA), legend=None)

    grafico = (
        alt.Chart(dados)
        .mark_bar(cornerRadius=3)
        .encode(
            **codificacao,
            color=cor,
            tooltip=[
                alt.Tooltip(f"{categoria}:N", title=rotulo_categoria),
                alt.Tooltip(f"{fmt}:N", title=rotulo_valor),
            ],
        )
        .properties(height=altura, title=titulo)
    )

    if selecao:
        grafico = grafico.add_params(alt.selection_point(fields=[categoria], name=selecao))

    return _tema(grafico)


def linha_temporal(
    dados: pd.DataFrame,
    *,
    tempo: str,
    valor: str,
    titulo: str = "",
    rotulo_valor: str = "",
    formato: Literal["moeda", "quantidade", "horas", "percentual"] = "quantidade",
    cor: str = COR_NEUTRA,
    altura: int = _ALTURA_PADRAO,
) -> alt.Chart:
    """Serie temporal com area. Com o calendario denso, mes sem movimento
    aparece como zero em vez de sumir do eixo."""
    dados, fmt = _coluna_formatada(dados, valor, formato)
    rotulo_valor = rotulo_valor or valor.replace("_", " ").capitalize()

    base = alt.Chart(dados).encode(
        x=alt.X(f"{tempo}:N", title="Periodo", axis=alt.Axis(labelAngle=-45)),
        y=_eixo_quantitativo(valor, rotulo_valor, formato),
        tooltip=[
            alt.Tooltip(f"{tempo}:N", title="Periodo"),
            alt.Tooltip(f"{fmt}:N", title=rotulo_valor),
        ],
    )

    area = base.mark_area(opacity=0.18, color=cor)
    linha = base.mark_line(color=cor, strokeWidth=2.5, point=alt.OverlayMarkDef(size=55, color=cor))

    return _tema((area + linha).properties(height=altura, title=titulo))


def series_comparadas(
    dados: pd.DataFrame,
    *,
    tempo: str,
    series: list[str],
    titulo: str = "",
    rotulo_valor: str = "Valor",
    formato: Literal["moeda", "quantidade"] = "moeda",
    cores: list[str] | None = None,
    altura: int = _ALTURA_PADRAO,
) -> alt.Chart:
    """Duas ou mais series no mesmo eixo — previsto x realizado, entrada x saida."""
    longo = dados.melt(id_vars=[tempo], value_vars=series, var_name="serie", value_name="valor")
    longo["valor"] = longo["valor"].astype(float)
    longo["_valor_fmt"] = (
        longo["valor"].map(formatar_brl) if formato == "moeda"
        else longo["valor"].map(lambda v: f"{int(v):,}".replace(",", "."))
    )
    longo["serie"] = longo["serie"].str.replace("_", " ").str.capitalize()

    grafico = (
        alt.Chart(longo)
        .mark_bar(cornerRadius=2)
        .encode(
            x=alt.X(f"{tempo}:N", title="Periodo", axis=alt.Axis(labelAngle=-45)),
            y=_eixo_quantitativo("valor", rotulo_valor, formato),
            color=alt.Color(
                "serie:N",
                title="",
                scale=alt.Scale(range=cores or PALETA),
            ),
            xOffset="serie:N",
            tooltip=[
                alt.Tooltip(f"{tempo}:N", title="Periodo"),
                alt.Tooltip("serie:N", title="Serie"),
                alt.Tooltip("_valor_fmt:N", title=rotulo_valor),
            ],
        )
        .properties(height=altura, title=titulo)
    )
    return _tema(grafico)


def donut(
    dados: pd.DataFrame,
    *,
    categoria: str,
    valor: str,
    titulo: str = "",
    formato: Literal["moeda", "quantidade"] = "quantidade",
    altura: int = _ALTURA_PADRAO,
) -> alt.Chart:
    dados, fmt = _coluna_formatada(dados, valor, formato)
    grafico = (
        alt.Chart(dados)
        .mark_arc(innerRadius=60, cornerRadius=3)
        .encode(
            theta=alt.Theta(f"{valor}:Q", stack=True),
            color=alt.Color(f"{categoria}:N", title="", scale=alt.Scale(range=PALETA)),
            tooltip=[
                alt.Tooltip(f"{categoria}:N", title=categoria.capitalize()),
                alt.Tooltip(f"{fmt}:N", title=valor.capitalize()),
            ],
        )
        .properties(height=altura, title=titulo)
    )
    return _tema(grafico)


def heatmap_sazonalidade(
    dados: pd.DataFrame,
    *,
    dia_semana: str,
    valor: str,
    titulo: str = "",
    altura: int = 140,
) -> alt.Chart:
    """Sazonalidade semanal — `dia_semana` existia na dimensao e nunca foi usado."""
    dados, fmt = _coluna_formatada(dados, valor, "quantidade")
    grafico = (
        alt.Chart(dados)
        .mark_rect(cornerRadius=3)
        .encode(
            x=alt.X(f"{dia_semana}:N", title="", sort=None),
            color=alt.Color(
                f"{valor}:Q",
                title="Exames",
                scale=alt.Scale(scheme="blues"),
                legend=alt.Legend(orient="right"),
            ),
            tooltip=[
                alt.Tooltip(f"{dia_semana}:N", title="Dia"),
                alt.Tooltip(f"{fmt}:N", title="Exames"),
            ],
        )
        .properties(height=altura, title=titulo)
    )
    return _tema(grafico)


def barras_dre(dados: pd.DataFrame, *, titulo: str = "", altura: int = 240) -> alt.Chart:
    """DRE gerencial: positivo para cima, negativo para baixo, resultado em azul."""
    copia = dados.copy()
    copia["valor"] = copia["valor"].astype(float)
    copia["_valor_fmt"] = copia["valor"].map(formatar_brl)

    grafico = (
        alt.Chart(copia)
        .mark_bar(cornerRadius=3)
        .encode(
            x=alt.X("linha:N", title="", sort=None, axis=alt.Axis(labelAngle=0)),
            y=alt.Y("valor:Q", title="Valor (R$)", axis=alt.Axis(format="~s")),
            color=alt.Color(
                "tipo:N",
                title="",
                scale=alt.Scale(
                    domain=["positivo", "negativo", "resultado"],
                    range=[COR_POSITIVA, COR_NEGATIVA, COR_NEUTRA],
                ),
                legend=None,
            ),
            tooltip=[
                alt.Tooltip("linha:N", title="Linha"),
                alt.Tooltip("_valor_fmt:N", title="Valor"),
            ],
        )
        .properties(height=altura, title=titulo)
    )
    return _tema(grafico)


def curva_abc(dados: pd.DataFrame, *, titulo: str = "", altura: int = 320) -> alt.Chart:
    """Barras de receita + linha de participacao acumulada (Pareto)."""
    copia = dados.copy()
    copia["faturado"] = copia["faturado"].astype(float)
    copia["_faturado_fmt"] = copia["faturado"].map(formatar_brl)
    copia["_acumulado_fmt"] = copia["acumulado"].map(lambda v: f"{v:.1f}%".replace(".", ","))
    ordem = copia["procedimento"].tolist()

    barras = (
        alt.Chart(copia)
        .mark_bar(cornerRadius=2, color=COR_NEUTRA)
        .encode(
            x=alt.X("procedimento:N", title="", sort=ordem, axis=alt.Axis(labelAngle=-45)),
            y=alt.Y("faturado:Q", title="Receita (R$)", axis=alt.Axis(format="~s")),
            tooltip=[
                alt.Tooltip("procedimento:N", title="Procedimento"),
                alt.Tooltip("_faturado_fmt:N", title="Receita"),
                alt.Tooltip("classe:N", title="Classe"),
            ],
        )
    )

    linha = (
        alt.Chart(copia)
        .mark_line(color=COR_ALERTA, strokeWidth=2.5, point=True)
        .encode(
            x=alt.X("procedimento:N", sort=ordem),
            y=alt.Y("acumulado:Q", title="Acumulado (%)", scale=alt.Scale(domain=[0, 100])),
            tooltip=[
                alt.Tooltip("procedimento:N", title="Procedimento"),
                alt.Tooltip("_acumulado_fmt:N", title="Acumulado"),
            ],
        )
    )

    combinado = alt.layer(barras, linha).resolve_scale(y="independent")
    return _tema(combinado.properties(height=altura, title=titulo))
