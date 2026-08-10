"""Filtro de periodo compartilhado pelos dashboards.

O apontamento do professor foi "implementar periodo no BI". Antes nao havia
NENHUM filtro de data: todo agregado era "desde o inicio dos tempos", e apenas
2 das 11 consultas sequer tocavam `bi_dim_tempo`.

Um componente unico para as 4 paginas garante que o periodo signifique a mesma
coisa em todas — e a `Periodo` que sai daqui e a unica forma de filtrar data em
`src/bi/metricas.py`.
"""

from datetime import date, timedelta

import streamlit as st
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.bi.etl import ultima_execucao
from src.bi.metricas import Periodo
from src.bi.models import DimTempo

_PRESETS = ["Mes atual", "Ultimos 3 meses", "Ultimos 12 meses", "Tudo", "Personalizado"]


def _limites_do_dw(session: Session) -> tuple[date, date]:
    """Primeira e ultima data do calendario carregado."""
    minimo, maximo = session.execute(
        select(func.min(DimTempo.data), func.max(DimTempo.data))
    ).one()
    hoje = date.today()
    return (minimo or hoje, maximo or hoje)


def _referencia(session: Session) -> date:
    """Ancora dos presets.

    Deliberadamente NAO e `date.today()`: a base de demonstracao e retrodatada,
    e ancorar em hoje faria "Mes atual" vir vazio numa base recem-semeada. A
    ancora e a ultima data com movimento, limitada a hoje.
    """
    _minimo, maximo = _limites_do_dw(session)
    return min(maximo, date.today()) if maximo else date.today()


def seletor_de_periodo(session: Session, *, chave: str = "bi_periodo") -> Periodo:
    """Renderiza o seletor e devolve o periodo escolhido."""
    minimo, maximo = _limites_do_dw(session)
    referencia = _referencia(session)

    coluna_preset, coluna_datas = st.columns([3, 2])

    with coluna_preset:
        preset = st.segmented_control(
            "Periodo",
            options=_PRESETS,
            default=_PRESETS[1],
            key=f"{chave}_preset",
        ) or _PRESETS[1]

    if preset == "Mes atual":
        inicio = referencia.replace(day=1)
        fim = referencia
    elif preset == "Ultimos 3 meses":
        inicio = (referencia.replace(day=1) - timedelta(days=62)).replace(day=1)
        fim = referencia
    elif preset == "Ultimos 12 meses":
        inicio = (referencia.replace(day=1) - timedelta(days=365)).replace(day=1)
        fim = referencia
    elif preset == "Tudo":
        inicio, fim = minimo, maximo
    else:
        with coluna_datas:
            intervalo = st.date_input(
                "Intervalo",
                value=(referencia.replace(day=1), referencia),
                min_value=minimo,
                max_value=maximo,
                key=f"{chave}_intervalo",
                format="DD/MM/YYYY",
            )
        if isinstance(intervalo, tuple) and len(intervalo) == 2:
            inicio, fim = intervalo
        else:
            inicio, fim = referencia.replace(day=1), referencia

    inicio = max(inicio, minimo)
    fim = min(fim, maximo)
    if inicio > fim:
        inicio = fim

    if preset != "Personalizado":
        with coluna_datas:
            st.caption(
                f"De **{inicio.strftime('%d/%m/%Y')}** ate **{fim.strftime('%d/%m/%Y')}**"
            )

    return Periodo(inicio=inicio, fim=fim, rotulo=preset)


def rodape_de_atualizacao(session: Session) -> None:
    """Quando o ETL rodou pela ultima vez.

    Sem isso o usuario nao tem como saber se o numero na tela e de hoje ou de
    tres semanas atras — e um BI sem data de carga nao e confiavel.
    """
    execucao = ultima_execucao(session)
    if execucao is None or execucao.finalizado_em is None:
        st.caption("Dados nunca carregados. Use **Atualizar dados do BI**.")
        return

    quando = execucao.finalizado_em.strftime("%d/%m/%Y as %H:%M")
    duracao = f" · carga em {execucao.duracao_seg}s" if execucao.duracao_seg else ""
    st.caption(f"Dados atualizados em {quando}{duracao}")


def botao_atualizar(*, chave: str) -> bool:
    """Dispara o ETL sob demanda. Retorna True se a carga rodou."""
    if not st.button("Atualizar dados do BI", key=chave, type="secondary"):
        return False

    from src.bi.etl import executar_etl

    with st.spinner("Executando ETL..."):
        executar_etl()
    st.success("Dados atualizados.")
    return True


def sem_dados(mensagem: str = "Nenhum dado no periodo selecionado.") -> None:
    st.info(f"{mensagem} Ajuste o filtro de periodo ou atualize os dados do BI.")
