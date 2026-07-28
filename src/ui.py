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
from src.rbac.models import Perfil
from src.rbac.service import listar_permissoes_do_usuario
from src.ui_css import injetar_css_global
from src.ui_icons import ICONES_MAPA, ICONE_HOME, ICONE_SAIR


def formatar_brl(valor: float) -> str:
    """Formata valor como moeda brasileira: R$ 1.234,56."""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _existem_perfis(session) -> bool:
    from sqlalchemy import select

    return session.scalar(select(Perfil.id).limit(1)) is not None

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
            ("Meu Perfil", "pages/meu_perfil.py", None),
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
            bootstrap = not _existem_perfis(session)
            acesso_plano = usuario is None or (usuario.perfil_id is None and bootstrap)
            if not acesso_plano and not verificar_permissao(session, usuario_id, permissao):
                st.error("Acesso negado. Voce nao possui permissao para acessar esta pagina.")
                st.stop()

    injetar_css_global()

    return {"user": user, "usuario_id": usuario_id}


def renderizar_menu(usuario_id: UUID) -> None:
    """Renderiza o menu lateral com secoes filtradas por permissao do usuario."""
    with st.spinner("Carregando..."):
        with session_scope() as session:
            permissoes = {p.codigo for p in listar_permissoes_do_usuario(session, usuario_id)}
            acesso_plano = len(permissoes) == 0 and not _existem_perfis(session)
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
            nome = user.get("name", "")
            email = user.get("email", "")
            iniciais = "".join(p[0].upper() for p in nome.split()[:2]) if nome else "??"
            picture = user.get("picture", "")
            if picture:
                avatar = (
                    f'<img src="{picture}" style="width:36px;height:36px;'
                    f'border-radius:50%;object-fit:cover;margin-bottom:6px;" alt="">'
                )
            else:
                avatar = (
                    f'<div style="'
                    f'display:inline-flex;align-items:center;justify-content:center;'
                    f'width:36px;height:36px;border-radius:50%;'
                    f'background:linear-gradient(135deg, #1565C0, #00897B);'
                    f'color:#fff;font-size:14px;font-weight:700;'
                    f'margin-bottom:6px;'
                    f'">{iniciais}</div>'
                )
            st.sidebar.markdown(
                f"""
                <div style="padding:8px 14px 12px 14px;text-align:center;
                border-radius:8px;margin:0 8px;">
                    {avatar}
                    <p style="margin:0;font-size:13px;font-weight:600;color:#F1F5F9;">
                        {nome}
                    </p>
                    <p style="margin:2px 0 0 0;font-size:11px;color:#94A3B8;">
                        {email}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.sidebar.markdown(
            "<hr style='border-color:#1E3A5F;border-width:0.5px;opacity:0.4;margin:6px 14px;'>",
            unsafe_allow_html=True,
        )

        st.sidebar.markdown(
            f"""<a href="/home" target="_self" style="
                display:inline-flex;align-items:center;gap:8px;
                width:calc(100% - 28px);padding:8px 14px;margin:0 14px;
                border-radius:8px;text-decoration:none;
                color:#F1F5F9;font-size:13px;font-weight:500;
                transition:all 0.2s ease;"
                onmouseover="this.style.background='rgba(21,101,192,0.12)';"
                onmouseout="this.style.background='transparent';">
                <span style="display:inline-flex;width:20px;height:20px;flex-shrink:0;">{ICONE_HOME}</span>
                Inicio
            </a>""",
            unsafe_allow_html=True,
        )

        st.sidebar.markdown(
            "<hr style='border-color:#1E3A5F;border-width:0.5px;opacity:0.4;margin:10px 14px;'>",
            unsafe_allow_html=True,
        )

        if op_secoes:
            st.sidebar.markdown(
                "<p style='color:#94A3B8;font-size:10px;"
                "letter-spacing:1.0px;text-transform:uppercase;font-weight:600;"
                "margin:16px 0 2px 0;padding:0 14px;'>"
                "Operacional</p>",
                unsafe_allow_html=True,
            )
            _renderizar_grupo_secoes(op_secoes)

        if fer_secoes:
            st.sidebar.markdown(
                "<hr style='border-color:#1E3A5F;border-width:0.5px;opacity:0.4;margin:14px 14px;'>",
                unsafe_allow_html=True,
            )
            st.sidebar.markdown(
                "<p style='color:#94A3B8;font-size:10px;"
                "letter-spacing:1.0px;text-transform:uppercase;font-weight:600;"
                "margin:16px 0 2px 0;padding:0 14px;'>"
                "Ferramentas</p>",
                unsafe_allow_html=True,
            )
            _renderizar_grupo_secoes(fer_secoes)

        st.sidebar.markdown(
            "<hr style='border-color:#1E3A5F;border-width:0.5px;opacity:0.4;margin:20px 14px 14px 14px;'>",
            unsafe_allow_html=True,
        )

        from src.auth import build_logout_url
        from src.config import get_auth_config

        config = get_auth_config()
        logout_url = build_logout_url(config)

        st.sidebar.markdown(
            f"""
            <div style="padding:0 8px;">
                <a href="{logout_url}" target="_self"
                   style="display:inline-flex;align-items:center;justify-content:center;gap:8px;
                   width:100%;height:40px;border-radius:8px;border:1px solid #1E3A5F;
                   color:#F1F5F9;text-decoration:none;font-size:13px;font-weight:500;
                   transition:all 0.2s ease;"
                   onmouseover="this.style.background='rgba(21,101,192,0.15)';this.style.borderColor='#2196F3';this.style.color='#64B5F6';"
                   onmouseout="this.style.background='transparent';this.style.borderColor='#1E3A5F';this.style.color='#F1F5F9';">
                    {ICONE_SAIR} Sair
                </a>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _renderizar_grupo_secoes(secoes: list[tuple[str, list[tuple[str, str]]]]) -> None:
    for secao, itens in secoes:
        icone = ICONES_MAPA.get(secao, "")
        st.sidebar.markdown(
            f"""<p style="color:#94A3B8;font-size:10px;
            letter-spacing:1.0px;text-transform:uppercase;font-weight:600;
            margin-top:16px;margin-bottom:8px;padding:0 14px;">
            <span style="display:inline-flex;align-items:center;gap:6px;">{icone} {secao}</span></p>""",
            unsafe_allow_html=True,
        )
        for label, path in itens:
            st.page_link(path, label=label)


def _renderizar_logo_sidebar() -> None:
    st.sidebar.markdown(_logo_sidebar_html("assets/logo_labvida.png"), unsafe_allow_html=True)
    st.sidebar.markdown(
        '<p style="margin:6px 0 0 0;font-size:18px;font-weight:700;color:#F1F5F9;text-align:center;">LabVida</p>'
        '<p style="margin:2px 0 0 0;font-size:10px;color:#94A3B8;letter-spacing:1.2px;text-transform:uppercase;text-align:center;">'
        'ERP Laboratorial</p>',
        unsafe_allow_html=True,
    )


def _logo_sidebar_html(image_path: str) -> str:
    logo_bytes = Path(image_path).read_bytes()
    logo_base64 = b64encode(logo_bytes).decode("ascii")
    return (
        '<div style="display:flex;justify-content:center;margin:10px 0 12px 0;">'
        f'<img src="data:image/png;base64,{logo_base64}" alt="LabVida" '
        'style="width:48px;height:auto;display:block;object-fit:contain;border-radius:10px;" />'
        '</div>'
    )
