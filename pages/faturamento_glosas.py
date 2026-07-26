import streamlit as st

from src.db import session_scope
from src.faturamento.glosa.dtos import GlosaCreate
from src.faturamento.glosa.errors import GlosaError
from src.faturamento.glosa.service import (
    listar_glosas_com_contexto,
    listar_guias_itens_faturados,
    registrar_glosa,
)
from src.ui import renderizar_menu, shell
from src.ui_components import renderizar_cabecalho, renderizar_empty_state, renderizar_secao
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

    for item in itens:
        guia_item_id = item["guia_item_id"]

        with st.container(border=True):
            col_info, col_btn = st.columns([4, 1])
            with col_info:
                st.write(f"**Lote:** {item['codigo_lote']} | **Convênio:** {item['convenio_nome']}")
                st.write(f"**Procedimento:** {item['procedimento_nome']} | **Valor faturado:** R$ {item['valor_faturado']:.2f}")
                st.caption(f"Unidade: {item['unidade_nome']}")
            with col_btn:
                expandir = st.button("Registrar Glosa", key=f"btn_glosa_{guia_item_id}")

            if expandir or st.session_state.get(f"show_form_{guia_item_id}", False):
                st.session_state[f"show_form_{guia_item_id}"] = True

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

                if st.button("Cancelar", key=f"cancelar_{guia_item_id}"):
                    st.session_state[f"show_form_{guia_item_id}"] = False
                    st.rerun()


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


if __name__ == "__main__":
    main()
