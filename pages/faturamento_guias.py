import streamlit as st
from datetime import date, timedelta

from src.cadastro.convenio.service import listar_convenios, listar_convenios_ativos
from src.db import session_scope
from src.faturamento.lote_faturamento.dtos import GuiaItemCreate, LoteFaturamentoCreate
from src.faturamento.lote_faturamento.errors import FaturamentoError
from src.faturamento.lote_faturamento.service import (
    adicionar_itens_ao_lote,
    contar_laudos_pendentes,
    criar_lote,
    fechar_lote,
    listar_laudos_pendentes_por_convenio,
    listar_lotes,
)
from src.ui import renderizar_menu, shell, usuario_id_logado

_PARTICULAR = "Particular (sem convênio)"


def _convenio_label(c) -> str:
    ans = c.registro_ans or "sem ANS"
    return f"{c.nome} ({ans})"


def main() -> None:
    ctx = shell("LabVida - Faturamento de Guias", layout="wide", permissao="faturamento:gerenciar_lotes")
    renderizar_menu(ctx["usuario_id"])

    st.title("Faturamento de Guias TISS")
    st.caption("Criação de lotes por convênio, inclusão de laudos liberados e fechamento para cobrança")

    with session_scope() as session:
        todos_convenios = {c.id: c.nome for c in listar_convenios(session)}
        convenios_ativos = listar_convenios_ativos(session)
        lotes = listar_lotes(session)

    st.divider()
    _render_novo_lote(convenios_ativos)
    st.divider()
    _render_lotes_abertos(lotes, todos_convenios)
    st.divider()
    _render_historico(lotes, todos_convenios)


def _render_novo_lote(convenios_ativos) -> None:
    st.subheader("Novo Lote de Faturamento")

    if not convenios_ativos:
        st.warning("Nenhum convênio ativo cadastrado.")
        return

    convenio_opcoes = {_convenio_label(c): c.id for c in convenios_ativos}
    convenio_opcoes[_PARTICULAR] = None
    convenio_label = st.selectbox("Convênio", options=list(convenio_opcoes.keys()), key="novo_lote_convenio")
    convenio_id = convenio_opcoes[convenio_label]

    with session_scope() as session:
        pendentes = contar_laudos_pendentes(session, convenio_id)
    st.caption(f"{pendentes} laudos liberados pendentes de faturamento para este convênio")

    col1, col2 = st.columns([3, 1])
    with col2:
        st.write("")
        if st.button("Criar Lote", type="primary", key="criar_lote_btn"):
            try:
                dto = LoteFaturamentoCreate(convenio_id=convenio_id)
                with session_scope() as session:
                    lote = criar_lote(session, dto)
                st.toast(f"Lote {lote.codigo_lote} criado com sucesso!")
                st.rerun()
            except FaturamentoError as e:
                st.error(str(e))


def _render_lotes_abertos(lotes, todos_convenios) -> None:
    st.subheader("Lotes Abertos")

    lotes_abertos = [l for l in lotes if l.status == "ABERTO"]

    if not lotes_abertos:
        st.info("Nenhum lote ABERTO. Crie um lote na seção acima.")
        return

    for lote in lotes_abertos:
        nome_convenio = todos_convenios.get(lote.convenio_id, _PARTICULAR)
        total_itens = sum(len(g.itens) for g in lote.guias)

        with st.expander(
            f"{lote.codigo_lote} — {nome_convenio} — {total_itens} itens — R$ {lote.valor_total:.2f}",
            expanded=total_itens == 0,
        ):
            with session_scope() as session:
                laudos_pendentes = listar_laudos_pendentes_por_convenio(session, lote.convenio_id)

            if not laudos_pendentes:
                st.caption("Nenhum laudo liberado pendente para este convênio.")
                if total_itens > 0:
                    _render_fechar_lote(lote)
                else:
                    st.caption(f"Itens faturados: {total_itens}")
            else:
                st.write(f"**{len(laudos_pendentes)} laudos disponíveis para faturamento:**")

                selecionados = {}
                for laudo_info in laudos_pendentes:
                    laudo_id = laudo_info["laudo_id"]
                    c1, c2, c3, c4 = st.columns([3, 2, 1, 1])
                    with c1:
                        st.write(f"Laudo `{str(laudo_id)[:12]}...`")
                    with c2:
                        st.write(f"Item OS `{str(laudo_info['os_item_id'])[:12]}...`")
                    with c3:
                        valor_key = f"vlr_{lote.id}_{laudo_id}"
                        valor = st.number_input(
                            "R$", min_value=0.01, value=50.00, step=1.0,
                            key=valor_key, label_visibility="collapsed",
                        )
                    with c4:
                        if st.checkbox("Incluir", key=f"chk_{lote.id}_{laudo_id}"):
                            selecionados[laudo_id] = {
                                "procedimento_id": laudo_info["procedimento_id"],
                                "valor": valor,
                            }

                c_btn, c_info = st.columns([2, 3])
                with c_btn:
                    if selecionados and st.button(
                        f"Adicionar {len(selecionados)} itens ao lote",
                        type="primary",
                        key=f"add_{lote.id}",
                    ):
                        dtos = [
                            GuiaItemCreate(
                                laudo_id=laudo_id,
                                procedimento_id=dados["procedimento_id"],
                                valor_faturado=dados["valor"],
                            )
                            for laudo_id, dados in selecionados.items()
                        ]
                        try:
                            with session_scope() as session:
                                adicionar_itens_ao_lote(session, lote.id, dtos)
                            st.toast(f"{len(dtos)} item(ns) adicionado(s) ao lote!")
                            st.rerun()
                        except FaturamentoError as e:
                            st.error(str(e))

                with c_info:
                    if total_itens > 0:
                        st.caption(f"Já faturados neste lote: {total_itens} itens")

                if total_itens > 0:
                    st.divider()
                    _render_fechar_lote(lote)


def _render_fechar_lote(lote) -> None:
    venc = date.today() + timedelta(days=30)
    st.caption(f"Ao fechar, será gerado um título a receber de **R$ {lote.valor_total:.2f}** com vencimento em **{venc.strftime('%d/%m/%Y')}**.")
    if st.button("Finalizar Faturamento", type="primary", key=f"fechar_{lote.id}"):
        try:
            with session_scope() as session:
                fechar_lote(session, lote.id, usuario_id_logado())
            st.toast(f"Lote {lote.codigo_lote} fechado! Título a receber gerado.")
            st.rerun()
        except FaturamentoError as e:
            st.error(str(e))


def _render_historico(lotes, todos_convenios) -> None:
    st.subheader("Histórico de Lotes")

    if not lotes:
        st.info("Nenhum lote registrado.")
        return

    rows = []
    for l in lotes:
        total_itens = sum(len(g.itens) for g in l.guias)
        rows.append({
            "Código": l.codigo_lote,
            "Convênio": todos_convenios.get(l.convenio_id, _PARTICULAR),
            "Status": l.status,
            "Valor Total": f"R$ {l.valor_total:.2f}",
            "Itens": total_itens,
            "Criado em": l.criado_em.strftime("%d/%m/%Y %H:%M") if l.criado_em else "—",
            "Fechado em": l.fechado_em.strftime("%d/%m/%Y %H:%M") if l.fechado_em else "—",
        })
    st.dataframe(rows, hide_index=True, use_container_width=True)


if __name__ == "__main__":
    main()
