"""Componentes reutilizaveis de UI do LabVida."""

from src.ui_components.action_bar import renderizar_barra_acoes
from src.ui_components.data_grid import ColunaGrid, ResultadoGrid, renderizar_grid
from src.ui_components.empty_state import renderizar_estado_vazio
from src.ui_components.erros import tratar_erros
from src.ui_components.filter_bar import renderizar_barra_filtros
from src.ui_components.kpi_card import renderizar_kpi_card
from src.ui_components.page_header import renderizar_cabecalho
from src.ui_components.section_header import renderizar_secao
from src.ui_components.status_badge import (
    MAPA_STATUS_POR_DOMINIO,
    renderizar_status_badge,
)

renderizar_empty_state = renderizar_estado_vazio

__all__ = [
    "renderizar_cabecalho",
    "renderizar_kpi_card",
    "renderizar_status_badge",
    "renderizar_estado_vazio",
    "renderizar_empty_state",
    "renderizar_barra_acoes",
    "renderizar_secao",
    "renderizar_barra_filtros",
    "renderizar_grid",
    "ColunaGrid",
    "ResultadoGrid",
    "tratar_erros",
    "MAPA_STATUS_POR_DOMINIO",
]
