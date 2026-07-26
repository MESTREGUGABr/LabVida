"""Componente de card de KPI (indicador numerico)."""

from __future__ import annotations

import streamlit as st

from src.ui_theme import BORDER_RADIUS, NEUTRAL_200, NEUTRAL_600, NEUTRAL_800, SHADOW_CARD, WHITE


def renderizar_kpi_card(
    rotulo: str,
    valor: str,
    delta: str | None = None,
    icone: str | None = None,
    cor_destaque: str | None = None,
) -> None:
    estilo_valor = f"color:{cor_destaque};" if cor_destaque else ""
    estilo_icone = f"color:{cor_destaque};" if cor_destaque else "color:#90A4AE;"

    delta_html = ""
    if delta:
        delta_cor = "#00897B" if not delta.startswith("-") else "#C62828"
        delta_seta = "\u2191" if not delta.startswith("-") else "\u2193"
        delta_html = (
            f"<span style='font-size:12px;color:{delta_cor};margin-left:10px;font-weight:600;'>"
            f"{delta_seta} {delta.lstrip('+-')}</span>"
        )

    icone_html = ""
    if icone:
        icone_html = (
            f"<span style='font-size:24px;opacity:0.85;{estilo_icone}'>{icone}</span>"
        )

    st.markdown(
        f"""
        <div style="
            background:{WHITE};
            border:1px solid {NEUTRAL_200};
            border-radius:{BORDER_RADIUS};
            padding:20px 24px;
            box-shadow:{SHADOW_CARD};
            display:flex;
            flex-direction:column;
            gap:6px;
        ">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <span style="font-size:11px;color:{NEUTRAL_600};font-weight:600;
                    text-transform:uppercase;letter-spacing:0.6px;">{rotulo}</span>
                {icone_html}
            </div>
            <div style="font-size:32px;font-weight:700;color:{NEUTRAL_800};{estilo_valor}
                line-height:1.15;">
                {valor}{delta_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
