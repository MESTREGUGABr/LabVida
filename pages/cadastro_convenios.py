from uuid import UUID

import streamlit as st
from pydantic import ValidationError

from src.cadastro.dtos import ConvenioCreate, ConvenioRead, ConvenioUpdate
from src.cadastro.errors import CnpjConvenioDuplicado, ConvenioNaoEncontrado, NomeConvenioDuplicado
from src.cadastro.service import (
    atualizar_convenio,
    criar_convenio,
    inativar_convenio,
    listar_convenios,
    obter_convenio_por_id,
)
from src.db import session_scope


def main() -> None:
    st.set_page_config(page_title="LabVida - Cadastro de Convênios")

    if "user" not in st.session_state:
        st.markdown(
            '<meta http-equiv="refresh" content="0; url=/">',
            unsafe_allow_html=True,
        )
        st.stop()

    st.title("Cadastro de Convênios")
    st.caption("Gerenciamento de Convênios ativos e inativos do LabVida")

    tab_cadastrar, tab_listar, tab_editar = st.tabs(["Cadastrar", "Convênios", "Editar e inativar"])

    with tab_cadastrar:
        _render_cadastro()

    with tab_listar:
        _render_lista()

    with tab_editar:
        _render_edicao()


def _render_cadastro() -> None:
    st.subheader("Cadastrar Convênio")

    with st.form("form_cadastrar_convenio", clear_on_submit=True):
        nome = st.text_input("Nome")
        cnpj = st.text_input("CNPJ")
        telefone = st.text_input("Telefone")
        email = st.text_input("Email")
        submitted = st.form_submit_button("Cadastrar")

    if not submitted:
        return

    try:
        dto = ConvenioCreate(
            nome=nome,
            cnpj=cnpj or None,
            telefone=telefone or None,
            email=email or None,
        )
        with session_scope() as session:
            criar_convenio(session, dto)
    except (ValidationError, ValueError) as error:
        st.error(_mensagem_validacao(error))
    except (NomeConvenioDuplicado, CnpjConvenioDuplicado) as error:
        st.error(str(error))
    else:
        st.success("Convênio cadastrado com sucesso")


def _render_lista() -> None:
    st.subheader("Convênios")

    try:
        convenios = _listar_convenios()
    except Exception as error:
        st.error(f"Erro ao listar Convênios: {error}")
        return

    if not convenios:
        st.info("Nenhum Convênio cadastrado")
        return

    st.dataframe(
        [
            {
                "Nome": convenio.nome,
                "CNPJ": convenio.cnpj or "-",
                "Telefone": convenio.telefone or "-",
                "Email": convenio.email or "-",
                "Status": _formatar_status(convenio.ativo),
            }
            for convenio in convenios
        ],
        hide_index=True,
        use_container_width=True,
    )


def _render_edicao() -> None:
    st.subheader("Editar ou inativar Convênio")

    try:
        convenios = _listar_convenios()
    except Exception as error:
        st.error(f"Erro ao carregar Convênios: {error}")
        return

    if not convenios:
        st.info("Nenhum Convênio cadastrado")
        return

    opcoes = {f"{convenio.nome} - {_formatar_status(convenio.ativo)}": convenio.id for convenio in convenios}
    selecionado = st.selectbox("Convênio", options=list(opcoes.keys()))
    convenio_id = opcoes[selecionado]

    try:
        with session_scope() as session:
            convenio = obter_convenio_por_id(session, convenio_id)
    except ConvenioNaoEncontrado as error:
        st.error(str(error))
        return

    _render_form_edicao(convenio)
    _render_inativacao(convenio.id, convenio.ativo)


def _render_form_edicao(convenio: ConvenioRead) -> None:
    with st.form(f"form_editar_convenio_{convenio.id}"):
        nome = st.text_input("Nome", value=convenio.nome)
        cnpj = st.text_input("CNPJ", value=convenio.cnpj or "")
        telefone = st.text_input("Telefone", value=convenio.telefone or "")
        email = st.text_input("Email", value=convenio.email or "")
        ativo = st.checkbox("Convênio ativo", value=convenio.ativo)
        submitted = st.form_submit_button("Salvar alterações")

    if not submitted:
        return

    try:
        dto = ConvenioUpdate(
            nome=nome,
            cnpj=cnpj or None,
            telefone=telefone or None,
            email=email or None,
            ativo=ativo,
        )
        with session_scope() as session:
            atualizar_convenio(session, convenio.id, dto)
    except (ValidationError, ValueError) as error:
        st.error(_mensagem_validacao(error))
    except (NomeConvenioDuplicado, CnpjConvenioDuplicado, ConvenioNaoEncontrado) as error:
        st.error(str(error))
    else:
        st.success("Convênio atualizado com sucesso")
        st.rerun()


def _render_inativacao(convenio_id: UUID, ativo: bool) -> None:
    st.divider()
    st.warning("Inativar mantém o Convênio visível para preservar histórico.")

    if not ativo:
        st.info("Convênio já está inativo")
        return

    if not st.button("Inativar Convênio", type="secondary"):
        return

    try:
        with session_scope() as session:
            inativar_convenio(session, convenio_id)
    except ConvenioNaoEncontrado as error:
        st.error(str(error))
    else:
        st.success("Convênio inativado com sucesso")
        st.rerun()


def _listar_convenios() -> list[ConvenioRead]:
    with session_scope() as session:
        return listar_convenios(session)


def _formatar_status(ativo: bool) -> str:
    return "ATIVO" if ativo else "INATIVO"


def _mensagem_validacao(error: Exception) -> str:
    if isinstance(error, ValidationError):
        primeiro_erro = error.errors()[0]
        return str(primeiro_erro["msg"]).replace("Value error, ", "")
import streamlit as st
from pydantic import ValidationError

from src.cadastro.convenio.dtos import ConvenioCreate, StatusConvenio
from src.cadastro.convenio.errors import ConvenioNaoEncontrado
from src.cadastro.convenio.service import alternar_status, criar_convenio, listar_convenios
from src.db import session_scope
from src.ui import exigir_login


def main() -> None:
    st.set_page_config(page_title="LabVida - Convênios")
    exigir_login()

    st.title("Convênios")
    st.caption("Operadoras conveniadas; o status controla o uso em Ordens de Serviço")

    with st.form("form_convenio", clear_on_submit=True):
        nome = st.text_input("Nome")
        registro_ans = st.text_input("Registro ANS (opcional)")
        submitted = st.form_submit_button("Cadastrar convênio")

    if submitted:
        try:
            dto = ConvenioCreate(nome=nome, registro_ans=registro_ans or None)
            with session_scope() as session:
                criar_convenio(session, dto)
        except (ValidationError, ValueError) as error:
            st.error(_mensagem(error))
        else:
            st.success("Convênio cadastrado com sucesso")

    with session_scope() as session:
        convenios = listar_convenios(session)

    if not convenios:
        st.info("Nenhum convênio cadastrado")
        return

    st.subheader("Convênios cadastrados")
    for convenio in convenios:
        coluna_nome, coluna_status, coluna_acao = st.columns([3, 1, 1])
        coluna_nome.write(f"**{convenio.nome}**  \nANS: {convenio.registro_ans or '—'}")
        ativo = convenio.status == StatusConvenio.ATIVO
        coluna_status.write("🟢 Ativo" if ativo else "🔴 Inativo")
        rotulo = "Inativar" if ativo else "Ativar"
        if coluna_acao.button(rotulo, key=f"status_{convenio.id}"):
            try:
                with session_scope() as session:
                    alternar_status(session, convenio.id, ativo=not ativo)
            except ConvenioNaoEncontrado as error:
                st.error(str(error))
            else:
                st.rerun()


def _mensagem(error: Exception) -> str:
    if isinstance(error, ValidationError):
        return str(error.errors()[0]["msg"]).replace("Value error, ", "")
    return str(error)


if __name__ == "__main__":
    main()
