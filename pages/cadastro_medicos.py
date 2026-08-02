import streamlit as st
from pydantic import ValidationError

from src.cadastro.medico.dtos import UFS_VALIDAS, MedicoCreate
from src.cadastro.medico.errors import CrmDuplicado
from src.cadastro.medico.service import criar_medico, listar_medicos_ativos
from src.db import session_scope
from src.ui import renderizar_menu, shell, usuario_id_logado
from src.ui_components import (
    ColunaGrid,
    renderizar_cabecalho,
    renderizar_empty_state,
    renderizar_grid,
)
from src.ui_icons import ICONE_MEDICO


def main() -> None:
    ctx = shell("LabVida - Médicos", permissao="cadastro:medicos:escrever")
    renderizar_menu(ctx["usuario_id"])

    renderizar_cabecalho(
        titulo="Medicos",
        subtitulo="Medicos solicitantes; o responsavel tecnico habilita a liberacao de laudo",
        icone=ICONE_MEDICO,
    )

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
                criar_medico(session, dto, usuario_id_logado())
        except (ValidationError, ValueError) as error:
            st.error(_mensagem(error))
        except CrmDuplicado as error:
            st.error(str(error))
        else:
            st.success("Médico cadastrado com sucesso")

    with session_scope() as session:
        medicos = listar_medicos_ativos(session)

    if medicos:
        renderizar_grid(
            [
                {
                    "nome": m.nome,
                    "crm": f"{m.crm}/{m.uf_crm}",
                    "responsavel_tecnico": m.responsavel_tecnico,
                }
                for m in medicos
            ],
            colunas=[
                ColunaGrid("nome", "Nome"),
                ColunaGrid("crm", "CRM", largura=140),
                ColunaGrid("responsavel_tecnico", "Responsavel tecnico", tipo="booleano", largura=190),
            ],
            chave="grid_medicos",
            altura=360,
        )
    else:
        renderizar_empty_state(
            icone=ICONE_MEDICO,
            titulo="Nenhum medico cadastrado",
            mensagem="Os medicos cadastrados aparecerao aqui.",
        )


def _mensagem(error: Exception) -> str:
    if isinstance(error, ValidationError):
        return str(error.errors()[0]["msg"]).replace("Value error, ", "")
    return str(error)


if __name__ == "__main__":
    main()
