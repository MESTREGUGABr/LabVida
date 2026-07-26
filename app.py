import base64
import streamlit as st

from src.auth import AuthConfig, build_login_url, exchange_code, fetch_user
from src.config import get_auth_config
from src.db import session_scope
from src.usuario.service import sincronizar_usuario


def main() -> None:
    st.set_page_config(
        page_title="LabVida",
        page_icon="\U0001f9ea",
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
                "name": user.name.title(),
                "email": user.email.lower(),
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

    _renderizar_login(config)


def _logo_base64() -> str:
    try:
        with open("assets/logo_labvida.png", "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return ""


def _renderizar_login(config: AuthConfig) -> None:
    login_url, _ = build_login_url(config)
    logo_b64 = _logo_base64()

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

    logo_img = (
        f'<img src="data:image/png;base64,{logo_b64}" '
        f'width="64" style="border-radius:12px;" alt="LabVida">'
    ) if logo_b64 else ""

    st.markdown(
        f"""
        <style>
        [data-testid="stSidebar"] {{ display: none; }}
        [data-testid="stHeader"] {{ display: none; }}
        #MainMenu {{ visibility: hidden; }}
        footer {{ visibility: hidden; }}

        .stApp {{
            background: linear-gradient(160deg, #0A2540 0%, #0D3B66 35%, #12508C 70%, #0D3B66 100%);
        }}

        .stApp::before {{
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background:
                radial-gradient(ellipse at 15% 40%, rgba(0, 137, 123, 0.08) 0%, transparent 50%),
                radial-gradient(ellipse at 85% 60%, rgba(21, 101, 192, 0.10) 0%, transparent 50%),
                radial-gradient(ellipse at 50% 25%, rgba(255, 255, 255, 0.03) 0%, transparent 40%);
            pointer-events: none;
        }}

        .login-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            text-align: center;
            position: relative;
            z-index: 1;
        }}

        .login-card {{
            background: rgba(255, 255, 255, 0.97);
            backdrop-filter: blur(24px);
            border-radius: 16px;
            padding: 48px 44px 44px 44px;
            width: 420px;
            max-width: 90vw;
            box-shadow:
                0 8px 32px rgba(0, 0, 0, 0.10),
                0 2px 8px rgba(0, 0, 0, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}

        .login-logo {{
            display: inline-block;
            margin-bottom: 20px;
        }}

        .login-logo img {{
            width: 64px;
            border-radius: 12px;
        }}

        .login-title {{
            color: #0A2540;
            font-size: 28px;
            font-weight: 700;
            letter-spacing: -0.4px;
            margin-bottom: 4px;
        }}

        .login-subtitle {{
            color: #607D8B;
            font-size: 14px;
            font-weight: 500;
            margin-bottom: 28px;
        }}

        .login-divider {{
            width: 100%;
            height: 2px;
            background: linear-gradient(to right, transparent, #1565C0, #00897B, transparent);
            margin-bottom: 32px;
        }}

        .google-btn {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            width: 100%;
            background-color: #ffffff;
            color: #37474F;
            font-size: 14px;
            font-weight: 500;
            letter-spacing: 0.25px;
            padding: 14px 24px;
            border: 1px solid #dadce0;
            border-radius: 8px;
            cursor: pointer;
            text-decoration: none;
            transition: box-shadow 0.2s ease, background-color 0.2s ease, transform 0.15s ease;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
        }}

        .google-btn:hover {{
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);
            background-color: #fafafa;
            color: #212121;
            transform: translateY(-1px);
        }}

        .google-btn:active {{
            background-color: #f0f0f0;
            transform: translateY(0);
        }}

        .login-footer {{
            color: rgba(255, 255, 255, 0.30);
            font-size: 11px;
            margin-top: 28px;
            position: relative;
            z-index: 1;
        }}

        @media (max-width: 480px) {{
            .login-card {{
                padding: 36px 24px 32px 24px;
            }}
            .login-title {{ font-size: 22px; }}
            .login-subtitle {{ font-size: 12px; }}
        }}
        </style>

        <div class="login-container">
            <div class="login-card">
                <div class="login-logo">{logo_img}</div>
                <div class="login-title">LabVida</div>
                <div class="login-subtitle">ERP para Laboratorio de Analises Clinicas</div>
                <div class="login-divider"></div>
                <a href="{login_url}" target="_self" class="google-btn">
                    {google_g_svg} Entrar com Google
                </a>
            </div>
            <div class="login-footer">
                LabVida v1.0 &middot; Ambiente Seguro &middot; LGPD Compliance
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
