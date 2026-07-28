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
from src.ui_components import renderizar_cabecalho, renderizar_empty_state, renderizar_secao, renderizar_status_badge
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


def _render_acompanhar() -> None:
    renderizar_secao(titulo="Pedidos")

    with session_scope() as session:
        pedidos = listar_pedidos(session)
        fornecedores = listar_fornecedores(session)
        forn_nomes = {f.id: f.nome for f in fornecedores}

    if not pedidos:
        st.info("Nenhum pedido registrado.")
        return

    for p in pedidos:
        status_tipo = {"RASCUNHO": "neutral", "APROVADO": "info", "RECEBIDO": "success", "CANCELADO": "error"}
        tipo = status_tipo.get(p.status, "neutral")
        total_itens = len(p.itens)

        with st.container(border=True):
            c1, c2 = st.columns([4, 1])
            with c1:
                st.write(f"**Pedido** — R$ {p.valor_total:.2f} — {total_itens} itens")
                st.caption(f"Fornecedor: {forn_nomes.get(p.fornecedor_id, 'Desconhecido')} | Criado: {p.criado_em.strftime('%d/%m/%Y %H:%M')}")
            with c2:
                st.write("")
                renderizar_status_badge(p.status, tipo)
                if p.status == "RASCUNHO":
                    col_a, col_b = st.columns(2)
                    confirmar = st.checkbox("Confirmo a aprovação", key=f"confirm_aprovar_{p.id}")
                    with col_a:
                        if st.button("Aprovar", key=f"aprovar_{p.id}", disabled=not confirmar):
                            try:
                                with session_scope() as session:
                                    aprovar_pedido(session, p.id)
                                st.toast("Pedido aprovado! Título a pagar gerado.")
                                st.rerun()
                            except PedidoError as e:
                                st.error(str(e))
                    with col_b:
                        if st.button("Cancelar", key=f"cancelar_{p.id}"):
                            try:
                                with session_scope() as session:
                                    cancelar_pedido(session, p.id)
                                st.toast("Pedido cancelado.")
                                st.rerun()
                            except PedidoError as e:
                                st.error(str(e))
                elif p.status == "APROVADO":
                    if st.button("Receber", key=f"receber_{p.id}"):
                        try:
                            with session_scope() as session:
                                receber_pedido(session, p.id)
                            st.toast("Pedido recebido! Estoque atualizado.")
                            st.rerun()
                        except PedidoError as e:
                            st.error(str(e))


if __name__ == "__main__":
    main()
