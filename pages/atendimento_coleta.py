import streamlit as st

from src.atendimento.amostra.dtos import ColetaCreate, TipoMaterial
from src.atendimento.amostra.errors import (
    ColetaNaoPermitida,
    ColetorInvalido,
    OrdemServicoInexistente,
)
from src.atendimento.amostra.service import listar_amostras, registrar_coleta
from src.atendimento.ordem_servico.dtos import StatusOrdemServico, StatusOsItem
from src.atendimento.ordem_servico.service import listar_itens, listar_os
from src.cadastro.procedimento.service import listar_procedimentos_ativos
from src.cadastro.service import listar_pacientes_ativos
from src.db import session_scope
from src.ui import renderizar_menu, shell, usuario_id_logado
from src.ui_components import (
    renderizar_cabecalho,
    renderizar_empty_state,
    renderizar_secao,
)
from src.ui_icons import ICONE_AMOSTRA, ICONE_COLETA, ICONE_OS

_STATUS_BLOQUEADO = {StatusOrdemServico.CONCLUIDA, StatusOrdemServico.CANCELADA}


def main() -> None:
    ctx = shell("LabVida - Coleta", permissao="atendimento:coletar")
    renderizar_menu(ctx["usuario_id"])

    renderizar_cabecalho(
        titulo="Registro de Coleta",
        subtitulo="Gera a amostra (cadeia de custodia) e vincula o coletor a OS",
        icone=ICONE_COLETA,
    )

    with session_scope() as session:
        ordens = [o for o in listar_os(session) if o.status not in _STATUS_BLOQUEADO]
        pacientes = {p.id: p.nome for p in listar_pacientes_ativos(session)}

    if not ordens:
        renderizar_empty_state(
            icone=ICONE_COLETA,
            titulo="Nenhuma OS disponivel",
            mensagem="Nao ha Ordens de Servico disponiveis para coleta no momento.",
        )
        return

    renderizar_secao(
        titulo=f"{ICONE_OS} Selecionar Ordem de Servico",
        descricao="Escolha a OS e o tipo de material para registrar a coleta",
    )

    opcoes = {
        f"{o.codigo_os} — {pacientes.get(o.paciente_id, '—')} ({o.status})": o.id for o in ordens
    }

    col1, col2 = st.columns(2)
    with col1:
        label = st.selectbox("Ordem de Servico", options=list(opcoes.keys()))
    with col2:
        tipo_material = st.selectbox(
            "Tipo de material", options=list(TipoMaterial), format_func=_formatar_material
        )

    ordem_id = opcoes[label]

    # Issue #15: mostrar o que a OS pede, para o coletor saber o que coletar.
    with session_scope() as session:
        itens = listar_itens(session, ordem_id)
        procedimentos = {p.id: p.nome for p in listar_procedimentos_ativos(session)}

    itens_ativos = [i for i in itens if i.status != StatusOsItem.CANCELADO]
    st.markdown(f"**{ICONE_OS} Exames solicitados nesta OS**", unsafe_allow_html=True)
    if itens_ativos:
        st.dataframe(
            [
                {
                    "Procedimento": procedimentos.get(i.procedimento_id, "—"),
                    "Status do item": i.status,
                }
                for i in itens_ativos
            ],
            hide_index=True,
            width="stretch",
        )
        st.caption(
            "Registre uma coleta por tipo de material necessário para cobrir estes exames."
        )
    else:
        st.caption("Esta OS não possui procedimentos ativos.")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Registrar Coleta", type="primary", width="stretch"):
        try:
            dto = ColetaCreate(
                ordem_servico_id=ordem_id,
                tipo_material=tipo_material,
                coletor_usuario_id=usuario_id_logado(),
            )
            with session_scope() as session:
                amostra = registrar_coleta(session, dto)
        except (OrdemServicoInexistente, ColetorInvalido, ColetaNaoPermitida) as error:
            st.error(str(error))
        else:
            st.success(f"Coleta registrada. Amostra: **{amostra.codigo_barras}**")
            st.toast(f"Amostra {amostra.codigo_barras} gerada", icon="\u2705")

    st.markdown("<br>", unsafe_allow_html=True)

    renderizar_secao(
        titulo=f"{ICONE_COLETA} Amostras desta OS",
        descricao="Amostras coletadas para a Ordem de Servico selecionada",
    )

    with session_scope() as session:
        amostras = listar_amostras(session, ordem_id)

    if amostras:
        st.dataframe(
            [
                {
                    "Codigo de barras": a.codigo_barras,
                    "Material": _formatar_material(a.tipo_material),
                    "Status": a.status,
                }
                for a in amostras
            ],
            hide_index=True,
            width="stretch",
        )
    else:
        renderizar_empty_state(
            icone=ICONE_AMOSTRA,
            titulo="Nenhuma amostra coletada",
            mensagem="As amostras coletadas para esta OS aparecerao aqui.",
        )


def _formatar_material(material: TipoMaterial) -> str:
    return TipoMaterial(material).value.capitalize()


if __name__ == "__main__":
    main()
