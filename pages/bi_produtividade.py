import streamlit as st
import pandas as pd

from src.db import session_scope
from src.ui import renderizar_menu, shell
from src.ui_components import renderizar_cabecalho, renderizar_empty_state, renderizar_secao
from src.ui_icons import ICONE_PRODUTIVIDADE


def main() -> None:
    ctx = shell("BI - Produtividade", layout="wide", permissao="bi:visualizar")
    renderizar_menu(ctx["usuario_id"])

    renderizar_cabecalho(
        titulo="Produtividade Operacional",
        subtitulo="Indicadores de atendimento e exames por unidade",
        icone=ICONE_PRODUTIVIDADE,
    )

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
        renderizar_empty_state(
            icone=ICONE_PRODUTIVIDADE,
            titulo="Nenhum dado disponivel",
            mensagem="Execute o ETL primeiro para popular os indicadores de produtividade.",
        )
        if st.button("Carregar dados do BI", type="primary"):
            from src.bi.etl import executar_etl
            with st.spinner("Executando ETL..."):
                executar_etl()
            st.rerun()
        return

    total_exames = int(exames_por_unidade["exames"].sum()) if not exames_por_unidade.empty else 0
    total_unidades = len(exames_por_unidade)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Exames", total_exames)
    col2.metric("Unidades Ativas", total_unidades)
    col3.metric("Média por Unidade", f"{total_exames / total_unidades:.0f}" if total_unidades else "0")

    col1, col2 = st.columns(2)
    with col1:
        renderizar_secao(titulo="Exames por Unidade")
        st.bar_chart(exames_por_unidade.set_index("unidade"), use_container_width=True)

    with col2:
        renderizar_secao(titulo="Exames por Convenio")
        st.bar_chart(exames_por_convenio.set_index("convenio"), use_container_width=True)

    renderizar_secao(titulo="Evolucao Mensal")
    st.line_chart(exames_por_mes.set_index("mes"), use_container_width=True)

    renderizar_secao(titulo="Distribuicao por Faixa Etaria")
    st.bar_chart(faixa_etaria.set_index("faixa_etaria"), use_container_width=True)


if __name__ == "__main__":
    main()
