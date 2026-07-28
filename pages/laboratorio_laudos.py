import streamlit as st
from sqlalchemy.orm import Session
from sqlalchemy import select

from src.atendimento.ordem_servico.models import OsItem
from src.cadastro.medico.service import listar_medicos_ativos
from src.db import session_scope
from src.laboratorial.dtos import LaudoCreate, LaudoUpdate
from src.laboratorial.models import StatusLaudo, StatusResultado
from src.laboratorial.service import LaboratorialService
from src.ui import renderizar_menu, shell
from src.ui_components import (
    renderizar_cabecalho,
    renderizar_empty_state,
    renderizar_secao,
)
from src.ui_icons import ICONE_ADICIONAR, ICONE_LAUDO, ICONE_MEDICO, ICONE_RESULTADO

def _listar_os_itens(session: Session):
    from src.atendimento.ordem_servico.dtos import StatusOrdemServico, StatusOsItem
    from src.atendimento.ordem_servico.models import OrdemServico
    return session.scalars(
        select(OsItem)
        .join(OsItem.ordem_servico)
        .where(
            OrdemServico.status == StatusOrdemServico.EM_ANALISE,
            OsItem.status != StatusOsItem.CANCELADO,
        )
    ).all()


def main() -> None:
    ctx = shell("Emissao de Laudos", layout="wide", permissao="laboratorial:liberar_laudo")
    renderizar_menu(ctx["usuario_id"])

    renderizar_cabecalho(
        titulo="Laudos e Liberacao",
        subtitulo="Emita e assine digitalmente os laudos dos exames",
        icone=ICONE_LAUDO,
    )

    with session_scope() as session:
        itens = _listar_os_itens(session)
        if not itens:
            renderizar_empty_state(
                icone=ICONE_LAUDO,
                titulo="Nenhuma OS cadastrada",
                mensagem="Cadastre uma Ordem de Servico para emitir laudos.",
            )
            return

        service = LaboratorialService(session)
        opcoes_itens = {
            f"{item.ordem_servico.codigo_os} — {item.procedimento.nome}": item
            for item in itens
            if item.ordem_servico
            and (
                service.listar_resultados_por_os_item(item.id)
                or service.obter_laudo_por_os_item(item.id)
            )
        }

        if not opcoes_itens:
            renderizar_empty_state(
                icone=ICONE_LAUDO,
                titulo="Nenhum resultado disponivel",
                mensagem="Nenhuma OS possui resultados para emitir laudo.",
            )
            return

        escolha = st.selectbox(
            "Selecione a OS / Exame para Laudo", options=list(opcoes_itens.keys())
        )
        item_selecionado = opcoes_itens[escolha]

        laudo = service.obter_laudo_por_os_item(item_selecionado.id)
        resultados = service.listar_resultados_por_os_item(item_selecionado.id)

        renderizar_secao(
            titulo=f"{ICONE_RESULTADO} Resultados do Exame",
            descricao="Analitos registrados para este exame",
        )

        todos_revisados = True
        if resultados:
            for res in resultados:
                if res.status != StatusResultado.REVISADO:
                    todos_revisados = False
                st.write(f"- **{res.analito}:** {res.valor} ({res.status.value})")
        else:
            st.warning("Nenhum resultado registrado ainda.")
            todos_revisados = False

        if not todos_revisados:
            st.warning(
                "Atencao: Nem todos os resultados foram digitados e REVISADOS. "
                "Voce nao deve liberar o laudo ainda."
            )

        st.divider()

        if not laudo:
            renderizar_empty_state(
                icone=ICONE_ADICIONAR,
                titulo="Laudo nao iniciado",
                mensagem="Este exame ainda nao tem Laudo. Clique abaixo para iniciar o Rascunho.",
                rotulo_acao="Criar Rascunho de Laudo",
            )

            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("Criar Rascunho de Laudo", type="primary", width="stretch"):
                    try:
                        service.criar_laudo(LaudoCreate(os_item_id=item_selecionado.id))
                        session.commit()
                        st.toast("Laudo criado como Rascunho.", icon="\u2705")
                        st.rerun()
                    except ValueError as e:
                        st.error(str(e))
            return

        renderizar_secao(
            titulo=f"Status do Laudo: {laudo.status.value}",
            descricao="Assine e libere o laudo quando todos os resultados estiverem revisados",
        )

        if laudo.status == StatusLaudo.LIBERADO:
            st.success(
                f"Laudo liberado em {laudo.liberado_em.strftime('%d/%m/%Y %H:%M')}"
            )
            st.write(
                f"**Assinatura Digital:** {laudo.assinatura_digital or 'Sem assinatura'}"
            )
        else:
            medicos = [
                medico
                for medico in listar_medicos_ativos(session)
                if medico.responsavel_tecnico
            ]
            medico_opts = {
                f"{medico.nome} · CRM {medico.crm}/{medico.uf_crm}": medico.id
                for medico in medicos
            }

            if not medico_opts:
                renderizar_empty_state(
                    icone=ICONE_MEDICO,
                    titulo="Nenhum responsavel tecnico",
                    mensagem="Nenhum medico responsavel tecnico ativo esta cadastrado. Cadastre um medico com a flag de responsavel tecnico.",
                )
                st.stop()

            col1, col2 = st.columns(2)
            with col1:
                responsavel = st.selectbox(
                    "Responsavel Tecnico", options=list(medico_opts.keys())
                )
            with col2:
                assinatura = st.text_input("Assinatura Digital (Hash/Chave)")

            if st.button("Salvar e LIBERAR Laudo", type="primary", width="stretch", disabled=not todos_revisados):
                try:
                    service.atualizar_laudo(
                        laudo.id,
                        LaudoUpdate(
                            responsavel_tecnico_id=medico_opts[responsavel],
                            assinatura_digital=assinatura if assinatura else None,
                            status=StatusLaudo.LIBERADO,
                        ),
                        usuario_id=ctx["usuario_id"],
                    )
                    session.commit()
                    st.toast("Laudo LIBERADO com sucesso!", icon="\u2705")
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))


if __name__ == "__main__":
    main()
