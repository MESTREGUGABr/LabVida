import streamlit as st
from pydantic import ValidationError

from src.cadastro.unidade.dtos import SetorCreate, TipoUnidade, UnidadeCreate
from src.cadastro.unidade.errors import UnidadeNaoEncontrada
from src.cadastro.unidade.service import (
    criar_setor,
    criar_unidade,
    listar_setores_ativos,
    listar_unidades_ativas,
)
from src.db import session_scope
from src.ui import exigir_login


def main() -> None:
    st.set_page_config(page_title="LabVida - Unidades e Setores")
    exigir_login()

    st.title("Unidades e Setores")
    st.caption("Cadastro das unidades da rede (central e coletas) e seus setores")

    tab_unidade, tab_setor = st.tabs(["Unidades", "Setores"])

    with tab_unidade:
        _render_unidades()

    with tab_setor:
        _render_setores()


def _render_unidades() -> None:
    with st.form("form_unidade", clear_on_submit=True):
        nome = st.text_input("Nome")
        tipo = st.selectbox("Tipo", options=list(TipoUnidade), format_func=_formatar_tipo)
        endereco = st.text_input("Endereço (opcional)")
        submitted = st.form_submit_button("Cadastrar unidade")

    if submitted:
        try:
            dto = UnidadeCreate(nome=nome, tipo=tipo, endereco=endereco or None)
            with session_scope() as session:
                criar_unidade(session, dto)
        except (ValidationError, ValueError) as error:
            st.error(_mensagem(error))
        else:
            st.success("Unidade cadastrada com sucesso")

    unidades = _unidades()
    if unidades:
        st.dataframe(
            [{"Nome": u.nome, "Tipo": _formatar_tipo(u.tipo), "Endereço": u.endereco or "—"} for u in unidades],
            hide_index=True,
            use_container_width=True,
        )
    else:
        st.info("Nenhuma unidade cadastrada")


def _render_setores() -> None:
    unidades = _unidades()
    if not unidades:
        st.info("Cadastre uma unidade antes de adicionar setores")
        return

    opcoes = {u.nome: u.id for u in unidades}
    nome_unidade = st.selectbox("Unidade", options=list(opcoes.keys()))
    unidade_id = opcoes[nome_unidade]

    with st.form("form_setor", clear_on_submit=True):
        nome = st.text_input("Nome do setor")
        submitted = st.form_submit_button("Adicionar setor")

    if submitted:
        try:
            dto = SetorCreate(unidade_id=unidade_id, nome=nome)
            with session_scope() as session:
                criar_setor(session, dto)
        except (ValidationError, ValueError) as error:
            st.error(_mensagem(error))
        except UnidadeNaoEncontrada as error:
            st.error(str(error))
        else:
            st.success("Setor adicionado com sucesso")

    with session_scope() as session:
        setores = listar_setores_ativos(session, unidade_id)

    if setores:
        st.dataframe(
            [{"Setor": s.nome} for s in setores], hide_index=True, use_container_width=True
        )
    else:
        st.info("Nenhum setor nesta unidade")


def _unidades() -> list:
    with session_scope() as session:
        return listar_unidades_ativas(session)


def _formatar_tipo(tipo: TipoUnidade) -> str:
    return {TipoUnidade.CENTRAL: "Central", TipoUnidade.COLETA: "Coleta"}[TipoUnidade(tipo)]


def _mensagem(error: Exception) -> str:
    if isinstance(error, ValidationError):
        return str(error.errors()[0]["msg"]).replace("Value error, ", "")
    return str(error)


if __name__ == "__main__":
    main()
