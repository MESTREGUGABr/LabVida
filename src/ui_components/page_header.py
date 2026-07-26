"""Componente de cabecalho de pagina com titulo, subtitulo e badge."""

import re

import streamlit as st

from src.ui_theme import NEUTRAL_500, NEUTRAL_600, PRIMARY_50, PRIMARY_600


def _icone_header(icone: str, tamanho: int = 24) -> str:
    scaled = re.sub(r'width="[^"]*"', f'width="{tamanho}"', icone)
    scaled = re.sub(r'height="[^"]*"', f'height="{tamanho}"', scaled)
    return f'<span style="display:inline-flex;align-items:center;vertical-align:middle;margin-right:10px;color:{PRIMARY_600};">{scaled}</span>'


def renderizar_cabecalho(
    titulo: str,
    subtitulo: str | None = None,
    icone: str | None = None,
    badge: str | None = None,
) -> None:
    prefixo = _icone_header(icone) if icone else ""
    conteudo_titulo = f"{prefixo}{titulo}"

    if badge:
        conteudo_titulo += f"  <span style='font-size:11px;font-weight:600;background:{PRIMARY_50};color:{PRIMARY_600};padding:2px 10px;border-radius:12px;margin-left:12px;vertical-align:middle;'>{badge}</span>"

    st.markdown(
        f"<h1 style='margin-bottom:0;'>{conteudo_titulo}</h1>",
        unsafe_allow_html=True,
    )

    if subtitulo:
        st.markdown(
            f"<p style='color:{NEUTRAL_600};font-size:14px;margin-top:4px;margin-bottom:0;'>{subtitulo}</p>",
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
