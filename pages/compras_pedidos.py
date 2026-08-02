import streamlit as st

from src.compras.fornecedor.service import listar_ativos as listar_fornecedores
from src.compras.insumo.service import listar_insumos
from src.compras.pedido_compra.dtos import PedidoItemCreate, SolicitacaoCreate
from src.compras.pedido_compra.errors import PedidoError
from src.compras.pedido_compra.service import (
    aprovar_pedido,
    cancelar_pedido,
    criar_solicitacao,
    listar_pedidos,
    receber_pedido,
)
from src.db import session_scope
from src.ui import renderizar_menu, shell, usuario_id_logado
from src.ui_components import (
    ColunaGrid,
    renderizar_cabecalho,
    renderizar_grid,
    renderizar_secao,
    tratar_erros,
)
from src.ui_icons import ICONE_PEDIDO


def main() -> None:
    ctx = shell("LabVida - Pedidos de Compra", layout="wide", permissao="compras:solicitar")
    renderizar_menu(ctx["usuario_id"])

    renderizar_cabecalho(
        titulo="Pedidos de Compra",
        subtitulo="Solicitacao, aprovacao e recebimento de pedidos de insumos",
        icone=ICONE_PEDIDO,
    )

    tab_nomes = ["Novo Pedido", "Acompanhar"]
    aba = st.radio("Seção", tab_nomes, horizontal=True, key="tab_compras", label_visibility="collapsed")

    if aba == tab_nomes[0]:
        _render_novo_pedido()
    elif aba == tab_nomes[1]:
        _render_acompanhar()


def _render_novo_pedido() -> None:
    renderizar_secao(titulo="Novo Pedido de Compra")

    with session_scope() as session:
        fornecedores = listar_fornecedores(session)
        insumos = listar_insumos(session)

    if not fornecedores:
        st.warning("Cadastre um fornecedor antes de criar pedidos.")
        return
    if not insumos:
        st.warning("Cadastre um insumo antes de criar pedidos.")
        return

    forn_opcoes = {f.nome: f.id for f in fornecedores}
    forn_label = st.selectbox("Fornecedor", options=list(forn_opcoes.keys()))
    fornecedor_id = forn_opcoes[forn_label]

    st.write("**Itens do Pedido**")
    insumo_opcoes = {i.nome: i.id for i in insumos}

    if "itens_count" not in st.session_state:
        st.session_state["itens_count"] = 1

    itens = []
    for idx in range(st.session_state["itens_count"]):
        col_a, col_b, col_c = st.columns([3, 1, 1])
        with col_a:
            insumo_label = st.selectbox(f"Insumo", options=list(insumo_opcoes.keys()), key=f"insumo_{idx}")
        with col_b:
            qtd = st.number_input("Qtd", min_value=0.001, value=1.0, step=1.0, key=f"qtd_{idx}")
        with col_c:
            valor = st.number_input("R$ Unit", min_value=0.01, value=10.0, step=1.0, key=f"vlr_{idx}")
        itens.append(PedidoItemCreate(
            insumo_material_id=insumo_opcoes[insumo_label],
            quantidade=qtd,
            valor_unitario=valor,
        ))

    col_add, col_del = st.columns(2)
    if col_add.button("+ Adicionar item"):
        st.session_state["itens_count"] += 1
        st.rerun()
    if col_del.button("- Remover último"):
        if st.session_state["itens_count"] > 1:
            st.session_state["itens_count"] -= 1
            st.rerun()

    if st.button("Criar Pedido (Rascunho)", type="primary"):
        try:
            dto = SolicitacaoCreate(fornecedor_id=fornecedor_id, itens=itens)
            with session_scope() as session:
                pedido = criar_solicitacao(session, dto, usuario_id_logado())
            st.toast(f"Pedido criado em RASCUNHO! Total: R$ {pedido.valor_total:.2f}")
            st.rerun()
        except PedidoError as e:
            st.error(str(e))


_COLUNAS_PEDIDO = [
    ColunaGrid("numero", "Pedido", largura=110),
    ColunaGrid("fornecedor", "Fornecedor"),
    ColunaGrid("status", "Status", largura=120),
    ColunaGrid("qtd_itens", "Itens", tipo="inteiro", largura=90),
    ColunaGrid("valor_total", "Valor total", tipo="moeda", largura=140),
    ColunaGrid("criado_em", "Criado em", tipo="data_hora", largura=160),
    ColunaGrid("id", "id", oculta=True),
]

_COLUNAS_ITEM = [
    ColunaGrid("insumo", "Produto"),
    ColunaGrid("quantidade", "Quantidade", tipo="numero", largura=130),
    ColunaGrid("valor_unitario", "Valor unitario", tipo="moeda", largura=140),
    ColunaGrid("subtotal", "Subtotal", tipo="moeda", largura=140),
]


@st.dialog("Confirmar acao no pedido")
def _dialogo_acao(pedido: dict, acao: str) -> None:
    rotulos = {
        "aprovar": ("Aprovar o pedido gera o **titulo a pagar** correspondente.", aprovar_pedido),
        "cancelar": ("O cancelamento nao pode ser desfeito.", cancelar_pedido),
        "receber": ("O recebimento dá entrada dos produtos no **estoque**.", receber_pedido),
    }
    aviso, operacao = rotulos[acao]

    st.write(f"Pedido **{pedido['numero']}** — {pedido['fornecedor']}")
    st.caption(aviso)

    coluna_ok, coluna_cancelar = st.columns(2)
    with coluna_ok:
        if st.button("Confirmar", type="primary", width="stretch"):
            with tratar_erros(f"{acao} o pedido") as resultado, session_scope() as session:
                operacao(session, pedido["id"])
            if resultado:
                st.toast(f"Pedido {acao[:-1]}ado.")
                st.rerun()
    with coluna_cancelar:
        if st.button("Voltar", width="stretch"):
            st.rerun()


def _render_acompanhar() -> None:
    renderizar_secao(titulo="Pedidos")

    with tratar_erros("carregar os pedidos") as resultado, session_scope() as session:
        pedidos = listar_pedidos(session)
        nomes_fornecedor = {f.id: f.nome for f in listar_fornecedores(session)}
        nomes_insumo = {i.id: i.nome for i in listar_insumos(session)}
        linhas = [
            {
                "id": str(p.id),
                "numero": f"PC-{str(p.id)[:6].upper()}",
                "fornecedor": nomes_fornecedor.get(p.fornecedor_id, "Desconhecido"),
                "status": p.status,
                "qtd_itens": len(p.itens),
                "valor_total": p.valor_total,
                "criado_em": p.criado_em,
            }
            for p in pedidos
        ]
        # Os itens sao lidos aqui, dentro da sessao: acessa-los depois do
        # `session_scope` fechar levantaria DetachedInstanceError.
        itens_por_pedido = {
            str(p.id): [
                {
                    "insumo": nomes_insumo.get(item.insumo_material_id, "Insumo removido"),
                    "quantidade": item.quantidade,
                    "valor_unitario": item.valor_unitario,
                    "subtotal": float(item.quantidade) * float(item.valor_unitario),
                }
                for item in p.itens
            ]
            for p in pedidos
        }
    if not resultado:
        return

    grid = renderizar_grid(
        linhas,
        colunas=_COLUNAS_PEDIDO,
        chave="grid_pedidos",
        selecao="linha",
        altura=340,
        mensagem_vazio="Nenhum pedido registrado. Use a aba **Novo Pedido**.",
    )

    pedido = grid.selecionado
    if pedido is None:
        st.caption("Selecione um pedido para ver os produtos e agir sobre ele.")
        return

    st.divider()
    renderizar_secao(titulo=f"Produtos do pedido {pedido['numero']}")
    renderizar_grid(
        itens_por_pedido.get(pedido["id"], []),
        colunas=_COLUNAS_ITEM,
        chave=f"grid_itens_{pedido['id']}",
        altura=220,
        paginar=False,
        mensagem_vazio="Este pedido nao tem produtos lancados.",
    )

    acoes = {"RASCUNHO": ["aprovar", "cancelar"], "APROVADO": ["receber"]}.get(pedido["status"], [])
    if not acoes:
        st.caption(f"Pedido {pedido['status'].lower()} — nenhuma acao disponivel.")
        return

    colunas = st.columns(len(acoes) + 2)
    for indice, acao in enumerate(acoes):
        with colunas[indice]:
            if st.button(acao.capitalize(), key=f"acao_{acao}", width="stretch"):
                _dialogo_acao(pedido, acao)


if __name__ == "__main__":
    main()
