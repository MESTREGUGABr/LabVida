import streamlit as st
from pydantic import ValidationError

from src.cadastro.medico.dtos import UFS_VALIDAS, MedicoCreate
from src.cadastro.medico.errors import CrmDuplicado
from src.cadastro.medico.service import criar_medico, listar_medicos_ativos
from src.db import session_scope
from src.ui import exigir_login


def main() -> None:
    st.set_page_config(page_title="LabVida - Médicos")
    exigir_login()

    st.title("Médicos")
    st.caption("Médicos solicitantes; o responsável técnico habilita a liberação de laudo")

    with st.form("form_medico", clear_on_submit=True):
        nome = st.text_input("Nome")
        crm = st.text_input("CRM")
        uf_crm = st.selectbox("UF do CRM", options=sorted(UFS_VALIDAS))
        responsavel_tecnico = st.checkbox("Responsável técnico")
        submitted = st.form_submit_button("Cadastrar médico")

    if submitted:
        try:
            dto = MedicoCreate(
                nome=nome, crm=crm, uf_crm=uf_crm, responsavel_tecnico=responsavel_tecnico
            )
            with session_scope() as session:
                criar_medico(session, dto)
        except (ValidationError, ValueError) as error:
            st.error(_mensagem(error))
        except CrmDuplicado as error:
            st.error(str(error))
        else:
            st.success("Médico cadastrado com sucesso")

    with session_scope() as session:
        medicos = listar_medicos_ativos(session)

    if medicos:
        st.dataframe(
            [
                {
                    "Nome": m.nome,
                    "CRM": f"{m.crm}/{m.uf_crm}",
                    "Responsável técnico": "Sim" if m.responsavel_tecnico else "Não",
                }
                for m in medicos
            ],
            hide_index=True,
            use_container_width=True,
        )
    else:
        st.info("Nenhum médico cadastrado")


def _mensagem(error: Exception) -> str:
    if isinstance(error, ValidationError):
        return str(error.errors()[0]["msg"]).replace("Value error, ", "")
    return str(error)


if __name__ == "__main__":
    main()
