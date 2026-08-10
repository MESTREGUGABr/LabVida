"""Apuracao e fechamento de competencia (fase F4).

Responde ao apontamento "colocar mes do faturamento" e "fluxo de fechamento".

Nesta fase o fechamento ainda NAO bloqueia lancamento em outras telas — o guarda
`exigir_aberta()` existe e esta testado, mas so passa a ser chamado pelos
lancamentos quando o item faturavel entrar (F5). Fechar aqui ja congela a
apuracao, que e o que o gestor precisa para ter um numero que para de mudar.
"""

from datetime import date

import streamlit as st

from src.db import session_scope
from src.faturamento.competencia import service as competencia_service
from src.ui import formatar_brl, renderizar_menu, shell, usuario_id_logado
from src.ui_components import (
    ColunaGrid,
    renderizar_cabecalho,
    renderizar_grid,
    renderizar_secao,
    tratar_erros,
)
from src.ui_icons import ICONE_FATURAMENTO

_COLUNAS = [
    ColunaGrid("mes", "Competencia", largura=140),
    ColunaGrid("status", "Status", largura=110),
    ColunaGrid("faturado", "Faturado", tipo="moeda", largura=140),
    ColunaGrid("glosado", "Glosado", tipo="moeda", largura=140),
    ColunaGrid("liberado", "Liberado", tipo="moeda", largura=140),
    ColunaGrid("fechada_em", "Fechada em", tipo="data", largura=140),
    ColunaGrid("iso", "iso", oculta=True),
]


@st.dialog("Fechar competencia")
def _dialogo_fechar(competencia: date, apuracao) -> None:
    st.write(f"Fechar **{competencia.strftime('%m/%Y')}**?")
    st.caption(
        "O fechamento CONGELA a apuracao: os totais param de mudar, mesmo que "
        "algo seja lancado depois."
    )

    coluna_a, coluna_b = st.columns(2)
    coluna_a.metric("Faturado", formatar_brl(float(apuracao.valor_faturado)))
    coluna_b.metric("Laudos sem faturar", apuracao.laudos_nao_faturados)

    if apuracao.laudos_nao_faturados:
        st.warning(
            f"{apuracao.laudos_nao_faturados} laudo(s) liberado(s) nesta competencia "
            "ainda nao foram faturados. Eles continuarao faturaveis, mas nao entram "
            "no total congelado."
        )

    justificativa = st.text_input("Observacao (opcional)")

    coluna_ok, coluna_cancelar = st.columns(2)
    with coluna_ok:
        if st.button("Confirmar fechamento", type="primary", width="stretch"):
            with tratar_erros("fechar a competencia") as resultado, session_scope() as session:
                competencia_service.fechar(
                    session, competencia, usuario_id_logado(), justificativa or None
                )
            if resultado:
                st.toast(f"Competencia {competencia:%m/%Y} fechada.")
                st.rerun()
    with coluna_cancelar:
        if st.button("Cancelar", width="stretch"):
            st.rerun()


@st.dialog("Reabrir competencia")
def _dialogo_reabrir(competencia: date) -> None:
    st.write(f"Reabrir **{competencia.strftime('%m/%Y')}**?")
    st.caption("A reabertura desfaz um fechamento contabil e fica registrada na auditoria.")
    justificativa = st.text_input("Motivo da reabertura")

    coluna_ok, coluna_cancelar = st.columns(2)
    with coluna_ok:
        if st.button("Confirmar reabertura", type="primary", width="stretch"):
            with tratar_erros("reabrir a competencia") as resultado, session_scope() as session:
                competencia_service.reabrir(
                    session, competencia, usuario_id_logado(), justificativa
                )
            if resultado:
                st.toast(f"Competencia {competencia:%m/%Y} reaberta.")
                st.rerun()
    with coluna_cancelar:
        if st.button("Cancelar", width="stretch"):
            st.rerun()


def main() -> None:
    ctx = shell(
        "LabVida - Competencia", layout="wide", permissao="faturamento:gerenciar_lotes"
    )
    renderizar_menu(ctx["usuario_id"])

    renderizar_cabecalho(
        titulo="Competencia",
        subtitulo="Apuracao mensal pelo fato gerador — o laudo liberado, nao a data de faturar",
        icone=ICONE_FATURAMENTO,
    )

    with tratar_erros("carregar as competencias") as resultado, session_scope() as session:
        competencias = competencia_service.listar(session)
        apuracoes = {
            c.competencia: competencia_service.apurar(session, c.competencia)
            for c in competencias
        }
        linhas = [
            {
                "iso": c.competencia.isoformat(),
                "mes": c.competencia.strftime("%m/%Y"),
                "status": c.status,
                "faturado": apuracoes[c.competencia].valor_faturado,
                "glosado": apuracoes[c.competencia].valor_glosado,
                "liberado": apuracoes[c.competencia].valor_liberado,
                "fechada_em": c.fechada_em,
            }
            for c in competencias
        ]
    if not resultado:
        return

    if not linhas:
        st.info("Nenhuma competencia registrada ainda.")
        return

    aberta = next((linha for linha in linhas if linha["status"] == "ABERTA"), None)
    if aberta:
        apuracao = apuracoes[date.fromisoformat(aberta["iso"])]
        colunas = st.columns(4)
        colunas[0].metric("Competencia aberta", aberta["mes"])
        colunas[1].metric("Faturado", formatar_brl(float(apuracao.valor_faturado)))
        colunas[2].metric("Taxa de glosa", f"{apuracao.taxa_glosa:.1f}%".replace(".", ","))
        colunas[3].metric("Laudos sem faturar", apuracao.laudos_nao_faturados)

    renderizar_secao(titulo="Competencias")
    grid = renderizar_grid(
        linhas, colunas=_COLUNAS, chave="grid_competencias", selecao="linha", altura=360
    )

    selecionada = grid.selecionado
    if selecionada is None:
        st.caption("Selecione uma competencia para fechar ou reabrir.")
        return

    competencia = date.fromisoformat(selecionada["iso"])
    apuracao = apuracoes[competencia]

    st.divider()
    if selecionada["status"] == "ABERTA":
        if st.button(f"Fechar {selecionada['mes']}", type="primary"):
            _dialogo_fechar(competencia, apuracao)
    else:
        if st.button(f"Reabrir {selecionada['mes']}"):
            _dialogo_reabrir(competencia)


if __name__ == "__main__":
    main()
