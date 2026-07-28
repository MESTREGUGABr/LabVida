import streamlit as st
from sqlalchemy.orm import Session
from sqlalchemy import select

from src.atendimento.ordem_servico.models import OsItem
from src.db import session_scope
from src.laboratorial.dtos import ResultadoCreate, ResultadoUpdate
from src.laboratorial.models import StatusResultado
from src.laboratorial.service import LaboratorialService
from src.ui import renderizar_menu, shell, usuario_id_logado
from src.ui_components import (
    renderizar_cabecalho,
    renderizar_empty_state,
    renderizar_secao,
    renderizar_status_badge,
)
from src.ui_icons import ICONE_ADICIONAR, ICONE_BUSCA, ICONE_PRODUTIVIDADE, ICONE_RESULTADO


def _listar_os_itens(session: Session):
    return session.scalars(select(OsItem)).all()


def main() -> None:
    ctx = shell("Resultados de Exames", layout="wide", permissao="laboratorial:registrar_resultado")
    renderizar_menu(ctx["usuario_id"])

    renderizar_cabecalho(
        titulo="Digitacao e Conferencia de Resultados",
        subtitulo="Selecione um item de Ordem de Servico para lancar ou revisar resultados",
        icone=ICONE_PRODUTIVIDADE,
    )

    with session_scope() as session:
        itens = _listar_os_itens(session)
        if not itens:
            renderizar_empty_state(
                icone=ICONE_PRODUTIVIDADE,
                titulo="Nenhuma OS cadastrada",
                mensagem="Cadastre uma Ordem de Servico para registrar resultados de exames.",
            )
            return

        opcoes_itens = {
            f"{item.ordem_servico.codigo_os} — {item.procedimento.nome}": item
            for item in itens
            if item.ordem_servico
        }

        renderizar_secao(
            titulo=f"{ICONE_BUSCA} Selecionar Exame",
            descricao="Escolha o item de OS para visualizar e lancar resultados",
        )

        escolha = st.selectbox(
            "Selecione a Amostra / Item de OS", options=list(opcoes_itens.keys()),
            label_visibility="collapsed",
        )

        item_selecionado = opcoes_itens[escolha]

        service = LaboratorialService(session)
        resultados_existentes = service.listar_resultados_por_os_item(item_selecionado.id)
        usuario_id = usuario_id_logado()

        renderizar_secao(
            titulo=f"{ICONE_RESULTADO} Resultados do Exame",
            descricao="Resultados ja registrados para este item de OS",
        )

        if resultados_existentes:
            for res in resultados_existentes:
                status_label = res.status.value
                status_type = "success" if res.status == StatusResultado.REVISADO else "warning"
                with st.expander(
                    f"{res.analito} — {res.valor} ({status_label})"
                ):
                    col_info, col_status = st.columns([3, 1])
                    with col_info:
                        st.caption(f"Ultima alteracao: {res.importado_em.strftime('%d/%m/%Y %H:%M')}")
                    with col_status:
                        renderizar_status_badge(status_label, status_type)

                    st.markdown("<br>", unsafe_allow_html=True)

                    col_valor, col_btn = st.columns([3, 1])
                    with col_valor:
                        novo_valor = st.text_input(
                            "Novo valor",
                            value=res.valor,
                            key=f"val_{res.id}",
                            placeholder="Digite o valor corrigido...",
                        )
                    with col_btn:
                        st.write("")
                        if st.button("Salvar", key=f"btn_{res.id}", type="primary", width="stretch"):
                            try:
                                service.atualizar_resultado(
                                    res.id,
                                    ResultadoUpdate(
                                        valor=novo_valor,
                                        status=StatusResultado.REVISADO,
                                        usuario_id=usuario_id,
                                    ),
                                )
                                st.toast("Resultado atualizado!", icon="\u2705")
                                st.rerun()
                            except ValueError as e:
                                st.error(str(e))

                    st.markdown("<br>", unsafe_allow_html=True)

                    auditoria = service.listar_auditoria_resultado(res.id)
                    if auditoria:
                        st.caption("Historico de alteracoes:")
                        for aud in auditoria:
                            st.caption(
                                f"{aud.ocorrido_em.strftime('%d/%m %H:%M')} "
                                f"— '{aud.valor_anterior}' \u2192 '{aud.valor_novo}'"
                            )
        else:
            renderizar_empty_state(
                icone=ICONE_RESULTADO,
                titulo="Nenhum resultado registrado",
                mensagem="Use o formulario abaixo para inserir o primeiro resultado deste exame.",
            )

        st.divider()

        renderizar_secao(
            titulo=f"{ICONE_ADICIONAR} Inserir Novo Resultado",
            descricao="Lance um novo valor de analito para este exame",
        )

        with st.form("form_resultado"):
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                novo_analito = st.text_input("Analito")
            with col2:
                novo_valor = st.text_input("Valor Encontrado")
            with col3:
                submitted = st.form_submit_button("Registrar", type="primary", width="stretch")

            if submitted:
                if not novo_analito.strip() or not novo_valor.strip():
                    st.error("Informe o analito e o valor encontrado.")
                else:
                    try:
                        service.registrar_resultado(
                            ResultadoCreate(
                                os_item_id=item_selecionado.id,
                                analito=novo_analito.strip(),
                                valor=novo_valor.strip(),
                                usuario_id=usuario_id,
                            )
                        )
                        st.toast("Resultado inserido com sucesso!", icon="\u2705")
                        st.rerun()
                    except ValueError as e:
                        st.error(str(e))


if __name__ == "__main__":
    main()
