"""Helpers transversais de UI do Streamlit — Stack D.

Shell unificado de navegacao: login gate, page config, menu lateral com RBAC.
Substitui o guarda manual que cada pagina repetia antes da Stack D.
"""

from collections.abc import Sequence
from base64 import b64encode
from pathlib import Path
from uuid import UUID

import streamlit as st

from src.db import session_scope
from src.rbac.gate import verificar_permissao
from src.rbac.service import listar_permissoes_do_usuario
from src.ui_css import injetar_css_global
from src.ui_icons import ICONES_MAPA, ICONE_HOME

_MENU = [
    (
        "Cadastro",
        [
            ("Pacientes", "pages/cadastro_pacientes.py", "cadastro:pacientes:escrever"),
            ("Medicos", "pages/cadastro_medicos.py", "cadastro:medicos:escrever"),
            ("Convenios", "pages/cadastro_convenios.py", "cadastro:convenios:escrever"),
            ("Procedimentos", "pages/cadastro_procedimentos.py", "cadastro:procedimentos:escrever"),
            ("Unidades e Setores", "pages/cadastro_unidades.py", "cadastro:unidades:escrever"),
        ],
    ),
    (
        "Atendimento e Coleta",
        [
            ("Ordens de Servico", "pages/atendimento_os.py", "atendimento:abrir_os"),
            ("Registro de Coleta", "pages/atendimento_coleta.py", "atendimento:coletar"),
        ],
    ),
    (
        "Logistica de Amostras",
        [
            ("Gestao de Malotes", "pages/logistica_malotes.py", "logistica:despachar_malote"),
            ("Recepcao Central", "pages/logistica_recebimento.py", "logistica:receber_malote"),
        ],
    ),
    (
        "Laboratorial",
        [
            ("Cadastros Laboratoriais", "pages/laboratorio_cadastros.py", "laboratorial:registrar_resultado"),
            ("Resultados de Exames", "pages/laboratorio_resultados.py", "laboratorial:registrar_resultado"),
            ("Emissao de Laudos", "pages/laboratorio_laudos.py", "laboratorial:liberar_laudo"),
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
        "Administracao",
        [
            ("Usuarios e Perfis", "pages/admin_usuarios.py", "admin:gerenciar_usuarios"),
        ],
    ),
    (
        "BI \u2014 Indicadores",
        [
            ("Produtividade", "pages/bi_produtividade.py", "bi:visualizar"),
            ("Financeiro", "pages/bi_financeiro.py", "bi:visualizar"),
            ("Logistica", "pages/bi_logistica.py", "bi:visualizar"),
        ],
    ),
]

_SECOES_OPERACIONAIS = [
    "Cadastro",
    "Atendimento e Coleta",
    "Logistica de Amostras",
    "Laboratorial",
    "Faturamento",
    "Financeiro",
    "Compras",
]
_SECOES_FERRAMENTAS = ["BI \u2014 Indicadores", "Administracao"]


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
    """Shell unificado: login gate + page config + CSS global + RBAC opcional."""
    st.set_page_config(
        page_title=page_title,
        page_icon="\U0001f9ea",
        layout=layout,
    )

    user = exigir_login()
    usuario_id = UUID(user["id"])
    st.session_state["_usuario_id"] = usuario_id

    if permissao is not None:
        with session_scope() as session:
            from src.usuario.models import Usuario

            usuario = session.get(Usuario, usuario_id)
            acesso_plano = usuario is None or usuario.perfil_id is None
            if not acesso_plano and not verificar_permissao(session, usuario_id, permissao):
                st.error("Acesso negado. Voce nao possui permissao para acessar esta pagina.")
                st.stop()

    injetar_css_global()

    return {"user": user, "usuario_id": usuario_id}


def renderizar_menu(usuario_id: UUID) -> None:
    """Renderiza o menu lateral com secoes filtradas por permissao do usuario."""
    with session_scope() as session:
        permissoes = {p.codigo for p in listar_permissoes_do_usuario(session, usuario_id)}

    acesso_plano = len(permissoes) == 0
    user = st.session_state.get("user", {})

    op_secoes = []
    fer_secoes = []
    for secao, itens in _MENU:
        visiveis = [
            (label, path)
            for label, path, req in itens
            if acesso_plano or req is None or req in permissoes
        ]
        if not visiveis:
            continue
        if secao in _SECOES_OPERACIONAIS:
            op_secoes.append((secao, visiveis))
        else:
            fer_secoes.append((secao, visiveis))

    with st.sidebar:
        _renderizar_logo_sidebar()

        if user.get("name"):
            st.sidebar.markdown(
                f"""
                <div style="padding:6px 12px 10px 12px;text-align:center;">
                    <p style="margin:0;font-size:14px;font-weight:600;color:#37474F;">
                        {user.get("name", "")}
                    </p>
                    <p style="margin:2px 0 0 0;font-size:12px;color:#78909C;">
                        {user.get("email", "")}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.sidebar.markdown(
            "<hr style='border-color:#E8EAED;border-width:0.5px;opacity:0.5;margin:6px 12px;'>",
            unsafe_allow_html=True,
        )

        st.sidebar.markdown(
            f"""<a href="/home" target="_self"
            style="display:block;padding:9px 12px;color:#37474F;text-decoration:none;
            border-radius:6px;font-size:14px;font-weight:500;
            border-left:3px solid transparent;transition:all 0.2s ease;
            margin:1px 4px;">
            <span style="display:inline-flex;align-items:center;gap:8px;">
            {ICONE_HOME} Inicio</span></a>""",
            unsafe_allow_html=True,
        )

        st.sidebar.markdown(
            "<hr style='border-color:#E8EAED;border-width:0.5px;opacity:0.5;margin:10px 12px;'>",
            unsafe_allow_html=True,
        )

        if op_secoes:
            st.sidebar.markdown(
                "<p style='color:#90A4AE;font-size:11px;"
                "letter-spacing:0.8px;text-transform:uppercase;font-weight:600;"
                "margin:16px 0 2px 0;padding:0 12px;'>"
                "Operacional</p>",
                unsafe_allow_html=True,
            )
            _renderizar_grupo_secoes(op_secoes)

        if fer_secoes:
            st.sidebar.markdown(
                "<hr style='border-color:#E8EAED;border-width:0.5px;opacity:0.5;margin:14px 12px;'>",
                unsafe_allow_html=True,
            )
            st.sidebar.markdown(
                "<p style='color:#90A4AE;font-size:11px;"
                "letter-spacing:0.8px;text-transform:uppercase;font-weight:600;"
                "margin:16px 0 2px 0;padding:0 12px;'>"
                "Ferramentas</p>",
                unsafe_allow_html=True,
            )
            _renderizar_grupo_secoes(fer_secoes)

        st.sidebar.markdown(
            "<hr style='border-color:#E8EAED;border-width:0.5px;opacity:0.5;margin:20px 12px 14px 12px;'>",
            unsafe_allow_html=True,
        )

        if st.sidebar.button("\U0001f6aa Sair", use_container_width=True):
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


def _renderizar_grupo_secoes(secoes: list[tuple[str, list[tuple[str, str]]]]) -> None:
    for secao, itens in secoes:
        icone = ICONES_MAPA.get(secao, "")
        st.sidebar.markdown(
            f"""<p style="color:#90A4AE;font-size:11px;
            letter-spacing:0.8px;text-transform:uppercase;font-weight:600;
            margin-top:14px;margin-bottom:2px;padding:0 12px;">
            <span style="display:inline-flex;align-items:center;gap:6px;">{icone} {secao}</span></p>""",
            unsafe_allow_html=True,
        )
        for label, path in itens:
            st.page_link(path, label=label)


def _renderizar_logo_sidebar() -> None:
    st.sidebar.markdown(_logo_sidebar_html("assets/logo_1.png"), unsafe_allow_html=True)
    st.sidebar.markdown(
        '<p style="margin:6px 0 0 0;font-size:18px;font-weight:700;color:#37474F;text-align:center;">LabVida</p>'
        '<p style="margin:2px 0 0 0;font-size:11px;color:#90A4AE;letter-spacing:1.2px;text-transform:uppercase;text-align:center;">'
        'ERP Laboratorial</p>',
        unsafe_allow_html=True,
    )


def _logo_sidebar_html(image_path: str) -> str:
    logo_bytes = Path(image_path).read_bytes()
    logo_base64 = b64encode(logo_bytes).decode("ascii")
    return (
        '<div style="display:flex;justify-content:center;margin:8px 0 10px 0;">'
        f'<img src="data:image/png;base64,{logo_base64}" alt="LabVida" '
        'style="width:120px;height:auto;display:block;object-fit:contain;" />'
        '</div>'
    )
