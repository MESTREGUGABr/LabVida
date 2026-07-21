import streamlit as st

from src.cadastro.unidade.service import listar_unidades_ativas
from src.db import session_scope
from src.logistica.malote.service import listar_malotes_em_transito_para_unidade, obter_malote
from src.logistica.recebimento.dtos import ProtocoloRecebimentoCreate
from src.logistica.recebimento.errors import LogisticaError
from src.logistica.recebimento.service import obter_protocolo, receber_malote
from src.ui import exigir_login, usuario_id_logado


def main() -> None:
    st.set_page_config(page_title="LabVida - Recepção Central", layout="wide")
    exigir_login()

    st.title("Recepção de Malotes — Laboratório Central")
    st.caption("Conferência física, checagem de integridade e entrada das amostras no setor técnico")

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

    st.subheader(f"Conferência do Malote: {malote.codigo_malote}")
    st.write(f"Quantidade de tubos/amostras esperados: **{len(malote.itens)}**")

    if malote.itens:
        st.dataframe(
            [{"Item ID": str(item.id), "Amostra ID": str(item.amostra_id)} for item in malote.itens],
            hide_index=True,
            use_container_width=True,
        )

    integridade_ok = st.radio(
        "Integridade das Amostras",
        options=[True, False],
        format_func=lambda ok: "✅ Íntegras (sem vazamento/ranhura) — aceitar todas" if ok else "❌ Danificadas/Rejeitadas — recusar todas",
    )

    observacao = st.text_area("Observações da recepção (opcional)", placeholder="Ex: Malote chegou com gelo adequado e sem avarias.")

    if st.button("Confirmar Recebimento", type="primary"):
        try:
            dto = ProtocoloRecebimentoCreate(
                malote_id=malote.id,
                recebido_por_usuario_id=usuario_id,
                integridade_ok=integridade_ok,
                observacao=observacao,
            )
            with session_scope() as session:
                protocolo = receber_malote(session, dto)
            
            if integridade_ok:
                st.success(f"Malote **{malote.codigo_malote}** recebido com sucesso! Amostras liberadas para o setor Laboratorial (`EM_ANALISE`).")
            else:
                st.warning(f"Malote **{malote.codigo_malote}** registrado com amostras recusadas (`REJEITADA`). Notificação gerada.")
            st.rerun()
        except LogisticaError as e:
            st.error(str(e))


if __name__ == "__main__":
    main()
