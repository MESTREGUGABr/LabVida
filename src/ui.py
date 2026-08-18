"""Helpers transversais de UI do Streamlit — Stack D.

Shell unificado de navegacao: login gate, page config, menu lateral com RBAC.
Substitui o guarda manual que cada pagina repetia antes da Stack D.
"""

import html
from base64 import b64encode
from pathlib import Path
from uuid import UUID

import streamlit as st
from streamlit.errors import StreamlitAPIException

from src.db import session_scope
from src.rbac.gate import verificar_permissao
from src.rbac.models import Perfil
from src.rbac.service import listar_permissoes_do_usuario
from src.ui_css import injetar_css_global
from src.ui_icons import ICONES_MAPA


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
            ("Competencia", "pages/faturamento_competencia.py", "faturamento:gerenciar_lotes"),
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
            ("Visao Executiva", "pages/bi_visao_executiva.py", "bi:visualizar"),
            ("Produtividade", "pages/bi_produtividade.py", "bi:visualizar"),
            ("Financeiro", "pages/bi_financeiro.py", "bi:visualizar"),
            ("Logistica", "pages/bi_logistica.py", "bi:visualizar"),
            ("Estoque", "pages/bi_estoque.py", "bi:visualizar"),
            ("Auditoria", "pages/bi_auditoria.py", "admin:visualizar_auditoria"),
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
    # Sob `st.navigation`, o entrypoint (app.py) ja configurou a pagina e o
    # Streamlit recusa uma segunda chamada. A pagina continua funcionando
    # isolada (AppTest, execucao direta), onde esta e a primeira chamada.
    try:
        st.set_page_config(
            page_title=page_title,
            page_icon="\U0001f9ea",
            layout=layout,
        )
    except StreamlitAPIException:
        pass

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


def permissoes_do_usuario(usuario_id: UUID) -> tuple[set[str], bool]:
    """Permissoes efetivas e se o sistema esta em modo bootstrap.

    Bootstrap = nenhum perfil cadastrado ainda. Nesse estado o acesso e plano,
    senao a primeira pessoa a logar num banco novo nao conseguiria configurar
    nada (ADR 0002).
    """
    with session_scope() as session:
        permissoes = {p.codigo for p in listar_permissoes_do_usuario(session, usuario_id)}
        bootstrap = not _existem_perfis(session)
    return permissoes, (not permissoes and bootstrap)


def paginas_permitidas(usuario_id: UUID) -> dict[str, list[tuple[str, str]]]:
    """`(titulo, caminho)` por secao, filtrado por permissao.

    Logica pura, separada da construcao dos `st.Page`: `StreamlitPage` so se
    inicializa dentro de um script run, entao a regra de visibilidade nao
    poderia ser testada se nascesse acoplada a ele.

    A visibilidade usa exatamente a permissao que `shell()` exige na pagina —
    de proposito. Mostrar um item que a propria tela vai barrar com "acesso
    negado" e pior do que nao mostrar. Liberar leitura para perfis read-only
    exige afrouxar tambem o gate de cada pagina, e isso e mudanca por tela.
    """
    permissoes, acesso_plano = permissoes_do_usuario(usuario_id)

    secoes: dict[str, list[tuple[str, str]]] = {"Inicio": [("Home", "pages/home.py")]}

    for secao, itens in _MENU:
        visiveis = [
            (titulo, caminho)
            for titulo, caminho, permissao in itens
            if acesso_plano or permissao is None or permissao in permissoes
        ]
        if visiveis:
            secoes[secao] = visiveis

    return secoes


def renderizar_rodape_lateral(usuario_id: UUID) -> None:
    """Cartao do usuario e logout no rodape da barra lateral."""
    user = st.session_state.get("user", {})
    nome = html.escape(user.get("name", "Usuario"))
    email = html.escape(user.get("email", ""))
    with st.sidebar:
        st.divider()
        # HTML proprio em vez de `st.caption`: caption passa pelo parser de
        # markdown do Streamlit, que faz autolink de e-mail solto (vira
        # `mailto:` clicavel sem querer). `nome`/`email` vem de input do
        # usuario no cadastro — sem o `html.escape()` acima, isso seria XSS
        # armazenado.
        st.markdown(
            f'<p style="margin:0;font-size:13px;font-weight:600;">{nome}</p>'
            f'<p style="margin:2px 0 8px 0;font-size:12px;opacity:0.7;">{email}</p>',
            unsafe_allow_html=True,
        )
        if st.button("Sair", width="stretch", key="botao_sair"):
            # Limpar e rerodar devolve ao login: o entrypoint decide a tela pela
            # presenca de `user` na sessao.
            st.session_state.clear()
            st.rerun()


def renderizar_menu(usuario_id: UUID) -> None:
    """Menu lateral: logo, navegacao por secao (HTML/CSS + SVG) e rodape.

    Volta a ser desenhado a mao (era so o rodape desde a F1, quando a
    navegacao passou a ser `st.navigation`) — a pedido do professor, que
    prefere HTML/CSS nativo do Streamlit. Os SVGs vem de `src/ui_icons.py`,
    embutidos inline, sem depender de nenhuma fonte externa.
    """
    _renderizar_menu_lateral(usuario_id)
    renderizar_rodape_lateral(usuario_id)


def _renderizar_menu_lateral(usuario_id: UUID) -> None:
    secoes = paginas_permitidas(usuario_id)
    inicio = secoes.pop("Inicio", [])

    op_secoes = [(s, i) for s, i in secoes.items() if s in _SECOES_OPERACIONAIS]
    fer_secoes = [(s, i) for s, i in secoes.items() if s not in _SECOES_OPERACIONAIS]

    with st.sidebar:
        _renderizar_logo_sidebar()

        for _titulo, caminho in inicio:
            st.page_link(caminho, label="Inicio")

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
        for titulo, caminho in itens:
            st.page_link(caminho, label=titulo)


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


