from decimal import Decimal

import streamlit as st
from pydantic import ValidationError

from src.atendimento.autorizacao.dtos import AutorizacaoCreate, StatusAutorizacao
from src.atendimento.autorizacao.service import listar_autorizacoes, registrar_autorizacao
from src.atendimento.ordem_servico.dtos import OrdemServicoCreate, OsItemInput
from src.atendimento.ordem_servico.errors import (
    ConvenioInvalidoParaOS,
    MedicoInvalidoParaOS,
    PacienteInvalidoParaOS,
    ProcedimentoInvalidoParaOS,
    UnidadeInvalidaParaOS,
    ValorItemNaoDefinido,
)
from src.atendimento.ordem_servico.service import (
    abrir_os,
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
from src.ui import exigir_login, usuario_id_logado

_PARTICULAR = "Particular (sem convênio)"
_SEM_MEDICO = "Não informado"


def main() -> None:
    st.set_page_config(page_title="LabVida - Ordens de Serviço", layout="wide")
    exigir_login()

    st.title("Ordens de Serviço")
    st.caption("A OS é a entidade-espinha: abre o atendimento e percorre todo o fluxo")

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
        st.info("Cadastre ao menos um paciente, uma unidade e um procedimento para abrir uma OS.")
        return

    pacientes_opcoes = {f"{p.nome} - CPF {p.cpf}": p.id for p in pacientes}
    unidades_opcoes = {u.nome: u.id for u in unidades}
    medicos_opcoes = {_SEM_MEDICO: None} | {f"{m.nome} ({m.crm}/{m.uf_crm})": m.id for m in medicos}
    convenios_opcoes = {_PARTICULAR: None} | {c.nome: c.id for c in convenios}
    procedimentos_opcoes = {f"{p.codigo_tuss} - {p.nome}": p.id for p in procedimentos}

    paciente_label = st.selectbox("Paciente", options=list(pacientes_opcoes.keys()))
    unidade_label = st.selectbox("Unidade", options=list(unidades_opcoes.keys()))
    medico_label = st.selectbox("Médico solicitante", options=list(medicos_opcoes.keys()))
    convenio_label = st.selectbox("Convênio", options=list(convenios_opcoes.keys()))
    convenio_id = convenios_opcoes[convenio_label]

    selecionados = st.multiselect("Procedimentos", options=list(procedimentos_opcoes.keys()))
    if convenio_id is not None:
        st.caption("Deixe o valor em 0,00 para usar o valor de tabela vigente do convênio.")

    valores: dict[str, float] = {}
    for label in selecionados:
        valores[label] = st.number_input(
            f"Valor negociado — {label} (R$)",
            min_value=0.0,
            value=0.0,
            step=10.0,
            key=f"valor_{label}",
        )

    if not st.button("Abrir OS", type="primary"):
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


def _render_listar() -> None:
    with session_scope() as session:
        ordens = listar_os(session)
        pacientes = {p.id: p.nome for p in listar_pacientes_ativos(session)}
        convenios = {c.id: c.nome for c in listar_convenios(session)}
        unidades = {u.id: u.nome for u in listar_unidades_ativas(session)}
        procedimentos = {p.id: p.nome for p in listar_procedimentos_ativos(session)}

    if not ordens:
        st.info("Nenhuma Ordem de Serviço aberta")
        return

    st.dataframe(
        [
            {
                "Código": o.codigo_os,
                "Paciente": pacientes.get(o.paciente_id, "—"),
                "Convênio": convenios.get(o.convenio_id, _PARTICULAR),
                "Unidade": unidades.get(o.unidade_id, "—"),
                "Status": o.status,
                "Aberta em": o.aberta_em.strftime("%d/%m/%Y %H:%M"),
            }
            for o in ordens
        ],
        hide_index=True,
        use_container_width=True,
    )

    opcoes = {o.codigo_os: o.id for o in ordens}
    codigo = st.selectbox("Detalhar OS", options=list(opcoes.keys()))
    ordem_id = opcoes[codigo]

    with session_scope() as session:
        itens = listar_itens(session, ordem_id)
        historico = listar_historico(session, ordem_id)
        autorizacoes = listar_autorizacoes(session, ordem_id)

    st.subheader("Itens")
    st.dataframe(
        [
            {
                "Procedimento": procedimentos.get(i.procedimento_id, "—"),
                "Valor": f"R$ {i.valor_negociado:.2f}",
                "Status": i.status,
            }
            for i in itens
        ],
        hide_index=True,
        use_container_width=True,
    )

    st.subheader("Histórico de status")
    st.dataframe(
        [{"Status": h.status, "Em": h.ocorrido_em.strftime("%d/%m/%Y %H:%M")} for h in historico],
        hide_index=True,
        use_container_width=True,
    )

    _render_autorizacoes(ordem_id, autorizacoes)


def _render_autorizacoes(ordem_id, autorizacoes) -> None:
    st.subheader("Autorizações de convênio")
    if autorizacoes:
        st.dataframe(
            [
                {
                    "Guia": a.numero_guia,
                    "Status": a.status,
                    "Validade": a.validade.strftime("%d/%m/%Y") if a.validade else "—",
                }
                for a in autorizacoes
            ],
            hide_index=True,
            use_container_width=True,
        )

    with st.form(f"form_autorizacao_{ordem_id}", clear_on_submit=True):
        numero_guia = st.text_input("Número da guia")
        status = st.selectbox("Status", options=list(StatusAutorizacao))
        validade = st.date_input("Validade (opcional)", value=None, format="DD/MM/YYYY")
        submitted = st.form_submit_button("Registrar autorização")

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
        st.success("Autorização registrada")
        st.rerun()


def _mensagem(error: Exception) -> str:
    if isinstance(error, ValidationError):
        return str(error.errors()[0]["msg"]).replace("Value error, ", "")
    return str(error)


if __name__ == "__main__":
    main()
