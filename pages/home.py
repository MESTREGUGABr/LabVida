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

    st.subheader("Cadastro")
    st.page_link("pages/cadastro_pacientes.py", label="Pacientes", icon=":material/person:")
    st.page_link("pages/cadastro_medicos.py", label="Médicos", icon=":material/stethoscope:")
    st.page_link("pages/cadastro_convenios.py", label="Convênios", icon=":material/contract:")
    st.page_link("pages/cadastro_procedimentos.py", label="Procedimentos", icon=":material/labs:")
    st.page_link("pages/cadastro_unidades.py", label="Unidades e Setores", icon=":material/apartment:")

    st.subheader("Atendimento e Coleta")
    st.page_link("pages/atendimento_os.py", label="Ordens de Serviço", icon=":material/receipt_long:")
    st.page_link("pages/atendimento_coleta.py", label="Registro de Coleta", icon=":material/science:")

    st.subheader("Logística de Amostras")
    st.page_link("pages/logistica_malotes.py", label="Gestão de Malotes", icon=":material/local_shipping:")
    st.page_link("pages/logistica_recebimento.py", label="Recepção Central", icon=":material/inventory:")

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
