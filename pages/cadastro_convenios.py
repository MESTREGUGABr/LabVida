import streamlit as st
from pydantic import ValidationError

from src.cadastro.convenio.dtos import ConvenioCreate, StatusConvenio
from src.cadastro.convenio.errors import ConvenioNaoEncontrado
from src.cadastro.convenio.service import alternar_status, criar_convenio, listar_convenios
from src.cadastro.errors import CnpjConvenioDuplicado, NomeConvenioDuplicado
from src.db import session_scope
from src.ui import renderizar_menu, shell
from src.ui_components import renderizar_cabecalho, renderizar_empty_state, renderizar_status_badge
from src.ui_icons import ICONE_CONVENIO


def main() -> None:
    ctx = shell("LabVida - Convênios", permissao="cadastro:convenios:escrever")
    renderizar_menu(ctx["usuario_id"])

    renderizar_cabecalho(
        titulo="Convenios",
        subtitulo="Operadoras conveniadas; o status controla o uso em Ordens de Servico",
        icone=ICONE_CONVENIO,
    )

    with st.form("form_convenio", clear_on_submit=True):
        col1, col2 = st.columns(2)
        nome = col1.text_input("Nome")
        cnpj = col2.text_input("CNPJ (opcional)")
        telefone = col1.text_input("Telefone (opcional)")
        email = col2.text_input("E-mail (opcional)")
        registro_ans = st.text_input("Registro ANS (opcional)")
        submitted = st.form_submit_button("Cadastrar convênio")

    if submitted:
        try:
            dto = ConvenioCreate(
                nome=nome,
                cnpj=cnpj or None,
                telefone=telefone or None,
                email=email or None,
                registro_ans=registro_ans or None,
            )
            with session_scope() as session:
                criar_convenio(session, dto)
        except (ValidationError, ValueError, NomeConvenioDuplicado, CnpjConvenioDuplicado) as error:
            st.error(_mensagem(error))
        else:
            st.success("Convênio cadastrado com sucesso")

    with session_scope() as session:
        convenios = listar_convenios(session)

    if not convenios:
        renderizar_empty_state(
            icone=ICONE_CONVENIO,
            titulo="Nenhum convenio cadastrado",
            mensagem="Os convenios cadastrados aparecerao aqui.",
        )
        return

    st.subheader("Convenios cadastrados")
    for convenio in convenios:
        col_nome, col_doc, col_status, col_acao = st.columns([2.5, 1.5, 1, 1])

        extras: list[str] = []
        if convenio.cnpj:
            extras.append(f"CNPJ: {convenio.cnpj}")
        if convenio.telefone:
            extras.append(f"Tel: {convenio.telefone}")
        if convenio.registro_ans:
            extras.append(f"ANS: {convenio.registro_ans}")
        linha_extras = "  \n".join(extras) if extras else "—"
        col_nome.write(f"**{convenio.nome}**  \n{linha_extras}")

        doc_info = convenio.email or "—"
        col_doc.write(doc_info)

        ativo = convenio.status == StatusConvenio.ATIVO
        with col_status:
            renderizar_status_badge("Ativo" if ativo else "Inativo", "success" if ativo else "neutral")

        rotulo = "Inativar" if ativo else "Ativar"
        if col_acao.button(rotulo, key=f"status_{convenio.id}"):
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
