"""Helpers transversais de UI do Streamlit.

Guarda de sessão reutilizável: enquanto a Stack D não entrega o shell de
navegação definitivo, as páginas usam `exigir_login()` em vez de repetir o
redirecionamento por meta-refresh.
"""

from uuid import UUID

import streamlit as st


def exigir_login() -> dict:
    if "user" not in st.session_state:
        st.markdown(
            '<meta http-equiv="refresh" content="0; url=/">',
            unsafe_allow_html=True,
        )
        st.stop()
    return st.session_state["user"]


def usuario_id_logado() -> UUID:
    user = exigir_login()
    return UUID(user["id"])
