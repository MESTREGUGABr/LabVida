"""Componente de estado vazio para listas, tabelas e areas sem dados."""

from __future__ import annotations

import streamlit as st

from src.ui_theme import NEUTRAL_300, NEUTRAL_500, NEUTRAL_600, PRIMARY_600


def renderizar_estado_vazio(
    icone: str,
    titulo: str,
    mensagem: str,
    rotulo_acao: str | None = None,
    ao_clicar_acao: callable | None = None,
) -> None:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            f"""
            <div style="text-align:center;padding:56px 24px;">
                <div style="font-size:48px;margin-bottom:20px;opacity:0.3;">{icone}</div>
                <h3 style="color:{NEUTRAL_500};margin-bottom:6px;font-size:16px;">{titulo}</h3>
                <p style="color:{NEUTRAL_600};font-size:13px;margin-bottom:24px;line-height:1.5;">{mensagem}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if rotulo_acao:
            if ao_clicar_acao:
                st.button(
                    rotulo_acao,
                    on_click=ao_clicar_acao,
                    type="primary",
                )
            else:
                st.markdown(
                    f"""
                    <div style="text-align:center;">
                        <span style="
                            display:inline-block;
                            background:{PRIMARY_600};
                            color:white;
                            padding:10px 24px;
                            border-radius:8px;
                            font-size:13px;
                            font-weight:500;
                        ">{rotulo_acao}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
