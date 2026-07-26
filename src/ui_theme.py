"""Constantes de tema do LabVida — paleta institucional premium."""

from typing import Final

SIDEBAR_BG: Final[str] = "#F4F5F7"
SIDEBAR_TEXT: Final[str] = "#37474F"
SIDEBAR_TEXT_SECONDARY: Final[str] = "#78909C"
SIDEBAR_LABEL: Final[str] = "#90A4AE"
SIDEBAR_HOVER_BG: Final[str] = "rgba(232, 74, 39, 0.06)"
SIDEBAR_ACTIVE_BG: Final[str] = "rgba(232, 74, 39, 0.08)"
SIDEBAR_SEPARATOR: Final[str] = "#E8EAED"
SIDEBAR_ACTIVE_BAR: Final[str] = "#E84A27"
SIDEBAR_GRADIENT_START: Final[str] = "#E84A27"
SIDEBAR_GRADIENT_END: Final[str] = "#F3A812"

BG_PAGE: Final[str] = "#FAFBFC"
BG_CARD: Final[str] = "#FFFFFF"
BG_HOVER: Final[str] = "rgba(232, 74, 39, 0.06)"

PRIMARY_900: Final[str] = "#0D2B4A"
PRIMARY_800: Final[str] = "#143B5E"
PRIMARY_700: Final[str] = "#1E4D73"
PRIMARY_600: Final[str] = "#24608A"
PRIMARY_500: Final[str] = "#1E75C4"
PRIMARY_400: Final[str] = "#2B8AD4"
PRIMARY_300: Final[str] = "#4FA3E0"
PRIMARY_100: Final[str] = "#E3F2FD"
PRIMARY_50: Final[str] = "#F0F7FF"

ACCENT_ORANGE: Final[str] = "#E84A27"
ACCENT_ORANGE_HOVER: Final[str] = "#C83718"
ACCENT_TEAL: Final[str] = "#00897B"
ACCENT_TEAL_HOVER: Final[str] = "#00695C"
ACCENT_AMBER: Final[str] = "#E67E22"
ACCENT_BLUE: Final[str] = "#1E75C4"

NEUTRAL_900: Final[str] = "#212121"
NEUTRAL_800: Final[str] = "#37474F"
NEUTRAL_700: Final[str] = "#455A64"
NEUTRAL_600: Final[str] = "#607D8B"
NEUTRAL_500: Final[str] = "#90A4AE"
NEUTRAL_400: Final[str] = "#B0BEC5"
NEUTRAL_300: Final[str] = "#CFD8DC"
NEUTRAL_200: Final[str] = "#E0E4E8"
NEUTRAL_100: Final[str] = "#F0F2F5"
NEUTRAL_50: Final[str] = "#FAFBFC"

WHITE: Final[str] = "#FFFFFF"

STATUS_SUCCESS: Final[str] = "#00897B"
STATUS_SUCCESS_BG: Final[str] = "#E0F2F1"
STATUS_WARNING: Final[str] = "#E67E22"
STATUS_WARNING_BG: Final[str] = "#FFF3E0"
STATUS_ERROR: Final[str] = "#D32F2F"
STATUS_ERROR_BG: Final[str] = "#FFEBEE"
STATUS_INFO: Final[str] = "#1E75C4"
STATUS_INFO_BG: Final[str] = "#E3F2FD"
STATUS_NEUTRAL: Final[str] = "#607D8B"
STATUS_NEUTRAL_BG: Final[str] = "#ECEFF1"

BORDER_RADIUS: Final[str] = "8px"
BORDER_RADIUS_SM: Final[str] = "6px"
SHADOW_CARD: Final[str] = "0 1px 3px rgba(0, 0, 0, 0.06), 0 1px 2px rgba(0, 0, 0, 0.04)"
SHADOW_ELEVATED: Final[str] = "0 4px 12px rgba(0, 0, 0, 0.08), 0 2px 4px rgba(0, 0, 0, 0.04)"

ICONES_MODULOS: Final[dict[str, str]] = {
    "Cadastro": "\U0001f4da",
    "Atendimento e Coleta": "\U0001f3a5",
    "Logistica de Amostras": "\U0001f4e6",
    "Laboratorial": "\U0001f52c",
    "Faturamento": "\U0001f4c4",
    "Financeiro": "\U0001f4b0",
    "Compras": "\U0001f6d2",
    "Administracao": "\U0001f6e0",
    "BI \u2014 Indicadores": "\U0001f4ca",
}

ICONES_PAGINAS: Final[dict[str, str]] = {
    "Pacientes": "\U0001f9d1",
    "Medicos": "\U0001f3a5",
    "Convenios": "\U0001f3e5",
    "Procedimentos": "\U0001f4cb",
    "Unidades e Setores": "\U0001f3e2",
    "Ordens de Servico": "\U0001f4cb",
    "Registro de Coleta": "\U0001f489",
    "Gestao de Malotes": "\U0001f4e6",
    "Recepcao Central": "\U0001f4e5",
    "Cadastros Laboratoriais": "\U0001f6e0",
    "Resultados de Exames": "\U0001f4ca",
    "Emissao de Laudos": "\U0001f4c4",
    "Esteira da Bancada": "\U0001f3af",
    "Faturamento de Guias TISS": "\U0001f4c8",
    "Controle de Glosas": "\U0001f6d1",
    "Contas a Receber e Pagar": "\U0001f4b3",
    "Fluxo de Caixa": "\U0001f4b5",
    "Fornecedores": "\U0001f69a",
    "Pedidos de Compra": "\U0001f4e6",
    "Estoque": "\U0001f4e6",
    "Usuarios e Perfis": "\U0001f465",
    "Produtividade": "\U0001f4c8",
    "Financeiro": "\U0001f4b0",
    "Logistica": "\U0001f69a",
}
