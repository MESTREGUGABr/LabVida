"""Injecao de CSS global para o tema visual do LabVida."""

import streamlit as st

from src.ui_theme import (
    ACCENT_AMBER,
    ACCENT_BLUE,
    ACCENT_ORANGE,
    ACCENT_ORANGE_HOVER,
    ACCENT_TEAL,
    ACCENT_TEAL_HOVER,
    BG_PAGE,
    BORDER_RADIUS,
    BORDER_RADIUS_SM,
    NEUTRAL_100,
    NEUTRAL_200,
    NEUTRAL_300,
    NEUTRAL_400,
    NEUTRAL_50,
    NEUTRAL_500,
    NEUTRAL_600,
    NEUTRAL_700,
    NEUTRAL_800,
    NEUTRAL_900,
    PRIMARY_500,
    SHADOW_CARD,
    SIDEBAR_ACTIVE_BAR,
    SIDEBAR_ACTIVE_BG,
    SIDEBAR_BG,
    SIDEBAR_GRADIENT_END,
    SIDEBAR_GRADIENT_START,
    SIDEBAR_HOVER_BG,
    SIDEBAR_LABEL,
    SIDEBAR_SEPARATOR,
    SIDEBAR_TEXT,
    SIDEBAR_TEXT_SECONDARY,
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
    WHITE,
)

CSS_GLOBAL = f"""
<style>
/* ===== TYPOGRAPHY GLOBAL ===== */
html, body, div, p, span, a, label,
h1, h2, h3, h4, h5, h6,
input, select, button, textarea,
table, th, td, tr, li, ul, ol,
[data-testid], [data-baseweb] {{
    font-family: "Inter", system-ui, -apple-system, BlinkMacSystemFont,
                 "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
}}

/* ===== RESET & BASE ===== */
.stApp {{
    background-color: {BG_PAGE};
}}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {{
    background-color: {SIDEBAR_BG};
    position: relative;
}}

section[data-testid="stSidebar"]::before {{
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(to right, {SIDEBAR_GRADIENT_START}, {SIDEBAR_GRADIENT_END});
    z-index: 10;
}}

[data-testid="stSidebarNav"],
[data-testid="stSidebarNavContainer"],
[data-testid="stSidebarNavItems"],
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapseButton"] {{
    display: none !important;
}}

section[data-testid="stSidebar"] ul,
section[data-testid="stSidebar"] nav,
section[data-testid="stSidebar"] > div:first-child > div:first-child {{
    display: none !important;
}}

section[data-testid="stSidebar"] > div > div:first-child:has(ul) {{
    display: none !important;
}}

[data-testid="stSidebarCollapseButton"] {{
    display: none !important;
}}

section[data-testid="stSidebar"] > div:first-child {{
    padding-top: 6px;
}}

section[data-testid="stSidebar"] * {{
    color: {SIDEBAR_TEXT};
}}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] h4 {{
    color: {SIDEBAR_TEXT};
    padding-top: 0;
}}

section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] small,
section[data-testid="stSidebar"] span {{
    color: {SIDEBAR_TEXT};
}}

section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{
    color: {SIDEBAR_LABEL};
    font-size: 11px;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    font-weight: 600;
    margin-top: 10px;
    margin-bottom: 2px;
    padding: 0 12px;
}}

section[data-testid="stSidebar"] a[href] {{
    color: {SIDEBAR_TEXT};
    text-decoration: none;
    padding: 9px 12px;
    display: block;
    border-radius: {BORDER_RADIUS_SM};
    transition: all 0.2s ease;
    font-size: 14px;
    font-weight: 500;
    border-left: 3px solid transparent;
    margin: 1px 4px;
}}

section[data-testid="stSidebar"] a[href]:hover {{
    background-color: {SIDEBAR_HOVER_BG};
    color: {ACCENT_ORANGE};
    font-weight: 500;
    border-left: 3px solid {ACCENT_ORANGE};
}}

section[data-testid="stSidebar"] a[href][aria-current="page"] {{
    background-color: {SIDEBAR_ACTIVE_BG};
    color: {ACCENT_ORANGE};
    font-weight: 600;
    border-left: 3px solid {SIDEBAR_ACTIVE_BAR};
}}

section[data-testid="stSidebar"] hr {{
    border-color: {SIDEBAR_SEPARATOR};
    margin: 14px 8px;
    border-width: 0.5px;
    opacity: 0.6;
}}

section[data-testid="stSidebar"] button {{
    background-color: transparent;
    color: {SIDEBAR_TEXT_SECONDARY};
    border: 1px solid {SIDEBAR_SEPARATOR};
    border-radius: {BORDER_RADIUS_SM};
    padding: 8px 16px;
    font-size: 13px;
    cursor: pointer;
    transition: all 0.2s ease;
    font-weight: 500;
    margin: 4px 8px;
}}

section[data-testid="stSidebar"] button:hover {{
    background-color: {SIDEBAR_HOVER_BG};
    border-color: {ACCENT_ORANGE};
    color: {ACCENT_ORANGE};
}}

/* ===== HOME LINK HOVER (custom <a> tag) ===== */
section[data-testid="stSidebar"] a[href="/home"]:hover {{
    background-color: {SIDEBAR_HOVER_BG};
    color: {ACCENT_ORANGE};
    font-weight: 600;
    border-left: 3px solid {ACCENT_ORANGE};
}}

/* ===== HEADERS ===== */
h1 {{
    color: {NEUTRAL_900};
    font-size: 26px;
    font-weight: 700;
    letter-spacing: -0.3px;
    margin-bottom: 4px;
}}

h2 {{
    color: {NEUTRAL_800};
    font-size: 20px;
    font-weight: 600;
    letter-spacing: -0.2px;
}}

h3 {{
    color: {NEUTRAL_800};
    font-size: 16px;
    font-weight: 600;
}}

/* ===== CARDS ===== */
div[data-testid="stVerticalBlockBorderWrapper"] {{
    background-color: {WHITE};
    border: 1px solid {NEUTRAL_200};
    border-radius: {BORDER_RADIUS};
    box-shadow: {SHADOW_CARD};
    padding: 4px;
}}

/* ===== TABLES ===== */
div[data-testid="stTable"] {{
    border-radius: {BORDER_RADIUS};
    overflow: hidden;
    border: 1px solid {NEUTRAL_200};
}}

div[data-testid="stTable"] table {{
    width: 100%;
    border-collapse: collapse;
}}

div[data-testid="stTable"] th {{
    background-color: {NEUTRAL_50};
    color: {NEUTRAL_800};
    font-weight: 600;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    padding: 10px 12px;
    border-bottom: 2px solid {NEUTRAL_200};
}}

div[data-testid="stTable"] td {{
    padding: 10px 12px;
    font-size: 13px;
    color: {NEUTRAL_900};
    border-bottom: 1px solid {NEUTRAL_100};
}}

div[data-testid="stTable"] tr:hover td {{
    background-color: rgba(232, 74, 39, 0.03);
}}

/* ===== METRICS / KPIS ===== */
div[data-testid="stMetric"] {{
    background-color: {WHITE};
    border: 1px solid {NEUTRAL_200};
    border-radius: {BORDER_RADIUS};
    padding: 16px;
    box-shadow: {SHADOW_CARD};
}}

div[data-testid="stMetric"] label {{
    font-size: 12px;
    color: {NEUTRAL_600};
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

div[data-testid="stMetric"] div[data-testid="stMetricValue"] {{
    font-size: 28px;
    font-weight: 700;
    color: {NEUTRAL_900};
}}

/* ===== FORMS ===== */
div[data-testid="stForm"] {{
    background-color: {WHITE};
    border: 1px solid {NEUTRAL_200};
    border-radius: {BORDER_RADIUS};
    padding: 24px;
    box-shadow: {SHADOW_CARD};
}}

div[data-testid="stForm"] button[kind="primary"] {{
    background-color: {ACCENT_ORANGE};
    border: none;
    border-radius: {BORDER_RADIUS_SM};
    padding: 8px 20px;
    font-weight: 500;
    color: {WHITE};
    transition: all 0.15s ease;
}}

div[data-testid="stForm"] button[kind="primary"]:hover {{
    background-color: {ACCENT_ORANGE_HOVER};
    box-shadow: 0 2px 8px rgba(232, 74, 39, 0.3);
}}

/* ===== TABS ===== */
button[data-baseweb="tab"] {{
    font-weight: 500;
    color: {NEUTRAL_600};
    padding: 10px 16px;
}}

button[data-baseweb="tab"][aria-selected="true"] {{
    color: {ACCENT_ORANGE};
    border-bottom-color: {ACCENT_ORANGE};
}}

/* ===== BUTTONS ===== */
button[kind="primary"] {{
    background-color: {ACCENT_ORANGE};
    border: none;
    border-radius: {BORDER_RADIUS_SM};
    padding: 8px 20px;
    font-weight: 500;
    color: {WHITE};
    transition: all 0.15s ease;
}}

button[kind="primary"]:hover {{
    background-color: {ACCENT_ORANGE_HOVER};
    box-shadow: 0 2px 8px rgba(232, 74, 39, 0.3);
}}

button[kind="secondary"] {{
    border: 1px solid {NEUTRAL_300};
    border-radius: {BORDER_RADIUS_SM};
    color: {NEUTRAL_700};
    font-weight: 500;
    transition: all 0.15s ease;
}}

button[kind="secondary"]:hover {{
    border-color: {NEUTRAL_500};
    color: {NEUTRAL_900};
}}

/* ===== INPUTS ===== */
div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input,
div[data-testid="stDateInput"] input,
div[data-testid="stTextArea"] textarea {{
    border: 1.5px solid {NEUTRAL_400} !important;
    border-radius: {BORDER_RADIUS_SM} !important;
    background-color: {WHITE} !important;
    padding: 8px 12px !important;
    font-size: 14px !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}}

div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div,
div[data-baseweb="textarea"] > div {{
    border: 1.5px solid {NEUTRAL_400} !important;
    border-radius: {BORDER_RADIUS_SM} !important;
    background-color: {WHITE} !important;
    box-shadow: none !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}}

div[data-testid="stTextInput"] input:focus,
div[data-testid="stNumberInput"] input:focus,
div[data-testid="stDateInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus,
div[data-baseweb="input"]:focus-within > div,
div[data-baseweb="select"]:focus-within > div,
div[data-baseweb="textarea"]:focus-within > div {{
    border-color: {ACCENT_ORANGE} !important;
    box-shadow: 0 0 0 3px rgba(232, 74, 39, 0.12) !important;
    background-color: {WHITE} !important;
}}

div[data-testid="stTextInput"] input::placeholder,
div[data-testid="stTextArea"] textarea::placeholder {{
    color: {NEUTRAL_400};
}}

div[data-testid="stSelectbox"] [data-baseweb="select"] > div,
div[data-testid="stMultiSelect"] [data-baseweb="select"] > div {{
    border: 1px solid {NEUTRAL_300} !important;
    border-radius: {BORDER_RADIUS_SM} !important;
    background-color: {WHITE} !important;
    box-shadow: none !important;
}}

/* ===== EXPANDERS ===== */
details {{
    background-color: {WHITE};
    border: 1px solid {NEUTRAL_200};
    border-radius: {BORDER_RADIUS};
    box-shadow: {SHADOW_CARD};
}}

/* ===== DIVIDERS ===== */
hr {{
    border-color: {NEUTRAL_200};
    margin: 20px 0;
}}

/* ===== HEADER BAR ===== */
[data-testid="stHeader"] {{
    background-color: transparent;
}}
</style>
"""


def injetar_css_global() -> None:
    st.markdown(CSS_GLOBAL, unsafe_allow_html=True)
