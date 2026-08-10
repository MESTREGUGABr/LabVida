"""Pagina Meu Perfil — dados do usuario logado."""

import streamlit as st

from src.db import session_scope
from src.rbac import service as rbac_service
from src.ui import renderizar_menu, shell, usuario_id_logado
from src.ui_components import renderizar_cabecalho, renderizar_secao, renderizar_status_badge
from src.ui_icons import ICONE_USUARIO
from src.usuario import repository as usuario_repo
from src.usuario.errors import CredenciaisInvalidas, SenhaFraca
from src.usuario.service import alterar_propria_senha
from src.ui_theme import NEUTRAL_200, WHITE


def main() -> None:
    ctx = shell("LabVida - Meu Perfil", layout="centered")
    renderizar_menu(ctx["usuario_id"])

    user = ctx["user"]
    usuario_id = usuario_id_logado()

    renderizar_cabecalho(
        titulo="Meu Perfil",
        subtitulo="Gerencie suas informacoes pessoais e de conta",
        icone=ICONE_USUARIO,
    )

    with session_scope() as session:
        usuario = usuario_repo.obter_por_id(session, usuario_id)
        if not usuario:
            st.error("Usuario nao encontrado.")
            return

        perfil_nome = "Nenhum (acesso plano)"
        if usuario.perfil_id:
            perfil = rbac_service.listar_perfis(session)
            for p in perfil:
                if p.id == usuario.perfil_id:
                    perfil_nome = p.nome
                    break

        # ── card info ──
        st.markdown(
            f"""
            <div style="background:{WHITE};border:1px solid {NEUTRAL_200};
            border-radius:10px;padding:28px;max-width:560px;margin:0 auto;">
            """,
            unsafe_allow_html=True,
        )

        # avatar + nome
        picture = user.get("picture", "")
        avatar_html = ""
        if picture:
            avatar_html = f'<img src="{picture}" width="64" height="64" style="border-radius:50%;" alt="">'
        else:
            iniciais = "".join(p[0].upper() for p in user["name"].split()[:2]) if user.get("name") else "??"
            avatar_html = f"""<div style="width:64px;height:64px;border-radius:50%;
            background:linear-gradient(135deg,#1565C0,#00897B);color:#fff;
            display:inline-flex;align-items:center;justify-content:center;
            font-size:22px;font-weight:700;">{iniciais}</div>"""

        st.markdown(
            f"""
            <div style="text-align:center;margin-bottom:24px;">
                {avatar_html}
                <h2 style="margin:12px 0 2px 0;">{usuario.nome}</h2>
                <p style="color:#607D8B;font-size:13px;margin:0;">{usuario.email}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("</div>", unsafe_allow_html=True)

    # ── seccoes ──
    st.markdown("<br>", unsafe_allow_html=True)

    with session_scope() as session:
        usuario = usuario_repo.obter_por_id(session, usuario_id)
        if not usuario:
            return

        # Nome
        renderizar_secao(titulo="Informacoes Pessoais")
        with st.form("form_nome"):
            novo_nome = st.text_input("Nome completo", value=usuario.nome)
            if st.form_submit_button("Salvar alteracoes", type="primary"):
                if novo_nome.strip() and novo_nome.strip() != usuario.nome:
                    usuario.nome = novo_nome.strip()
                    with session_scope() as s:
                        s.merge(usuario)
                        s.commit()
                    st.session_state["user"]["name"] = novo_nome.strip()
                    st.toast("Nome atualizado!", icon="\u2705")
                    st.rerun()
                else:
                    st.info("Nenhuma alteracao detectada.")

    # Perfil atual
    renderizar_secao(titulo="Nivel de Acesso")
    tipo = "info" if perfil_nome != "Nenhum (acesso plano)" else "neutral"
    renderizar_status_badge(perfil_nome, tipo)
    st.markdown("<br>", unsafe_allow_html=True)

    # Seguranca
    renderizar_secao(titulo="Seguranca", descricao="Altere a senha da sua conta")
    with st.form("form_alterar_senha"):
        senha_atual = st.text_input("Senha atual", type="password")
        nova_senha = st.text_input(
            "Nova senha", type="password", help="Minimo de 8 caracteres."
        )
        confirmar_senha = st.text_input("Confirmar nova senha", type="password")
        alterar = st.form_submit_button("Alterar senha", type="primary")

    if alterar:
        if not senha_atual or not nova_senha:
            st.error("Preencha a senha atual e a nova senha.")
        elif nova_senha != confirmar_senha:
            st.error("As senhas nao coincidem.")
        else:
            try:
                with session_scope() as session:
                    alterar_propria_senha(session, usuario_id, senha_atual, nova_senha)
            except CredenciaisInvalidas:
                st.error("Senha atual incorreta.")
            except SenhaFraca as e:
                st.error(str(e))
            else:
                st.toast("Senha alterada!", icon="✅")


if __name__ == "__main__":
    main()
