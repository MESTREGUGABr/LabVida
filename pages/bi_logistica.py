import streamlit as st
import pandas as pd

from src.db import session_scope
from src.ui import renderizar_menu, shell
from src.ui_components import renderizar_cabecalho, renderizar_empty_state, renderizar_secao
from src.ui_icons import ICONE_AMOSTRA


def main() -> None:
    ctx = shell("BI - Logística", layout="wide", permissao="bi:visualizar")
    renderizar_menu(ctx["usuario_id"])

    renderizar_cabecalho(
        titulo="Indicadores Logisticos",
        subtitulo="Amostras, malotes e eficiencia da cadeia de custodia",
        icone=ICONE_AMOSTRA,
    )

    with session_scope() as session:
        from sqlalchemy import text

        amostras_por_unidade = pd.read_sql(
            text(
                "SELECT u.nome AS unidade, SUM(f.qtd_amostras) AS amostras "
                "FROM bi_fato_logistica f "
                "JOIN bi_dim_unidade u ON u.sk_unidade = f.sk_unidade "
                "GROUP BY u.nome ORDER BY amostras DESC"
            ),
            session.get_bind(),
        )

        divergencias = pd.read_sql(
            text(
                "SELECT u.nome AS unidade, SUM(f.amostras_divergentes) AS divergentes "
                "FROM bi_fato_logistica f "
                "JOIN bi_dim_unidade u ON u.sk_unidade = f.sk_unidade "
                "GROUP BY u.nome ORDER BY divergentes DESC"
            ),
            session.get_bind(),
        )

        totais_log = pd.read_sql(
            text(
                "SELECT SUM(qtd_amostras) AS total_amostras, "
                "SUM(amostras_divergentes) AS total_divergentes "
                "FROM bi_fato_logistica"
            ),
            session.get_bind(),
        )

        pendencias = pd.read_sql(
            text(
                "SELECT a.status, COUNT(*) AS quantidade "
                "FROM amostras a "
                "WHERE a.status NOT IN ('CONCLUIDA', 'CANCELADA') "
                "GROUP BY a.status ORDER BY quantidade DESC"
            ),
            session.get_bind(),
        )

    if amostras_por_unidade.empty and pendencias.empty:
        renderizar_empty_state(
            icone=ICONE_AMOSTRA,
            titulo="Nenhum dado logistico",
            mensagem="Execute o ETL primeiro para popular os indicadores logisticos.",
        )
        if st.button("Carregar dados do BI", type="primary"):
            from src.bi.etl import executar_etl
            with st.spinner("Executando ETL..."):
                executar_etl()
            st.rerun()
        return

    raw_amostras = totais_log["total_amostras"].iloc[0] if not totais_log.empty else 0
    raw_divergentes = totais_log["total_divergentes"].iloc[0] if not totais_log.empty else 0
    total_amostras = int(raw_amostras) if raw_amostras is not None else 0
    total_divergentes = int(raw_divergentes) if raw_divergentes is not None else 0
    taxa_divergencia = (total_divergentes / total_amostras * 100) if total_amostras else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Amostras", total_amostras)
    col2.metric("Divergências", total_divergentes)
    col3.metric("Taxa de Divergência", f"{taxa_divergencia:.1f}%")

    col1, col2 = st.columns(2)
    with col1:
        if not amostras_por_unidade.empty:
            renderizar_secao(titulo="Amostras por Unidade")
            st.bar_chart(amostras_por_unidade.set_index("unidade"), width="stretch")

    with col2:
        if not divergencias.empty:
            renderizar_secao(titulo="Divergencias por Unidade")
            st.bar_chart(divergencias.set_index("unidade"), width="stretch")

    if not pendencias.empty:
        renderizar_secao(titulo="Status Atual das Amostras")
        st.dataframe(
            pendencias.rename(columns={"status": "Status", "quantidade": "Quantidade"}),
            hide_index=True,
            width="stretch",
        )


if __name__ == "__main__":
    main()
