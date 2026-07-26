import streamlit as st

from src.compras.insumo.dtos import InsumoCreate
from src.compras.insumo.errors import InsumoError
from src.compras.insumo.service import (
    criar_insumo,
    listar_insumos,
    listar_todos_movimentos,
)
from src.db import session_scope
from src.ui import renderizar_menu, shell
from src.ui_components import renderizar_cabecalho, renderizar_empty_state, renderizar_secao
from src.ui_icons import ICONE_ESTOQUE


def main() -> None:
    ctx = shell("LabVida - Estoque", layout="wide", permissao="compras:visualizar_estoque")
    renderizar_menu(ctx["usuario_id"])

    renderizar_cabecalho(
        titulo="Estoque",
        subtitulo="Cadastro de insumos e controle de movimentacoes",
        icone=ICONE_ESTOQUE,
    )

    tab1, tab2 = st.tabs(["Insumos", "Movimentações"])

    with tab1:
        _render_insumos()
    with tab2:
        _render_movimentacoes()


def _render_insumos() -> None:
    col_form, col_list = st.columns([1, 2])

    with col_form:
        renderizar_secao(titulo="Novo Insumo")
        nome = st.text_input("Nome")
        finalidade = st.text_input("Finalidade")
        if st.button("Cadastrar", type="primary"):
            try:
                dto = InsumoCreate(nome=nome, finalidade=finalidade)
                with session_scope() as session:
                    criar_insumo(session, dto)
                st.toast(f"Insumo {nome} cadastrado!")
                st.rerun()
            except InsumoError as e:
                st.error(str(e))

    with col_list:
        renderizar_secao(titulo="Estoque Atual")
        with session_scope() as session:
            insumos = listar_insumos(session)

        if not insumos:
            st.info("Nenhum insumo cadastrado.")
            return

        rows = []
        for i in insumos:
            rows.append({
                "Insumo": i.nome,
                "Finalidade": i.finalidade,
                "Qtd Estoque": f"{i.quantidade_estoque:.3f}",
            })
        st.dataframe(rows, hide_index=True, width="stretch")


def _render_movimentacoes() -> None:
    renderizar_secao(titulo="Historico de Movimentacoes")

    with session_scope() as session:
        movs = listar_todos_movimentos(session)
        insumos = listar_insumos(session)
        insumo_nomes = {i.id: i.nome for i in insumos}

    if not movs:
        st.info("Nenhuma movimentação de estoque registrada.")
        return

    rows = []
    for m in movs:
        tipo = "+ Entrada" if m.tipo == "ENTRADA" else "- Saída"
        rows.append({
            "Data": m.ocorrido_em.strftime("%d/%m/%Y %H:%M"),
            "Insumo": insumo_nomes.get(m.insumo_material_id, "Desconhecido"),
            "Tipo": tipo,
            "Qtd": f"{m.quantidade:.3f}",
            "Observação": m.observacao or "—",
        })
    st.dataframe(rows, hide_index=True, width="stretch")


if __name__ == "__main__":
    main()
