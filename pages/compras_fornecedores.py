import streamlit as st

from src.compras.fornecedor.dtos import FornecedorCreate
from src.compras.fornecedor.errors import FornecedorError
from src.compras.fornecedor.service import (
    alternar_status,
    criar_fornecedor,
    editar_fornecedor,
    listar_todos,
)
from src.db import session_scope
from src.ui import exigir_login


def main() -> None:
    st.set_page_config(page_title="LabVida - Fornecedores", layout="wide")
    exigir_login()

    st.title("Fornecedores")
    st.caption("Cadastro de fornecedores de insumos")

    tab1, tab2 = st.tabs(["Cadastrar", "Listar"])

    with tab1:
        _render_cadastrar()
    with tab2:
        _render_listar()


def _render_cadastrar() -> None:
    st.subheader("Novo Fornecedor")

    nome = st.text_input("Nome do Fornecedor")
    cnpj = st.text_input("CNPJ (somente números)", max_chars=14)

    if st.button("Cadastrar", type="primary"):
        try:
            dto = FornecedorCreate(nome=nome, cnpj=cnpj)
            with session_scope() as session:
                fornecedor = criar_fornecedor(session, dto)
            st.toast(f"Fornecedor {fornecedor.nome} cadastrado!")
            st.rerun()
        except FornecedorError as e:
            st.error(str(e))
        except ValueError as e:
            st.error(str(e))


def _render_listar() -> None:
    st.subheader("Fornecedores")

    with session_scope() as session:
        fornecedores = listar_todos(session)

    if not fornecedores:
        st.info("Nenhum fornecedor cadastrado.")
        return

    for f in fornecedores:
        emoji = "🟢" if f.status == "ATIVO" else "🔴"
        with st.container(border=True):
            c1, c2 = st.columns([4, 1])
            with c1:
                st.write(f"{emoji} **{f.nome}**")
                st.caption(f"CNPJ: {f.cnpj} | Status: {f.status}")
            with c2:
                if f.status == "ATIVO":
                    col_a, col_b = st.columns(2)
                    with col_a:
                        if st.button("Inativar", key=f"inativar_{f.id}"):
                            with session_scope() as session:
                                alternar_status(session, f.id, ativo=False)
                            st.toast(f"{f.nome} inativado")
                            st.rerun()
                    with col_b:
                        if st.button("Editar", key=f"editar_{f.id}"):
                            st.session_state[f"edit_forn_{f.id}"] = True
                else:
                    if st.button("Ativar", key=f"ativar_{f.id}"):
                        with session_scope() as session:
                            alternar_status(session, f.id, ativo=True)
                        st.toast(f"{f.nome} ativado")
                        st.rerun()

            if st.session_state.get(f"edit_forn_{f.id}", False):
                novo_nome = st.text_input("Novo nome", value=f.nome, key=f"nome_edit_{f.id}")
                c_ok, c_cancel = st.columns(2)
                with c_ok:
                    if st.button("Salvar", key=f"salvar_edit_{f.id}"):
                        try:
                            with session_scope() as session:
                                editar_fornecedor(session, f.id, novo_nome)
                            st.toast("Fornecedor atualizado!")
                            st.session_state.pop(f"edit_forn_{f.id}", None)
                            st.rerun()
                        except FornecedorError as e:
                            st.error(str(e))
                with c_cancel:
                    if st.button("Cancelar", key=f"cancel_edit_{f.id}"):
                        st.session_state.pop(f"edit_forn_{f.id}", None)
                        st.rerun()


if __name__ == "__main__":
    main()
