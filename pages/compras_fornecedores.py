"""Cadastro de fornecedores.

Reescrita na fase F1: a listagem era um loop de `st.container` por fornecedor,
com a edicao controlada por `st.session_state[f"edit_forn_{id}"]`. Esse padrao
so permitia um formulario aberto por vez e colapsava em reruns nao relacionados.
Agora e grid com selecao + `st.dialog`.
"""

import streamlit as st

from src.compras.fornecedor.dtos import FornecedorCreate
from src.compras.fornecedor.service import (
    alternar_status,
    criar_fornecedor,
    editar_fornecedor,
    listar_todos,
)
from src.db import session_scope
from src.ui import renderizar_menu, shell
from src.ui_components import (
    ColunaGrid,
    renderizar_cabecalho,
    renderizar_grid,
    renderizar_secao,
    tratar_erros,
)
from src.ui_icons import ICONE_FORNECEDOR

_COLUNAS = [
    ColunaGrid("nome", "Fornecedor"),
    ColunaGrid("cnpj_formatado", "CNPJ", largura=170),
    ColunaGrid("situacao", "Situacao", largura=110),
    ColunaGrid("criado_em", "Cadastrado em", tipo="data", largura=150),
    ColunaGrid("id", "id", oculta=True),
]


def _formatar_cnpj(cnpj: str) -> str:
    digitos = "".join(c for c in (cnpj or "") if c.isdigit())
    if len(digitos) != 14:
        return cnpj or ""
    return f"{digitos[:2]}.{digitos[2:5]}.{digitos[5:8]}/{digitos[8:12]}-{digitos[12:]}"


def _linhas(fornecedores) -> list[dict]:
    return [
        {
            "id": str(f.id),
            "nome": f.nome,
            "cnpj_formatado": _formatar_cnpj(f.cnpj),
            "situacao": "Ativo" if f.status == "ATIVO" else "Inativo",
            "criado_em": f.criado_em,
        }
        for f in fornecedores
    ]


@st.dialog("Editar fornecedor")
def _dialogo_editar(fornecedor: dict) -> None:
    st.caption(f"CNPJ {fornecedor['cnpj_formatado']}")
    novo_nome = st.text_input("Nome do fornecedor", value=fornecedor["nome"])

    coluna_salvar, coluna_cancelar = st.columns(2)
    with coluna_salvar:
        if st.button("Salvar", type="primary", width="stretch"):
            with tratar_erros("editar o fornecedor") as resultado, session_scope() as session:
                editar_fornecedor(session, fornecedor["id"], novo_nome)
            if resultado:
                st.toast("Fornecedor atualizado.")
                st.rerun()
    with coluna_cancelar:
        if st.button("Cancelar", width="stretch"):
            st.rerun()


@st.dialog("Confirmar alteracao de situacao")
def _dialogo_situacao(fornecedor: dict, *, ativar: bool) -> None:
    acao = "reativar" if ativar else "inativar"
    st.write(f"Deseja **{acao}** o fornecedor **{fornecedor['nome']}**?")
    if not ativar:
        st.caption("Fornecedor inativo nao pode receber novas solicitacoes de compra.")

    coluna_ok, coluna_cancelar = st.columns(2)
    with coluna_ok:
        if st.button("Confirmar", type="primary", width="stretch"):
            with tratar_erros(f"{acao} o fornecedor") as resultado, session_scope() as session:
                alternar_status(session, fornecedor["id"], ativo=ativar)
            if resultado:
                st.toast(f"{fornecedor['nome']} {'reativado' if ativar else 'inativado'}.")
                st.rerun()
    with coluna_cancelar:
        if st.button("Cancelar", width="stretch"):
            st.rerun()


def main() -> None:
    ctx = shell("LabVida - Fornecedores", layout="wide", permissao="compras:gerenciar_fornecedores")
    renderizar_menu(ctx["usuario_id"])

    renderizar_cabecalho(
        titulo="Fornecedores",
        subtitulo="Cadastro de fornecedores de insumos",
        icone=ICONE_FORNECEDOR,
    )

    aba_listar, aba_cadastrar = st.tabs(["Fornecedores", "Cadastrar"])

    with aba_listar:
        _render_listar()
    with aba_cadastrar:
        _render_cadastrar()


def _render_cadastrar() -> None:
    renderizar_secao(titulo="Novo fornecedor")

    with st.form("form_fornecedor", clear_on_submit=True):
        nome = st.text_input("Nome do fornecedor")
        cnpj = st.text_input("CNPJ (somente numeros)", max_chars=14)
        enviado = st.form_submit_button("Cadastrar", type="primary")

    if not enviado:
        return

    with tratar_erros("cadastrar o fornecedor") as resultado, session_scope() as session:
        fornecedor = criar_fornecedor(session, FornecedorCreate(nome=nome, cnpj=cnpj))
    if resultado:
        st.toast(f"Fornecedor {fornecedor.nome} cadastrado.")
        st.rerun()


def _render_listar() -> None:
    with tratar_erros("carregar os fornecedores") as resultado, session_scope() as session:
        fornecedores = listar_todos(session)
    if not resultado:
        return

    linhas = _linhas(fornecedores)
    ativos = sum(1 for linha in linhas if linha["situacao"] == "Ativo")

    coluna_total, coluna_ativos, coluna_inativos = st.columns(3)
    coluna_total.metric("Fornecedores", len(linhas))
    coluna_ativos.metric("Ativos", ativos)
    coluna_inativos.metric("Inativos", len(linhas) - ativos)

    grid = renderizar_grid(
        linhas,
        colunas=_COLUNAS,
        chave="grid_fornecedores",
        selecao="linha",
        altura=380,
        mensagem_vazio="Nenhum fornecedor cadastrado. Use a aba **Cadastrar**.",
    )

    selecionado = grid.selecionado
    if selecionado is None:
        st.caption("Selecione um fornecedor na tabela para editar ou alterar a situacao.")
        return

    st.divider()
    st.write(f"Selecionado: **{selecionado['nome']}**")

    coluna_editar, coluna_situacao, _ = st.columns([1, 1, 3])
    esta_ativo = selecionado["situacao"] == "Ativo"

    with coluna_editar:
        if st.button("Editar", width="stretch"):
            _dialogo_editar(selecionado)
    with coluna_situacao:
        rotulo = "Inativar" if esta_ativo else "Reativar"
        if st.button(rotulo, width="stretch"):
            _dialogo_situacao(selecionado, ativar=not esta_ativo)


if __name__ == "__main__":
    main()
