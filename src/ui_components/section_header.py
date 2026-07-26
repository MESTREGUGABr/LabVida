"""Componente de cabecalho de secao com titulo, descricao e acoes."""

from __future__ import annotations

import streamlit as st

from src.ui_theme import NEUTRAL_200, NEUTRAL_600, NEUTRAL_800


def renderizar_secao(
    titulo: str,
    descricao: str | None = None,
    rotulo_acao: str | None = None,
    ao_clicar_acao: callable | None = None,
    chave_acao: str | None = None,
) -> None:
    col_esq, col_dir = st.columns([3, 1])

    with col_esq:
        st.markdown(
            f"<h3 style='margin-bottom:0;color:{NEUTRAL_800};'>{titulo}</h3>",
            unsafe_allow_html=True,
        )
        if descricao:
            st.markdown(
                f"<p style='color:{NEUTRAL_600};font-size:13px;margin-top:2px;'>{descricao}</p>",
                unsafe_allow_html=True,
            )

    with col_dir:
        if rotulo_acao:
            chave = chave_acao or f"secao_acao_{titulo}"
            btn = st.button(
                rotulo_acao,
                key=chave,
                type="primary",
                on_click=ao_clicar_acao,
            )

    st.markdown(f"<hr style='border-color:{NEUTRAL_200};margin-top:8px;'>", unsafe_allow_html=True)
