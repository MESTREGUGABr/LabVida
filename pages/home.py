import streamlit as st

from src.auth import AuthConfig, build_logout_url


def _get_config() -> AuthConfig:
    return AuthConfig(
        domain=st.secrets["auth0"]["domain"],
        client_id=st.secrets["auth0"]["client_id"],
        client_secret=st.secrets["auth0"]["client_secret"],
        redirect_uri=st.secrets.get("auth0", {}).get(
            "redirect_uri", "http://localhost:8501"
        ),
    )


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

    st.divider()

    if st.button("Sair"):
        st.session_state.clear()
        config = _get_config()
        logout_url = build_logout_url(config)
        st.markdown(
            f'<meta http-equiv="refresh" content="0; url={logout_url}">',
            unsafe_allow_html=True,
        )
        st.stop()


if __name__ == "__main__":
    main()
