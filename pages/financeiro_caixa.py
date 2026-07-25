import streamlit as st
from calendar import monthrange
from datetime import date

from src.db import session_scope
from src.financeiro.movimento_caixa.service import fluxo_caixa_por_periodo
from src.ui import exigir_login


def main() -> None:
    st.set_page_config(page_title="LabVida - Fluxo de Caixa", layout="wide")
    exigir_login()

    st.title("Fluxo de Caixa")
    st.caption("Consolidado de entradas e saídas por período")

    hoje = date.today()
    col1, col2 = st.columns(2)
    with col1:
        mes = st.selectbox("Mês", list(range(1, 13)), index=hoje.month - 1)
    with col2:
        ano = st.number_input("Ano", min_value=2020, max_value=2100, value=hoje.year)

    inicio = date(ano, mes, 1)
    fim = date(ano, mes, monthrange(ano, mes)[1])

    with session_scope() as session:
        resultado = fluxo_caixa_por_periodo(session, inicio, fim)

    st.divider()

    col_e, col_s, col_sal = st.columns(3)
    with col_e:
        st.metric("Total Entradas", f"R$ {resultado['total_entradas']:.2f}")
    with col_s:
        st.metric("Total Saídas", f"R$ {resultado['total_saidas']:.2f}")
    with col_sal:
        delta_color = "normal" if resultado["saldo"] >= 0 else "inverse"
        st.metric("Saldo", f"R$ {resultado['saldo']:.2f}", delta_color=delta_color)

    st.divider()
    st.subheader("Movimentos do Período")

    if not resultado["movimentos"]:
        st.info(f"Nenhum movimento em {mes:02d}/{ano}.")
        return

    rows = []
    for m in resultado["movimentos"]:
        tipo = "+ Entrada" if m.tipo == "ENTRADA" else "- Saída"
        rows.append({
            "Data": m.ocorrido_em.strftime("%d/%m/%Y %H:%M"),
            "Tipo": tipo,
            "Valor": f"R$ {m.valor:.2f}",
            "Descrição": m.descricao or "—",
        })
    st.dataframe(rows, hide_index=True, use_container_width=True)


if __name__ == "__main__":
    main()
