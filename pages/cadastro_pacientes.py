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
from src.ui import renderizar_menu, shell, usuario_id_logado
from src.ui_components import (
    ColunaGrid,
    renderizar_cabecalho,
    renderizar_empty_state,
    renderizar_grid,
    renderizar_secao,
)
from src.ui_icons import ICONE_USUARIO

DATA_MINIMA_DATE_INPUT = date(1000, 1, 1)


def main() -> None:
    ctx = shell("LabVida - Cadastro de Pacientes", permissao="cadastro:pacientes:escrever")
    renderizar_menu(ctx["usuario_id"])

    renderizar_cabecalho(
        titulo="Cadastro de Pacientes",
        subtitulo="Gerenciamento basico de Pacientes ativos do LabVida",
        icone=ICONE_USUARIO,
    )

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
    renderizar_secao(
        titulo="Novo Paciente",
        descricao="Preencha os dados para cadastrar um novo paciente no sistema",
    )

    with st.form("form_cadastrar_paciente", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome")
            cpf = st.text_input("CPF do Paciente")
            data_nascimento = st.date_input(
                "Data de nascimento",
                value=None,
                min_value=DATA_MINIMA_DATE_INPUT,
                max_value=date.today(),
                format="DD/MM/YYYY",
            )
        with col2:
            telefone = st.text_input("Telefone do Paciente")
            sexo = st.selectbox(
                "Sexo",
                options=list(SexoPaciente),
                index=list(SexoPaciente).index(SexoPaciente.NAO_INFORMADO),
                format_func=_formatar_sexo,
            )
        submitted = st.form_submit_button("Cadastrar", type="primary")

    if not submitted:
        return

    try:
        if data_nascimento is None:
            raise ValueError("Data de nascimento e obrigatoria")

        dto = PacienteCreate(
            nome=nome,
            cpf=cpf,
            data_nascimento=data_nascimento,
            telefone=telefone,
            sexo=sexo,
        )
        with session_scope() as session:
            criar_paciente(session, dto, usuario_id_logado())
    except (ValidationError, ValueError) as error:
        st.error(_mensagem_validacao(error))
    except CpfPacienteDuplicado as error:
        st.error(str(error))
    else:
        st.success("Paciente cadastrado com sucesso")


def _render_lista() -> None:
    renderizar_secao(
        titulo="Pacientes Ativos",
        descricao="Lista de todos os pacientes ativos no sistema",
    )

    try:
        pacientes = _listar_pacientes_ativos()
    except Exception as error:
        st.error(f"Erro ao listar Pacientes: {error}")
        return

    if not pacientes:
        renderizar_empty_state(
            icone=ICONE_USUARIO,
            titulo="Nenhum paciente cadastrado",
            mensagem="Os pacientes cadastrados aparecerao aqui.",
        )
        return

    busca = st.text_input(
        "Buscar por nome", placeholder="Digite parte do nome do paciente", key="busca_pac"
    ).strip().lower()
    if busca:
        pacientes = [p for p in pacientes if busca in p.nome.lower()]

    total = len(pacientes)
    if total == 0:
        st.info("Nenhum paciente corresponde à busca.")
        return

    _PAGINA = 25
    total_paginas = max(1, (total + _PAGINA - 1) // _PAGINA)
    pagina = st.selectbox(
        "Pagina", options=list(range(1, total_paginas + 1)), key="pagina_pac"
    )
    inicio = (pagina - 1) * _PAGINA
    exibidos = pacientes[inicio : inicio + _PAGINA]
    st.caption(
        f"Exibindo {inicio + 1}–{inicio + len(exibidos)} de {total} paciente(s) "
        f"· pagina {pagina}/{total_paginas}"
    )

    renderizar_grid(
        [
            {
                "nome": paciente.nome,
                # Sempre mascarado: o grid nao e excecao a LGPD.
                "cpf": paciente.cpf_mascarado,
                "data_nascimento": paciente.data_nascimento,
                "telefone": paciente.telefone,
                "sexo": _formatar_sexo(paciente.sexo),
            }
            for paciente in exibidos
        ],
        colunas=[
            ColunaGrid("nome", "Nome"),
            ColunaGrid("cpf", "CPF", largura=150),
            ColunaGrid("data_nascimento", "Nascimento", tipo="data", largura=130),
            ColunaGrid("telefone", "Telefone", largura=140),
            ColunaGrid("sexo", "Sexo", largura=110),
        ],
        chave="grid_pacientes",
        altura=400,
        # A paginacao ja e server-side, feita acima: paginar de novo no grid
        # daria duas paginacoes concorrentes sobre o mesmo conjunto.
        paginar=False,
    )


def _render_edicao() -> None:
    renderizar_secao(
        titulo="Editar ou Inativar Paciente",
        descricao="Selecione um paciente para editar dados ou inativar",
    )

    try:
        pacientes = _listar_pacientes_ativos()
    except Exception as error:
        st.error(f"Erro ao carregar Pacientes: {error}")
        return

    if not pacientes:
        renderizar_empty_state(
            icone=ICONE_USUARIO,
            titulo="Nenhum paciente ativo",
            mensagem="Nao ha pacientes ativos para editar ou inativar.",
        )
        return

    opcoes = {f"{paciente.nome} - CPF {paciente.cpf_mascarado}": paciente.id for paciente in pacientes}
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
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome", value=paciente.nome)
            cpf = st.text_input("CPF do Paciente", value=paciente.cpf)
            data_nascimento = st.date_input(
                "Data de nascimento",
                value=paciente.data_nascimento,
                min_value=DATA_MINIMA_DATE_INPUT,
                max_value=date.today(),
                format="DD/MM/YYYY",
            )
        with col2:
            telefone = st.text_input("Telefone do Paciente", value=paciente.telefone)
            sexo = st.selectbox(
                "Sexo",
                options=list(SexoPaciente),
                index=list(SexoPaciente).index(paciente.sexo),
                format_func=_formatar_sexo,
            )
        submitted = st.form_submit_button("Salvar alteracoes", type="primary")

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
            atualizar_paciente(session, paciente.id, dto, usuario_id_logado())
    except (ValidationError, ValueError) as error:
        st.error(_mensagem_validacao(error))
    except (CpfPacienteDuplicado, PacienteNaoEncontrado) as error:
        st.error(str(error))
    else:
        st.success("Paciente atualizado com sucesso")
        st.rerun()


def _render_inativacao(paciente_id: UUID) -> None:
    st.divider()
    st.warning("Inativar remove o Paciente da listagem de ativos, sem exclusao fisica.")

    confirmar = st.checkbox("Confirmo a inativação deste paciente")
    if not st.button("Inativar Paciente", type="secondary", disabled=not confirmar):
        return

    try:
        with session_scope() as session:
            inativar_paciente(session, paciente_id, usuario_id_logado())
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
        SexoPaciente.NAO_INFORMADO: "Nao informado",
    }[sexo]


def _mensagem_validacao(error: Exception) -> str:
    if isinstance(error, ValidationError):
        primeiro_erro = error.errors()[0]
        return str(primeiro_erro["msg"]).replace("Value error, ", "")
    return str(error)


if __name__ == "__main__":
    main()
