import streamlit as st
import pandas as pd

from src.db import session_scope
from src.ui import renderizar_menu, shell


def main() -> None:
    ctx = shell("BI - Financeiro", layout="wide", permissao="bi:visualizar")
    renderizar_menu(ctx["usuario_id"])

    st.title("Indicadores Financeiros")
    st.caption("Receita, glosas e rentabilidade por convênio e procedimento")

    with session_scope() as session:
        from sqlalchemy import text

        receita_por_convenio = pd.read_sql(
            text(
                "SELECT COALESCE(c.nome, 'Particular') AS convenio, "
                "SUM(f.valor_faturado) AS faturado, SUM(f.valor_glosado) AS glosado "
                "FROM bi_fato_faturamento f "
                "LEFT JOIN bi_dim_convenio c ON c.sk_convenio = f.sk_convenio "
                "GROUP BY c.nome ORDER BY faturado DESC"
            ),
            session.get_bind(),
        )

        receita_por_procedimento = pd.read_sql(
            text(
                "SELECT p.nome AS procedimento, SUM(f.valor_faturado) AS faturado "
                "FROM bi_fato_faturamento f "
                "JOIN bi_dim_procedimento p ON p.sk_procedimento = f.sk_procedimento "
                "GROUP BY p.nome ORDER BY faturado DESC LIMIT 10"
            ),
            session.get_bind(),
        )

        fluxo_caixa = pd.read_sql(
            text(
                "SELECT t.ano::text || '-' || LPAD(t.mes::text, 2, '0') AS mes, "
                "SUM(fi.valor_recebido) AS recebido, SUM(fi.valor_pago) AS pago "
                "FROM bi_fato_financeiro fi "
                "JOIN bi_dim_tempo t ON t.sk_tempo = fi.sk_tempo "
                "GROUP BY t.ano, t.mes ORDER BY t.ano, t.mes"
            ),
            session.get_bind(),
        )

        totais = pd.read_sql(
            text(
                "SELECT SUM(valor_faturado) AS total_faturado, SUM(valor_glosado) AS total_glosado "
                "FROM bi_fato_faturamento"
            ),
            session.get_bind(),
        )

    if receita_por_convenio.empty:
        st.info("Nenhum dado financeiro disponível. Execute o ETL primeiro.")
        return

    raw_faturado = totais["total_faturado"].iloc[0] if not totais.empty else 0
    raw_glosado = totais["total_glosado"].iloc[0] if not totais.empty else 0
    total_faturado = float(raw_faturado) if raw_faturado is not None else 0.0
    total_glosado = float(raw_glosado) if raw_glosado is not None else 0.0
    taxa_glosa = (total_glosado / total_faturado * 100) if total_faturado else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Faturado", f"R$ {total_faturado:,.2f}")
    col2.metric("Total Glosado", f"R$ {total_glosado:,.2f}")
    col3.metric("Taxa de Glosa", f"{taxa_glosa:.1f}%")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Receita por Convênio")
        st.bar_chart(
            receita_por_convenio.set_index("convenio")[["faturado", "glosado"]],
            use_container_width=True,
        )

    with col2:
        st.subheader("Top 10 Procedimentos")
        st.bar_chart(
            receita_por_procedimento.set_index("procedimento"),
            use_container_width=True,
        )

    st.subheader("Fluxo de Caixa (Recebido vs Pago)")
    if not fluxo_caixa.empty:
        st.bar_chart(
            fluxo_caixa.set_index("mes")[["recebido", "pago"]],
            use_container_width=True,
        )


if __name__ == "__main__":
    main()
