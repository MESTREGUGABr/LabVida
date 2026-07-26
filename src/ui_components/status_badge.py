"""Componente de chip/badge de status com cores por tipo."""

from __future__ import annotations

import streamlit as st

from src.ui_theme import (
    STATUS_ERROR,
    STATUS_ERROR_BG,
    STATUS_INFO,
    STATUS_INFO_BG,
    STATUS_NEUTRAL,
    STATUS_NEUTRAL_BG,
    STATUS_SUCCESS,
    STATUS_SUCCESS_BG,
    STATUS_WARNING,
    STATUS_WARNING_BG,
)

TIPO_CORES: dict[str, tuple[str, str]] = {
    "success": (STATUS_SUCCESS_BG, STATUS_SUCCESS),
    "warning": (STATUS_WARNING_BG, STATUS_WARNING),
    "error": (STATUS_ERROR_BG, STATUS_ERROR),
    "info": (STATUS_INFO_BG, STATUS_INFO),
    "neutral": (STATUS_NEUTRAL_BG, STATUS_NEUTRAL),
}

MAPA_STATUS_POR_DOMINIO: dict[str, str] = {
    "ativo": "success",
    "inativo": "neutral",
    "aberto": "warning",
    "em_andamento": "info",
    "concluido": "success",
    "cancelado": "error",
    "rascunho": "neutral",
    "aprovado": "info",
    "recebido": "success",
    "liberado": "success",
    "pendente": "warning",
    "glosado": "error",
    "pago": "success",
    "vencido": "error",
    "despachado": "info",
    "em_transito": "warning",
    "coletado": "success",
    "triado": "info",
    "assinado": "success",
    "faturado": "success",
    "recusado": "error",
    "encerrado": "neutral",
    "novo": "info",
    "urgente": "error",
    "integridade_ok": "success",
    "avariado": "error",
    "extraviado": "error",
}


def _tipo_para_cores(tipo: str) -> tuple[str, str]:
    return TIPO_CORES.get(tipo, (STATUS_NEUTRAL_BG, STATUS_NEUTRAL))


def renderizar_status_badge(status: str, tipo: str = "neutral") -> None:
    status_normalizado = status.lower().strip()
    if status_normalizado in MAPA_STATUS_POR_DOMINIO:
        tipo = MAPA_STATUS_POR_DOMINIO[status_normalizado]

    bg, cor = _tipo_para_cores(tipo)

    st.markdown(
        f"""
        <span style="
            display:inline-block;
            padding:2px 10px;
            border-radius:12px;
            font-size:12px;
            font-weight:600;
            background:{bg};
            color:{cor};
            white-space:nowrap;
            line-height:1.6;
        ">{status}</span>
        """,
        unsafe_allow_html=True,
    )
