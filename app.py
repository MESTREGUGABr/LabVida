"""Entrypoint do LabVida.

Decide entre a tela de login e a aplicacao. A navegacao entre paginas usa a
auto-descoberta classica de `pages/*.py` do Streamlit (MPA), com o menu
lateral desenhado a mao em `src/ui.py:renderizar_menu` (HTML/CSS + SVG) —
revertido de `st.navigation` a pedido do professor (preferencia por
HTML/CSS nativo do Streamlit). De brinde, tambem evita um bug de CSS do
projeto (ver `src/ui_css.py`) que quebrava os icones `:material/...:` do
menu nativo.

Fase F15: login local por e-mail e senha, no lugar do OAuth/PKCE via Auth0.
"""

import base64

import streamlit as st

from src.db import session_scope
from src.usuario.errors import CredenciaisInvalidas, EmailInvalido, EmailJaCadastrado, SenhaFraca
from src.usuario.service import autenticar, criar_usuario_com_senha


def main() -> None:
    logado = bool(st.session_state.get("user"))

    # Config da tela de login/redirect. Cada pagina em `pages/*.py` roda como
    # script MPA separado e chama a sua propria via `shell()` (com guarda
    # para o caso de rodar isolada em teste, ver StreamlitAPIException ali).
    st.set_page_config(
        page_title="LabVida",
        page_icon="\U0001f9ea",
        layout="wide" if logado else "centered",
        initial_sidebar_state="expanded" if logado else "collapsed",
    )

    if st.session_state.get("user"):
        _rodar_aplicacao()
        return

    _renderizar_login()


def _rodar_aplicacao() -> None:
    """Redireciona a raiz para a Home; o menu lateral de cada pagina cuida do resto."""
    st.switch_page("pages/home.py")


def _logo_base64() -> str:
    try:
        with open("assets/logo_labvida.png", "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return ""


def _renderizar_login() -> None:
    logo_b64 = _logo_base64()

    logo_img = (
        f'<img src="data:image/png;base64,{logo_b64}" '
        f'width="64" style="border-radius:12px;" alt="LabVida">'
    ) if logo_b64 else ""

    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] { display: none; }
        [data-testid="stHeader"] { display: none; }
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }

        .stApp {
            background: linear-gradient(160deg, #0A2540 0%, #0D3B66 35%, #12508C 70%, #0D3B66 100%);
        }

        .stApp::before {
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
        }

        [data-testid="stAppViewContainer"] [data-testid="stVerticalBlockBorderWrapper"] {
            background: rgba(255, 255, 255, 0.97);
            border-radius: 16px !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.10), 0 2px 8px rgba(0, 0, 0, 0.06);
        }

        .login-logo { text-align: center; margin-bottom: 8px; }

        .login-title {
            color: #0A2540;
            font-size: 26px;
            font-weight: 700;
            letter-spacing: -0.4px;
            text-align: center;
            margin-bottom: 2px;
        }

        .login-subtitle {
            color: #607D8B;
            font-size: 13px;
            font-weight: 500;
            text-align: center;
            margin-bottom: 4px;
        }

        .login-footer {
            color: rgba(255, 255, 255, 0.30);
            font-size: 11px;
            text-align: center;
            margin-top: 16px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    _, coluna_central, _ = st.columns([1, 1.3, 1])
    with coluna_central:
        with st.container(border=True):
            st.markdown(f'<div class="login-logo">{logo_img}</div>', unsafe_allow_html=True)
            st.markdown('<div class="login-title">LabVida</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="login-subtitle">ERP para Laboratorio de Analises Clinicas</div>',
                unsafe_allow_html=True,
            )

            aba_entrar, aba_criar_conta = st.tabs(["Entrar", "Criar conta"])
            with aba_entrar:
                _renderizar_form_entrar()
            with aba_criar_conta:
                _renderizar_form_criar_conta()

    st.markdown(
        '<div class="login-footer">LabVida v1.0 &middot; Ambiente Seguro &middot; LGPD Compliance</div>',
        unsafe_allow_html=True,
    )


def _renderizar_form_entrar() -> None:
    with st.form("form_entrar"):
        email = st.text_input("E-mail")
        senha = st.text_input("Senha", type="password")
        entrar = st.form_submit_button("Entrar", type="primary", width="stretch")

    if not entrar:
        return

    # Mensagem única para todo caso de falha (e-mail inexistente, senha
    # errada, conta sem senha, conta inativa) — nunca dar pista de qual foi.
    if not email or not senha:
        st.error("E-mail ou senha inválidos.")
        return

    try:
        with session_scope() as session:
            usuario = autenticar(session, email, senha)
    except CredenciaisInvalidas:
        st.error("E-mail ou senha inválidos.")
        return

    st.session_state["user"] = {
        "id": str(usuario.id),
        "name": usuario.nome.title(),
        "email": usuario.email,
    }
    st.rerun()


def _renderizar_form_criar_conta() -> None:
    st.caption(
        "Toda conta criada aqui recebe o perfil de administrador automaticamente."
    )
    with st.form("form_criar_conta"):
        nome = st.text_input("Nome", key="cadastro_nome")
        email = st.text_input("E-mail", key="cadastro_email")
        senha = st.text_input(
            "Senha", type="password", key="cadastro_senha", help="Mínimo de 8 caracteres."
        )
        confirmar_senha = st.text_input(
            "Confirmar senha", type="password", key="cadastro_confirmar_senha"
        )
        criar_conta = st.form_submit_button("Criar conta", type="primary", width="stretch")

    if not criar_conta:
        return

    if not nome or not email or not senha:
        st.error("Preencha nome, e-mail e senha.")
        return
    if senha != confirmar_senha:
        st.error("As senhas não coincidem.")
        return

    try:
        with session_scope() as session:
            usuario = criar_usuario_com_senha(session, email, nome, senha)
    except EmailInvalido as e:
        st.error(str(e))
        return
    except EmailJaCadastrado:
        st.error("Este e-mail já está cadastrado.")
        return
    except SenhaFraca as e:
        st.error(str(e))
        return

    st.session_state["user"] = {
        "id": str(usuario.id),
        "name": usuario.nome.title(),
        "email": usuario.email,
    }
    st.rerun()


if __name__ == "__main__":
    main()
