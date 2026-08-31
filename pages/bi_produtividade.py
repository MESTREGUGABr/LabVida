"""Produtividade operacional — volume, TAT, setor e sazonalidade."""

import streamlit as st

from src.bi import graficos, metricas
from src.bi.filtros import (
    botao_atualizar,
    rodape_de_atualizacao,
    seletor_de_filtros,
    seletor_de_periodo,
    sem_dados,
)
from src.db import session_scope
from src.ui import renderizar_menu, shell
from src.ui_components import renderizar_cabecalho, renderizar_empty_state, renderizar_secao
from src.ui_icons import ICONE_PRODUTIVIDADE


def main() -> None:
    ctx = shell("BI - Produtividade", layout="wide", permissao="bi:visualizar")
    renderizar_menu(ctx["usuario_id"])

    renderizar_cabecalho(
        titulo="Produtividade Operacional",
        subtitulo="Volume de exames, tempo de atendimento e distribuicao por setor",
        icone=ICONE_PRODUTIVIDADE,
    )

    with session_scope() as session:
        periodo = seletor_de_periodo(session, chave="produtividade")
        filtro = seletor_de_filtros(session, chave="produtividade")
        if filtro.procedimentos:
            st.caption(
                "O filtro de Exame nao se aplica ao TAT nem a Taxa de "
                "cancelamento — esses indicadores sao do grao da OS inteira, "
                "nao do exame individual."
            )
        indicadores = metricas.kpis(session, periodo, filtro)
        anteriores = metricas.kpis(session, periodo.anterior(), filtro)
        por_unidade = metricas.exames_por_unidade(session, periodo, filtro)
        por_mes = metricas.exames_por_mes(session, periodo, filtro)
        por_convenio = metricas.exames_por_convenio(session, periodo, filtro)
        por_faixa = metricas.exames_por_faixa_etaria(session, periodo, filtro)
        por_setor = metricas.exames_por_setor(session, periodo, filtro)
        sazonalidade = metricas.sazonalidade_por_dia_da_semana(session, periodo, filtro)
        tat_mes = metricas.tat_por_mes(session, periodo, filtro)
        tat_setor = metricas.tat_por_setor(session, periodo, filtro)
        taxa_cancelamento = metricas.taxa_cancelamento_itens(session, periodo, filtro)
        taxa_cancelamento_anterior = metricas.taxa_cancelamento_itens(session, periodo.anterior(), filtro)
        rodape_de_atualizacao(session)
        # Sem filtro (so periodo): filtro estreito demais zerando os KPIs nao
        # significa que o ETL nunca rodou.
        sem_filtro = metricas.kpis(session, periodo)

    if sem_filtro["exames"] == 0:
        renderizar_empty_state(
            icone=ICONE_PRODUTIVIDADE,
            titulo="Nenhum exame no periodo",
            mensagem="Amplie o periodo selecionado ou atualize os dados do BI.",
        )
        if botao_atualizar(chave="etl_produtividade_vazio"):
            st.rerun()
        return

    def variacao(chave: str) -> str | None:
        antes = anteriores.get(chave) or 0
        agora = indicadores.get(chave) or 0
        if not antes:
            return None
        return f"{(agora - antes) / antes * 100:+.1f}%"

    variacao_cancelamento = (
        f"{taxa_cancelamento - taxa_cancelamento_anterior:+.1f}pp"
        if taxa_cancelamento_anterior
        else None
    )

    st.divider()
    linha1 = st.columns(3)
    linha1[0].metric(
        "Exames", f"{indicadores['exames']:,}".replace(",", "."), variacao("exames")
    )
    linha1[1].metric("Unidades ativas", len(por_unidade))
    linha1[2].metric(
        "Media por unidade",
        f"{indicadores['exames'] / len(por_unidade):.0f}" if len(por_unidade) else "0",
    )

    st.write("")
    linha2 = st.columns(3)
    linha2[0].metric(
        "TAT (coleta -> laudo)",
        f"{indicadores['tat_horas']:.1f} h".replace(".", ","),
        delta=variacao("tat_horas"), delta_color="inverse",
    )
    linha2[1].metric(
        "Taxa de cancelamento",
        f"{taxa_cancelamento:.1f}%".replace(".", ","),
        delta=variacao_cancelamento, delta_color="inverse",
    )

    with st.container(border=True):
        renderizar_secao(titulo="Evolucao mensal de exames")
        st.altair_chart(
            graficos.linha_temporal(por_mes, tempo="mes", valor="exames", rotulo_valor="Exames"),
            use_container_width=True,
        )

    st.write("")
    esquerda, direita = st.columns(2)
    with esquerda:
        with st.container(border=True):
            renderizar_secao(titulo="Exames por unidade")
            if por_unidade.empty:
                sem_dados()
            else:
                st.altair_chart(
                    graficos.barra_categorica(
                        por_unidade, categoria="unidade", valor="exames", rotulo_valor="Exames"
                    ),
                    use_container_width=True,
                )
    with direita:
        with st.container(border=True):
            renderizar_secao(titulo="Exames por convenio")
            if por_convenio.empty:
                sem_dados()
            else:
                st.altair_chart(
                    graficos.barra_categorica(
                        por_convenio, categoria="convenio", valor="exames", rotulo_valor="Exames"
                    ),
                    use_container_width=True,
                )

    st.write("")
    esquerda, direita = st.columns(2)
    with esquerda:
        with st.container(border=True):
            renderizar_secao(titulo="Exames por setor")
            if por_setor.empty:
                sem_dados()
            else:
                st.altair_chart(
                    graficos.donut(por_setor, categoria="setor", valor="exames"),
                    use_container_width=True,
                )
    with direita:
        with st.container(border=True):
            renderizar_secao(titulo="Distribuicao por faixa etaria")
            if por_faixa.empty:
                sem_dados()
            else:
                st.altair_chart(
                    graficos.barra_categorica(
                        por_faixa, categoria="faixa_etaria", valor="exames",
                        rotulo_categoria="Faixa etaria", rotulo_valor="Exames",
                        horizontal=False, cor_unica=graficos.COR_NEUTRA,
                    ),
                    use_container_width=True,
                )

    st.write("")
    esquerda, direita = st.columns([2, 3])
    with esquerda:
        with st.container(border=True):
            renderizar_secao(titulo="Sazonalidade semanal")
            if sazonalidade.empty:
                sem_dados()
            else:
                st.altair_chart(
                    graficos.heatmap_sazonalidade(
                        sazonalidade, dia_semana="dia_semana", valor="exames", altura=200,
                    ),
                    use_container_width=True,
                )
    with direita:
        with st.container(border=True):
            renderizar_secao(titulo="Tempo medio de atendimento por setor")
            if tat_setor.empty:
                sem_dados("Nenhuma OS concluida no periodo.")
            else:
                st.altair_chart(
                    graficos.barra_categorica(
                        tat_setor, categoria="setor", valor="horas",
                        rotulo_valor="Horas", formato="horas",
                        cor_unica=graficos.COR_ALERTA, altura=200,
                    ),
                    use_container_width=True,
                )

    st.write("")
    with st.container(border=True):
        renderizar_secao(titulo="Tempo medio coleta -> laudo por mes")
        if tat_mes.empty:
            sem_dados("Nenhuma OS concluida no periodo.")
        else:
            st.altair_chart(
                graficos.linha_temporal(
                    tat_mes, tempo="mes", valor="horas", rotulo_valor="Horas",
                    formato="horas", cor=graficos.COR_ALERTA,
                ),
                use_container_width=True,
            )

    st.divider()
    if botao_atualizar(chave="etl_produtividade"):
        st.rerun()


if __name__ == "__main__":
    main()
