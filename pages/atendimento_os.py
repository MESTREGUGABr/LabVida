from decimal import Decimal

import streamlit as st
from pydantic import ValidationError

from src.atendimento.autorizacao.dtos import AutorizacaoCreate, StatusAutorizacao
from src.atendimento.autorizacao.service import listar_autorizacoes, registrar_autorizacao
from src.atendimento.ordem_servico.dtos import (
    OrdemServicoCreate,
    OsItemInput,
)
from src.atendimento.ordem_servico.errors import (
    ConvenioInvalidoParaOS,
    ItemNaoPodeSerCancelado,
    MedicoInvalidoParaOS,
    OrdemServicoNaoPodeSerCancelada,
    PacienteInvalidoParaOS,
    ProcedimentoInvalidoParaOS,
    UnidadeInvalidaParaOS,
    UsuarioNaoAutorizadoParaCancelamento,
    ValorItemNaoDefinido,
)
from src.atendimento.ordem_servico.service import (
    abrir_os,
    cancelar_item_os,
    cancelar_os,
    listar_historico,
    listar_itens,
    listar_os,
)
from src.cadastro.convenio.service import listar_convenios, listar_convenios_ativos
from src.cadastro.medico.service import listar_medicos_ativos
from src.cadastro.procedimento.service import listar_procedimentos_ativos
from src.cadastro.service import listar_pacientes_ativos
from src.cadastro.unidade.service import listar_unidades_ativas
from src.db import session_scope
from src.ui import renderizar_menu, shell, usuario_id_logado
from src.ui_components import (
    renderizar_cabecalho,
    renderizar_empty_state,
    renderizar_secao,
    renderizar_status_badge,
)
from src.ui_theme import ACCENT_ORANGE
from src.ui_icons import (
    ICONE_AUTORIZACAO,
    ICONE_BUSCA,
    ICONE_CONVENIO,
    ICONE_HISTORICO,
    ICONE_OS,
    ICONE_PRODUTIVIDADE,
    ICONE_USUARIO,
)

_PARTICULAR = "Particular (sem convenio)"
_SEM_MEDICO = "Nao informado"


def main() -> None:
    ctx = shell("LabVida - Ordens de Servico", layout="wide", permissao="atendimento:abrir_os")
    renderizar_menu(ctx["usuario_id"])

    renderizar_cabecalho(
        titulo="Ordens de Servico",
        subtitulo="A OS e a entidade central do fluxo: abre o atendimento e percorre todo o ciclo operacional",
        icone=ICONE_OS,
    )

    tab_abrir, tab_listar = st.tabs(["Abrir OS", "Acompanhar OS"])

    with tab_abrir:
        _render_abrir()

    with tab_listar:
        _render_listar()


def _render_abrir() -> None:
    with session_scope() as session:
        pacientes = listar_pacientes_ativos(session)
        unidades = listar_unidades_ativas(session)
        medicos = listar_medicos_ativos(session)
        convenios = listar_convenios_ativos(session)
        procedimentos = listar_procedimentos_ativos(session)

    if not pacientes or not unidades or not procedimentos:
        renderizar_empty_state(
            icone=ICONE_OS,
            titulo="Pre-requisitos pendentes",
            mensagem="Cadastre ao menos um paciente, uma unidade e um procedimento para abrir uma OS.",
        )
        return

    pacientes_opcoes = {f"{p.nome} - CPF {p.cpf_mascarado}": p.id for p in pacientes}
    unidades_opcoes = {u.nome: u.id for u in unidades}
    medicos_opcoes = {_SEM_MEDICO: None} | {f"{m.nome} ({m.crm}/{m.uf_crm})": m.id for m in medicos}
    convenios_opcoes = {_PARTICULAR: None} | {c.nome: c.id for c in convenios}
    procedimentos_opcoes = {f"{p.codigo_tuss} - {p.nome}": p.id for p in procedimentos}

    renderizar_secao(
        titulo=f"{ICONE_USUARIO} Dados do Atendimento",
        descricao="Selecione o paciente, a unidade de coleta e o medico solicitante",
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        paciente_label = st.selectbox("Paciente", options=list(pacientes_opcoes.keys()))
    with col2:
        unidade_label = st.selectbox("Unidade", options=list(unidades_opcoes.keys()))
    with col3:
        medico_label = st.selectbox("Medico solicitante", options=list(medicos_opcoes.keys()))

    st.markdown("<br>", unsafe_allow_html=True)

    renderizar_secao(
        titulo=f"{ICONE_CONVENIO} Convenio e Procedimentos",
        descricao="Selecione o convenio e os procedimentos solicitados",
    )

    col1, col2 = st.columns([1, 2])
    with col1:
        convenio_label = st.selectbox("Convenio", options=list(convenios_opcoes.keys()))
    convenio_id = convenios_opcoes[convenio_label]

    selecionados = st.multiselect("Procedimentos", options=list(procedimentos_opcoes.keys()))

    valores: dict[str, float] = {}
    if selecionados:
        if convenio_id is not None:
            st.caption("Deixe o valor em 0,00 para usar o valor de tabela vigente do convenio.")

        cols = st.columns(min(len(selecionados), 3))
        for i, label in enumerate(selecionados):
            with cols[i % 3]:
                valores[label] = st.number_input(
                    f"Valor — {label} (R$)",
                    min_value=0.0,
                    value=0.0,
                    step=10.0,
                    key=f"valor_{label}",
                )

    st.markdown("<br>", unsafe_allow_html=True)

    if not st.button("Abrir Ordem de Servico", type="primary", width="stretch"):
        return

    if not selecionados:
        st.error("Selecione ao menos um procedimento.")
        return

    itens = []
    for label in selecionados:
        valor = valores[label]
        valor_negociado = None if (convenio_id is not None and valor == 0) else Decimal(str(valor))
        itens.append(
            OsItemInput(procedimento_id=procedimentos_opcoes[label], valor_negociado=valor_negociado)
        )

    try:
        dto = OrdemServicoCreate(
            paciente_id=pacientes_opcoes[paciente_label],
            unidade_id=unidades_opcoes[unidade_label],
            medico_id=medicos_opcoes[medico_label],
            convenio_id=convenio_id,
            itens=itens,
        )
        with session_scope() as session:
            ordem = abrir_os(session, dto, usuario_id_logado())
    except (ValidationError, ValueError) as error:
        st.error(_mensagem(error))
    except (
        PacienteInvalidoParaOS,
        UnidadeInvalidaParaOS,
        MedicoInvalidoParaOS,
        ConvenioInvalidoParaOS,
        ProcedimentoInvalidoParaOS,
        ValorItemNaoDefinido,
    ) as error:
        st.error(str(error))
    else:
        st.success(f"OS aberta: **{ordem.codigo_os}**")
        st.toast(f"OS {ordem.codigo_os} aberta com sucesso", icon="\u2705")


def _render_listar() -> None:
    with session_scope() as session:
        ordens = listar_os(session)
        pacientes = {p.id: p.nome for p in listar_pacientes_ativos(session)}
        convenios = {c.id: c.nome for c in listar_convenios(session)}
        unidades = {u.id: u.nome for u in listar_unidades_ativas(session)}
        procedimentos = {p.id: p.nome for p in listar_procedimentos_ativos(session)}

    if not ordens:
        renderizar_empty_state(
            icone=ICONE_OS,
            titulo="Nenhuma Ordem de Servico",
            mensagem="As OS abertas aparecerao aqui para acompanhamento do fluxo.",
        )
        return

    renderizar_secao(
        titulo=f"{ICONE_PRODUTIVIDADE} Ordens de Servico",
        descricao=f"{len(ordens)} OS(s) encontrada(s)",
    )

    st.dataframe(
        [
            {
                "Codigo": o.codigo_os,
                "Paciente": pacientes.get(o.paciente_id, "\u2014"),
                "Convenio": convenios.get(o.convenio_id, _PARTICULAR),
                "Unidade": unidades.get(o.unidade_id, "\u2014"),
                "Status": o.status,
                "Abertura": o.aberta_em.strftime("%d/%m/%Y %H:%M"),
            }
            for o in ordens
        ],
        hide_index=True,
        width="stretch",
    )

    st.markdown("<br>", unsafe_allow_html=True)

    renderizar_secao(
        titulo=f"{ICONE_BUSCA} Detalhar Ordem de Servico",
        descricao="Selecione uma OS para ver itens, historico e autorizacoes",
    )

    opcoes = {o.codigo_os: o.id for o in ordens}
    codigo = st.selectbox("OS", options=list(opcoes.keys()), label_visibility="collapsed")
    ordem_id = opcoes[codigo]
    ordem = next(o for o in ordens if o.id == ordem_id)

    with session_scope() as session:
        itens = listar_itens(session, ordem_id)
        historico = listar_historico(session, ordem_id)
        autorizacoes = listar_autorizacoes(session, ordem_id)

    col_itens, col_hist = st.columns(2)

    with col_itens:
        st.markdown(f"**{ICONE_OS} Itens da OS**", unsafe_allow_html=True)
        if itens:
            st.dataframe(
                [
                    {
                        "Procedimento": procedimentos.get(i.procedimento_id, "\u2014"),
                        "Valor": f"R$ {i.valor_negociado:.2f}",
                        "Status": i.status,
                    }
                    for i in itens
                ],
                hide_index=True,
                width="stretch",
            )
        else:
            st.caption("Nenhum item registrado.")

    with col_hist:
        st.markdown(f"**{ICONE_HISTORICO} Historico de Status**", unsafe_allow_html=True)
        if historico:
            st.dataframe(
                [
                    {"Status": h.status, "Em": h.ocorrido_em.strftime("%d/%m/%Y %H:%M")}
                    for h in historico
                ],
                hide_index=True,
                width="stretch",
            )
        else:
            st.caption("Nenhum historico registrado.")

    st.markdown("<br>", unsafe_allow_html=True)

    _render_cancelamento(ordem_id, ordem, itens, procedimentos)

    _render_autorizacoes(ordem_id, autorizacoes)


def _render_cancelamento(ordem_id, ordem, itens, procedimentos) -> None:
    st.subheader("Cancelamento")

    with st.form(f"form_cancelar_os_{ordem_id}"):
        confirmar = st.checkbox(
            "Confirmo o cancelamento de todos os itens desta OS",
            key=f"confirmar_cancelar_os_{ordem_id}",
        )
        cancelar_integral = st.form_submit_button("Cancelar OS inteira", type="secondary")

    if cancelar_integral:
        if not confirmar:
            st.warning("Marque a confirmação para cancelar a OS inteira.")
        else:
            _executar_cancelamento(
                lambda session: cancelar_os(session, ordem_id, usuario_id_logado()),
                f"OS {ordem.codigo_os} cancelada com sucesso.",
                (OrdemServicoNaoPodeSerCancelada, UsuarioNaoAutorizadoParaCancelamento),
            )

    st.caption("Ou cancele somente um item da OS que ainda possa ser cancelado.")
    for item in itens:
        procedimento = procedimentos.get(item.procedimento_id, "Procedimento não identificado")

        with st.container(border=True):
            col_detalhe, col_acao = st.columns([4, 1])
            col_detalhe.write(f"**{procedimento}** — {item.status}")
            cancelar_item = col_acao.button(
                "Cancelar item",
                key=f"cancelar_item_{item.id}",
                type="secondary",
            )
            if cancelar_item:
                _executar_cancelamento(
                    lambda session: cancelar_item_os(session, item.id, usuario_id_logado()),
                    f"Item de {procedimento} cancelado.",
                    (ItemNaoPodeSerCancelado, UsuarioNaoAutorizadoParaCancelamento),
                )


def _executar_cancelamento(acao, mensagem_sucesso: str, erros: tuple[type[Exception], ...]) -> None:
    try:
        with session_scope() as session:
            acao(session)
    except erros as error:
        st.error(str(error))
    else:
        st.success(mensagem_sucesso)
        st.rerun()


def _render_autorizacoes(ordem_id, autorizacoes) -> None:
    renderizar_secao(
        titulo=f"{ICONE_AUTORIZACAO} Autorizacoes de Convenio",
        descricao="Consultar e registrar autorizacoes da operadora para esta OS",
    )

    if autorizacoes:
        st.dataframe(
            [
                {
                    "Guia": a.numero_guia,
                    "Status": a.status,
                    "Validade": a.validade.strftime("%d/%m/%Y") if a.validade else "\u2014",
                }
                for a in autorizacoes
            ],
            hide_index=True,
            width="stretch",
        )

    with st.form(f"form_autorizacao_{ordem_id}", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            numero_guia = st.text_input("Numero da guia")
        with col2:
            status = st.selectbox("Status", options=list(StatusAutorizacao))
        with col3:
            validade = st.date_input("Validade (opcional)", value=None, format="DD/MM/YYYY")
        submitted = st.form_submit_button("Registrar autorizacao", type="primary")

    if not submitted:
        return

    try:
        dto = AutorizacaoCreate(
            ordem_servico_id=ordem_id,
            numero_guia=numero_guia,
            status=status,
            validade=validade,
        )
        with session_scope() as session:
            registrar_autorizacao(session, dto)
    except (ValidationError, ValueError) as error:
        st.error(_mensagem(error))
    else:
        st.success("Autorizacao registrada")
        st.rerun()


def _mensagem(error: Exception) -> str:
    if isinstance(error, ValidationError):
        return str(error.errors()[0]["msg"]).replace("Value error, ", "")
    return str(error)


if __name__ == "__main__":
    main()
