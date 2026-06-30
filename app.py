import streamlit as st

from src.auth import AuthConfig, build_login_url, exchange_code, fetch_user
from src.config import get_auth_config
from src.db import session_scope
from src.usuario.service import sincronizar_usuario


def main() -> None:
    st.set_page_config(
        page_title="LabVida",
        page_icon="\U0001f52c",
        layout="centered",
        initial_sidebar_state="collapsed",
    )

    config = get_auth_config()

    if "code" in st.query_params:
        code = st.query_params["code"]
        code_verifier = st.query_params.get("state", "")
        if not code_verifier:
            st.error("Sessao expirada. Tente novamente.")
            st.stop()

        try:
            tokens = exchange_code(config, code, code_verifier)
            user = fetch_user(config, tokens["access_token"])
            with session_scope() as session:
                usuario = sincronizar_usuario(session, user.email, user.name)
            st.session_state["user"] = {
                "id": str(usuario.id),
                "name": user.name,
                "email": user.email,
                "picture": user.picture,
            }
            st.session_state["id_token"] = tokens.get("id_token", "")
        except Exception as e:
            st.error(f"Erro ao autenticar: {e}")
            st.stop()

        st.query_params.clear()
        st.rerun()

    if st.session_state.get("user"):
        st.switch_page("pages/home.py")

    _render_login_page(config)


def _render_login_page(config: AuthConfig) -> None:
    login_url, _ = build_login_url(config)

    google_g_svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24">'
        '<path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06'
        " 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z\"/>"
        '<path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23'
        " 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z\"/>"
        '<path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09'
        "V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z\"/>"
        '<path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09'
        " 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53"
        ' 6.16-4.53z"/>'
        "</svg>"
    )

    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] { display: none; }
        [data-testid="stHeader"] { display: none; }
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .login-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 80vh;
            text-align: center;
        }
        .login-title {
            color: #ffffff;
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
        }
        .login-subtitle {
            color: rgba(255,255,255,0.85);
            font-size: 1.1rem;
            font-weight: 400;
            margin-bottom: 2.5rem;
        }
        .google-btn {
            display: inline-flex;
            align-items: center;
            gap: 12px;
            background-color: #ffffff;
            color: #3c4043;
            font-family: "Google Sans", Roboto, Arial, sans-serif;
            font-size: 14px;
            font-weight: 500;
            letter-spacing: 0.25px;
            padding: 12px 24px;
            border: 1px solid #dadce0;
            border-radius: 4px;
            cursor: pointer;
            text-decoration: none;
            transition: box-shadow 0.2s ease, background-color 0.2s ease;
        }
        .google-btn:hover {
            box-shadow: 0 1px 6px rgba(32,33,36,0.28);
            background-color: #f8f9fa;
            color: #202124;
        }
        .google-btn:active {
            background-color: #e8eaed;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="login-container">
            <div class="login-title">\U0001f52c LabVida</div>
            <div class="login-subtitle">ERP para laboratorio de analises clinicas</div>
            <a href="{login_url}" target="_self" class="google-btn">
                {google_g_svg} Entrar com Google
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
