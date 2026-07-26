import streamlit as st
import pandas as pd

from src.db import session_scope
from src.ui import renderizar_menu, shell


def main() -> None:
    ctx = shell("BI - Logística", layout="wide", permissao="bi:visualizar")
    renderizar_menu(ctx["usuario_id"])

    st.title("Indicadores Logísticos")
    st.caption("Amostras, malotes e eficiência da cadeia de custódia")

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
        st.info("Nenhum dado logístico disponível. Execute o ETL primeiro.")
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
            st.subheader("Amostras por Unidade")
            st.bar_chart(amostras_por_unidade.set_index("unidade"), use_container_width=True)

    with col2:
        if not divergencias.empty:
            st.subheader("Divergências por Unidade")
            st.bar_chart(divergencias.set_index("unidade"), use_container_width=True)

    if not pendencias.empty:
        st.subheader("Status Atual das Amostras (Base Operacional)")
        st.dataframe(
            pendencias.rename(columns={"status": "Status", "quantidade": "Quantidade"}),
            hide_index=True,
            use_container_width=True,
        )


if __name__ == "__main__":
    main()
