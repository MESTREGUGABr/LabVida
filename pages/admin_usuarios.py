import streamlit as st
from src.db import session_scope
from src.rbac import service as rbac_service
from src.rbac.errors import PerfilNaoEncontrado
from src.usuario import repository as usuario_repository
from src.usuario.errors import UsuarioNaoEncontrado
from src.ui import renderizar_menu, shell
from src.ui_components import renderizar_cabecalho, renderizar_empty_state, renderizar_secao
from src.ui_icons import ICONE_LIBERAR


def main() -> None:
    ctx = shell("LabVida - Administração de Usuários", layout="wide", permissao="admin:gerenciar_usuarios")
    renderizar_menu(ctx["usuario_id"])

    renderizar_cabecalho(
        titulo="Administracao de Usuarios",
        subtitulo="Gerencie os perfis de acesso dos usuarios do LabVida",
        icone=ICONE_LIBERAR,
    )

    tab_usuarios, tab_perfis = st.tabs(["Usuários", "Perfis e Permissões"])

    with tab_usuarios:
        _render_usuarios()

    with tab_perfis:
        _render_perfis()


def _render_usuarios() -> None:
    renderizar_secao(titulo="Vincular Usuario a Perfil")

    with session_scope() as session:
        usuarios = usuario_repository.listar(session)
        perfis = rbac_service.listar_perfis(session)

        if not usuarios:
            st.info("Nenhum usuário encontrado. Faça login para sincronizar.")
            return

        if not perfis:
            st.info("Nenhum perfil cadastrado. Execute o seeder RBAC primeiro.")
            return

        perfis_opcoes = {f"{p.nome} — {p.descricao or 'Sem descrição'}": p.id for p in perfis}

    col1, col2, col3 = st.columns([3, 2, 1])
    for usuario in usuarios:
        col1.write(f"**{usuario.nome}**")
        col1.caption(usuario.email)

        perfil_atual = "Nenhum"
        if usuario.perfil_id:
            with session_scope() as session:
                perfil = rbac_service.listar_perfis(session)
                for p in perfil:
                    if p.id == usuario.perfil_id:
                        perfil_atual = p.nome
                        break

        col2.write(f"Perfil atual: **{perfil_atual}**")

        novo_perfil_label = col2.selectbox(
            "Alterar para",
            options=["— Manter —"] + list(perfis_opcoes.keys()),
            key=f"perfil_{usuario.id}",
            label_visibility="collapsed",
        )

        if novo_perfil_label != "— Manter —" and col3.button("Salvar", key=f"btn_{usuario.id}"):
            try:
                with session_scope() as session:
                    rbac_service.vincular_usuario_ao_perfil(
                        session, usuario.id, perfis_opcoes[novo_perfil_label]
                    )
                st.success(f"Perfil de {usuario.nome} atualizado!")
                st.rerun()
            except (UsuarioNaoEncontrado, PerfilNaoEncontrado) as e:
                st.error(str(e))


def _render_perfis() -> None:
    renderizar_secao(titulo="Perfis e Permissoes")

    with session_scope() as session:
        perfis = rbac_service.listar_perfis(session)
        todas_permissoes = rbac_service.listar_permissoes(session)

    if not perfis:
        st.info("Nenhum perfil cadastrado.")
        return

    for perfil in perfis:
        with st.expander(f"{perfil.nome} — {perfil.descricao or 'Sem descrição'}"):
            with session_scope() as session:
                permissoes = rbac_service.listar_permissoes_do_perfil(session, perfil.id)

            if permissoes:
                for p in permissoes:
                    st.write(f"- `{p.codigo}` — {p.descricao or ''}")
            else:
                st.caption("Nenhuma permissão atribuída.")


if __name__ == "__main__":
    main()
