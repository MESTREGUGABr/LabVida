import streamlit as st
import pandas as pd

from src.db import session_scope
from src.ui import renderizar_menu, shell


def main() -> None:
    ctx = shell("BI - Produtividade", layout="wide", permissao="bi:visualizar")
    renderizar_menu(ctx["usuario_id"])

    st.title("Produtividade Operacional")
    st.caption("Indicadores de atendimento e exames por unidade")

    with session_scope() as session:
        from sqlalchemy import text

        exames_por_unidade = pd.read_sql(
            text(
                "SELECT u.nome AS unidade, COUNT(*) AS exames "
                "FROM bi_fato_atendimento f "
                "JOIN bi_dim_unidade u ON u.sk_unidade = f.sk_unidade "
                "GROUP BY u.nome ORDER BY exames DESC"
            ),
            session.get_bind(),
        )

        exames_por_mes = pd.read_sql(
            text(
                "SELECT t.ano::text || '-' || LPAD(t.mes::text, 2, '0') AS mes, COUNT(*) AS exames "
                "FROM bi_fato_atendimento f "
                "JOIN bi_dim_tempo t ON t.sk_tempo = f.sk_tempo "
                "GROUP BY t.ano, t.mes ORDER BY t.ano, t.mes"
            ),
            session.get_bind(),
        )

        exames_por_convenio = pd.read_sql(
            text(
                "SELECT COALESCE(c.nome, 'Particular') AS convenio, COUNT(*) AS exames "
                "FROM bi_fato_atendimento f "
                "LEFT JOIN bi_dim_convenio c ON c.sk_convenio = f.sk_convenio "
                "GROUP BY c.nome ORDER BY exames DESC"
            ),
            session.get_bind(),
        )

        faixa_etaria = pd.read_sql(
            text(
                "SELECT p.faixa_etaria, COUNT(*) AS pacientes "
                "FROM bi_fato_atendimento f "
                "JOIN bi_dim_paciente_anon p ON p.sk_paciente = f.sk_paciente "
                "GROUP BY p.faixa_etaria ORDER BY p.faixa_etaria"
            ),
            session.get_bind(),
        )

    if exames_por_unidade.empty:
        st.info("Nenhum dado de atendimento disponível. Execute o ETL primeiro.")
        return

    total_exames = int(exames_por_unidade["exames"].sum()) if not exames_por_unidade.empty else 0
    total_unidades = len(exames_por_unidade)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Exames", total_exames)
    col2.metric("Unidades Ativas", total_unidades)
    col3.metric("Média por Unidade", f"{total_exames / total_unidades:.0f}" if total_unidades else "0")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Exames por Unidade")
        st.bar_chart(exames_por_unidade.set_index("unidade"), use_container_width=True)

    with col2:
        st.subheader("Exames por Convênio")
        st.bar_chart(exames_por_convenio.set_index("convenio"), use_container_width=True)

    st.subheader("Evolução Mensal")
    st.line_chart(exames_por_mes.set_index("mes"), use_container_width=True)

    st.subheader("Distribuição por Faixa Etária (Anônimo — LGPD)")
    st.bar_chart(faixa_etaria.set_index("faixa_etaria"), use_container_width=True)


if __name__ == "__main__":
    main()
