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
