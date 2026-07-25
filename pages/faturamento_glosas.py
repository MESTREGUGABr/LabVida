import streamlit as st

from src.db import session_scope
from src.faturamento.glosa.dtos import GlosaCreate
from src.faturamento.glosa.errors import GlosaError
from src.faturamento.glosa.service import (
    listar_glosas_com_contexto,
    listar_guias_itens_faturados,
    registrar_glosa,
)
from src.ui import exigir_login

_MOTIVOS_PADRAO = [
    "Erro de digitação no código TUSS",
    "Procedimento não autorizado pelo convênio",
    "Divergência de valores",
    "Falta de documentação",
    "Paciente não elegível",
    "Outro",
]


def main() -> None:
    st.set_page_config(page_title="LabVida - Controle de Glosas", layout="wide")
    exigir_login()

    st.title("Controle de Glosas")
    st.caption("Registro e acompanhamento de glosas (recusas de pagamento por convênio)")

    tab1, tab2 = st.tabs(["Registrar Glosa", "Glosas Registradas"])

    with tab1:
        _render_registrar_glosa()
    with tab2:
        _render_listar_glosas()


def _render_registrar_glosa() -> None:
    st.subheader("Itens Faturados")

    with session_scope() as session:
        itens = listar_guias_itens_faturados(session)

    if not itens:
        st.info("Nenhum item faturado disponível para registro de glosa.")
        st.caption("Fature laudos na tela de Faturamento de Guias TISS antes de registrar glosas.")
        return

    st.caption(f"{len(itens)} itens faturados encontrados")

    for item in itens:
        guia_item_id = item["guia_item_id"]

        with st.container(border=True):
            col_info, col_btn = st.columns([4, 1])
            with col_info:
                st.write(f"**Lote:** {item['codigo_lote']} | **Convênio:** {item['convenio_nome']}")
                st.write(f"**Procedimento:** {item['procedimento_nome']} | **Valor faturado:** R$ {item['valor_faturado']:.2f}")
                st.caption(f"Unidade: {item['unidade_nome']}")
            with col_btn:
                form_aberto = st.session_state.get(f"show_form_{guia_item_id}", False)
                btn_label = "Fechar" if form_aberto else "Registrar Glosa"
                if st.button(btn_label, key=f"btn_glosa_{guia_item_id}"):
                    if form_aberto:
                        st.session_state[f"show_form_{guia_item_id}"] = False
                        st.rerun()
                    else:
                        st.session_state[f"show_form_{guia_item_id}"] = True
                        st.rerun()

            if st.session_state.get(f"show_form_{guia_item_id}", False):

                motivo_opcoes = _MOTIVOS_PADRAO
                motivo = st.selectbox("Motivo", options=motivo_opcoes, key=f"motivo_{guia_item_id}")

                if motivo == "Outro":
                    motivo = st.text_input("Descreva o motivo", key=f"motivo_outro_{guia_item_id}")

                col1, col2 = st.columns(2)
                with col1:
                    valor_glosado = st.number_input(
                        "Valor Glosado (R$)",
                        min_value=0.01,
                        max_value=float(item["valor_faturado"]),
                        value=float(item["valor_faturado"]),
                        step=1.0,
                        key=f"valor_glosa_{guia_item_id}",
                    )
                with col2:
                    st.write("")
                    st.caption(f"Unidade de origem: **{item['unidade_nome']}** (detectada automaticamente)")

                if st.button("Confirmar Glosa", type="primary", key=f"confirmar_{guia_item_id}"):
                    try:
                        dto = GlosaCreate(
                            guia_item_id=guia_item_id,
                            motivo=motivo.strip(),
                            valor_glosado=valor_glosado,
                        )
                        with session_scope() as session:
                            registrar_glosa(session, dto)
                        st.toast("Glosa registrada com sucesso!")
                        st.session_state[f"show_form_{guia_item_id}"] = False
                        st.rerun()
                    except ValueError as e:
                        st.error(str(e))
                    except GlosaError as e:
                        st.error(str(e))


def _render_listar_glosas() -> None:
    st.subheader("Glosas Registradas")

    with session_scope() as session:
        glosas = listar_glosas_com_contexto(session)

    if not glosas:
        st.info("Nenhuma glosa registrada.")
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

    st.dataframe(rows, hide_index=True, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total de Glosas", len(glosas))
    with col2:
        st.metric("Valor Total Glosado", f"R$ {total_glosado:.2f}")


if __name__ == "__main__":
    main()
