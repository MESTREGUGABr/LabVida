import streamlit as st

from src.db import session_scope
from src.faturamento.glosa.dtos import GlosaCreate
from src.faturamento.glosa.service import (
    listar_glosas_com_contexto,
    listar_guias_itens_faturados,
    registrar_glosa,
)
from src.ui import renderizar_menu, shell, usuario_id_logado
from src.ui_components import (
    ColunaGrid,
    renderizar_cabecalho,
    renderizar_empty_state,
    renderizar_grid,
    renderizar_secao,
    tratar_erros,
)
from src.ui_icons import ICONE_ALERTA

_MOTIVOS_PADRAO = [
    "Erro de digitação no código TUSS",
    "Procedimento não autorizado pelo convênio",
    "Divergência de valores",
    "Falta de documentação",
    "Paciente não elegível",
    "Outro",
]


def main() -> None:
    ctx = shell("LabVida - Controle de Glosas", layout="wide", permissao="faturamento:registrar_glosa")
    renderizar_menu(ctx["usuario_id"])

    renderizar_cabecalho(
        titulo="Controle de Glosas",
        subtitulo="Registro e acompanhamento de glosas (recusas de pagamento por convenio)",
        icone=ICONE_ALERTA,
    )

    tab1, tab2 = st.tabs(["Registrar Glosa", "Glosas Registradas"])

    with tab1:
        _render_registrar_glosa()
    with tab2:
        _render_listar_glosas()


def _render_registrar_glosa() -> None:
    renderizar_secao(titulo="Itens Faturados")

    with session_scope() as session:
        itens = listar_guias_itens_faturados(session)

    if not itens:
        renderizar_empty_state(
            icone=ICONE_ALERTA,
            titulo="Nenhum item faturado",
            mensagem="Nao ha itens disponiveis para registro de glosa.",
        )
        st.caption("Fature laudos na tela de Faturamento de Guias TISS antes de registrar glosas.")
        return

    st.caption(f"{len(itens)} itens faturados encontrados")

    _selecionar_item_para_glosar(itens)


def _render_listar_glosas() -> None:
    renderizar_secao(titulo="Glosas Registradas")

    with session_scope() as session:
        glosas = listar_glosas_com_contexto(session)

    if not glosas:
        renderizar_empty_state(
            icone=ICONE_ALERTA,
            titulo="Nenhuma glosa registrada",
            mensagem="As glosas registradas aparecerao aqui.",
        )
        return

    rows = []
    total_glosado = 0.0
    for g in glosas:
        rows.append({
            "Lote": g.codigo_lote,
            "Convênio": g.convenio_nome,
            "Procedimento": g.procedimento_nome,
            "Motivo": g.motivo,
            "Valor Glosado": f"R$ {g.valor_glosado:.2f}",
            "Valor Faturado": f"R$ {g.valor_faturado:.2f}",
            "Data": g.criado_em.strftime("%d/%m/%Y %H:%M"),
        })
        total_glosado += g.valor_glosado

    st.dataframe(rows, hide_index=True, width="stretch")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total de Glosas", len(glosas))
    with col2:
        st.metric("Valor Total Glosado", f"R$ {total_glosado:.2f}")


_COLUNAS_ITEM = [
    ColunaGrid("codigo_lote", "Lote", largura=130),
    ColunaGrid("convenio_nome", "Convenio"),
    ColunaGrid("procedimento_nome", "Procedimento"),
    ColunaGrid("unidade_nome", "Unidade"),
    ColunaGrid("valor_faturado", "Faturado", tipo="moeda", largura=130),
    ColunaGrid("guia_item_id", "guia_item_id", oculta=True),
]


@st.dialog("Registrar glosa")
def _dialogo_glosa(item: dict) -> None:
    st.write(f"**{item['procedimento_nome']}**")
    st.caption(
        f"Lote {item['codigo_lote']} · {item['convenio_nome']} · "
        f"unidade {item['unidade_nome']}"
    )

    motivo = st.selectbox("Motivo", options=_MOTIVOS_PADRAO)
    if motivo == "Outro":
        motivo = st.text_input("Descreva o motivo")

    faturado = float(item["valor_faturado"])
    valor_glosado = st.number_input(
        "Valor glosado (R$)",
        min_value=0.01,
        max_value=faturado,
        value=faturado,
        step=1.0,
    )
    st.caption(
        "O servico valida o ACUMULADO do item: glosas parciais somadas nao podem "
        "passar do valor faturado."
    )

    coluna_ok, coluna_cancelar = st.columns(2)
    with coluna_ok:
        if st.button("Confirmar glosa", type="primary", width="stretch"):
            with tratar_erros("registrar a glosa") as resultado, session_scope() as session:
                registrar_glosa(
                    session,
                    GlosaCreate(
                        guia_item_id=item["guia_item_id"],
                        motivo=(motivo or "").strip(),
                        valor_glosado=valor_glosado,
                    ),
                    usuario_id=usuario_id_logado(),
                )
            if resultado:
                st.toast("Glosa registrada.")
                st.rerun()
    with coluna_cancelar:
        if st.button("Cancelar", width="stretch"):
            st.rerun()


def _selecionar_item_para_glosar(itens: list[dict]) -> None:
    """Grid + dialogo no lugar do formulario inline por linha.

    O padrao anterior guardava `st.session_state[f"show_form_{id}"]` por item:
    so um formulario podia ficar aberto por vez e ele colapsava em reruns nao
    relacionados (bug U4).
    """
    grid = renderizar_grid(
        itens,
        colunas=_COLUNAS_ITEM,
        chave="grid_itens_faturados",
        selecao="linha",
        altura=380,
    )

    item = grid.selecionado
    if item is None:
        st.caption("Selecione um item faturado na tabela para registrar a glosa.")
        return

    st.divider()
    if st.button(f"Registrar glosa em {item['procedimento_nome']}", type="primary"):
        _dialogo_glosa(item)


def _listar_itens_para_glosa(itens: list[dict]) -> None:
    _selecionar_item_para_glosar(itens)


if __name__ == "__main__":
    main()
