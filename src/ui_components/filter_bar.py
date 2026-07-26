"""Componente de barra de filtros reutilizavel."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import streamlit as st

from src.ui_theme import NEUTRAL_200, NEUTRAL_50, PRIMARY_500, WHITE


@dataclass
class Filtro:
    rotulo: str
    chave: str
    tipo: str = "text"
    opcoes: list[str] | None = None
    valor_padrao: Any = None
    placeholder: str | None = None


def renderizar_barra_filtros(
    filtros: list[Filtro],
    ao_aplicar: callable | None = None,
    ao_limpar: callable | None = None,
) -> dict[str, Any]:
    valores: dict[str, Any] = {}

    st.markdown(
        f"""
        <div style="
            background:{WHITE};
            border:1px solid {NEUTRAL_200};
            border-radius:8px;
            padding:16px 16px 8px 16px;
            margin-bottom:16px;
        ">
        """,
        unsafe_allow_html=True,
    )

    num_colunas = min(len(filtros), 5)
    if num_colunas == 0:
        num_colunas = 1

    colunas = st.columns(num_colunas + 2)

    for i, filtro in enumerate(filtros):
        col_idx = i % num_colunas
        with colunas[col_idx]:
            if filtro.tipo == "select" and filtro.opcoes:
                valor = st.selectbox(
                    filtro.rotulo,
                    options=filtro.opcoes,
                    key=f"filtro_{filtro.chave}",
                    label_visibility="collapsed",
                    placeholder=filtro.placeholder,
                    index=None,
                )
            else:
                valor = st.text_input(
                    filtro.rotulo,
                    key=f"filtro_{filtro.chave}",
                    value=filtro.valor_padrao or "",
                    placeholder=filtro.placeholder or filtro.rotulo,
                    label_visibility="collapsed",
                )
            valores[filtro.chave] = valor

    with colunas[-2]:
        st.button(
            "\U0001f50d Aplicar",
            key="filtro_aplicar",
            type="primary",
            on_click=ao_aplicar,
            use_container_width=True,
        )

    with colunas[-1]:
        st.button(
            "Limpar",
            key="filtro_limpar",
            type="secondary",
            on_click=ao_limpar,
            use_container_width=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    return valores
