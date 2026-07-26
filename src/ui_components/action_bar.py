"""Componente de barra de acoes (botoes primario, secundario, danger)."""

from __future__ import annotations

from dataclasses import dataclass

import streamlit as st

from src.ui_theme import NEUTRAL_700, PRIMARY_500, STATUS_ERROR


@dataclass
class Acao:
    rotulo: str
    tipo: str = "secondary"
    ao_clicar: callable | None = None
    desabilitado: bool = False
    icone: str | None = None
    chave: str | None = None


def renderizar_barra_acoes(acoes: list[Acao]) -> None:
    """Renderiza uma barra de botoes de acao em linha.

    acoes: lista de Acao com rotulo, tipo ('primary', 'secondary', 'danger'),
           ao_clicar, desabilitado, icone e chave.
    """
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<hr style='margin:0 0 12px 0;'>", unsafe_allow_html=True)

    num_acoes = len(acoes)
    colunas = st.columns(num_acoes) if num_acoes > 0 else []

    for i, acao in enumerate(acoes):
        with colunas[i]:
            rotulo_final = f"{acao.icone} {acao.rotulo}" if acao.icone else acao.rotulo

            if acao.tipo == "primary":
                tipo_botao = "primary"
            elif acao.tipo == "danger":
                tipo_botao = "secondary"
            else:
                tipo_botao = "secondary"

            chave = acao.chave or f"acao_{acao.rotulo}_{i}"

            st.button(
                rotulo_final,
                key=chave,
                type=tipo_botao,
                disabled=acao.desabilitado,
                on_click=acao.ao_clicar,
                use_container_width=True,
            )
