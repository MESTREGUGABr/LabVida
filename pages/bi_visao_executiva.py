"""Visao executiva — KPIs consolidados, DRE gerencial e receita x recebimento."""

import streamlit as st

from src.bi import graficos
from src.bi import metricas
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
        titulos_vencidos = metricas.alertas_titulos_vencidos(session)
        malotes_sem_retorno = metricas.alertas_malotes_sem_retorno(session)

    if not titulos_vencidos.empty or not malotes_sem_retorno.empty:
        with st.container(border=True):
            renderizar_secao(
                titulo="Atencao",
                descricao="Situacoes que podem precisar de acao imediata (nao depende do periodo abaixo)",
            )
            coluna_titulos, coluna_malotes = st.columns(2)
            with coluna_titulos:
                if titulos_vencidos.empty:
                    st.success("Nenhum titulo vencido.")
                else:
                    receber = titulos_vencidos[titulos_vencidos["tipo"] == "A receber"]
                    pagar = titulos_vencidos[titulos_vencidos["tipo"] == "A pagar"]
                    total_rec = receber["valor"].sum() if not receber.empty else 0.0
                    total_pag = pagar["valor"].sum() if not pagar.empty else 0.0

                    partes = []
                    if not receber.empty:
                        partes.append(f"{len(receber)} a receber ({formatar_brl(total_rec, markdown=True)})")
                    if not pagar.empty:
                        partes.append(f"{len(pagar)} a pagar ({formatar_brl(total_pag, markdown=True)})")

                    st.warning(f"Titulos vencidos: {', '.join(partes)}.")
                    with st.expander("Ver detalhes"):
                        # `st.dataframe` em vez do AgGrid de `renderizar_grid`: o AgGrid
                        # monta com largura zero quando o container esta escondido no
                        # primeiro render (`st.expander` comeca fechado) e nunca
                        # recalcula depois — ficava em branco mesmo com dado presente.
                        st.dataframe(
                            titulos_vencidos.rename(
                                columns={
                                    "tipo": "Tipo",
                                    "valor": "Valor",
                                    "vencimento": "Vencimento",
                                    "dias_atraso": "Dias em atraso",
                                }
                            ),
                            hide_index=True,
                            width="stretch",
                            column_config={"Valor": st.column_config.NumberColumn(format="R$ %.2f")},
                        )
            with coluna_malotes:
                if malotes_sem_retorno.empty:
                    st.success("Nenhuma remessa sem retorno.")
                else:
                    st.warning(f"{len(malotes_sem_retorno)} remessa(s) sem retorno.")
                    with st.expander("Ver detalhes"):
                        st.dataframe(
                            malotes_sem_retorno.rename(
                                columns={
                                    "codigo_malote": "Malote",
                                    "origem": "Origem",
                                    "destino": "Destino",
                                    "despachado_em": "Despachado em",
                                    "dias_em_transito": "Dias em transito",
                                }
                            ),
                            hide_index=True,
                            width="stretch",
                        )
        st.write("")

    with session_scope() as session:
        periodo = seletor_de_periodo(session, chave="executiva")
        filtro = seletor_de_filtros(session, chave="executiva", incluir_procedimento=False)
        if filtro.unidades:
            st.caption(
                "'Recebido (caixa)' e o 'DRE gerencial' sao caixa consolidado do "
                "laboratorio — um lote de faturamento pode reunir OSs de varias "
                "unidades, entao esse valor nao pertence a nenhuma unidade de coleta "
                "especifica e some ao filtrar por uma."
            )
        if filtro.convenios or filtro.incluir_particular:
            st.caption(
                "'Despesas pagas' e o 'Resultado' do DRE sao sempre o total consolidado "
                "— aluguel, fornecedor etc nao tem convenio, entao o filtro de Convenio "
                "so restringe a 'Receita recebida'. Com 'Particular' selecionado (sem "
                "nenhum paciente particular na base), a receita zera mas a despesa "
                "continua cheia, e o Resultado aparece negativo por isso — nao e bug."
            )
        indicadores = metricas.kpis(session, periodo, filtro)
        anteriores = metricas.kpis(session, periodo.anterior(), filtro)
        receita_mes = metricas.receita_por_mes(session, periodo, filtro)
        previsto_realizado = metricas.previsto_x_realizado(session, periodo, filtro)
        dre = metricas.dre_simplificado(session, periodo, filtro)
        dre_anterior = metricas.dre_simplificado(session, periodo.anterior(), filtro)
        taxa_glosa = metricas.taxa_glosa_por_convenio(session, periodo, filtro)
        aging = metricas.aging_carteira(session, periodo.fim)
        rodape_de_atualizacao(session)
        # Sem filtro (so periodo): filtro estreito demais (ex.: "Particular"
        # numa base sem paciente particular) zerando os KPIs NAO significa
        # que o ETL nunca rodou — checar com o filtro aplicado mostrava a
        # tela de "execute o ETL" pro caso errado.
        sem_filtro = metricas.kpis(session, periodo)
        houve_carga = sem_filtro["exames"] > 0 or sem_filtro["faturado"] > 0

    if not houve_carga:
        _sem_carga()
        return

    def variacao(chave: str) -> str | None:
        antes = anteriores.get(chave) or 0
        agora = indicadores.get(chave) or 0
        if not antes:
            return None
        return f"{(agora - antes) / antes * 100:+.1f}%"

    def _resultado(dataframe) -> float:
        linha = dataframe[dataframe["linha"] == "Resultado"]
        return float(linha["valor"].iloc[0]) if not linha.empty else 0.0

    resultado_atual = _resultado(dre)
    resultado_anterior = _resultado(dre_anterior)
    # Divide pelo modulo, nao pelo valor: "Resultado" pode ser negativo (mes
    # deficitario), e dividir por um anterior negativo inverteria o sinal do
    # delta (ex.: piorar de -100 pra -150 apareceria como "+50%", como se
    # tivesse melhorado). Os outros KPIs da pagina nunca ficam negativos,
    # entao esse caso nao aparecia antes do KPI de Resultado.
    variacao_resultado = (
        f"{(resultado_atual - resultado_anterior) / abs(resultado_anterior) * 100:+.1f}%"
        if resultado_anterior
        else None
    )

    st.divider()
    linha1 = st.columns(3)
    linha1[0].metric("Exames", f"{indicadores['exames']:,}".replace(",", "."), variacao("exames"))
    linha1[1].metric("Faturado", formatar_brl(indicadores["faturado"]), variacao("faturado"))
    linha1[2].metric("Recebido (caixa)", formatar_brl(indicadores["recebido"]), variacao("recebido"))

    st.write("")
    linha2 = st.columns(3)
    linha2[0].metric(
        "Taxa de glosa",
        f"{indicadores['taxa_glosa']:.1f}%".replace(".", ","),
        delta=variacao("taxa_glosa"),
        delta_color="inverse",
    )
    linha2[1].metric("Ticket medio", formatar_brl(indicadores["ticket_medio"]), variacao("ticket_medio"))
    linha2[2].metric("Resultado (DRE)", formatar_brl(resultado_atual), variacao_resultado)

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
