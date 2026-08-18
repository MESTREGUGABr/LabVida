"""Visao executiva — KPIs consolidados, DRE gerencial e receita x recebimento."""

import streamlit as st

from src.bi import graficos
from src.bi import metricas
from src.bi.filtros import botao_atualizar, rodape_de_atualizacao, seletor_de_periodo, sem_dados
from src.db import session_scope
from src.ui import formatar_brl, renderizar_menu, shell
from src.ui_components import renderizar_cabecalho, renderizar_empty_state, renderizar_secao
from src.ui_icons import ICONE_PRODUTIVIDADE


def _sem_carga() -> None:
    renderizar_empty_state(
        icone=ICONE_PRODUTIVIDADE,
        titulo="Nenhum dado disponivel",
        mensagem="Execute o ETL para popular o BI a partir da base operacional.",
    )
    if botao_atualizar(chave="etl_executiva_vazio"):
        st.rerun()


def main() -> None:
    ctx = shell("BI - Visao Executiva", layout="wide", permissao="bi:visualizar")
    renderizar_menu(ctx["usuario_id"])

    renderizar_cabecalho(
        titulo="Visao Executiva",
        subtitulo="Indicadores consolidados do laboratorio no periodo",
        icone=ICONE_PRODUTIVIDADE,
    )

    with session_scope() as session:
        periodo = seletor_de_periodo(session, chave="executiva")
        indicadores = metricas.kpis(session, periodo)
        anteriores = metricas.kpis(session, periodo.anterior())
        receita_mes = metricas.receita_por_mes(session, periodo)
        previsto_realizado = metricas.previsto_x_realizado(session, periodo)
        dre = metricas.dre_simplificado(session, periodo)
        taxa_glosa = metricas.taxa_glosa_por_convenio(session, periodo)
        aging = metricas.aging_carteira(session, periodo.fim)
        rodape_de_atualizacao(session)
        houve_carga = indicadores["exames"] > 0 or indicadores["faturado"] > 0

    if not houve_carga:
        _sem_carga()
        return

    def variacao(chave: str) -> str | None:
        antes = anteriores.get(chave) or 0
        agora = indicadores.get(chave) or 0
        if not antes:
            return None
        return f"{(agora - antes) / antes * 100:+.1f}%"

    st.divider()
    colunas = st.columns(5)
    colunas[0].metric("Exames", f"{indicadores['exames']:,}".replace(",", "."), variacao("exames"))
    colunas[1].metric("Faturado", formatar_brl(indicadores["faturado"]), variacao("faturado"))
    colunas[2].metric("Recebido (caixa)", formatar_brl(indicadores["recebido"]), variacao("recebido"))
    colunas[3].metric(
        "Taxa de glosa",
        f"{indicadores['taxa_glosa']:.1f}%".replace(".", ","),
        delta=variacao("taxa_glosa"),
        delta_color="inverse",
    )
    colunas[4].metric("Ticket medio", formatar_brl(indicadores["ticket_medio"]), variacao("ticket_medio"))

    esquerda, direita = st.columns(2)

    with esquerda:
        with st.container(border=True):
            renderizar_secao(titulo="Receita faturada por mes")
            if receita_mes.empty:
                sem_dados()
            else:
                st.altair_chart(
                    graficos.linha_temporal(
                        receita_mes, tempo="mes", valor="faturado",
                        rotulo_valor="Faturado", formato="moeda",
                    ),
                    use_container_width=True,
                )

    with direita:
        with st.container(border=True):
            renderizar_secao(titulo="Previsto x recebido")
            if previsto_realizado.empty:
                sem_dados()
            else:
                st.altair_chart(
                    graficos.series_comparadas(
                        previsto_realizado, tempo="mes", series=["previsto", "realizado"],
                        rotulo_valor="Valor", formato="moeda",
                        cores=[graficos.COR_NEUTRA, graficos.COR_POSITIVA],
                    ),
                    use_container_width=True,
                )

    st.write("")
    esquerda, direita = st.columns(2)

    with esquerda:
        with st.container(border=True):
            renderizar_secao(titulo="DRE gerencial (regime de caixa)")
            st.altair_chart(graficos.barras_dre(dre), use_container_width=True)

    with direita:
        with st.container(border=True):
            renderizar_secao(titulo="Carteira a receber por faixa de atraso")
            if aging.empty:
                sem_dados("Nenhum titulo em aberto.")
            else:
                st.altair_chart(
                    graficos.barra_categorica(
                        aging, categoria="faixa", valor="valor",
                        rotulo_categoria="Faixa", rotulo_valor="Valor",
                        formato="moeda", horizontal=False, altura=240,
                        tamanho_barra=graficos.TAMANHO_BARRA_DRE_AGING,
                    ),
                    use_container_width=True,
                )

    st.write("")
    with st.container(border=True):
        renderizar_secao(titulo="Taxa de glosa por convenio")
        if taxa_glosa.empty:
            sem_dados()
        else:
            st.altair_chart(
                graficos.barra_categorica(
                    taxa_glosa, categoria="convenio", valor="taxa_glosa",
                    rotulo_categoria="Convenio", rotulo_valor="Taxa de glosa",
                    formato="percentual", cor_unica=graficos.COR_NEGATIVA, altura=260,
                ),
                use_container_width=True,
            )

    st.divider()
    if botao_atualizar(chave="etl_executiva"):
        st.rerun()


if __name__ == "__main__":
    main()
