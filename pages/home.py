"""Pagina inicial do LabVida — Visao Geral operacional."""

from datetime import datetime, timedelta, timezone

import pandas as pd
import streamlit as st
from sqlalchemy import func

from src.atendimento.amostra.models import Amostra
from src.atendimento.ordem_servico.models import OrdemServico
from src.atendimento.ordem_servico.dtos import StatusOrdemServico
from src.atendimento.amostra.dtos import StatusAmostra
from src.db import session_scope
from src.faturamento.lote_faturamento.models import LoteFaturamento
from src.laboratorial.models import Laudo, StatusLaudo
from src.ui import renderizar_menu, shell
from src.ui_components import (
    renderizar_cabecalho,
    renderizar_empty_state,
    renderizar_kpi_card,
    renderizar_secao,
)
from src.ui_theme import ACCENT_ORANGE, ACCENT_TEAL, ACCENT_AMBER, ACCENT_BLUE
from src.ui_icons import (
    ICONE_ALERTA,
    ICONE_COLETA,
    ICONE_FINANCEIRO,
    ICONE_HOME,
    ICONE_LAUDO,
    ICONE_OK,
    ICONE_OS,
    ICONE_PRODUTIVIDADE,
    ICONE_TRANSITO,
)


def main() -> None:
    ctx = shell("LabVida \u2014 Home", layout="wide")
    renderizar_menu(ctx["usuario_id"])

    user = ctx["user"]

    renderizar_cabecalho(
        titulo="Visao Geral",
        subtitulo=f"Ola, {user['name']} \u2014 Resumo operacional do laboratorio",
        icone=ICONE_HOME,
    )

    _renderizar_kpis()

    st.markdown("<br>", unsafe_allow_html=True)

    col_a1, col_a2, col_a3, col_a4 = st.columns(4)
    links_rapidos = [
        (ICONE_OS, "Abrir OS", "atendimento_os"),
        (ICONE_COLETA, "Registrar Coleta", "atendimento_coleta"),
        (ICONE_LAUDO, "Novo Laudo", "laboratorio_laudos"),
        (ICONE_FINANCEIRO, "Faturar", "faturamento_guias"),
    ]
    for col, (icone, texto, pagina) in zip([col_a1, col_a2, col_a3, col_a4], links_rapidos):
        with col:
            st.markdown(
                f"""<a href="/{pagina}" target="_self" style="
                    display:flex;align-items:center;justify-content:center;gap:8px;
                    background:#1565C0;color:#fff;padding:10px 16px;
                    border-radius:8px;text-decoration:none;font-size:13px;font-weight:500;
                    transition:all 0.15s ease;
                " onmouseover="this.style.background='#0D47A1'"
                   onmouseout="this.style.background='#1565C0'">
                    {icone} {texto}
                </a>""",
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    col_esq, col_dir = st.columns([3, 2])

    with col_esq:
        _renderizar_os_recentes()

    with col_dir:
        _renderizar_alertas()
        _renderizar_grafico_semanal()


def _renderizar_kpis() -> None:
    with session_scope() as session:
        os_abertas = session.query(func.count(OrdemServico.id)).filter(
            OrdemServico.status.in_([
                StatusOrdemServico.ABERTA,
                StatusOrdemServico.EM_COLETA,
                StatusOrdemServico.COLETADA,
                StatusOrdemServico.EM_ANALISE,
            ])
        ).scalar() or 0

        amostras_pendentes = session.query(func.count(Amostra.id)).filter(
            Amostra.status == StatusAmostra.AGUARDANDO_COLETA
        ).scalar() or 0

        laudos_a_liberar = session.query(func.count(Laudo.id)).filter(
            Laudo.status == StatusLaudo.RASCUNHO
        ).scalar() or 0

        agora = datetime.now(timezone.utc)
        inicio_mes = datetime(agora.year, agora.month, 1, tzinfo=timezone.utc)
        faturamento_mes = session.query(
            func.coalesce(func.sum(LoteFaturamento.valor_total), 0)
        ).filter(
            LoteFaturamento.criado_em >= inicio_mes
        ).scalar() or 0.0

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        renderizar_kpi_card(
            rotulo="OS em aberto",
            valor=str(os_abertas),
            icone=ICONE_OS,
            cor_destaque=ACCENT_BLUE,
        )

    with col2:
        renderizar_kpi_card(
            rotulo="Amostras pendentes",
            valor=str(amostras_pendentes),
            icone=ICONE_COLETA,
            cor_destaque=ACCENT_AMBER,
        )

    with col3:
        renderizar_kpi_card(
            rotulo="Laudos a liberar",
            valor=str(laudos_a_liberar),
            icone=ICONE_LAUDO,
            cor_destaque=ACCENT_TEAL,
        )

    with col4:
        valor_fmt = f"R$ {faturamento_mes:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        renderizar_kpi_card(
            rotulo="Faturamento do mes",
            valor=valor_fmt,
            icone=ICONE_FINANCEIRO,
            cor_destaque=ACCENT_ORANGE,
        )

    st.markdown("<br>", unsafe_allow_html=True)


def _renderizar_os_recentes() -> None:
    renderizar_secao(
        titulo=f"{ICONE_OS} Ultimas Ordens de Servico",
        descricao="Ordens de Servico abertas recentemente no laboratorio",
        rotulo_acao="Nova OS",
    )

    with session_scope() as session:
        ordens = (
            session.query(OrdemServico)
            .order_by(OrdemServico.aberta_em.desc())
            .limit(10)
            .all()
        )

    if not ordens:
        renderizar_empty_state(
            icone=ICONE_OS,
            titulo="Nenhuma Ordem de Servico cadastrada",
            mensagem="As OS abertas recentemente aparecerao aqui.",
        )
        return

    linhas = []
    for os_ in ordens:
        status_label = os_.status.replace("_", " ").title()
        data_abertura = os_.aberta_em.strftime("%d/%m/%Y %H:%M") if os_.aberta_em else "\u2014"
        linhas.append({
            "Codigo": os_.codigo_os,
            "Abertura": data_abertura,
            "Status": status_label,
        })

    st.dataframe(
        linhas,
        hide_index=True,
        width="stretch",
        column_config={
            "Status": st.column_config.TextColumn(width="small"),
            "Codigo": st.column_config.TextColumn(width="small"),
            "Abertura": st.column_config.TextColumn(width="small"),
        },
    )


def _renderizar_alertas() -> None:
    renderizar_secao(
        titulo=f"{ICONE_ALERTA} Alertas",
        descricao="Itens que requerem atencao operacional",
    )

    with session_scope() as session:
        amostras_em_transito = session.query(func.count(Amostra.id)).filter(
            Amostra.status == StatusAmostra.EM_TRANSITO
        ).scalar() or 0

        amostras_aguardando = session.query(func.count(Amostra.id)).filter(
            Amostra.status == StatusAmostra.AGUARDANDO_COLETA
        ).scalar() or 0

        laudos_pendentes = session.query(func.count(Laudo.id)).filter(
            Laudo.status == StatusLaudo.RASCUNHO
        ).scalar() or 0

    alertas = []
    if amostras_aguardando > 0:
        alertas.append(
            (ICONE_COLETA, f"{amostras_aguardando} amostra(s) aguardando coleta", "warning")
        )
    if amostras_em_transito > 0:
        alertas.append(
            (ICONE_TRANSITO, f"{amostras_em_transito} amostra(s) em transito", "info")
        )
    if laudos_pendentes > 0:
        alertas.append(
            (ICONE_LAUDO, f"{laudos_pendentes} laudo(s) aguardando liberacao", "warning")
        )

    if not alertas:
        renderizar_empty_state(
            icone=ICONE_OK,
            titulo="Nenhum alerta no momento",
            mensagem="Todas as operacoes estao em dia.",
        )
        return

    for icone, texto, tipo in alertas:
        cores = {
            "warning": ("#FFF3E0", "#E67E22"),
            "info": ("#E3F2FD", "#1565C0"),
            "error": ("#FFEBEE", "#C62828"),
            "success": ("#E0F2F1", "#00897B"),
        }
        bg, cor = cores.get(tipo, ("#ECEFF1", "#607D8B"))

        st.markdown(
            f"""
            <div style="display:flex;align-items:center;gap:10px;
            background:{bg};border-radius:8px;padding:12px 16px;margin-bottom:8px;
            border-left:3px solid {cor};">
                <span style="font-size:18px;flex-shrink:0;">{icone}</span>
                <span style="font-size:13px;color:{cor};font-weight:500;">{texto}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _renderizar_grafico_semanal() -> None:
    renderizar_secao(
        titulo=f"{ICONE_PRODUTIVIDADE} Produtividade",
        descricao="Exames realizados nos ultimos 7 dias",
    )

    sete_dias_atras = datetime.now(timezone.utc) - timedelta(days=7)

    with session_scope() as session:
        resultados = (
            session.execute(
                session.query(
                    func.date(OrdemServico.aberta_em).label("dia"),
                    func.count(OrdemServico.id).label("total"),
                )
                .filter(OrdemServico.aberta_em >= sete_dias_atras)
                .group_by("dia")
                .order_by("dia")
            )
            .mappings()
            .all()
        )

    if not resultados:
        renderizar_empty_state(
            icone=ICONE_PRODUTIVIDADE,
            titulo="Sem dados de produtividade",
            mensagem="Os dados de exames dos ultimos 7 dias aparecerao aqui.",
        )
        return

    dados = {
        "Dia": [r["dia"].strftime("%d/%m") if r["dia"] else "?" for r in resultados],
        "Exames": [r["total"] for r in resultados],
    }
    df = pd.DataFrame(dados).set_index("Dia")

    st.bar_chart(df, width="stretch")


if __name__ == "__main__":
    main()
