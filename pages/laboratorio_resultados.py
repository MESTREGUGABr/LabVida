import time

import streamlit as st
from sqlalchemy.orm import Session
from sqlalchemy import select

from src.atendimento.ordem_servico.models import OrdemServico, OsItem
from src.db import session_scope
from src.laboratorial.dtos import ResultadoCreate, ResultadoUpdate
from src.laboratorial.models import StatusResultado
from src.laboratorial.service import LaboratorialService
from src.ui import renderizar_menu, shell, usuario_id_logado


def _listar_os_itens(session: Session):
    return session.scalars(select(OsItem)).all()


def main() -> None:
    ctx = shell("Resultados de Exames", layout="wide", permissao="laboratorial:registrar_resultado")
    renderizar_menu(ctx["usuario_id"])

    st.title("Digitação e Conferência de Resultados")
    st.markdown("Selecione um item de Ordem de Serviço para lançar ou revisar resultados.")

    with session_scope() as session:
        itens = _listar_os_itens(session)
        if not itens:
            st.info("Nenhuma OS cadastrada no momento.")
            return

        opcoes_itens = {
            f"OS {item.ordem_servico.id} - Proc {item.procedimento.nome}": item
            for item in itens
            if item.ordem_servico
        }
        escolha = st.selectbox(
            "Selecione a Amostra / Item de OS", options=list(opcoes_itens.keys())
        )

        item_selecionado = opcoes_itens[escolha]

        st.subheader("Resultados do Exame")
        service = LaboratorialService(session)
        resultados_existentes = service.listar_resultados_por_os_item(item_selecionado.id)

        usuario_id = usuario_id_logado()

        if resultados_existentes:
            for res in resultados_existentes:
                with st.expander(
                    f"Analito: {res.analito} - Valor: {res.valor} ({res.status.value})"
                ):
                    st.write(f"**Data da última alteração:** {res.importado_em}")

                    novo_valor = st.text_input(
                        "Atualizar Valor", value=res.valor, key=f"val_{res.id}"
                    )

                    if st.button("Revisar e Salvar", key=f"btn_{res.id}", type="primary"):
                        try:
                            service.atualizar_resultado(
                                res.id,
                                ResultadoUpdate(
                                    valor=novo_valor,
                                    status=StatusResultado.REVISADO,
                                    usuario_id=usuario_id,
                                ),
                            )
                            st.toast("Resultado atualizado com sucesso!", icon="✅")
                            time.sleep(0.5)
                            st.rerun()
                        except ValueError as e:
                            st.error(str(e))

                    st.markdown("**Auditoria (Histórico):**")
                    auditoria = service.listar_auditoria_resultado(res.id)
                    for aud in auditoria:
                        st.caption(
                            f"- {aud.ocorrido_em.strftime('%d/%m %H:%M')} | "
                            f"Valor: '{aud.valor_anterior}' -> '{aud.valor_novo}'"
                        )

        st.divider()
        st.subheader("Inserir Novo Resultado")
        with st.form("form_resultado"):
            novo_analito = st.text_input("Analito")
            novo_valor = st.text_input("Valor Encontrado")

            if st.form_submit_button("Registrar"):
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
                        st.toast("Resultado inserido com sucesso!", icon="✅")
                        time.sleep(0.5)
                        st.rerun()
                    except ValueError as e:
                        st.error(str(e))


if __name__ == "__main__":
    main()
