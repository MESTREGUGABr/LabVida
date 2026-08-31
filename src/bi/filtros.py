"""Filtro de periodo compartilhado pelos dashboards.

O apontamento do professor foi "implementar periodo no BI". Antes nao havia
NENHUM filtro de data: todo agregado era "desde o inicio dos tempos", e apenas
2 das 11 consultas sequer tocavam `bi_dim_tempo`.

Um componente unico para as 4 paginas garante que o periodo signifique a mesma
coisa em todas — e a `Periodo` que sai daqui e a unica forma de filtrar data em
`src/bi/metricas.py`.
"""

import uuid
from datetime import date, timedelta

import streamlit as st
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.bi.etl import ultima_execucao
from src.bi.metricas import FiltroDimensoes, Periodo
from src.bi.models import DimConvenio, DimProcedimento, DimTempo, DimUnidade

_PRESETS = ["Mes atual", "Ultimos 3 meses", "Ultimos 12 meses", "Tudo", "Personalizado"]
_PARTICULAR = "Particular"


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


def seletor_de_filtros(
    session: Session,
    *,
    chave: str,
    incluir_convenio: bool = True,
    incluir_procedimento: bool = True,
) -> FiltroDimensoes:
    """Widgets de Unidade/Convenio/Exame, combinaveis com o periodo.

    Nada selecionado num multiselect = sem filtro naquela dimensao (todas
    passam) — mesma convencao de "vazio = tudo" do resto do BI.
    """
    # So unidades de COLETA: nenhum fato do BI guarda `sk_unidade` de uma
    # unidade CENTRAL (laboratorio) — o fato sempre traz a unidade de coleta
    # de origem da OS. Oferecer o laboratorio como opcao so daria "zero
    # resultado" sempre, sem nenhum indicador dessa pagina responder a ele.
    unidades_opcoes = session.execute(
        select(DimUnidade.sk_unidade, DimUnidade.nome)
        .where(DimUnidade.tipo == "COLETA")
        .order_by(DimUnidade.nome)
    ).all()

    quantidade_colunas = 1 + int(incluir_convenio) + int(incluir_procedimento)
    colunas = st.columns(quantidade_colunas)

    with colunas[0]:
        escolhidas_unidade = st.multiselect(
            "Unidade",
            options=[nome for _, nome in unidades_opcoes],
            key=f"{chave}_filtro_unidade",
        )
    sk_unidades = [sk for sk, nome in unidades_opcoes if nome in escolhidas_unidade] or None

    sk_convenios: list[int] | None = None
    incluir_particular = False
    if incluir_convenio:
        convenios_opcoes = session.execute(
            select(DimConvenio.sk_convenio, DimConvenio.nome).order_by(DimConvenio.nome)
        ).all()
        with colunas[1]:
            escolhidos_convenio = st.multiselect(
                "Convenio",
                options=[_PARTICULAR] + [nome for _, nome in convenios_opcoes],
                key=f"{chave}_filtro_convenio",
            )
        incluir_particular = _PARTICULAR in escolhidos_convenio
        sk_convenios = [
            sk for sk, nome in convenios_opcoes if nome in escolhidos_convenio
        ] or None

    sk_procedimentos: list[int] | None = None
    if incluir_procedimento:
        procedimentos_opcoes = session.execute(
            select(DimProcedimento.sk_procedimento, DimProcedimento.nome).order_by(DimProcedimento.nome)
        ).all()
        with colunas[-1]:
            escolhidos_procedimento = st.multiselect(
                "Exame",
                options=[nome for _, nome in procedimentos_opcoes],
                key=f"{chave}_filtro_procedimento",
            )
        sk_procedimentos = [
            sk for sk, nome in procedimentos_opcoes if nome in escolhidos_procedimento
        ] or None

    return FiltroDimensoes(
        unidades=sk_unidades,
        convenios=sk_convenios,
        incluir_particular=incluir_particular,
        procedimentos=sk_procedimentos,
    )


def seletor_de_insumos(session: Session, *, chave: str) -> list[uuid.UUID] | None:
    """Filtro por insumo na pagina de Estoque — fora do esquema estrela
    (`InsumoMaterial` e tabela operacional, sem FK pra unidade/convenio)."""
    from src.compras.insumo.models import InsumoMaterial

    opcoes = session.execute(
        select(InsumoMaterial.id, InsumoMaterial.nome).order_by(InsumoMaterial.nome)
    ).all()
    escolhidos = st.multiselect(
        "Insumo",
        options=[nome for _, nome in opcoes],
        key=f"{chave}_filtro_insumo",
    )
    return [id_ for id_, nome in opcoes if nome in escolhidos] or None


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
