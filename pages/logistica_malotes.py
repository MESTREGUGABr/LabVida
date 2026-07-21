import streamlit as st

from src.atendimento.amostra.service import listar_amostras_coletadas
from src.cadastro.unidade.service import listar_unidades_ativas
from src.db import session_scope
from src.logistica.malote.dtos import MaloteCreate, StatusMalote
from src.logistica.malote.errors import LogisticaError
from src.logistica.malote.service import (
    adicionar_amostra_ao_malote,
    criar_malote,
    despachar_malote,
    listar_malotes_por_unidade_origem,
    obter_malote,
)
from src.ui import exigir_login, usuario_id_logado


def main() -> None:
    st.set_page_config(page_title="LabVida - Gestão de Malotes", layout="wide")
    exigir_login()

    st.title("Gestão de Malotes")
    st.caption("Criação, vinculação de amostras e despacho de malotes entre unidades")

    usuario_id = usuario_id_logado()

    with session_scope() as session:
        unidades = listar_unidades_ativas(session)
        unidades_coleta = [u for u in unidades if u.tipo == "COLETA"]
        unidades_central = [u for u in unidades if u.tipo == "CENTRAL"]
        amostras_coletadas = listar_amostras_coletadas(session)

    if not unidades:
        st.warning("Nenhuma unidade cadastrada no sistema.")
        return

    tab1, tab2 = st.tabs(["✨ Criar e Despachar Malote", "📋 Histórico de Malotes"])

    with tab1:
        st.subheader("1. Criar Novo Malote")
        col1, col2 = st.columns(2)
        with col1:
            origem_opcoes = {f"{u.nome} ({u.tipo})": u.id for u in (unidades_coleta or unidades)}
            origem_label = st.selectbox("Unidade de Origem (Posto de Coleta)", options=list(origem_opcoes.keys()), key="origem")
            origem_id = origem_opcoes[origem_label]

        with col2:
            destino_opcoes = {f"{u.nome} ({u.tipo})": u.id for u in (unidades_central or unidades)}
            destino_label = st.selectbox("Unidade de Destino (Laboratório Central)", options=list(destino_opcoes.keys()), key="destino")
            destino_id = destino_opcoes[destino_label]

        if st.button("Criar Malote", type="primary"):
            try:
                dto = MaloteCreate(
                    unidade_origem_id=origem_id,
                    unidade_destino_id=destino_id,
                    enviado_por_usuario_id=usuario_id,
                )
                with session_scope() as session:
                    malote = criar_malote(session, dto)
                st.success(f"Malote **{malote.codigo_malote}** criado com sucesso!")
                st.rerun()
            except LogisticaError as e:
                st.error(str(e))

        st.divider()
        st.subheader("2. Adicionar Amostras e Despachar")

        with session_scope() as session:
            malotes_abertos = [m for m in listar_malotes_por_unidade_origem(session, origem_id) if m.status == StatusMalote.ABERTO]

        if not malotes_abertos:
            st.info("Nenhum malote ABERTO disponível nesta unidade de origem.")
        else:
            malote_opcoes = {f"{m.codigo_malote} ({len(m.itens)} amostras)": m.id for m in malotes_abertos}
            malote_label = st.selectbox("Selecione o Malote", options=list(malote_opcoes.keys()))
            malote_id = malote_opcoes[malote_label]

            col_a, col_b = st.columns(2)
            with col_a:
                st.write("**Adicionar Amostra ao Malote**")
                if not amostras_coletadas:
                    st.caption("Nenhuma amostra COLETADA pendente de envio.")
                else:
                    amostra_opcoes = {f"Tubo {a.codigo_barras} ({a.tipo_material})": a.id for a in amostras_coletadas}
                    amostra_label = st.selectbox("Amostras Coletadas", options=list(amostra_opcoes.keys()))
                    amostra_id = amostra_opcoes[amostra_label]

                    if st.button("Adicionar ao Malote"):
                        try:
                            with session_scope() as session:
                                adicionar_amostra_ao_malote(session, malote_id, amostra_id)
                            st.success("Amostra adicionada ao malote!")
                            st.rerun()
                        except LogisticaError as e:
                            st.error(str(e))

            with col_b:
                st.write("**Despachar Malote**")
                with session_scope() as session:
                    malote_atual = obter_malote(session, malote_id)

                if malote_atual and malote_atual.itens:
                    st.write(f"Total de itens no malote: **{len(malote_atual.itens)}**")
                    if st.button("🚀 Despachar Malote (Em Trânsito)", type="primary"):
                        try:
                            with session_scope() as session:
                                despachar_malote(session, malote_id, usuario_id)
                            st.success(f"Malote **{malote_atual.codigo_malote}** despachado com sucesso!")
                            st.rerun()
                        except LogisticaError as e:
                            st.error(str(e))
                else:
                    st.caption("Adicione pelo menos uma amostra antes de despachar.")

    with tab2:
        with session_scope() as session:
            todos_malotes = listar_malotes_por_unidade_origem(session, origem_id)

        if todos_malotes:
            st.dataframe(
                [
                    {
                        "Código": m.codigo_malote,
                        "Status": m.status,
                        "Criado em": m.criado_em.strftime("%d/%m/%Y %H:%M"),
                        "Despachado em": m.despachado_em.strftime("%d/%m/%Y %H:%M") if m.despachado_em else "—",
                        "Nº Amostras": len(m.itens),
                    }
                    for m in todos_malotes
                ],
                hide_index=True,
                use_container_width=True,
            )
        else:
            st.info("Nenhum malote registrado para esta unidade.")


if __name__ == "__main__":
    main()
