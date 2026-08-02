"""Guarda de compatibilidade do streamlit-aggrid (spike da F0, ADR 0008).

O componente unico `renderizar_grid()` depende de uma superficie de API estreita
do st_aggrid. Estes testes falham se um upgrade de Streamlit ou de AgGrid quebrar
essa superficie — antes de 24 telas quebrarem juntas.

Nao renderizam no browser: exercitam import, superficie publica, construcao de
gridOptions com formatacao pt-BR e o registro do componente no runtime.
"""

import importlib
import importlib.metadata as metadata
from decimal import Decimal
from pathlib import Path

import pandas as pd
import pytest

st_aggrid = pytest.importorskip("st_aggrid", reason="streamlit-aggrid nao instalado")


def test_convive_com_streamlit_e_altair_instalados() -> None:
    """AgGrid nao pode forcar downgrade de Streamlit nem de Altair."""
    streamlit_versao = metadata.version("streamlit")
    altair_versao = metadata.version("altair")

    assert streamlit_versao.startswith("1.60"), (
        f"Streamlit mudou para {streamlit_versao} — revalidar o AgGrid (ADR 0008)"
    )
    # O BI depende de Altair >= 5 para as specs de `src/bi/graficos.py`.
    assert int(altair_versao.split(".")[0]) >= 5


def test_superficie_publica_esperada() -> None:
    """Os simbolos que `renderizar_grid()` importa precisam existir."""
    from st_aggrid import (  # noqa: F401
        AgGrid,
        ColumnsAutoSizeMode,
        DataReturnMode,
        GridOptionsBuilder,
        GridUpdateMode,
        JsCode,
    )


def test_grid_options_com_formatacao_pt_br() -> None:
    """Moeda BRL, data DD/MM/AAAA, selecao e paginacao sobrevivem ao build()."""
    from st_aggrid import GridOptionsBuilder, JsCode

    df = pd.DataFrame(
        [
            {
                "codigo": "OS-2026-a1b2c3",
                "paciente": "Maria Silva",
                "valor": Decimal("1234.56"),
                "emissao": pd.Timestamp("2026-03-14"),
                "status": "FATURADO",
            },
            {
                "codigo": "OS-2026-d4e5f6",
                "paciente": "Joao Souza",
                "valor": Decimal("87.90"),
                "emissao": pd.Timestamp("2026-03-15"),
                "status": "GLOSADO",
            },
        ]
    )

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_column(
        "valor",
        header_name="Valor",
        type=["numericColumn"],
        valueFormatter=JsCode(
            "function(p){ return p.value == null ? '' : "
            "'R$ ' + Number(p.value).toLocaleString('pt-BR', "
            "{minimumFractionDigits: 2, maximumFractionDigits: 2}); }"
        ),
    )
    gb.configure_column(
        "emissao",
        header_name="Emissao",
        valueFormatter=JsCode(
            "function(p){ return p.value ? new Date(p.value).toLocaleDateString('pt-BR') : ''; }"
        ),
    )
    gb.configure_selection("multiple", use_checkbox=True)
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=25)
    gb.configure_default_column(filterable=True, sortable=True, resizable=True)

    opcoes = gb.build()

    assert "columnDefs" in opcoes
    assert len(opcoes["columnDefs"]) == len(df.columns)
    assert opcoes.get("pagination") is True
    assert opcoes.get("paginationPageSize") == 25
    # o valueFormatter e o ponto mais fragil: JsCode precisa sobreviver a serializacao
    assert any("valueFormatter" in coluna for coluna in opcoes["columnDefs"])


def test_componente_registrado_com_frontend_local() -> None:
    """O componente precisa estar declarado e servir o build empacotado.

    `url=None` + `path` preenchido significa frontend local (producao).
    `url` preenchido significaria modo dev, apontando para um servidor Node.
    """
    from streamlit.components.v1 import custom_component

    modulo = importlib.import_module("st_aggrid.AgGrid")
    componente = getattr(modulo, "_component_func", None)

    assert componente is not None, "handle _component_func ausente"
    assert isinstance(componente, custom_component.CustomComponent)
    assert componente.url is None, "AgGrid em modo dev — frontend nao empacotado"
    assert componente.path, "caminho do frontend vazio"

    indice = Path(componente.path) / "index.html"
    assert indice.is_file(), f"index.html ausente em {componente.path}"
