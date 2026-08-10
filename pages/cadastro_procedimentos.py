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
    obter_valor_vigente,
    vincular_insumo_procedimento,
)
from src.cadastro.procedimento.repository import listar_insumos_do_procedimento
from src.compras.insumo.service import listar_insumos
from src.cadastro.convenio.errors import ConvenioNaoEncontrado
from src.db import session_scope
from src.ui import renderizar_menu, shell, usuario_id_logado
from src.ui_components import (
    ColunaGrid,
    renderizar_cabecalho,
    renderizar_grid,
    renderizar_secao,
)
from src.ui_icons import ICONE_PROCEDIMENTO


def main() -> None:
    ctx = shell("LabVida - Procedimentos", permissao="cadastro:procedimentos:escrever")
    renderizar_menu(ctx["usuario_id"])

    renderizar_cabecalho(
        titulo="Procedimentos",
        subtitulo="Catalogo de procedimentos (TUSS) e valores contratados por convenio",
        icone=ICONE_PROCEDIMENTO,
    )

    tab_nomes = ["Procedimentos", "Valores por convênio", "Insumos (Ficha Técnica)"]
    aba = st.radio("Seção", tab_nomes, horizontal=True, key="tab_proc", label_visibility="collapsed")

    if aba == tab_nomes[0]:
        _render_procedimentos()
    elif aba == tab_nomes[1]:
        _render_valores()
    elif aba == tab_nomes[2]:
        _render_insumos_procedimento()


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
                criar_procedimento(session, dto, usuario_id_logado())
        except (ValidationError, ValueError) as error:
            st.error(_mensagem(error))
        except CodigoTussDuplicado as error:
            st.error(str(error))
        else:
            st.success("Procedimento cadastrado com sucesso")

    procedimentos = _procedimentos()
    if procedimentos:
        renderizar_grid(
            [
                {"codigo_tuss": p.codigo_tuss, "nome": p.nome, "setor": p.setor or "—"}
                for p in procedimentos
            ],
            colunas=[
                ColunaGrid("codigo_tuss", "TUSS", largura=120),
                ColunaGrid("nome", "Procedimento"),
                ColunaGrid("setor", "Setor", largura=170),
            ],
            chave="grid_procedimentos",
            altura=360,
        )
    else:
        st.info("Nenhum procedimento cadastrado")


def _render_valores() -> None:
    procedimentos = _procedimentos()
    with session_scope() as session:
        convenios = listar_convenios_ativos(session)

    if not procedimentos:
        st.info("Cadastre procedimentos para definir valores")
        return

    procedimentos_opcoes = {f"{p.codigo_tuss} - {p.nome}": p.id for p in procedimentos}
    # `None` = tabela PARTICULAR (balcao), que passou a existir na fase F3.
    convenios_opcoes = {_PARTICULAR: None} | {c.nome: c.id for c in convenios}

    _render_tabela_vigente(procedimentos, convenios)

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
            definir_valor(session, dto, usuario_id_logado())
    except (ValidationError, ValueError) as error:
        st.error(_mensagem(error))
    except (ProcedimentoNaoEncontrado, ConvenioNaoEncontrado) as error:
        st.error(str(error))
    else:
        st.success(
            "Valor definido. A vigência anterior foi encerrada no dia anterior — "
            "não existem dois preços válidos na mesma data."
        )
        st.rerun()


_PARTICULAR = "Particular (balcão)"


def _render_tabela_vigente(procedimentos: list, convenios: list) -> None:
    """Grade do que esta valendo hoje — a tela nao listava valor nenhum antes."""
    nomes_convenio = {c.id: c.nome for c in convenios}
    hoje = date.today()

    linhas = []
    with session_scope() as session:
        for procedimento in procedimentos:
            for convenio_id in [None] + [c.id for c in convenios]:
                valor = obter_valor_vigente(session, procedimento.id, convenio_id, hoje)
                if valor is None:
                    continue
                linhas.append({
                    "procedimento": f"{procedimento.codigo_tuss} - {procedimento.nome}",
                    "tabela": _PARTICULAR if convenio_id is None else nomes_convenio.get(convenio_id, "?"),
                    "valor": valor,
                })

    renderizar_secao(titulo="Tabela vigente hoje")
    renderizar_grid(
        linhas,
        colunas=[
            ColunaGrid("procedimento", "Procedimento"),
            ColunaGrid("tabela", "Tabela", largura=200),
            ColunaGrid("valor", "Valor", tipo="moeda", largura=140),
        ],
        chave="grid_tabela_precos",
        altura=300,
        mensagem_vazio="Nenhum preço vigente. Defina um valor abaixo.",
    )


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


def _render_insumos_procedimento() -> None:
    procedimentos = _procedimentos()
    with session_scope() as session:
        insumos = listar_insumos(session)

    if not procedimentos or not insumos:
        st.info("Cadastre procedimentos e insumos para configurar a ficha técnica.")
        return

    procedimentos_opcoes = {f"{p.codigo_tuss} - {p.nome}": p for p in procedimentos}
    insumos_opcoes = {i.nome: i.id for i in insumos}

    proc_label = st.selectbox("Selecione o Procedimento", options=list(procedimentos_opcoes.keys()))
    procedimento_sel = procedimentos_opcoes[proc_label]

    col1, col2 = st.columns([2, 1])

    with col1:
        renderizar_secao(titulo=f"Insumos vinculados a {procedimento_sel.nome}")
        with session_scope() as session:
            links = listar_insumos_do_procedimento(session, procedimento_sel.id)
            insumo_nomes = {i.id: i.nome for i in insumos}

        if links:
            renderizar_grid(
                [
                    {
                        "insumo": insumo_nomes.get(l.insumo_material_id, "Desconhecido"),
                        "quantidade": l.quantidade_necessaria,
                    }
                    for l in links
                ],
                colunas=[
                    ColunaGrid("insumo", "Insumo Material"),
                    ColunaGrid("quantidade", "Qtd Necessária por Exame", tipo="numero", largura=200),
                ],
                chave="grid_proc_insumos",
                altura=250,
            )
        else:
            st.info("Nenhum insumo vinculado a este procedimento.")

    with col2:
        renderizar_secao(titulo="Vincular Novo Insumo")
        insumo_nome = st.selectbox("Insumo", options=list(insumos_opcoes.keys()))
        qtd_nec = st.number_input("Quantidade necessária", min_value=0.1, value=1.0, step=0.5)
        if st.button("Salvar Vínculo", type="primary"):
            insumo_id = insumos_opcoes[insumo_nome]
            with session_scope() as session:
                vincular_insumo_procedimento(session, procedimento_sel.id, insumo_id, qtd_nec)
            st.success("Insumo vinculado com sucesso!")
            st.rerun()


if __name__ == "__main__":
    main()
