import streamlit as st

from src.atendimento.amostra.dtos import ColetaCreate, TipoMaterial
from src.atendimento.amostra.errors import (
    ColetaNaoPermitida,
    ColetorInvalido,
    OrdemServicoInexistente,
)
from src.atendimento.amostra.service import listar_amostras, registrar_coleta
from src.atendimento.ordem_servico.dtos import StatusOrdemServico
from src.atendimento.ordem_servico.service import listar_os
from src.cadastro.service import listar_pacientes_ativos
from src.db import session_scope
from src.ui import exigir_login, usuario_id_logado

_STATUS_BLOQUEADO = {StatusOrdemServico.CONCLUIDA, StatusOrdemServico.CANCELADA}


def main() -> None:
    st.set_page_config(page_title="LabVida - Coleta")
    exigir_login()

    st.title("Registro de Coleta")
    st.caption("Gera a amostra (cadeia de custódia) e vincula o coletor à OS")

    with session_scope() as session:
        ordens = [o for o in listar_os(session) if o.status not in _STATUS_BLOQUEADO]
        pacientes = {p.id: p.nome for p in listar_pacientes_ativos(session)}

    if not ordens:
        st.info("Nenhuma Ordem de Serviço disponível para coleta")
        return

    opcoes = {
        f"{o.codigo_os} — {pacientes.get(o.paciente_id, '—')} ({o.status})": o.id for o in ordens
    }
    label = st.selectbox("Ordem de Serviço", options=list(opcoes.keys()))
    ordem_id = opcoes[label]

    tipo_material = st.selectbox("Tipo de material", options=list(TipoMaterial), format_func=_formatar_material)

    if st.button("Registrar coleta", type="primary"):
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

    with session_scope() as session:
        amostras = listar_amostras(session, ordem_id)

    st.subheader("Amostras desta OS")
    if amostras:
        st.dataframe(
            [
                {
                    "Código de barras": a.codigo_barras,
                    "Material": _formatar_material(a.tipo_material),
                    "Status": a.status,
                }
                for a in amostras
            ],
            hide_index=True,
            use_container_width=True,
        )
    else:
        st.info("Nenhuma amostra coletada ainda")


def _formatar_material(material: TipoMaterial) -> str:
    return TipoMaterial(material).value.capitalize()


if __name__ == "__main__":
    main()
