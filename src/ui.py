"""Helpers transversais de UI do Streamlit — Stack D.

Shell unificado de navegação: login gate, page config, menu lateral com RBAC.
Substitui o guarda manual que cada página repetia antes da Stack D.
"""

from collections.abc import Sequence
from uuid import UUID

import streamlit as st

from src.db import session_scope
from src.rbac.gate import verificar_permissao
from src.rbac.service import listar_permissoes_do_usuario


_MENU = [
    (
        "Cadastro",
        [
            ("Pacientes", "pages/cadastro_pacientes.py", "cadastro:pacientes:escrever"),
            ("Médicos", "pages/cadastro_medicos.py", "cadastro:medicos:escrever"),
            ("Convênios", "pages/cadastro_convenios.py", "cadastro:convenios:escrever"),
            ("Procedimentos", "pages/cadastro_procedimentos.py", "cadastro:procedimentos:escrever"),
            ("Unidades e Setores", "pages/cadastro_unidades.py", "cadastro:unidades:escrever"),
        ],
    ),
    (
        "Atendimento e Coleta",
        [
            ("Ordens de Serviço", "pages/atendimento_os.py", "atendimento:abrir_os"),
            ("Registro de Coleta", "pages/atendimento_coleta.py", "atendimento:coletar"),
        ],
    ),
    (
        "Logística de Amostras",
        [
            ("Gestão de Malotes", "pages/logistica_malotes.py", "logistica:despachar_malote"),
            ("Recepção Central", "pages/logistica_recebimento.py", "logistica:receber_malote"),
        ],
    ),
    (
        "Laboratorial",
        [
            ("Cadastros Laboratoriais", "pages/laboratorio_cadastros.py", "laboratorial:registrar_resultado"),
            ("Resultados de Exames", "pages/laboratorio_resultados.py", "laboratorial:registrar_resultado"),
            ("Emissão de Laudos", "pages/laboratorio_laudos.py", "laboratorial:liberar_laudo"),
            ("Esteira da Bancada", "pages/laboratorio_bancada.py", "laboratorial:registrar_resultado"),
        ],
    ),
    (
        "Faturamento",
        [
            ("Faturamento de Guias TISS", "pages/faturamento_guias.py", "faturamento:gerenciar_lotes"),
            ("Controle de Glosas", "pages/faturamento_glosas.py", "faturamento:registrar_glosa"),
        ],
    ),
    (
        "Financeiro",
        [
            ("Contas a Receber e Pagar", "pages/financeiro_contas.py", "financeiro:baixar_titulo"),
            ("Fluxo de Caixa", "pages/financeiro_caixa.py", "financeiro:baixar_titulo"),
        ],
    ),
    (
        "Compras",
        [
            ("Fornecedores", "pages/compras_fornecedores.py", "compras:gerenciar_fornecedores"),
            ("Pedidos de Compra", "pages/compras_pedidos.py", "compras:solicitar"),
            ("Estoque", "pages/compras_estoque.py", "compras:visualizar_estoque"),
        ],
    ),
    (
        "Administração",
        [
            ("Usuários e Perfis", "pages/admin_usuarios.py", "admin:gerenciar_usuarios"),
        ],
    ),
    (
        "BI — Indicadores",
        [
            ("Produtividade", "pages/bi_produtividade.py", "bi:visualizar"),
            ("Financeiro", "pages/bi_financeiro.py", "bi:visualizar"),
            ("Logística", "pages/bi_logistica.py", "bi:visualizar"),
        ],
    ),
]


def exigir_login() -> dict:
    if "user" not in st.session_state:
        st.markdown(
            '<meta http-equiv="refresh" content="0; url=/">',
            unsafe_allow_html=True,
        )
        st.stop()
    return st.session_state["user"]


def usuario_id_logado() -> UUID:
    if "_usuario_id" in st.session_state:
        return st.session_state["_usuario_id"]
    user = exigir_login()
    uid = UUID(user["id"])
    st.session_state["_usuario_id"] = uid
    return uid


def shell(page_title: str, *, layout: str = "centered", permissao: str | None = None) -> dict:
    """Shell unificado: login gate + page config + RBAC opcional.

    Substitui o bloco manual de guarda que existia em todas as páginas.
    Deve ser a primeira chamada Streamlit em toda página.

    Retorna dict com 'user' (dados do Auth0) e 'usuario_id' (UUID).
    """
    st.set_page_config(page_title=page_title, layout=layout)

    user = exigir_login()
    usuario_id = UUID(user["id"])
    st.session_state["_usuario_id"] = usuario_id

    if permissao is not None:
        with session_scope() as session:
            from src.usuario.models import Usuario

            usuario = session.get(Usuario, usuario_id)
            acesso_plano = usuario is None or usuario.perfil_id is None
            if not acesso_plano and not verificar_permissao(session, usuario_id, permissao):
                st.error("Acesso negado. Você não possui permissão para acessar esta página.")
                st.stop()

    return {"user": user, "usuario_id": usuario_id}


def _carregar_permissoes(usuario_id: UUID) -> set[str]:
    with session_scope() as session:
        permissoes = listar_permissoes_do_usuario(session, usuario_id)
        return {p.codigo for p in permissoes}


def renderizar_menu(usuario_id: UUID) -> None:
    """Renderiza o menu lateral com seções filtradas por permissão do usuário.

    Chamado no início de toda página (via shell ou home).
    Se o usuário não tem perfil (perfil_id nulo), mostra menu completo (ADR 0002).
    """
    with session_scope() as session:
        permissoes = {p.codigo for p in listar_permissoes_do_usuario(session, usuario_id)}

    acesso_plano = len(permissoes) == 0

    with st.sidebar:
        st.subheader("LabVida")
        st.caption("ERP para Laboratórios")

        for secao, itens in _MENU:
            visiveis = [
                (label, path)
                for label, path, req in itens
                if acesso_plano or req is None or req in permissoes
            ]
            if not visiveis:
                continue

            st.sidebar.markdown(f"**{secao}**")
            for label, path in visiveis:
                st.page_link(path, label=label)

        st.sidebar.divider()

        if st.sidebar.button("Sair"):
            from src.auth import build_logout_url
            from src.config import get_auth_config

            st.session_state.clear()
            config = get_auth_config()
            logout_url = build_logout_url(config)
            st.markdown(
                f'<meta http-equiv="refresh" content="0; url={logout_url}">',
                unsafe_allow_html=True,
            )
            st.stop()
