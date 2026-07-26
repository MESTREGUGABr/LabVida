"""Componente de card de KPI (indicador numerico)."""

from __future__ import annotations

import streamlit as st

from src.ui_theme import NEUTRAL_200, NEUTRAL_50, NEUTRAL_600, NEUTRAL_800, SHADOW_CARD, WHITE


def renderizar_kpi_card(
    rotulo: str,
    valor: str,
    delta: str | None = None,
    icone: str | None = None,
    cor_destaque: str | None = None,
) -> None:
    estilo_valor = f"color:{cor_destaque};" if cor_destaque else ""

    delta_html = ""
    if delta:
        delta_cor = "#2E7D32" if not delta.startswith("-") else "#C62828"
        delta_seta = "\u2191" if not delta.startswith("-") else "\u2193"
        delta_html = (
            f"<span style='font-size:12px;color:{delta_cor};margin-left:8px;'>"
            f"{delta_seta} {delta.lstrip('+-')}</span>"
        )

    icone_html = f"<span style='font-size:28px;opacity:0.7;'>{icone}</span>" if icone else ""

    st.markdown(
        f"""
        <div style="
            background:{WHITE};
            border:1px solid {NEUTRAL_200};
            border-radius:8px;
            padding:16px 20px;
            box-shadow:{SHADOW_CARD};
            display:flex;
            flex-direction:column;
            gap:4px;
        ">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                <span style="font-size:12px;color:{NEUTRAL_600};font-weight:500;
                    text-transform:uppercase;letter-spacing:0.5px;">{rotulo}</span>
                {icone_html}
            </div>
            <div style="font-size:28px;font-weight:700;color:{NEUTRAL_800};{estilo_valor}
                line-height:1.2;">
                {valor}{delta_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
