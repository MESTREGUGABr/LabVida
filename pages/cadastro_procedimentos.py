from datetime import date
from decimal import Decimal, InvalidOperation

import streamlit as st
from pydantic import ValidationError

from src.cadastro.convenio.service import listar_convenios_ativos
from src.cadastro.procedimento.dtos import ProcedimentoCreate, ProcedimentoValorCreate
from src.cadastro.procedimento.errors import CodigoTussDuplicado, ProcedimentoNaoEncontrado
from src.cadastro.procedimento.service import (
    criar_procedimento,
    definir_valor,
    listar_procedimentos_ativos,
)
from src.cadastro.convenio.errors import ConvenioNaoEncontrado
from src.db import session_scope
from src.ui import exigir_login


def main() -> None:
    st.set_page_config(page_title="LabVida - Procedimentos")
    exigir_login()

    st.title("Procedimentos")
    st.caption("Catálogo de procedimentos (TUSS) e valores contratados por convênio")

    tab_procedimento, tab_valor = st.tabs(["Procedimentos", "Valores por convênio"])

    with tab_procedimento:
        _render_procedimentos()

    with tab_valor:
        _render_valores()


def _render_procedimentos() -> None:
    with st.form("form_procedimento", clear_on_submit=True):
        codigo_tuss = st.text_input("Código TUSS")
        nome = st.text_input("Nome")
        setor = st.text_input("Setor (opcional)")
        submitted = st.form_submit_button("Cadastrar procedimento")

    if submitted:
        try:
            dto = ProcedimentoCreate(codigo_tuss=codigo_tuss, nome=nome, setor=setor or None)
            with session_scope() as session:
                criar_procedimento(session, dto)
        except (ValidationError, ValueError) as error:
            st.error(_mensagem(error))
        except CodigoTussDuplicado as error:
            st.error(str(error))
        else:
            st.success("Procedimento cadastrado com sucesso")

    procedimentos = _procedimentos()
    if procedimentos:
        st.dataframe(
            [{"TUSS": p.codigo_tuss, "Nome": p.nome, "Setor": p.setor or "—"} for p in procedimentos],
            hide_index=True,
            use_container_width=True,
        )
    else:
        st.info("Nenhum procedimento cadastrado")


def _render_valores() -> None:
    procedimentos = _procedimentos()
    with session_scope() as session:
        convenios = listar_convenios_ativos(session)

    if not procedimentos or not convenios:
        st.info("Cadastre procedimentos e convênios ativos para definir valores")
        return

    procedimentos_opcoes = {f"{p.codigo_tuss} - {p.nome}": p.id for p in procedimentos}
    convenios_opcoes = {c.nome: c.id for c in convenios}

    with st.form("form_valor", clear_on_submit=True):
        procedimento_label = st.selectbox("Procedimento", options=list(procedimentos_opcoes.keys()))
        convenio_label = st.selectbox("Convênio", options=list(convenios_opcoes.keys()))
        valor_texto = st.text_input("Valor (R$)", value="0,00")
        vigencia = st.date_input("Vigência a partir de", value=date.today(), format="DD/MM/YYYY")
        submitted = st.form_submit_button("Definir valor")

    if not submitted:
        return

    try:
        valor = _parse_valor(valor_texto)
        dto = ProcedimentoValorCreate(
            procedimento_id=procedimentos_opcoes[procedimento_label],
            convenio_id=convenios_opcoes[convenio_label],
            valor=valor,
            vigencia_inicio=vigencia,
        )
        with session_scope() as session:
            definir_valor(session, dto)
    except (ValidationError, ValueError) as error:
        st.error(_mensagem(error))
    except (ProcedimentoNaoEncontrado, ConvenioNaoEncontrado) as error:
        st.error(str(error))
    else:
        st.success("Valor definido com sucesso")


def _procedimentos() -> list:
    with session_scope() as session:
        return listar_procedimentos_ativos(session)


def _parse_valor(texto: str) -> Decimal:
    normalizado = texto.strip().replace(".", "").replace(",", ".")
    try:
        return Decimal(normalizado)
    except (InvalidOperation, ValueError):
        raise ValueError("Valor inválido")


def _mensagem(error: Exception) -> str:
    if isinstance(error, ValidationError):
        return str(error.errors()[0]["msg"]).replace("Value error, ", "")
    return str(error)


if __name__ == "__main__":
    main()
