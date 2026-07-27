import streamlit as st

from src.cadastro.unidade.service import listar_unidades_ativas
from src.db import session_scope
from src.logistica.malote.service import listar_malotes_em_transito_para_unidade, obter_malote
from src.logistica.recebimento.dtos import ProtocoloRecebimentoCreate
from src.logistica.recebimento.errors import LogisticaError
from src.logistica.recebimento.service import (
    listar_amostras_do_malote,
    obter_protocolo,
    receber_malote,
)
from src.ui import renderizar_menu, shell, usuario_id_logado
from src.ui_components import renderizar_cabecalho
from src.ui_icons import ICONE_RECEPCAO, ICONE_OK


def main() -> None:
    ctx = shell("LabVida - Recepção Central", layout="wide", permissao="logistica:receber_malote")
    renderizar_menu(ctx["usuario_id"])

    renderizar_cabecalho(
        titulo="Recepcao de Malotes",
        subtitulo="Conferencia fisica, checagem de integridade e entrada das amostras no setor tecnico — Laboratorio Central",
        icone=ICONE_RECEPCAO,
    )

    usuario_id = usuario_id_logado()

    with session_scope() as session:
        unidades = listar_unidades_ativas(session)
        unidades_central = [u for u in unidades if u.tipo == "CENTRAL"] or unidades

    origem_opcoes = {u.nome: u.id for u in unidades_central}
    unidade_label = st.selectbox("Unidade Central Atual", options=list(origem_opcoes.keys()))
    central_id = origem_opcoes[unidade_label]

    with session_scope() as session:
        malotes_em_transito = listar_malotes_em_transito_para_unidade(session, central_id)

    if not malotes_em_transito:
        st.info("Nenhum malote EM TRÂNSITO aguardando recepção no momento.")
        return

    malote_opcoes = {f"{m.codigo_malote} ({len(m.itens)} amostras)": m.id for m in malotes_em_transito}
    malote_label = st.selectbox("Selecione o Malote para Recebimento", options=list(malote_opcoes.keys()))
    malote_id = malote_opcoes[malote_label]

    with session_scope() as session:
        malote = obter_malote(session, malote_id)
        amostras = listar_amostras_do_malote(session, malote_id)

    st.subheader(f"Conferência do Malote: {malote.codigo_malote}")
    st.write(f"Quantidade de tubos/amostras esperados: **{len(amostras)}**")

    if amostras:
        st.dataframe(
            [
                {
                    "Código de barras": a.codigo_barras,
                    "Material": a.tipo_material.value,
                    "Status atual": a.status.value,
                }
                for a in amostras
            ],
            hide_index=True,
            width="stretch",
        )

    # Issue #16: recusar amostras individualmente (não mais tudo-ou-nada).
    rotulo_por_amostra = {
        a.id: f"{a.codigo_barras} — {a.tipo_material.value}" for a in amostras
    }
    rejeitadas_labels = st.multiselect(
        "Amostras danificadas/rejeitadas (deixe vazio para aceitar todas)",
        options=list(rotulo_por_amostra.values()),
        help="Selecione apenas as amostras com vazamento/ranhura. As demais entram como RECEBIDA.",
    )
    label_para_id = {label: aid for aid, label in rotulo_por_amostra.items()}
    amostras_rejeitadas = {label_para_id[label] for label in rejeitadas_labels}

    if amostras_rejeitadas:
        st.warning(
            f"{len(amostras_rejeitadas)} de {len(amostras)} amostra(s) serão recusadas; "
            f"as demais serão aceitas."
        )
    else:
        st.caption(f"{ICONE_OK} Todas as amostras serão aceitas como íntegras.")

    observacao = st.text_area(
        "Observações da recepção (opcional)",
        placeholder="Ex: Malote chegou com gelo adequado; tubo X com ranhura.",
    )

    if st.button("Confirmar Recebimento", type="primary"):
        try:
            dto = ProtocoloRecebimentoCreate(
                malote_id=malote.id,
                recebido_por_usuario_id=usuario_id,
                integridade_ok=not amostras_rejeitadas,
                observacao=observacao,
                amostras_rejeitadas=amostras_rejeitadas,
            )
            with session_scope() as session:
                receber_malote(session, dto)

            aceitas = len(amostras) - len(amostras_rejeitadas)
            if not amostras_rejeitadas:
                st.success(
                    f"Malote **{malote.codigo_malote}** recebido! {aceitas} amostra(s) "
                    f"liberadas para o Laboratorial (`EM_ANALISE`)."
                )
            else:
                st.warning(
                    f"Malote **{malote.codigo_malote}** conferido: {aceitas} aceita(s) e "
                    f"{len(amostras_rejeitadas)} recusada(s) (`REJEITADA`)."
                )
            st.rerun()
        except LogisticaError as e:
            st.error(str(e))


if __name__ == "__main__":
    main()
