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
from src.ui_components import (
    ColunaGrid,
    renderizar_cabecalho,
    renderizar_empty_state,
    renderizar_grid,
    renderizar_secao,
)
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
        estoque_inicial = st.number_input("Estoque inicial", min_value=0.0, value=0.0, step=1.0)
        estoque_minimo = st.number_input("Estoque mínimo (alerta)", min_value=0.0, value=0.0, step=1.0)
        if st.button("Cadastrar", type="primary"):
            try:
                dto = InsumoCreate(
                    nome=nome,
                    finalidade=finalidade,
                    quantidade_estoque=estoque_inicial,
                    estoque_minimo=estoque_minimo,
                )
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

        baixos = [i for i in insumos if i.estoque_minimo > 0 and i.quantidade_estoque < i.estoque_minimo]
        if baixos:
            nomes = ", ".join(i.nome for i in baixos)
            st.warning(f"⚠️ {len(baixos)} insumo(s) com estoque abaixo do mínimo: {nomes}")

        renderizar_grid(
            [
                {
                    "nome": i.nome,
                    "finalidade": i.finalidade,
                    "quantidade_estoque": i.quantidade_estoque,
                    "estoque_minimo": i.estoque_minimo,
                    "situacao": (
                        "Baixo" if i.estoque_minimo > 0 and i.quantidade_estoque < i.estoque_minimo
                        else "OK"
                    ),
                }
                for i in insumos
            ],
            colunas=[
                ColunaGrid("nome", "Insumo"),
                ColunaGrid("finalidade", "Finalidade"),
                ColunaGrid("quantidade_estoque", "Qtd em estoque", tipo="numero", largura=160),
                ColunaGrid("estoque_minimo", "Mínimo", tipo="numero", largura=120),
                ColunaGrid("situacao", "Situação", largura=100),
            ],
            chave="grid_insumos",
            altura=360,
        )


def _render_movimentacoes() -> None:
    renderizar_secao(titulo="Historico de Movimentacoes")

    with session_scope() as session:
        movs = listar_todos_movimentos(session)
        insumos = listar_insumos(session)
        insumo_nomes = {i.id: i.nome for i in insumos}

    if not movs:
        st.info("Nenhuma movimentação de estoque registrada.")
        return

    renderizar_grid(
        [
            {
                "ocorrido_em": m.ocorrido_em,
                "insumo": insumo_nomes.get(m.insumo_material_id, "Desconhecido"),
                "tipo": "Entrada" if m.tipo == "ENTRADA" else "Saida",
                "quantidade": m.quantidade,
                "observacao": m.observacao or "—",
            }
            for m in movs
        ],
        colunas=[
            ColunaGrid("ocorrido_em", "Data", tipo="data_hora", largura=160),
            ColunaGrid("insumo", "Insumo"),
            ColunaGrid("tipo", "Tipo", largura=110),
            ColunaGrid("quantidade", "Qtd", tipo="numero", largura=110),
            ColunaGrid("observacao", "Observacao"),
        ],
        chave="grid_movimentos_estoque",
        altura=380,
    )


if __name__ == "__main__":
    main()
