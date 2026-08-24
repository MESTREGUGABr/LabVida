"""Indicadores logisticos — volume, transito e divergencias da cadeia de custodia."""

import streamlit as st

from src.bi import graficos, metricas
from src.bi.filtros import botao_atualizar, rodape_de_atualizacao, seletor_de_periodo, sem_dados
from src.db import session_scope
from src.ui import renderizar_menu, shell
from src.ui_components import renderizar_cabecalho, renderizar_empty_state, renderizar_secao
from src.ui_icons import ICONE_AMOSTRA


def main() -> None:
    ctx = shell("BI - Logistica", layout="wide", permissao="bi:visualizar")
    renderizar_menu(ctx["usuario_id"])

    renderizar_cabecalho(
        titulo="Indicadores Logisticos",
        subtitulo="Amostras, tempo de transito e eficiencia da cadeia de custodia",
        icone=ICONE_AMOSTRA,
    )

    with session_scope() as session:
        periodo = seletor_de_periodo(session, chave="logistica")
        indicadores = metricas.kpis(session, periodo)
        anteriores = metricas.kpis(session, periodo.anterior())
        por_unidade = metricas.amostras_por_unidade(session, periodo)
        por_mes = metricas.amostras_por_mes(session, periodo)
        transito = metricas.tempo_transito_por_unidade(session, periodo)
        # Vem do fato, nao da tabela operacional `amostras` — a versao anterior
        # consultava o OLTP direto, furando o modelo dimensional.
        status = metricas.status_das_amostras(session, periodo)
        tempo_coleta_recebimento = metricas.tempo_coleta_recebimento_medio(session, periodo)
        tempo_coleta_recebimento_anterior = metricas.tempo_coleta_recebimento_medio(
            session, periodo.anterior()
        )
        rodape_de_atualizacao(session)

    if indicadores["amostras"] == 0:
        renderizar_empty_state(
            icone=ICONE_AMOSTRA,
            titulo="Nenhuma amostra no periodo",
            mensagem="Amplie o periodo selecionado ou atualize os dados do BI.",
        )
        if botao_atualizar(chave="etl_logistica_vazio"):
            st.rerun()
        return

    media_transito = float(transito["horas"].mean()) if not transito.empty else 0.0

    def variacao(chave: str) -> str | None:
        antes = anteriores.get(chave) or 0
        agora = indicadores.get(chave) or 0
        if not antes:
            return None
        return f"{(agora - antes) / antes * 100:+.1f}%"

    variacao_coleta_recebimento = (
        f"{(tempo_coleta_recebimento - tempo_coleta_recebimento_anterior) / tempo_coleta_recebimento_anterior * 100:+.1f}%"
        if tempo_coleta_recebimento_anterior
        else None
    )

    st.divider()
    linha1 = st.columns(3)
    linha1[0].metric(
        "Amostras", f"{indicadores['amostras']:,}".replace(",", "."), variacao("amostras")
    )
    linha1[1].metric(
        "Taxa de rejeicao", f"{indicadores['taxa_rejeicao']:.1f}%".replace(".", ","),
        delta=variacao("taxa_rejeicao"), delta_color="inverse",
    )
    linha1[2].metric("Transito medio", f"{media_transito:.1f} h".replace(".", ","))

    st.write("")
    linha2 = st.columns(3)
    linha2[0].metric("Unidades de origem", len(por_unidade))
    linha2[1].metric(
        "Coleta -> recebimento",
        f"{tempo_coleta_recebimento:.1f} h".replace(".", ","),
        delta=variacao_coleta_recebimento, delta_color="inverse",
    )

    with st.container(border=True):
        renderizar_secao(titulo="Amostras coletadas por mes")
        st.altair_chart(
            graficos.linha_temporal(por_mes, tempo="mes", valor="amostras", rotulo_valor="Amostras"),
            use_container_width=True,
        )

    st.write("")
    esquerda, direita = st.columns(2)
    with esquerda:
        with st.container(border=True):
            renderizar_secao(titulo="Amostras por unidade de origem")
            st.altair_chart(
                graficos.barra_categorica(
                    por_unidade, categoria="unidade", valor="amostras", rotulo_valor="Amostras"
                ),
                use_container_width=True,
            )
    with direita:
        with st.container(border=True):
            renderizar_secao(titulo="Tempo medio de transito")
            if transito.empty:
                sem_dados("Nenhum malote com despacho e recebimento registrados.")
            else:
                st.altair_chart(
                    graficos.barra_categorica(
                        transito, categoria="unidade", valor="horas",
                        rotulo_valor="Horas", formato="horas", cor_unica=graficos.COR_ALERTA,
                    ),
                    use_container_width=True,
                )

    st.write("")
    esquerda, direita = st.columns(2)
    with esquerda:
        with st.container(border=True):
            renderizar_secao(titulo="Amostras rejeitadas por unidade")
            rejeitadas = por_unidade[por_unidade["rejeitadas"] > 0]
            if rejeitadas.empty:
                sem_dados("Nenhuma amostra rejeitada no periodo.")
            else:
                st.altair_chart(
                    graficos.barra_categorica(
                        rejeitadas, categoria="unidade", valor="rejeitadas",
                        rotulo_valor="Rejeitadas", cor_unica=graficos.COR_NEGATIVA,
                    ),
                    use_container_width=True,
                )
    with direita:
        with st.container(border=True):
            renderizar_secao(titulo="Situacao atual das amostras")
            if status.empty:
                sem_dados()
            else:
                st.altair_chart(
                    graficos.donut(status, categoria="status", valor="quantidade"),
                    use_container_width=True,
                )

    st.divider()
    if botao_atualizar(chave="etl_logistica"):
        st.rerun()


if __name__ == "__main__":
    main()
