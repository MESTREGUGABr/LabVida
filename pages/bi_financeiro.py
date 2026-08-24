"""Indicadores financeiros — receita, glosa, ticket medio e fluxo de caixa.

O grafico rotulado "Fluxo de Caixa" agora e regime de CAIXA de verdade: sai de
`movimentos_caixa`, nao do cronograma de vencimentos, e titulo em aberto nao
conta como dinheiro recebido.
"""

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
from src.ui import formatar_brl, renderizar_menu, shell
from src.ui_components import renderizar_cabecalho, renderizar_empty_state, renderizar_secao
from src.ui_icons import ICONE_FINANCEIRO


def main() -> None:
    ctx = shell("BI - Financeiro", layout="wide", permissao="bi:visualizar")
    renderizar_menu(ctx["usuario_id"])

    renderizar_cabecalho(
        titulo="Indicadores Financeiros",
        subtitulo="Receita, glosas, ticket medio e fluxo de caixa por periodo",
        icone=ICONE_FINANCEIRO,
    )

    with session_scope() as session:
        periodo = seletor_de_periodo(session, chave="financeiro")
        filtro = seletor_de_filtros(session, chave="financeiro")
        if filtro.procedimentos:
            st.caption(
                "O filtro de Exame nao se aplica a 'Recebido (caixa)' nem a "
                "'Fluxo de caixa realizado' — o regime de caixa nao tem essa dimensao."
            )
        if filtro.unidades:
            st.caption(
                "'Recebido (caixa)' e o 'Fluxo de caixa realizado' tambem sao caixa "
                "consolidado do laboratorio — um lote de faturamento pode reunir OSs "
                "de varias unidades, entao esse valor nao pertence a nenhuma unidade "
                "de coleta especifica e some ao filtrar por uma."
            )
        if filtro.convenios or filtro.incluir_particular:
            st.caption(
                "As 'saidas' do 'Fluxo de caixa realizado' sao sempre o total "
                "consolidado — aluguel, fornecedor etc nao tem convenio, entao o "
                "filtro de Convenio so restringe entrada/receita, nunca despesa."
            )
        indicadores = metricas.kpis(session, periodo, filtro)
        anteriores = metricas.kpis(session, periodo.anterior(), filtro)
        por_convenio = metricas.receita_por_convenio(session, periodo, filtro)
        por_mes = metricas.receita_por_mes(session, periodo, filtro)
        ticket_convenio = metricas.ticket_medio_por_convenio(session, periodo, filtro)
        ticket_procedimento = metricas.ticket_medio_por_procedimento(session, periodo, filtro)
        abc = metricas.curva_abc_procedimentos(session, periodo, filtro)
        glosa_motivo = metricas.glosa_por_motivo(session, periodo, filtro)
        taxa_glosa = metricas.taxa_glosa_por_convenio(session, periodo, filtro)
        caixa = metricas.fluxo_caixa_mensal(session, periodo, filtro)
        rodape_de_atualizacao(session)
        # Sem filtro (so periodo): filtro estreito demais zerando os KPIs nao
        # significa que o ETL nunca rodou.
        sem_filtro = metricas.kpis(session, periodo)

    if sem_filtro["faturado"] == 0 and sem_filtro["recebido"] == 0:
        renderizar_empty_state(
            icone=ICONE_FINANCEIRO,
            titulo="Nenhum dado financeiro no periodo",
            mensagem="Amplie o periodo selecionado ou atualize os dados do BI.",
        )
        if botao_atualizar(chave="etl_financeiro_vazio"):
            st.rerun()
        return

    def variacao(chave: str) -> str | None:
        antes = anteriores.get(chave) or 0
        agora = indicadores.get(chave) or 0
        if not antes:
            return None
        return f"{(agora - antes) / antes * 100:+.1f}%"

    st.divider()
    linha1 = st.columns(3)
    linha1[0].metric("Faturado", formatar_brl(indicadores["faturado"]), variacao("faturado"))
    linha1[1].metric(
        "Glosado", formatar_brl(indicadores["glosado"]),
        delta=variacao("glosado"), delta_color="inverse",
    )
    linha1[2].metric("Liberado", formatar_brl(indicadores["liberado"]), variacao("liberado"))

    st.write("")
    linha2 = st.columns(3)
    linha2[0].metric("Recebido (caixa)", formatar_brl(indicadores["recebido"]), variacao("recebido"))
    linha2[1].metric(
        "Taxa de glosa", f"{indicadores['taxa_glosa']:.1f}%".replace(".", ","),
        delta=variacao("taxa_glosa"), delta_color="inverse",
    )
    linha2[2].metric(
        "Ticket medio", formatar_brl(indicadores["ticket_medio"]), variacao("ticket_medio")
    )

    with st.container(border=True):
        renderizar_secao(titulo="Faturado x glosado por mes")
        if por_mes.empty:
            sem_dados()
        else:
            st.altair_chart(
                graficos.series_comparadas(
                    por_mes, tempo="mes", series=["faturado", "glosado"],
                    rotulo_valor="Valor", formato="moeda",
                    cores=[graficos.COR_NEUTRA, graficos.COR_NEGATIVA],
                ),
                use_container_width=True,
            )

    st.write("")
    esquerda, direita = st.columns(2)
    with esquerda:
        with st.container(border=True):
            renderizar_secao(titulo="Receita por convenio")
            if por_convenio.empty:
                sem_dados()
            else:
                st.altair_chart(
                    graficos.barra_categorica(
                        por_convenio, categoria="convenio", valor="liberado",
                        rotulo_categoria="Convenio", rotulo_valor="Liberado", formato="moeda",
                    ),
                    use_container_width=True,
                )
    with direita:
        with st.container(border=True):
            renderizar_secao(titulo="Ticket medio por convenio")
            if ticket_convenio.empty:
                sem_dados()
            else:
                st.altair_chart(
                    graficos.barra_categorica(
                        ticket_convenio, categoria="convenio", valor="ticket_medio",
                        rotulo_categoria="Convenio", rotulo_valor="Ticket medio",
                        formato="moeda", cor_unica=graficos.COR_POSITIVA,
                    ),
                    use_container_width=True,
                )

    st.write("")
    with st.container(border=True):
        renderizar_secao(titulo="Curva ABC de procedimentos")
        if abc.empty:
            sem_dados()
        else:
            st.altair_chart(graficos.curva_abc(abc), use_container_width=True)

    st.write("")
    esquerda, direita = st.columns(2)
    with esquerda:
        with st.container(border=True):
            renderizar_secao(titulo="Glosa por motivo")
            if glosa_motivo.empty:
                sem_dados("Nenhuma glosa no periodo.")
            else:
                st.altair_chart(
                    graficos.barra_categorica(
                        glosa_motivo, categoria="motivo", valor="glosado",
                        rotulo_categoria="Motivo", rotulo_valor="Glosado",
                        formato="moeda", cor_unica=graficos.COR_NEGATIVA,
                    ),
                    use_container_width=True,
                )
    with direita:
        with st.container(border=True):
            renderizar_secao(titulo="Taxa de glosa por convenio")
            if taxa_glosa.empty:
                sem_dados()
            else:
                st.altair_chart(
                    graficos.barra_categorica(
                        taxa_glosa, categoria="convenio", valor="taxa_glosa",
                        rotulo_categoria="Convenio", rotulo_valor="Taxa de glosa",
                        formato="percentual", cor_unica=graficos.COR_ALERTA,
                    ),
                    use_container_width=True,
                )

    st.write("")
    with st.container(border=True):
        renderizar_secao(titulo="Fluxo de caixa realizado")
        if caixa.empty:
            sem_dados("Nenhum movimento de caixa no periodo.")
        else:
            st.altair_chart(
                graficos.series_comparadas(
                    caixa, tempo="mes", series=["entradas", "saidas"],
                    rotulo_valor="Valor", formato="moeda",
                    cores=[graficos.COR_POSITIVA, graficos.COR_NEGATIVA],
                ),
                use_container_width=True,
            )

    if not ticket_procedimento.empty:
        st.write("")
        with st.container(border=True):
            renderizar_secao(titulo="Maiores tickets medios por procedimento")
            st.dataframe(
                ticket_procedimento.rename(
                    columns={
                        "procedimento": "Procedimento",
                        "ticket_medio": "Ticket medio",
                        "exames": "Exames",
                    }
                ),
                hide_index=True,
                width="stretch",
                column_config={"Ticket medio": st.column_config.NumberColumn(format="R$ %.2f")},
            )

    st.divider()
    if botao_atualizar(chave="etl_financeiro"):
        st.rerun()


if __name__ == "__main__":
    main()
