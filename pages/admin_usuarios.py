import streamlit as st
from src.db import session_scope
from src.rbac import service as rbac_service
from src.rbac.dtos import PerfilCreate
from src.rbac.errors import PerfilNaoEncontrado
from src.usuario import repository as usuario_repository
from src.usuario.errors import UsuarioNaoEncontrado
from src.ui import renderizar_menu, shell
from src.ui_components import (
    renderizar_cabecalho,
    renderizar_empty_state,
    renderizar_secao,
    renderizar_status_badge,
)
from src.ui_icons import ICONE_LIBERAR, ICONE_BUSCA, ICONE_ADICIONAR
from src.ui_theme import NEUTRAL_50, NEUTRAL_100, NEUTRAL_200, NEUTRAL_300, NEUTRAL_600, NEUTRAL_800, WHITE, PRIMARY_50, PRIMARY_600


def main() -> None:
    ctx = shell("LabVida - Administracao de Usuarios", layout="wide", permissao="admin:gerenciar_usuarios")
    renderizar_menu(ctx["usuario_id"])

    renderizar_cabecalho(
        titulo="Administracao de Usuarios",
        subtitulo="Gerencie os perfis de acesso dos usuarios do LabVida",
        icone=ICONE_LIBERAR,
    )

    tab_usuarios, tab_perfis = st.tabs(["Usuarios", "Perfis e Permissoes"])

    with tab_usuarios:
        _render_usuarios()

    with tab_perfis:
        _render_perfis()


# ── TAB USUARIOS ──────────────────────────────────────────

def _render_usuarios() -> None:
    renderizar_secao(
        titulo="Vincular Usuario a Perfil",
        descricao="Atribua perfis de acesso aos usuarios cadastrados",
    )

    with session_scope() as session:
        usuarios = usuario_repository.listar(session)
        perfis = rbac_service.listar_perfis(session)

    if not usuarios:
        st.info("Nenhum usuario encontrado. Faca login para sincronizar.")
        return

    if not perfis:
        st.info("Nenhum perfil cadastrado. Execute o seeder RBAC primeiro.")
        return

    perfis_opcoes = {f"{p.nome} — {p.descricao or 'Sem descricao'}": p.id for p in perfis}
    perfis_por_id = {p.id: p for p in perfis}

    # ── busca ──
    busca = st.text_input(
        "", placeholder="Buscar por nome ou e-mail...",
        key="busca_usuarios", label_visibility="collapsed",
    )
    st.markdown("<br>", unsafe_allow_html=True)

    usuarios_filtrados = usuarios
    if busca:
        termo = busca.lower()
        usuarios_filtrados = [
            u for u in usuarios
            if termo in (u.nome or "").lower() or termo in (u.email or "").lower()
        ]

    if not usuarios_filtrados:
        st.caption("Nenhum usuario encontrado para esta busca.")
        return

    # ── cabecalho da tabela ──
    st.markdown(
        f"""<div style="display:flex;align-items:center;padding:8px 14px;
        background:{NEUTRAL_50};border:1px solid {NEUTRAL_200};border-radius:8px 8px 0 0;
        font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.5px;
        color:{NEUTRAL_600};">
        <span style="flex:3;">Usuario</span>
        <span style="flex:3;">E-mail</span>
        <span style="flex:2;">Perfil Atual</span>
        <span style="flex:4;">Alterar Perfil</span>
        </div>""",
        unsafe_allow_html=True,
    )

    # ── linhas ──
    for i, usuario in enumerate(usuarios_filtrados):
        bg = WHITE if i % 2 == 0 else NEUTRAL_50
        perfil_atual_nome = "Nenhum"
        perfil_atual_id = None
        if usuario.perfil_id and usuario.perfil_id in perfis_por_id:
            perfil_atual_nome = perfis_por_id[usuario.perfil_id].nome
            perfil_atual_id = usuario.perfil_id

        st.markdown(
            f"""<div style="display:flex;align-items:center;padding:10px 14px;
            background:{bg};border:1px solid {NEUTRAL_200};border-top:none;
            font-size:13px;color:{NEUTRAL_800};">
            <div style="flex:3;">
                <span style="font-weight:600;">{usuario.nome or "—"}</span>
            </div>
            <div style="flex:3;color:{NEUTRAL_600};font-size:12px;">
                {usuario.email or "—"}
            </div>
            <div style="flex:2;">
            </div>
            <div style="flex:4;">
            </div>
            </div>""",
            unsafe_allow_html=True,
        )

        col_nome, col_email, col_perfil, col_acao = st.columns([3, 3, 2, 4])

        with col_perfil:
            if perfil_atual_nome == "Nenhum":
                renderizar_status_badge("Nenhum", "neutral")
            else:
                renderizar_status_badge(perfil_atual_nome, "info")

        with col_acao:
            sub_col1, sub_col2 = st.columns([3, 1])
            with sub_col1:
                novo_label = st.selectbox(
                    "Perfil",
                    options=["— Manter atual —"] + list(perfis_opcoes.keys()),
                    key=f"sel_perfil_{usuario.id}",
                    label_visibility="collapsed",
                    placeholder="Alterar perfil...",
                )
            with sub_col2:
                if novo_label != "— Manter atual —" and st.button(
                    "Salvar", key=f"btn_salvar_{usuario.id}", type="primary", use_container_width=True,
                ):
                    try:
                        with session_scope() as sess:
                            rbac_service.vincular_usuario_ao_perfil(
                                sess, usuario.id, perfis_opcoes[novo_label]
                            )
                        st.toast("Perfil atualizado!", icon="\u2705")
                        st.rerun()
                    except (UsuarioNaoEncontrado, PerfilNaoEncontrado) as e:
                        st.error(str(e))

        st.markdown("<hr style='margin:0;border-color:#E0E4E8;border-width:0.5px;'>", unsafe_allow_html=True)


# ── TAB PERFIS ─────────────────────────────────────────────

def _render_perfis() -> None:
    renderizar_secao(
        titulo="Perfis e Permissoes",
        descricao="Visualize e gerencie os perfis de acesso do sistema",
    )

    with session_scope() as session:
        perfis = rbac_service.listar_perfis(session)
        todas_permissoes = rbac_service.listar_permissoes(session)

    col_busca, col_btn = st.columns([3, 1])
    with col_busca:
        busca_perfis = st.text_input(
            "", placeholder="Buscar perfil ou permissao...",
            key="busca_perfis", label_visibility="collapsed",
        )
    with col_btn:
        criar = st.toggle("+ Criar Perfil", key="toggle_criar_perfil")
    if criar:
        with st.form("form_novo_perfil"):
            novo_nome = st.text_input("Nome do perfil")
            nova_desc = st.text_input("Descricao")
            col_form1, col_form2 = st.columns([1, 1])
            with col_form1:
                submitted = st.form_submit_button("Criar", type="primary", use_container_width=True)
            with col_form2:
                cancelar = st.form_submit_button("Cancelar", use_container_width=True)
            if submitted:
                if not novo_nome.strip():
                    st.error("Informe o nome do perfil.")
                else:
                    try:
                        with session_scope() as sess:
                            rbac_service.criar_perfil(sess, PerfilCreate(
                                nome=novo_nome.strip(),
                                descricao=nova_desc.strip() or None,
                            ))
                        st.toast("Perfil criado!", icon="\u2705")
                        st.rerun()
                    except Exception as e:
                        st.error(str(e))
            if cancelar:
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    if busca_perfis:
        termo = busca_perfis.lower()
        perfis = [p for p in perfis if termo in p.nome.lower() or (p.descricao and termo in p.descricao.lower())]

    if not perfis:
        st.info("Nenhum perfil cadastrado ou encontrado.")
        return

    permissoes_por_id = {p.id: p for p in todas_permissoes}

    for perfil in perfis:
        with session_scope() as session:
            perms = rbac_service.listar_permissoes_do_perfil(session, perfil.id)

        n_permissoes = len(perms)
        badge_count = f"{n_permissoes} permiss{'ao' if n_permissoes == 1 else 'oes'}"

        with st.expander(f"{perfil.nome} — {perfil.descricao or 'Sem descricao'}"):
            st.markdown(
                f"""<span style="display:inline-block;padding:3px 10px;border-radius:10px;
                font-size:11px;font-weight:600;background:{PRIMARY_50};color:{PRIMARY_600};">
                {badge_count}</span>""",
                unsafe_allow_html=True,
            )
            st.markdown("<br><br>", unsafe_allow_html=True)

            if perms:
                # grid 2 colunas
                cols = st.columns(2)
                for j, p in enumerate(perms):
                    with cols[j % 2]:
                        st.markdown(
                            f"""<div style="padding:6px 10px;margin:2px 0;border-radius:6px;
                            background:{NEUTRAL_50};border:1px solid {NEUTRAL_200};font-size:12px;">
                            <code style="font-size:11px;">{p.codigo}</code>
                            <span style="color:{NEUTRAL_600};margin-left:6px;">{p.descricao or ''}</span>
                            </div>""",
                            unsafe_allow_html=True,
                        )
            else:
                st.caption("Nenhuma permissao atribuida.")


if __name__ == "__main__":
    main()
