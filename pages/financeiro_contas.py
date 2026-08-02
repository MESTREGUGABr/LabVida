import streamlit as st

from src.cadastro.convenio.service import listar_convenios
from src.db import session_scope
from src.faturamento.lote_faturamento.service import listar_lotes
from src.financeiro.titulo_receber.service import (
    baixar_titulo as baixar_receber,
    listar_todos as receber_todos,
)
from src.financeiro.titulo_pagar.service import (
    baixar_titulo as baixar_pagar,
    listar_todos as pagar_todos,
)
from src.financeiro.conciliacao_pagamento.service import listar_todas as conciliacoes_todas
from src.ui import formatar_brl, renderizar_menu, shell, usuario_id_logado
from src.ui_components import (
    ColunaGrid,
    renderizar_cabecalho,
    renderizar_empty_state,
    renderizar_grid,
    renderizar_secao,
    tratar_erros,
)
from src.ui_icons import ICONE_FINANCEIRO


def main() -> None:
    ctx = shell("LabVida - Contas", layout="wide", permissao="financeiro:baixar_titulo")
    renderizar_menu(ctx["usuario_id"])

    renderizar_cabecalho(
        titulo="Contas",
        subtitulo="Contas a receber e contas a pagar",
        icone=ICONE_FINANCEIRO,
    )

    tab1, tab2, tab3 = st.tabs(["Contas a Receber", "Contas a Pagar", "Conciliações"])

    with tab1:
        _render_receber()
    with tab2:
        _render_pagar()
    with tab3:
        _render_conciliacoes()


def _render_conciliacoes() -> None:
    renderizar_secao(
        titulo="Conciliações de Pagamento",
        descricao="Divergências entre o valor faturado e o efetivamente recebido",
    )

    with session_scope() as session:
        conciliacoes = conciliacoes_todas(session)

    if not conciliacoes:
        renderizar_empty_state(
            icone=ICONE_FINANCEIRO,
            titulo="Nenhuma conciliação",
            mensagem="Divergências surgem ao baixar um título recebendo menos que o faturado.",
        )
        return

    total_divergencia = sum(c.divergencia for c in conciliacoes)
    com_divergencia = [c for c in conciliacoes if c.divergencia > 0]

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Conciliações com divergência", len(com_divergencia))
    with col2:
        st.metric("Total divergente", f"R$ {total_divergencia:.2f}")

    if total_divergencia > 0:
        st.warning(
            f"Há R$ {total_divergencia:.2f} de divergência acumulada — revise os recebimentos abaixo."
        )

    st.dataframe(
        [
            {
                "Título": str(c.titulo_receber_id)[:8],
                "Recebido": f"R$ {c.valor_recebido:.2f}",
                "Divergência": f"R$ {c.divergencia:.2f}",
                "Data": c.conciliado_em.strftime("%d/%m/%Y %H:%M"),
                "Observação": c.observacao or "—",
            }
            for c in conciliacoes
        ],
        hide_index=True,
        width="stretch",
    )


def _render_receber() -> None:
    renderizar_secao(titulo="Contas a Receber")

    with session_scope() as session:
        titulos = receber_todos(session)
        convs = {c.id: c.nome for c in listar_convenios(session)}
        lotes = {l.id: l.convenio_id for l in listar_lotes(session)}

    if not titulos:
        renderizar_empty_state(
            icone=ICONE_FINANCEIRO,
            titulo="Nenhum titulo a receber",
            mensagem="Feche um lote de faturamento para gerar titulos a receber.",
        )
        st.caption("Feche um lote de faturamento para gerar títulos a receber.")
        return

    pendentes = [t for t in titulos if t.status == "PENDENTE"]
    st.caption(f"{len(pendentes)} pendentes de {len(titulos)} total")

    linhas = [
        {
            "id": str(t.id),
            "valor": t.valor,
            "vencimento": t.vencimento,
            "status": t.status,
            "referencia": _conv_label(convs, lotes, t.lote_faturamento_id),
        }
        for t in titulos
    ]

    grid = renderizar_grid(
        linhas,
        colunas=_COLUNAS_RECEBER,
        chave="grid_receber",
        selecao="linha",
        altura=380,
    )

    titulo = grid.selecionado
    if titulo is None:
        st.caption("Selecione um titulo na tabela para dar baixa.")
        return

    st.divider()
    if titulo["status"] != "PENDENTE":
        st.caption(f"Titulo {titulo['status'].lower()} — nenhuma acao disponivel.")
        return

    if st.button("Dar baixa no titulo selecionado", type="primary"):
        _dialogo_baixa_receber(titulo)


def _render_pagar() -> None:
    renderizar_secao(titulo="Contas a Pagar")

    with session_scope() as session:
        titulos = pagar_todos(session)

    if not titulos:
        renderizar_empty_state(
            icone=ICONE_FINANCEIRO,
            titulo="Nenhum titulo a pagar",
            mensagem="Os titulos a pagar gerados a partir de pedidos de compra aparecerao aqui.",
        )
        st.caption("Execute o seeder financeiro ou crie pedidos de compra (Compras).")
        return

    pendentes = [t for t in titulos if t.status == "PENDENTE"]
    st.caption(f"{len(pendentes)} pendentes de {len(titulos)} total")

    linhas = [
        {
            "id": str(t.id),
            "valor": t.valor,
            "vencimento": t.vencimento,
            "status": t.status,
            "referencia": (
                f"Pedido {str(t.pedido_compra_id)[:8]}" if t.pedido_compra_id
                else "Lancamento manual"
            ),
        }
        for t in titulos
    ]

    grid = renderizar_grid(
        linhas,
        colunas=_COLUNAS_PAGAR,
        chave="grid_pagar",
        selecao="linha",
        altura=380,
    )

    titulo = grid.selecionado
    if titulo is None:
        st.caption("Selecione um titulo na tabela para dar baixa.")
        return

    st.divider()
    if titulo["status"] != "PENDENTE":
        st.caption(f"Titulo {titulo['status'].lower()} — nenhuma acao disponivel.")
        return

    if st.button("Confirmar pagamento do titulo selecionado", type="primary"):
        _dialogo_baixa_pagar(titulo)


def _conv_label(convs, lotes, lote_id):
    convenio_id = lotes.get(lote_id)
    if convenio_id:
        nome = convs.get(convenio_id)
        if nome:
            return f"Lote → {nome}"
    return "Lote (Particular)"



if __name__ == "__main__":
    main()


_COLUNAS_RECEBER = [
    ColunaGrid("valor", "Valor", tipo="moeda", largura=140),
    ColunaGrid("vencimento", "Vencimento", tipo="data", largura=140),
    ColunaGrid("status", "Status", largura=120),
    ColunaGrid("referencia", "Convenio / lote"),
    ColunaGrid("id", "id", oculta=True),
]

_COLUNAS_PAGAR = [
    ColunaGrid("valor", "Valor", tipo="moeda", largura=140),
    ColunaGrid("vencimento", "Vencimento", tipo="data", largura=140),
    ColunaGrid("status", "Status", largura=120),
    ColunaGrid("referencia", "Origem"),
    ColunaGrid("id", "id", oculta=True),
]


@st.dialog("Baixar titulo a receber")
def _dialogo_baixa_receber(titulo: dict) -> None:
    """Baixa com dialogo no lugar do formulario inline por linha (bug U4)."""
    valor_total = float(titulo["valor"])
    st.write(f"Titulo de **{formatar_brl(valor_total)}**")
    st.caption(f"{titulo['referencia']} · vence em {titulo['vencimento'].strftime('%d/%m/%Y')}")

    valor_pago = st.number_input(
        "Valor recebido (R$)", min_value=0.01, value=valor_total, step=1.0
    )
    observacao = st.text_input("Observacao")

    if valor_pago < valor_total:
        st.warning(
            f"Recebimento menor que o titulo em {formatar_brl(valor_total - valor_pago)}. "
            "A divergenca fica registrada na aba Conciliacoes."
        )

    coluna_ok, coluna_cancelar = st.columns(2)
    with coluna_ok:
        if st.button("Confirmar baixa", type="primary", width="stretch"):
            with tratar_erros("baixar o titulo") as resultado, session_scope() as session:
                baixar_receber(
                    session, titulo["id"], valor_pago, observacao or None,
                    usuario_id=usuario_id_logado(),
                )
            if resultado:
                st.toast(f"Titulo baixado: {formatar_brl(valor_pago)}.")
                st.rerun()
    with coluna_cancelar:
        if st.button("Cancelar", width="stretch"):
            st.rerun()


@st.dialog("Confirmar pagamento")
def _dialogo_baixa_pagar(titulo: dict) -> None:
    st.write(f"Titulo de **{formatar_brl(float(titulo['valor']))}**")
    st.caption(f"{titulo['referencia']} · vence em {titulo['vencimento'].strftime('%d/%m/%Y')}")
    observacao = st.text_input("Observacao")

    coluna_ok, coluna_cancelar = st.columns(2)
    with coluna_ok:
        if st.button("Confirmar pagamento", type="primary", width="stretch"):
            with tratar_erros("pagar o titulo") as resultado, session_scope() as session:
                baixar_pagar(
                    session, titulo["id"], observacao or None, usuario_id=usuario_id_logado()
                )
            if resultado:
                st.toast("Titulo pago.")
                st.rerun()
    with coluna_cancelar:
        if st.button("Cancelar", width="stretch"):
            st.rerun()
