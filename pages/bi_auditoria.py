"""Auditoria — ocorrencias registradas no log de auditoria do sistema.

Diferente das outras 4 paginas de BI, esta consulta `auditoria_log` direto,
sem passar pelo ETL/esquema estrela: e um log de eventos imutavel (nao muda
de regime como financeiro, nao tem estados sobrepostos como OS), entao nao
ha ganho em replica-lo num fato novo so pra filtrar por periodo.
"""

import streamlit as st

from src.bi import graficos, metricas
from src.bi.filtros import seletor_de_periodo, sem_dados
from src.db import session_scope
from src.ui import renderizar_menu, shell
from src.ui_components import (
    ColunaGrid,
    renderizar_cabecalho,
    renderizar_empty_state,
    renderizar_grid,
    renderizar_secao,
)
from src.ui_icons import ICONE_HISTORICO


def main() -> None:
    ctx = shell("BI - Auditoria", layout="wide", permissao="admin:visualizar_auditoria")
    renderizar_menu(ctx["usuario_id"])

    renderizar_cabecalho(
        titulo="Auditoria",
        subtitulo="Ocorrencias registradas no log de auditoria do sistema",
        icone=ICONE_HISTORICO,
    )

    with session_scope() as session:
        periodo = seletor_de_periodo(session, chave="auditoria")
        indicadores = metricas.auditoria_kpis(session, periodo)
        anteriores = metricas.auditoria_kpis(session, periodo.anterior())
        por_mes = metricas.ocorrencias_por_mes(session, periodo)
        por_acao = metricas.ocorrencias_por_acao(session, periodo)
        por_entidade = metricas.ocorrencias_por_entidade(session, periodo)
        recentes = metricas.ocorrencias_recentes(session, periodo)

    if indicadores["ocorrencias"] == 0:
        renderizar_empty_state(
            icone=ICONE_HISTORICO,
            titulo="Nenhuma ocorrencia no periodo",
            mensagem="Amplie o periodo selecionado.",
        )
        return

    def variacao(chave: str) -> str | None:
        antes = anteriores.get(chave) or 0
        agora = indicadores.get(chave) or 0
        if not antes:
            return None
        return f"{(agora - antes) / antes * 100:+.1f}%"

    st.caption("Dados em tempo real, direto do log de auditoria.")
    st.divider()
    st.metric(
        "Ocorrencias",
        f"{indicadores['ocorrencias']:,}".replace(",", "."),
        variacao("ocorrencias"),
    )

    with st.container(border=True):
        renderizar_secao(titulo="Evolucao mensal de ocorrencias")
        st.altair_chart(
            graficos.linha_temporal(
                por_mes, tempo="mes", valor="ocorrencias", rotulo_valor="Ocorrencias"
            ),
            use_container_width=True,
        )

    st.write("")
    esquerda, direita = st.columns(2)
    with esquerda:
        with st.container(border=True):
            renderizar_secao(titulo="Top acoes")
            if por_acao.empty:
                sem_dados()
            else:
                st.altair_chart(
                    graficos.barra_categorica(
                        por_acao, categoria="acao", valor="ocorrencias",
                        rotulo_categoria="Acao", rotulo_valor="Ocorrencias",
                    ),
                    use_container_width=True,
                )
    with direita:
        with st.container(border=True):
            renderizar_secao(titulo="Top entidades")
            if por_entidade.empty:
                sem_dados()
            else:
                st.altair_chart(
                    graficos.barra_categorica(
                        por_entidade, categoria="entidade", valor="ocorrencias",
                        rotulo_categoria="Entidade", rotulo_valor="Ocorrencias",
                    ),
                    use_container_width=True,
                )

    st.write("")
    with st.container(border=True):
        renderizar_secao(titulo="Ocorrencias recentes")
        renderizar_grid(
            recentes,
            colunas=[
                ColunaGrid(campo="ocorrido_em", rotulo="Data/hora", tipo="data_hora"),
                ColunaGrid(campo="usuario_nome", rotulo="Usuario"),
                ColunaGrid(campo="acao", rotulo="Acao"),
                ColunaGrid(campo="entidade", rotulo="Entidade"),
            ],
            chave="grid_auditoria_recentes",
            altura=380,
        )


if __name__ == "__main__":
    main()
