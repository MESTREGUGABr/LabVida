"""Injecao de CSS global para o tema visual do LabVida — paleta saude."""
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
    PRIMARY_50,
    PRIMARY_100,
    PRIMARY_300,
    PRIMARY_400,
    PRIMARY_500,
    PRIMARY_600,
    PRIMARY_700,
    PRIMARY_800,
    PRIMARY_900,
    SHADOW_CARD,
    SHADOW_ELEVATED,
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
/* ===== CSS CUSTOM PROPERTIES (DARK MODE BASE) ===== */
:root {{
    --lv-primary: {PRIMARY_600};
    --lv-primary-hover: {PRIMARY_700};
    --lv-primary-light: {PRIMARY_50};
    --lv-accent-teal: {ACCENT_TEAL};
    --lv-accent-orange: {ACCENT_ORANGE};
    --lv-bg-page: {BG_PAGE};
    --lv-bg-card: {WHITE};
    --lv-text-primary: {NEUTRAL_900};
    --lv-text-secondary: {NEUTRAL_600};
    --lv-text-muted: {NEUTRAL_500};
    --lv-border: {NEUTRAL_200};
    --lv-border-light: {NEUTRAL_100};
    --lv-shadow-card: {SHADOW_CARD};
    --lv-sidebar-bg: {SIDEBAR_BG};
    --lv-sidebar-text: {SIDEBAR_TEXT};
    --lv-sidebar-text-secondary: {SIDEBAR_TEXT_SECONDARY};
    --lv-sidebar-hover: {SIDEBAR_HOVER_BG};
    --lv-sidebar-active: {SIDEBAR_ACTIVE_BG};
    --lv-sidebar-separator: {SIDEBAR_SEPARATOR};
    --lv-sidebar-active-bar: {SIDEBAR_ACTIVE_BAR};
    --lv-focus-ring: rgba(21, 101, 192, 0.15);
}}

/* ===== TYPOGRAPHY GLOBAL ===== */
html, body, div, p, span, a, label,
h1, h2, h3, h4, h5, h6,
input, select, button, textarea,
table, th, td, tr, li, ul, ol {{
    font-family: "Inter", system-ui, -apple-system, BlinkMacSystemFont,
                 "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
}}

[data-testid="stExpander"] * {{
    font-family: unset;
}}

/* A regra global de tipografia acima sobrescreve a fonte de icone
   (Material Symbols Rounded, ja auto-hospedada pelo Streamlit — nao e
   dependencia de rede) que o proprio Streamlit aplica via CSS-in-JS sem
   `!important` em varios componentes nativos. Sem essa excecao, o
   navegador cai no fallback de ligature e mostra o nome cru do icone
   ("visibility", "keyboard_double_arrow_left" etc.) em vez do glifo.
   `stTextInputIcon` e o botao de mostrar/ocultar senha; `stIconMaterial` e
   o testid generico que cobre praticamente todo o resto (colapsar sidebar,
   dataframe, paginacao, menu, feedback, file uploader...). */
[data-testid="stTextInputIcon"],
[data-testid="stIconMaterial"] {{
    font-family: "Material Symbols Rounded" !important;
}}

/* ===== RESET & BASE ===== */
.stApp {{
    background-color: var(--lv-bg-page);
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

/* O menu lateral e desenhado a mao em src/ui.py (HTML/CSS + SVG) em vez de
   `st.navigation` — os icones nativos (`:material/...:`) sao ligature de
   fonte e ficam sensiveis a conflito de CSS (ver acima). A navegacao
   automatica do Streamlit fica desligada do lado do servidor via
   `client.showSidebarNavigation = false` em `.streamlit/config.toml`, nao
   por CSS — o servidor nunca manda esse elemento, entao nao ha nada pra
   esconder aqui nem pra "piscar" antes de ser escondido. */

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
    font-size: 10px;
    letter-spacing: 1.0px;
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
    font-size: 13px;
    font-weight: 500;
    border-left: 3px solid transparent;
    margin: 1px 8px;
}}

section[data-testid="stSidebar"] a[href]:hover {{
    background-color: {SIDEBAR_HOVER_BG};
    color: {PRIMARY_300};
    font-weight: 500;
    border-left: 3px solid {PRIMARY_300};
}}

section[data-testid="stSidebar"] a[href][aria-current="page"] {{
    background-color: {SIDEBAR_ACTIVE_BG};
    color: {PRIMARY_300};
    font-weight: 600;
    border-left: 3px solid {SIDEBAR_ACTIVE_BAR};
}}

section[data-testid="stSidebar"] hr {{
    border-color: {SIDEBAR_SEPARATOR};
    margin: 14px 12px;
    border-width: 0.5px;
    opacity: 0.5;
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
    border-color: {PRIMARY_300};
    color: {PRIMARY_300};
}}

/* ===== HOME LINK HOVER ===== */
section[data-testid="stSidebar"] a[href="/home"]:hover {{
    background-color: {SIDEBAR_HOVER_BG};
    color: {PRIMARY_300};
    font-weight: 600;
    border-left: 3px solid {PRIMARY_300};
}}

/* ===== HEADERS ===== */
h1 {{
    color: {NEUTRAL_900};
    font-size: 28px;
    font-weight: 700;
    letter-spacing: -0.4px;
    margin-bottom: 4px;
}}

h2 {{
    color: {NEUTRAL_800};
    font-size: 22px;
    font-weight: 600;
    letter-spacing: -0.3px;
}}

h3 {{
    color: {NEUTRAL_800};
    font-size: 18px;
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
    color: {NEUTRAL_700};
    font-weight: 600;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    padding: 10px 14px;
    border-bottom: 2px solid {NEUTRAL_200};
}}

div[data-testid="stTable"] td {{
    padding: 10px 14px;
    font-size: 13px;
    color: {NEUTRAL_900};
    border-bottom: 1px solid {NEUTRAL_100};
}}

div[data-testid="stTable"] tr:hover td {{
    background-color: rgba(21, 101, 192, 0.03);
}}

/* ===== METRICS / KPIS ===== */
div[data-testid="stMetric"] {{
    background-color: {WHITE};
    border: 1px solid {NEUTRAL_200};
    border-radius: {BORDER_RADIUS};
    padding: 20px;
    box-shadow: {SHADOW_CARD};
    /* Habilita `cqw` no valor/rotulo abaixo: a fonte passa a reagir a
    largura real do card (definida pelo numero de st.columns), nao a
    largura da janela — um vw fixo nao diferencia 4 de 5 colunas. */
    container-type: inline-size;
}}

div[data-testid="stMetric"] label {{
    font-size: 11px;
    color: {NEUTRAL_600};
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.6px;
}}

/* Rotulo pode ser longo (ex: "TAT medio (coleta -> laudo)") — quebra em vez
de cortar com reticencia, que e o padrao do Streamlit. O Streamlit aplica o
truncamento via CSS-in-JS (sem `!important`) num elemento interno, entao a
sobrescrita so vence com `!important` e mirando `*` dentro do container. */
div[data-testid="stMetricLabel"],
div[data-testid="stMetricLabel"] * {{
    white-space: normal !important;
    overflow-wrap: break-word !important;
    overflow: visible !important;
    text-overflow: clip !important;
}}

div[data-testid="stMetric"] div[data-testid="stMetricValue"],
div[data-testid="stMetric"] div[data-testid="stMetricValue"] * {{
    /* `cqw` responsivo pela largura do card: encolhe pra caber sem cortar.
    Nao existe "shrink-to-fit" so por CSS que reaja ao COMPRIMENTO do texto
    (ex: "R$ 9.096,74" vs "R$ 1.234.567,89") sem JS — por isso a rede de
    seguranca abaixo permite quebrar em 2 linhas em vez de vazar pra fora
    do card quando o numero for grande demais mesmo na fonte minima. */
    font-size: clamp(16px, 11cqw, 32px) !important;
    font-weight: 700;
    color: {NEUTRAL_900};
    overflow: visible !important;
    text-overflow: clip !important;
    white-space: normal !important;
    overflow-wrap: break-word !important;
    line-height: 1.15;
    max-width: none !important;
}}

/* ===== FORMS ===== */
div[data-testid="stForm"] {{
    background-color: {WHITE};
    border: 1px solid {NEUTRAL_200};
    border-radius: {BORDER_RADIUS};
    padding: 28px;
    box-shadow: {SHADOW_CARD};
}}

div[data-testid="stForm"] button[kind="primary"] {{
    background-color: {PRIMARY_600};
    border: none;
    border-radius: {BORDER_RADIUS_SM};
    padding: 10px 24px;
    font-weight: 500;
    color: {WHITE};
    transition: all 0.15s ease;
    min-height: 40px;
}}

div[data-testid="stForm"] button[kind="primary"]:hover {{
    background-color: {PRIMARY_700};
    box-shadow: 0 2px 8px rgba(21, 101, 192, 0.3);
}}

/* ===== TABS ===== */
button[data-baseweb="tab"] {{
    font-weight: 500;
    color: {NEUTRAL_600};
    padding: 10px 18px;
    font-size: 13px;
}}

button[data-baseweb="tab"][aria-selected="true"] {{
    color: {PRIMARY_600};
    border-bottom-color: {PRIMARY_600};
}}

/* ===== BUTTONS ===== */
button[kind="primary"] {{
    background-color: {PRIMARY_600};
    border: none;
    border-radius: {BORDER_RADIUS_SM};
    padding: 10px 24px;
    font-weight: 500;
    color: {WHITE};
    transition: all 0.15s ease;
    min-height: 40px;
}}

button[kind="primary"]:hover {{
    background-color: {PRIMARY_700};
    box-shadow: 0 2px 8px rgba(21, 101, 192, 0.3);
}}

button[kind="secondary"] {{
    border: 1px solid {NEUTRAL_300};
    border-radius: {BORDER_RADIUS_SM};
    color: {NEUTRAL_700};
    font-weight: 500;
    transition: all 0.15s ease;
    min-height: 40px;
}}

button[kind="secondary"]:hover {{
    border-color: {NEUTRAL_400};
    color: {NEUTRAL_900};
    background-color: {NEUTRAL_50};
}}

/* ===== INPUTS ===== */
div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input,
div[data-testid="stDateInput"] input,
div[data-testid="stTextArea"] textarea {{
    border: 1.5px solid {NEUTRAL_300} !important;
    border-radius: {BORDER_RADIUS_SM} !important;
    background-color: {WHITE} !important;
    padding: 10px 14px !important;
    font-size: 14px !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}}

div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div,
div[data-baseweb="textarea"] > div {{
    border: 1.5px solid {NEUTRAL_300} !important;
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
    border-color: {PRIMARY_500} !important;
    box-shadow: 0 0 0 3px var(--lv-focus-ring) !important;
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

/* ===== DIVIDERS ===== */
hr {{
    border-color: {NEUTRAL_200};
    margin: 24px 0;
}}

/* ===== HEADER BAR ===== */
[data-testid="stHeader"] {{
    background-color: transparent;
}}

/* ===== SCROLLBAR (SIDEBAR) ===== */
section[data-testid="stSidebar"] ::-webkit-scrollbar {{
    width: 4px;
}}
section[data-testid="stSidebar"] ::-webkit-scrollbar-track {{
    background: transparent;
}}
section[data-testid="stSidebar"] ::-webkit-scrollbar-thumb {{
    background: {SIDEBAR_SEPARATOR};
    border-radius: 4px;
}}

/* ===== TOAST / NOTIFICATIONS ===== */
div[data-testid="stToast"] {{
    border-radius: {BORDER_RADIUS_SM};
    font-size: 13px;
}}

/* ===== DATAFRAME / ST.COLUMN_CONFIG ===== */
div[data-testid="stDataFrame"] {{
    border-radius: {BORDER_RADIUS};
    border: 1px solid {NEUTRAL_200};
    overflow: hidden;
}}

/* ===== RESPONSIVE: MOBILE ===== */
@media (max-width: 768px) {{
    h1 {{ font-size: 22px; }}
    h2 {{ font-size: 18px; }}
    h3 {{ font-size: 16px; }}
    div[data-testid="stForm"] {{ padding: 20px; }}
    button[kind="primary"],
    button[kind="secondary"] {{
        padding: 8px 16px;
        min-height: 36px;
    }}
}}

/* ===== DARK MODE ===== */
[data-theme="dark"] .stApp {{
    background-color: #0F172A;
}}

[data-theme="dark"] h1,
[data-theme="dark"] h2,
[data-theme="dark"] h3,
[data-theme="dark"] h4 {{
    color: #E2E8F0 !important;
}}

[data-theme="dark"] p,
[data-theme="dark"] span,
[data-theme="dark"] label,
[data-theme="dark"] div {{
    color: #CBD5E1;
}}

[data-theme="dark"] div[data-testid="stVerticalBlockBorderWrapper"] {{
    background-color: #1E293B;
    border-color: #334155;
}}

[data-theme="dark"] div[data-testid="stForm"] {{
    background-color: #1E293B;
    border-color: #334155;
}}

[data-theme="dark"] div[data-testid="stMetric"] {{
    background-color: #1E293B;
    border-color: #334155;
}}

[data-theme="dark"] div[data-testid="stMetric"] label {{
    color: #94A3B8;
}}

[data-theme="dark"] div[data-testid="stMetric"] div[data-testid="stMetricValue"] {{
    color: #E2E8F0;
}}

[data-theme="dark"] div[data-testid="stTable"] {{
    border-color: #334155;
}}

[data-theme="dark"] div[data-testid="stTable"] th {{
    background-color: #1E293B;
    color: #94A3B8;
    border-bottom-color: #334155;
}}

[data-theme="dark"] div[data-testid="stTable"] td {{
    color: #CBD5E1;
    border-bottom-color: #1E293B;
}}

[data-theme="dark"] div[data-testid="stTable"] tr:hover td {{
    background-color: rgba(21, 101, 192, 0.08);
}}

[data-theme="dark"] div[data-testid="stDataFrame"] {{
    border-color: #334155;
}}

[data-theme="dark"] div[data-testid="stTextInput"] input,
[data-theme="dark"] div[data-testid="stNumberInput"] input,
[data-theme="dark"] div[data-testid="stDateInput"] input,
[data-theme="dark"] div[data-testid="stTextArea"] textarea {{
    background-color: #1E293B !important;
    border-color: #334155 !important;
    color: #E2E8F0 !important;
}}

[data-theme="dark"] div[data-testid="stTextInput"] input::placeholder,
[data-theme="dark"] div[data-testid="stTextArea"] textarea::placeholder {{
    color: #475569;
}}

[data-theme="dark"] div[data-baseweb="input"] > div,
[data-theme="dark"] div[data-baseweb="select"] > div,
[data-theme="dark"] div[data-baseweb="textarea"] > div {{
    background-color: #1E293B !important;
    border-color: #334155 !important;
}}

[data-theme="dark"] hr {{
    border-color: #334155;
}}

[data-theme="dark"] button[kind="secondary"] {{
    border-color: #334155;
    color: #CBD5E1;
}}

[data-theme="dark"] button[kind="secondary"]:hover {{
    border-color: #475569;
    color: #E2E8F0;
    background-color: #1E293B;
}}

[data-theme="dark"] div[data-testid="stSelectbox"] [data-baseweb="select"] > div,
[data-theme="dark"] div[data-testid="stMultiSelect"] [data-baseweb="select"] > div {{
    background-color: #1E293B !important;
    border-color: #334155 !important;
}}

[data-theme="dark"] button[data-baseweb="tab"] {{
    color: #94A3B8;
}}
</style>
"""

CSS_DARK_MODE_TOGGLE_JS = """
<script>
(function() {
    var dark = sessionStorage.getItem('lv_dark_mode');
    if (dark === 'true') {
        document.body.setAttribute('data-theme', 'dark');
    }
})();
</script>
"""


def injetar_css_global() -> None:
    st.markdown(CSS_GLOBAL + CSS_DARK_MODE_TOGGLE_JS, unsafe_allow_html=True)


def injetar_toggle_dark_mode() -> None:
    """Alterna modo escuro via JS puro."""
    st.markdown(
        """
        <script>
        (function() {
            var isDark = document.body.getAttribute('data-theme') === 'dark';
            if (isDark) {
                document.body.removeAttribute('data-theme');
                sessionStorage.setItem('lv_dark_mode', 'false');
            } else {
                document.body.setAttribute('data-theme', 'dark');
                sessionStorage.setItem('lv_dark_mode', 'true');
            }
        })();
        </script>
        """,
        unsafe_allow_html=True,
    )
