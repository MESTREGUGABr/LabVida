from datetime import date
from uuid import UUID

import streamlit as st
from pydantic import ValidationError

from src.cadastro.dtos import PacienteCreate, PacienteRead, PacienteUpdate, SexoPaciente
from src.cadastro.errors import CpfPacienteDuplicado, PacienteNaoEncontrado
from src.cadastro.service import (
    atualizar_paciente,
    criar_paciente,
    inativar_paciente,
    listar_pacientes_ativos,
    obter_paciente_por_id,
)
from src.db import session_scope


def main() -> None:
    st.set_page_config(page_title="LabVida - Cadastro de Pacientes")

    if "user" not in st.session_state:
        st.markdown(
            '<meta http-equiv="refresh" content="0; url=/">',
            unsafe_allow_html=True,
        )
        st.stop()

    st.title("Cadastro de Pacientes")
    st.caption("Gerenciamento básico de Pacientes ativos do LabVida")

    tab_cadastrar, tab_listar, tab_editar = st.tabs(
        ["Cadastrar", "Pacientes ativos", "Editar e inativar"]
    )

    with tab_cadastrar:
        _render_cadastro()

    with tab_listar:
        _render_lista()

    with tab_editar:
        _render_edicao()


def _render_cadastro() -> None:
    st.subheader("Cadastrar Paciente")

    with st.form("form_cadastrar_paciente", clear_on_submit=True):
        nome = st.text_input("Nome")
        cpf = st.text_input("CPF do Paciente")
        data_nascimento = st.date_input(
            "Data de nascimento",
            value=None,
            max_value=date.today(),
            format="DD/MM/YYYY",
        )
        telefone = st.text_input("Telefone do Paciente")
        sexo = st.selectbox(
            "Sexo",
            options=list(SexoPaciente),
            index=list(SexoPaciente).index(SexoPaciente.NAO_INFORMADO),
            format_func=_formatar_sexo,
        )
        submitted = st.form_submit_button("Cadastrar")

    if not submitted:
        return

    try:
        if data_nascimento is None:
            raise ValueError("Data de nascimento é obrigatória")

        dto = PacienteCreate(
            nome=nome,
            cpf=cpf,
            data_nascimento=data_nascimento,
            telefone=telefone,
            sexo=sexo,
        )
        with session_scope() as session:
            criar_paciente(session, dto)
    except (ValidationError, ValueError) as error:
        st.error(_mensagem_validacao(error))
    except CpfPacienteDuplicado as error:
        st.error(str(error))
    else:
        st.success("Paciente cadastrado com sucesso")


def _render_lista() -> None:
    st.subheader("Pacientes ativos")

    try:
        pacientes = _listar_pacientes_ativos()
    except Exception as error:
        st.error(f"Erro ao listar Pacientes: {error}")
        return

    if not pacientes:
        st.info("Nenhum Paciente ativo cadastrado")
        return

    st.dataframe(
        [
            {
                "Nome": paciente.nome,
                "CPF do Paciente": paciente.cpf,
                "Data de nascimento": paciente.data_nascimento.isoformat(),
                "Telefone do Paciente": paciente.telefone,
                "Sexo": _formatar_sexo(paciente.sexo),
            }
            for paciente in pacientes
        ],
        hide_index=True,
        use_container_width=True,
    )


def _render_edicao() -> None:
    st.subheader("Editar ou inativar Paciente")

    try:
        pacientes = _listar_pacientes_ativos()
    except Exception as error:
        st.error(f"Erro ao carregar Pacientes: {error}")
        return

    if not pacientes:
        st.info("Nenhum Paciente ativo cadastrado")
        return

    opcoes = {f"{paciente.nome} - CPF {paciente.cpf}": paciente.id for paciente in pacientes}
    selecionado = st.selectbox("Paciente", options=list(opcoes.keys()))
    paciente_id = opcoes[selecionado]

    try:
        with session_scope() as session:
            paciente = obter_paciente_por_id(session, paciente_id)
    except PacienteNaoEncontrado as error:
        st.error(str(error))
        return

    _render_form_edicao(paciente)
    _render_inativacao(paciente.id)


def _render_form_edicao(paciente: PacienteRead) -> None:
    with st.form(f"form_editar_paciente_{paciente.id}"):
        nome = st.text_input("Nome", value=paciente.nome)
        cpf = st.text_input("CPF do Paciente", value=paciente.cpf)
        data_nascimento = st.date_input(
            "Data de nascimento",
            value=paciente.data_nascimento,
            max_value=date.today(),
            format="DD/MM/YYYY",
        )
        telefone = st.text_input("Telefone do Paciente", value=paciente.telefone)
        sexo = st.selectbox(
            "Sexo",
            options=list(SexoPaciente),
            index=list(SexoPaciente).index(paciente.sexo),
            format_func=_formatar_sexo,
        )
        submitted = st.form_submit_button("Salvar alterações")

    if not submitted:
        return

    try:
        dto = PacienteUpdate(
            nome=nome,
            cpf=cpf,
            data_nascimento=data_nascimento,
            telefone=telefone,
            sexo=sexo,
        )
        with session_scope() as session:
            atualizar_paciente(session, paciente.id, dto)
    except (ValidationError, ValueError) as error:
        st.error(_mensagem_validacao(error))
    except (CpfPacienteDuplicado, PacienteNaoEncontrado) as error:
        st.error(str(error))
    else:
        st.success("Paciente atualizado com sucesso")
        st.rerun()


def _render_inativacao(paciente_id: UUID) -> None:
    st.divider()
    st.warning("Inativar remove o Paciente da listagem de ativos, sem exclusão física.")

    if not st.button("Inativar Paciente", type="secondary"):
        return

    try:
        with session_scope() as session:
            inativar_paciente(session, paciente_id)
    except PacienteNaoEncontrado as error:
        st.error(str(error))
    else:
        st.success("Paciente inativado com sucesso")
        st.rerun()


def _listar_pacientes_ativos() -> list[PacienteRead]:
    with session_scope() as session:
        return listar_pacientes_ativos(session)


def _formatar_sexo(sexo: SexoPaciente) -> str:
    return {
        SexoPaciente.MASCULINO: "Masculino",
        SexoPaciente.FEMININO: "Feminino",
        SexoPaciente.NAO_INFORMADO: "Não informado",
    }[sexo]


def _mensagem_validacao(error: Exception) -> str:
    if isinstance(error, ValidationError):
        primeiro_erro = error.errors()[0]
        return str(primeiro_erro["msg"]).replace("Value error, ", "")
    return str(error)


if __name__ == "__main__":
    main()
