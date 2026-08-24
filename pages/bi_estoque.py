"""Estoque — saldo, criticidade e movimentacao de insumos.

Como `bi_auditoria.py`, consulta `InsumoMaterial`/`EstoqueMovimento` direto,
sem ETL/fato novo no esquema estrela: sao tabelas operacionais de baixo
volume, sem "regime" nem estados sobrepostos que justifiquem isso.
"""

import streamlit as st

from src.bi import graficos, metricas
from src.bi.filtros import seletor_de_periodo, sem_dados
from src.db import session_scope
from src.ui import renderizar_menu, shell
from src.ui_components import (
    ColunaGrid,
    renderizar_cabecalho,
    renderizar_empty_state,
    renderizar_grid,
    renderizar_secao,
)
from src.ui_icons import ICONE_ESTOQUE


def main() -> None:
    ctx = shell("BI - Estoque", layout="wide", permissao="bi:visualizar")
    renderizar_menu(ctx["usuario_id"])

    renderizar_cabecalho(
        titulo="Estoque",
        subtitulo="Saldo e criticidade dos insumos, movimentacao no periodo",
        icone=ICONE_ESTOQUE,
    )

    with session_scope() as session:
        periodo = seletor_de_periodo(session, chave="estoque")
        indicadores = metricas.estoque_kpis(session)
        por_mes = metricas.movimentacao_estoque_por_mes(session, periodo)
        maior_consumo = metricas.insumos_maior_consumo(session, periodo)
        criticos = metricas.insumos_criticos(session)
        cobertura = metricas.cobertura_dias(session, periodo)

    if indicadores["total_insumos"] == 0:
        renderizar_empty_state(
            icone=ICONE_ESTOQUE,
            titulo="Nenhum insumo cadastrado",
            mensagem="Cadastre insumos em Compras > Estoque.",
        )
        return

    st.caption("Saldo e criticidade em tempo real; movimentacao e giro no periodo selecionado.")
    st.divider()
    colunas = st.columns(2)
    colunas[0].metric(
        "Insumos criticos", f"{indicadores['insumos_criticos']} de {indicadores['total_insumos']}"
    )
    colunas[1].metric(
        "Cobertura de estoque",
        f"{cobertura:.0f} dias" if cobertura is not None else "Sem consumo no periodo",
    )

    with st.container(border=True):
        renderizar_secao(titulo="Movimentacao mensal (entradas x saidas)")
        if por_mes.empty:
            sem_dados()
        else:
            st.altair_chart(
                graficos.series_comparadas(
                    por_mes, tempo="mes", series=["entradas", "saidas"],
                    rotulo_valor="Quantidade", formato="quantidade",
                    cores=[graficos.COR_POSITIVA, graficos.COR_NEGATIVA],
                ),
                use_container_width=True,
            )

    st.write("")
    with st.container(border=True):
        renderizar_secao(titulo="Insumos com maior consumo no periodo")
        if maior_consumo.empty:
            sem_dados()
        else:
            st.altair_chart(
                graficos.barra_categorica(
                    maior_consumo, categoria="nome", valor="saida_total",
                    rotulo_categoria="Insumo", rotulo_valor="Consumido",
                ),
                use_container_width=True,
            )

    st.write("")
    with st.container(border=True):
        renderizar_secao(titulo="Insumos abaixo do minimo")
        if criticos.empty:
            st.success("Nenhum insumo abaixo do minimo.")
        else:
            renderizar_grid(
                criticos,
                colunas=[
                    ColunaGrid(campo="nome", rotulo="Insumo"),
                    ColunaGrid(campo="quantidade_estoque", rotulo="Saldo atual", tipo="numero"),
                    ColunaGrid(campo="estoque_minimo", rotulo="Minimo", tipo="numero"),
                    ColunaGrid(campo="deficit", rotulo="Deficit", tipo="numero"),
                ],
                chave="grid_insumos_criticos",
                altura=320,
            )


if __name__ == "__main__":
    main()
