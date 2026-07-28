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
    validar_lote,
)
from src.ui import renderizar_menu, shell, usuario_id_logado
from src.ui_components import (
    renderizar_cabecalho,
    renderizar_empty_state,
    renderizar_secao,
)
from src.ui_icons import (
    ICONE_AMOSTRA,
    ICONE_CONVENIO,
    ICONE_FATURAMENTO,
    ICONE_OS,
    ICONE_PRODUTIVIDADE,
)

_PARTICULAR = "Particular (sem convenio)"


def _convenio_label(c) -> str:
    ans = c.registro_ans or "sem ANS"
    return f"{c.nome} ({ans})"


def main() -> None:
    ctx = shell("LabVida - Faturamento de Guias", layout="wide", permissao="faturamento:gerenciar_lotes")
    renderizar_menu(ctx["usuario_id"])

    renderizar_cabecalho(
        titulo="Faturamento de Guias TISS",
        subtitulo="Criacao de lotes por convenio, inclusao de laudos liberados e fechamento para cobranca",
        icone=ICONE_FATURAMENTO,
    )

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
    renderizar_secao(
        titulo=f"{ICONE_AMOSTRA} Novo Lote de Faturamento",
        descricao="Crie um lote para agrupar laudos a faturar por convenio",
    )

    if not convenios_ativos:
        renderizar_empty_state(
            icone=ICONE_CONVENIO,
            titulo="Nenhum convenio ativo",
            mensagem="Cadastre um convenio ativo para criar lotes de faturamento.",
        )
        return

    convenio_opcoes = {_convenio_label(c): c.id for c in convenios_ativos}
    convenio_opcoes[_PARTICULAR] = None

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        convenio_label = st.selectbox(
            "Convenio", options=list(convenio_opcoes.keys()), key="novo_lote_convenio"
        )
    convenio_id = convenio_opcoes[convenio_label]

    with session_scope() as session:
        pendentes = contar_laudos_pendentes(session, convenio_id)
    with col2:
        st.markdown(
            f"<p style='color:#757575;font-size:13px;margin-top:28px;'>{pendentes} laudos pendentes</p>",
            unsafe_allow_html=True,
        )

    with col3:
        if st.button("Criar Lote", type="primary", key="criar_lote_btn", width="stretch"):
            try:
                dto = LoteFaturamentoCreate(convenio_id=convenio_id)
                with session_scope() as session:
                    lote = criar_lote(session, dto)
                st.toast(f"Lote {lote.codigo_lote} criado com sucesso!")
                st.rerun()
            except FaturamentoError as e:
                st.error(str(e))


def _render_lotes_abertos(lotes, todos_convenios) -> None:
    renderizar_secao(
        titulo=f"{ICONE_OS} Lotes Abertos",
        descricao="Adicione laudos e feche os lotes para gerar titulos a receber",
    )

    lotes_abertos = [l for l in lotes if l.status == "ABERTO"]

    if not lotes_abertos:
        renderizar_empty_state(
            icone=ICONE_AMOSTRA,
            titulo="Nenhum lote aberto",
            mensagem="Crie um lote na secao acima para comecar o faturamento.",
        )
        return

    for lote in lotes_abertos:
        nome_convenio = todos_convenios.get(lote.convenio_id, _PARTICULAR)
        total_itens = sum(len(g.itens) for g in lote.guias)

        toggle_key = f"expand_lote_{lote.id}"
        if toggle_key not in st.session_state:
            st.session_state[toggle_key] = total_itens == 0

        aberto = st.session_state[toggle_key]
        prefixo = "\u2013" if aberto else "+"

        col_toggle, col_label = st.columns([0.5, 9.5])
        with col_toggle:
            if st.button(
                prefixo,
                key=f"btn_lote_{lote.id}",
                use_container_width=True,
            ):
                st.session_state[toggle_key] = not aberto
                st.rerun()
        with col_label:
            st.markdown(
                f"**{lote.codigo_lote}** \u2014 {nome_convenio} \u2014 "
                f"{total_itens} itens \u2014 R$ {lote.valor_total:.2f}"
            )

        if aberto:
            with session_scope() as session:
                laudos_pendentes = listar_laudos_pendentes_por_convenio(session, lote.convenio_id)

            if not laudos_pendentes:
                st.caption("Nenhum laudo liberado pendente para este convenio.")
                if total_itens > 0:
                    _render_fechar_lote(lote)
                else:
                    st.caption(f"Itens faturados: {total_itens}")
            else:
                st.write(f"**{len(laudos_pendentes)} laudos disponiveis para faturamento:**")

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
                        valor_default = float(laudo_info.get("valor_negociado", 50.0))
                        valor = st.number_input(
                            "R$", min_value=0.01, value=valor_default, step=1.0,
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
                        st.caption(f"Ja faturados neste lote: {total_itens} itens")

                if total_itens > 0:
                    st.divider()
                    _render_fechar_lote(lote)


def _render_fechar_lote(lote) -> None:
    venc = date.today() + timedelta(days=30)
    st.caption(
        f"Ao fechar, sera gerado um titulo a receber de "
        f"**R$ {lote.valor_total:.2f}** com vencimento em **{venc.strftime('%d/%m/%Y')}**."
    )

    resultado_key = f"validacao_{lote.id}"
    aprovado = st.session_state.get(resultado_key, False)

    c_val, c_fech = st.columns([1, 1])
    with c_val:
        if st.button("Validar lote", type="secondary", key=f"validar_{lote.id}"):
            try:
                with session_scope() as session:
                    resultado = validar_lote(session, lote.id)
                if resultado["ok"]:
                    st.session_state[resultado_key] = True
                    st.toast("Pré-auditoria aprovada! O lote pode ser fechado.")
                else:
                    st.session_state[resultado_key] = False
                    st.session_state[f"problemas_{lote.id}"] = resultado["problemas"]
                st.rerun()
            except FaturamentoError as e:
                st.error(str(e))

    problemas = st.session_state.get(f"problemas_{lote.id}")
    if problemas:
        for p in problemas:
            st.error(p)
        st.caption("Corrija os problemas antes de fechar o lote.")

    with c_fech:
        fechar_label = "Finalizar Faturamento" if aprovado else "Finalizar Faturamento (valide primeiro)"
        if st.button(fechar_label, type="primary", key=f"fechar_{lote.id}", disabled=not aprovado):
            try:
                with session_scope() as session:
                    fechar_lote(session, lote.id, usuario_id_logado())
                st.session_state.pop(resultado_key, None)
                st.session_state.pop(f"problemas_{lote.id}", None)
                st.toast(f"Lote {lote.codigo_lote} fechado! Titulo a receber gerado.")
                st.rerun()
            except FaturamentoError as e:
                st.error(str(e))


def _render_historico(lotes, todos_convenios) -> None:
    renderizar_secao(
        titulo=f"{ICONE_PRODUTIVIDADE} Historico de Lotes",
        descricao="Todos os lotes de faturamento registrados no sistema",
    )

    if not lotes:
        renderizar_empty_state(
            icone=ICONE_PRODUTIVIDADE,
            titulo="Nenhum lote registrado",
            mensagem="O historico de lotes de faturamento aparecera aqui.",
        )
        return

    rows = []
    for l in lotes:
        total_itens = sum(len(g.itens) for g in l.guias)
        rows.append({
            "Codigo": l.codigo_lote,
            "Convenio": todos_convenios.get(l.convenio_id, _PARTICULAR),
            "Status": l.status,
            "Valor Total": f"R$ {l.valor_total:.2f}",
            "Itens": total_itens,
            "Criado em": l.criado_em.strftime("%d/%m/%Y %H:%M") if l.criado_em else "\u2014",
            "Fechado em": l.fechado_em.strftime("%d/%m/%Y %H:%M") if l.fechado_em else "\u2014",
        })
    st.dataframe(rows, hide_index=True, width="stretch")


if __name__ == "__main__":
    main()
