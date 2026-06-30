import streamlit as st

from src.auth import build_logout_url
from src.config import get_auth_config


def main() -> None:
    st.set_page_config(page_title="LabVida - Home")

    if "user" not in st.session_state:
        st.markdown(
            '<meta http-equiv="refresh" content="0; url=/">',
            unsafe_allow_html=True,
        )
        st.stop()

    user = st.session_state["user"]

    st.title("LabVida")
    st.caption(f"Ola, {user['name']}")

    st.divider()

    st.write("Bem-vindo ao LabVida!")
    st.page_link("pages/cadastro_pacientes.py", label="Cadastro de Pacientes")
    st.page_link("pages/cadastro_convenios.py", label="Cadastro de Convênios")

    st.divider()

    if st.button("Sair"):
        st.session_state.clear()
        config = get_auth_config()
        logout_url = build_logout_url(config)
        st.markdown(
            f'<meta http-equiv="refresh" content="0; url={logout_url}">',
            unsafe_allow_html=True,
        )
        st.stop()


if __name__ == "__main__":
    main()
