import streamlit as st
from src.db import session_scope
from src.rbac import service as rbac_service
from src.rbac.dtos import PerfilCreate
from src.usuario import repository as usuario_repository
from src.ui import renderizar_menu, shell
from src.ui_components import (
    ColunaGrid,
    renderizar_cabecalho,
    renderizar_grid,
    renderizar_secao,
    tratar_erros,
)
from src.ui_icons import ICONE_LIBERAR
from src.ui_theme import NEUTRAL_50, NEUTRAL_200, NEUTRAL_600, PRIMARY_50, PRIMARY_600


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

_COLUNAS_USUARIO = [
    ColunaGrid("nome", "Usuario"),
    ColunaGrid("email", "E-mail"),
    ColunaGrid("perfil", "Perfil atual", largura=200),
    ColunaGrid("id", "id", oculta=True),
]

_MANTER = "— Manter atual —"
_REMOVER = "Remover perfil"


@st.dialog("Alterar perfil do usuario")
def _dialogo_perfil(usuario: dict, perfis_opcoes: dict) -> None:
    st.write(f"**{usuario['nome']}**")
    st.caption(f"{usuario['email']} · perfil atual: {usuario['perfil']}")

    escolha = st.selectbox(
        "Novo perfil",
        options=[_MANTER, _REMOVER] + list(perfis_opcoes.keys()),
    )

    coluna_ok, coluna_cancelar = st.columns(2)
    with coluna_ok:
        if st.button("Salvar", type="primary", width="stretch", disabled=escolha == _MANTER):
            with tratar_erros("alterar o perfil") as resultado, session_scope() as session:
                if escolha == _REMOVER:
                    rbac_service.desvincular_usuario_do_perfil(session, usuario["id"])
                else:
                    rbac_service.vincular_usuario_ao_perfil(
                        session, usuario["id"], perfis_opcoes[escolha]
                    )
            if resultado:
                st.toast("Perfil atualizado.")
                st.rerun()
    with coluna_cancelar:
        if st.button("Cancelar", width="stretch"):
            st.rerun()


def _render_usuarios() -> None:
    """Listagem de usuarios.

    Ate a fase F1 esta tela desenhava a tabela com `st.markdown` de `<div>`
    flex e depois sobrepunha `st.columns` por cima para encaixar os widgets —
    duas grades independentes que so PARECIAM alinhadas. Agora e o componente
    unico de grid, com a acao num dialogo.
    """
    renderizar_secao(
        titulo="Vincular Usuario a Perfil",
        descricao="Atribua perfis de acesso aos usuarios cadastrados",
    )

    with tratar_erros("carregar usuarios e perfis") as resultado, session_scope() as session:
        usuarios = usuario_repository.listar(session)
        perfis = rbac_service.listar_perfis(session)
    if not resultado:
        return

    if not usuarios:
        st.info("Nenhum usuario encontrado. Faca login para sincronizar.")
        return
    if not perfis:
        st.info("Nenhum perfil cadastrado. Execute o seeder RBAC primeiro.")
        return

    perfis_opcoes = {f"{p.nome} — {p.descricao or 'Sem descricao'}": p.id for p in perfis}
    nomes_por_id = {p.id: p.nome for p in perfis}

    linhas = [
        {
            "id": str(u.id),
            "nome": u.nome or "—",
            "email": u.email or "—",
            "perfil": nomes_por_id.get(u.perfil_id, "Nenhum"),
        }
        for u in usuarios
    ]

    sem_perfil = sum(1 for linha in linhas if linha["perfil"] == "Nenhum")
    coluna_total, coluna_sem = st.columns(2)
    coluna_total.metric("Usuarios", len(linhas))
    coluna_sem.metric("Sem perfil", sem_perfil)

    grid = renderizar_grid(
        linhas,
        colunas=_COLUNAS_USUARIO,
        chave="grid_usuarios",
        selecao="linha",
        altura=380,
    )

    usuario = grid.selecionado
    if usuario is None:
        st.caption("Selecione um usuario na tabela para alterar o perfil de acesso.")
        return

    st.divider()
    if st.button(f"Alterar perfil de {usuario['nome']}", type="primary"):
        _dialogo_perfil(usuario, perfis_opcoes)


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
        toggle_key = f"expand_perfil_{perfil.id}"
        if toggle_key not in st.session_state:
            st.session_state[toggle_key] = False

        aberto = st.session_state[toggle_key]
        prefixo = "\u2013" if aberto else "+"

        col_toggle, col_label = st.columns([0.5, 9.5])
        with col_toggle:
            if st.button(
                prefixo,
                key=f"btn_perfil_{perfil.id}",
                use_container_width=True,
            ):
                st.session_state[toggle_key] = not aberto
                st.rerun()
        with col_label:
            st.markdown(f"**{perfil.nome}** \u2014 *{perfil.descricao or 'Sem descricao'}*")

        if aberto:
            with session_scope() as session:
                perms = rbac_service.listar_permissoes_do_perfil(session, perfil.id)

            n_permissoes = len(perms)
            badge_count = f"{n_permissoes} permiss{'ao' if n_permissoes == 1 else 'oes'}"

            st.markdown(
                f"""<span style="display:inline-block;padding:3px 10px;border-radius:10px;
                font-size:11px;font-weight:600;background:{PRIMARY_50};color:{PRIMARY_600};">
                {badge_count}</span>""",
                unsafe_allow_html=True,
            )
            st.markdown("<br><br>", unsafe_allow_html=True)

            if perms:
                for j, p in enumerate(perms):
                    col_info, col_acao = st.columns([8, 1])
                    with col_info:
                        st.markdown(
                            f"""<div style="padding:6px 10px;margin:2px 0;border-radius:6px;
                            background:{NEUTRAL_50};border:1px solid {NEUTRAL_200};font-size:12px;">
                            <code style="font-size:11px;">{p.codigo}</code>
                            <span style="color:{NEUTRAL_600};margin-left:6px;">{p.descricao or ''}</span>
                            </div>""",
                            unsafe_allow_html=True,
                        )
                    with col_acao:
                        if st.button("\u2715", key=f"rem_perm_{perfil.id}_{p.id}", help="Remover permissão"):
                            with session_scope() as sess:
                                rbac_service.remover_permissao_do_perfil(sess, perfil.id, p.id)
                            st.toast("Permissão removida!", icon="\U0001f5d1")
                            st.rerun()
            else:
                st.caption("Nenhuma permissao atribuida.")

            perms_ids = {p.id for p in perms}
            disponiveis = [p for p in todas_permissoes if p.id not in perms_ids]
            if disponiveis:
                st.markdown("<br>", unsafe_allow_html=True)
                col_perm_sel, col_perm_btn = st.columns([7, 2])
                with col_perm_sel:
                    opcoes_permissoes = {
                        f"{p.codigo} \u2014 {p.descricao or ''}": p.id for p in disponiveis
                    }
                    selecionada = st.selectbox(
                        "Adicionar permissao",
                        options=list(opcoes_permissoes.keys()),
                        key=f"add_perm_{perfil.id}",
                        label_visibility="collapsed",
                        placeholder="Selecionar permissao...",
                    )
                with col_perm_btn:
                    if st.button(
                        "Adicionar",
                        key=f"btn_add_perm_{perfil.id}",
                        type="primary",
                        use_container_width=True,
                    ):
                        with session_scope() as sess:
                            rbac_service.atribuir_permissao_ao_perfil(
                                sess, perfil.id, opcoes_permissoes[selecionada]
                            )
                        st.toast("Permissao adicionada!", icon="\u2705")
                        st.rerun()


if __name__ == "__main__":
    main()
