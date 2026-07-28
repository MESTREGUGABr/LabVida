import streamlit as st

from src.cadastro.convenio.service import listar_convenios
from src.db import session_scope
from src.faturamento.lote_faturamento.service import listar_lotes
from src.financeiro.titulo_receber.errors import FinanceiroError
from src.financeiro.titulo_receber.service import (
    baixar_titulo as baixar_receber,
    listar_todos as receber_todos,
)
from src.financeiro.titulo_pagar.errors import TituloPagarJaBaixado, TituloPagarNaoEncontrado
from src.financeiro.titulo_pagar.service import (
    baixar_titulo as baixar_pagar,
    listar_todos as pagar_todos,
)
from src.financeiro.conciliacao_pagamento.service import listar_todas as conciliacoes_todas
from src.ui import renderizar_menu, shell, usuario_id_logado
from src.ui_components import renderizar_cabecalho, renderizar_empty_state, renderizar_secao, renderizar_status_badge
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

    for t in titulos:
        status_tipo = "success" if t.status == "PAGO" else "warning" if t.status == "PENDENTE" else "error"
        ref = _conv_label(convs, lotes, t.lote_faturamento_id)

        with st.container(border=True):
            c1, c2 = st.columns([4, 1])
            with c1:
                st.metric(f"R$ {t.valor:.2f}", f"Vencimento: {t.vencimento.strftime('%d/%m/%Y')}")
                st.caption(f"Status: {t.status} | {ref}")
            with c2:
                st.write("")
                renderizar_status_badge(t.status, status_tipo)
                if t.status == "PENDENTE":
                    if st.button("Baixar", key=f"receber_{t.id}"):
                        st.session_state[f"form_receber_{t.id}"] = True

            if st.session_state.get(f"form_receber_{t.id}", False):
                col_a, col_b = st.columns(2)
                with col_a:
                    valor_pago = st.number_input(
                        "Valor recebido (R$)",
                        min_value=0.01,
                        value=float(t.valor),
                        step=1.0,
                        key=f"valor_rec_{t.id}",
                    )
                with col_b:
                    obs = st.text_input("Observação", key=f"obs_rec_{t.id}")
                    c_confirm, c_cancel = st.columns(2)
                    with c_confirm:
                        if st.button("Confirmar", type="primary", key=f"conf_rec_{t.id}"):
                            try:
                                with session_scope() as session:
                                    resultado = baixar_receber(
                                        session, t.id, valor_pago, obs or None,
                                        usuario_id=usuario_id_logado(),
                                    )
                                divergencia = resultado.valor - valor_pago
                                if divergencia > 0:
                                    st.toast(f"Recebido R$ {valor_pago:.2f}. Divergência: R$ {divergencia:.2f}")
                                else:
                                    st.toast(f"Título de R$ {t.valor:.2f} baixado com sucesso!")
                                st.session_state.pop(f"form_receber_{t.id}", None)
                                st.rerun()
                            except FinanceiroError as e:
                                st.error(str(e))
                    with c_cancel:
                        if st.button("Cancelar", key=f"cancel_rec_{t.id}"):
                            st.session_state.pop(f"form_receber_{t.id}", None)
                            st.rerun()


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

    for t in titulos:
        emoji = "🟢" if t.status == "PAGO" else "🟡"
        ref = f"Pedido: {str(t.pedido_compra_id)[:12]}..." if t.pedido_compra_id else "Lançamento manual"

        with st.container(border=True):
            c1, c2 = st.columns([4, 1])
            with c1:
                st.write(f"{emoji} **R$ {t.valor:.2f}** — Vencimento: {t.vencimento.strftime('%d/%m/%Y')}")
                st.caption(f"Status: {t.status} | {ref}")
            with c2:
                if t.status == "PENDENTE":
                    if st.button("Baixar", key=f"pagar_{t.id}"):
                        st.session_state[f"form_pagar_{t.id}"] = True

            if st.session_state.get(f"form_pagar_{t.id}", False):
                obs = st.text_input("Observação", key=f"obs_pag_{t.id}")
                c_confirm, c_cancel = st.columns(2)
                with c_confirm:
                    if st.button("Confirmar Pagamento", type="primary", key=f"conf_pag_{t.id}"):
                        try:
                            with session_scope() as session:
                                baixar_pagar(session, t.id, obs or None, usuario_id=usuario_id_logado())
                            st.toast(f"Título de R$ {t.valor:.2f} pago com sucesso!")
                            st.session_state.pop(f"form_pagar_{t.id}", None)
                            st.rerun()
                        except (TituloPagarNaoEncontrado, TituloPagarJaBaixado, FinanceiroError) as e:
                            st.error(str(e))
                with c_cancel:
                    if st.button("Cancelar", key=f"cancel_pag_{t.id}"):
                        st.session_state.pop(f"form_pagar_{t.id}", None)
                        st.rerun()


def _conv_label(convs, lotes, lote_id):
    convenio_id = lotes.get(lote_id)
    if convenio_id:
        nome = convs.get(convenio_id)
        if nome:
            return f"Lote → {nome}"
    return "Lote (Particular)"



if __name__ == "__main__":
    main()
