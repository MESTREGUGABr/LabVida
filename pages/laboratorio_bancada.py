"""Esteira operacional de amostras recebidas na bancada laboratorial."""

import streamlit as st
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.atendimento.amostra.models import Amostra
from src.atendimento.amostra.dtos import StatusAmostra
from src.atendimento.ordem_servico.dtos import StatusOrdemServico, StatusOsItem
from src.atendimento.ordem_servico.models import OrdemServico, OsItem
from src.cadastro.models import Paciente
from src.db import session_scope
from src.laboratorial.dtos import ResultadoCreate, ResultadoUpdate
from src.laboratorial.models import StatusResultado
from src.laboratorial.service import LaboratorialService
from src.ui import renderizar_menu, shell, usuario_id_logado
from src.ui_components import renderizar_cabecalho, renderizar_secao
from src.ui_icons import ICONE_BANCADA


def main() -> None:
    ctx = shell("LabVida - Esteira da Bancada", layout="wide", permissao="laboratorial:registrar_resultado")
    renderizar_menu(ctx["usuario_id"])

    renderizar_cabecalho(
        titulo="Esteira da Bancada",
        subtitulo="Amostras recebidas na central, prontas para processamento e revisao tecnica",
        icone=ICONE_BANCADA,
    )

    with session_scope() as session:
        fila = _listar_fila(session)
        equipamentos = list(LaboratorialService(session).listar_equipamentos())

    if not fila:
        st.info("Nenhuma amostra RECEBIDA aguardando processamento.")
        return

    st.markdown("### Triagem por amostra")
    esquerda, direita = st.columns([1.25, 1])

    with esquerda:
        opcoes = {
            f"{amostra.codigo_barras} · {item.procedimento.nome} · {paciente.nome}": amostra.id
            for amostra, ordem, item, paciente in fila
        }
        escolha = st.selectbox("Amostras pendentes", options=list(opcoes))
        amostra_id = opcoes[escolha]

        st.dataframe(
            [
                {
                    "Amostra": amostra.codigo_barras,
                    "OS": ordem.codigo_os,
                    "Paciente": paciente.nome,
                    "Exame": item.procedimento.nome,
                    "Status": amostra.status,
                }
                for amostra, ordem, item, paciente in fila
            ],
            hide_index=True,
            width="stretch",
        )

    selecionada = next(row for row in fila if row[0].id == amostra_id)
    amostra, ordem, item, paciente = selecionada

    with direita:
        st.markdown(f"**AMOSTRA SELECIONADA**\n\n## {amostra.codigo_barras}")
        st.write(f"**Paciente:** {paciente.nome}")
        st.write(f"**Ordem de Serviço:** {ordem.codigo_os}")
        st.write(f"**Exame:** {item.procedimento.nome}")
        st.write(f"**Status da amostra:** `{amostra.status}`")
        st.write(f"**Status da OS:** `{ordem.status}`")

    _render_resultados(amostra, item, equipamentos)


def _listar_fila(session):
    return list(
        session.execute(
            select(Amostra, OrdemServico, OsItem, Paciente)
            .join(OrdemServico, OrdemServico.id == Amostra.ordem_servico_id)
            .join(OsItem, OsItem.ordem_servico_id == OrdemServico.id)
            .join(Paciente, Paciente.id == OrdemServico.paciente_id)
            .options(joinedload(OsItem.procedimento))
            .where(
                Amostra.status == StatusAmostra.RECEBIDA,
                OrdemServico.status == StatusOrdemServico.EM_ANALISE,
                OsItem.status != StatusOsItem.CANCELADO,
            )
            .order_by(Amostra.codigo_barras, OsItem.id)
        ).all()
    )


def _render_resultados(amostra, item, equipamentos) -> None:
    with session_scope() as session:
        service = LaboratorialService(session)
        resultados = list(service.listar_resultados_por_os_item(item.id))

    st.divider()
    renderizar_secao(titulo="Resultados do exame")
    if resultados:
        for resultado in resultados:
            _render_resultado(resultado, item, equipamentos)
    else:
        st.info("Nenhum resultado lançado para este exame.")

    with st.expander("Registrar resultado", expanded=not resultados):
        _render_novo_resultado(item, equipamentos)


def _render_resultado(resultado, item, equipamentos) -> None:
    col1, col2, col3 = st.columns([1.4, 1, 1])
    with col1:
        st.write(f"**{resultado.analito}**")
        st.caption(f"Valor: {resultado.valor}")
    with col2:
        st.write(f"Status: `{resultado.status.value}`")
    with col3:
        if resultado.status == StatusResultado.AGUARDANDO_REVISAO:
            if st.button("Marcar como revisado", key=f"review-{resultado.id}"):
                with session_scope() as session:
                    LaboratorialService(session).atualizar_resultado(
                        resultado.id,
                        ResultadoUpdate(
                            status=StatusResultado.REVISADO,
                            usuario_id=usuario_id_logado(),
                        ),
                    )
                    session.commit()
                st.rerun()


def _render_novo_resultado(item, equipamentos) -> None:
    with st.form(f"novo-resultado-{item.id}"):
        analito = st.text_input("Analito", placeholder="Ex: Hemoglobina")
        valor = st.text_input("Valor encontrado")
        equipamento_options = {"Sem equipamento informado": None}
        equipamento_options.update({equipamento.nome: equipamento.id for equipamento in equipamentos})
        equipamento = st.selectbox("Equipamento", list(equipamento_options))

        if st.form_submit_button("Registrar resultado", type="primary"):
            if not analito.strip() or not valor.strip():
                st.error("Informe o analito e o valor encontrado.")
                return
            with session_scope() as session:
                LaboratorialService(session).registrar_resultado(
                    ResultadoCreate(
                        os_item_id=item.id,
                        equipamento_id=equipamento_options[equipamento],
                        analito=analito.strip(),
                        valor=valor.strip(),
                        usuario_id=usuario_id_logado(),
                    )
                )
                session.commit()
            st.success("Resultado registrado e enviado para revisão.")
            st.rerun()


if __name__ == "__main__":
    main()
