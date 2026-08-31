"""Carga do esquema estrela do BI.

Propriedades que este ETL garante e o anterior nao garantia:

- **Idempotencia.** Rodar duas vezes sobre os mesmos dados de origem produz
  exatamente as mesmas linhas. O ETL anterior tinha `date.today()` em quatro
  pontos de `_carga_fatos`, entao os numeros mudavam conforme o dia da execucao.
- **Datacao pelo fato gerador.** Amostra pela coleta, faturamento pelo
  fechamento do lote, caixa pelo movimento. Nenhuma medida cai em "hoje".
- **Chave natural em todo fato**, com `INSERT ... ON CONFLICT DO UPDATE` e poda
  do que sumiu da origem. E o que torna a carga reexecutavel e, mais tarde,
  incremental.
- **Sem N+1.** As agregacoes acontecem no banco, em uma query por fato, no lugar
  dos loops que faziam duas queries por Ordem de Servico.
- **Observabilidade.** Cada execucao vira uma linha em `bi_etl_execucao`, para o
  dashboard poder dizer quando os dados foram atualizados.
"""

import hashlib
import uuid
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal

from sqlalchemy import Select, func, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import Session

from src.atendimento.amostra.models import Amostra, Coleta
from src.atendimento.ordem_servico.models import OrdemServico, OsItem
from src.bi.models import (
    DimConvenio,
    DimFaixaEtaria,
    DimMotivoGlosa,
    DimPacienteAnon,
    DimProcedimento,
    DimSetor,
    DimTempo,
    DimUnidade,
    EtlExecucao,
    FatoAtendimento,
    FatoFaturamento,
    FatoFinanceiro,
    FatoGlosa,
    FatoLogistica,
    FatoOrdemServico,
)
from src.cadastro.convenio.models import Convenio
from src.cadastro.models import Paciente
from src.cadastro.procedimento.models import Procedimento
from src.cadastro.unidade.models import Unidade
from src.db import session_scope
from src.faturamento.glosa.models import Glosa
from src.faturamento.lote_faturamento.models import GuiaItem, GuiaTiss, LoteFaturamento
from src.financeiro.movimento_caixa.models import MovimentoCaixa
from src.financeiro.titulo_pagar.models import TituloPagar
from src.financeiro.titulo_receber.models import TituloReceber
from src.laboratorial.models import Laudo, StatusLaudo
from src.logistica.malote.models import Malote, MaloteAmostra
from src.logistica.recebimento.models import AmostraMovimentacao, ProtocoloRecebimento

_DIAS_SEMANA = [
    "Segunda-feira", "Terca-feira", "Quarta-feira",
    "Quinta-feira", "Sexta-feira", "Sabado", "Domingo",
]

_NOMES_MES = [
    "Janeiro", "Fevereiro", "Marco", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
]

# (chave, descricao, ordem, idade_min, idade_max). None = sem limite.
_FAIXAS_ETARIAS = [
    ("0-12", "0-12 anos", 1, 0, 12),
    ("13-18", "13-18 anos", 2, 13, 18),
    ("19-30", "19-30 anos", 3, 19, 30),
    ("31-50", "31-50 anos", 4, 31, 50),
    ("51-65", "51-65 anos", 5, 51, 65),
    ("66+", "66+ anos", 6, 66, None),
    ("DESCONHECIDA", "Desconhecida", 9, None, None),
]

_SEM_SETOR = "SEM_SETOR"
_SEM_MOTIVO = "NAO_INFORMADO"


# ---------------------------------------------------------------------------
# Utilitarios
# ---------------------------------------------------------------------------


def _hash_paciente(paciente_id) -> str:
    """Pseudonimo deterministico do paciente (LGPD): nao reversivel para PII."""
    return hashlib.sha256(str(paciente_id).encode()).hexdigest()


def _normalizar(texto: str | None, padrao: str) -> str:
    """Chave natural de dimensao vinda de texto livre."""
    if texto is None:
        return padrao
    limpo = " ".join(texto.split()).strip()
    return limpo.casefold() if limpo else padrao


def _faixa_etaria(nascimento: date | None, referencia: date) -> str:
    """Faixa vigente NA DATA DO FATO — congelada, nunca recalculada (ADR 0009)."""
    if nascimento is None:
        return "DESCONHECIDA"
    idade = (
        referencia.year
        - nascimento.year
        - ((referencia.month, referencia.day) < (nascimento.month, nascimento.day))
    )
    if idade < 0:
        return "DESCONHECIDA"
    for chave, _descricao, _ordem, minimo, maximo in _FAIXAS_ETARIAS:
        if minimo is None:
            continue
        if idade >= minimo and (maximo is None or idade <= maximo):
            return chave
    return "DESCONHECIDA"


def _horas(inicio: datetime | None, fim: datetime | None) -> Decimal | None:
    if inicio is None or fim is None:
        return None
    return Decimal(str(round((fim - inicio).total_seconds() / 3600, 2)))


def _valor(bruto) -> Decimal:
    return Decimal(str(bruto)) if bruto is not None else Decimal("0")


# Postgres limita cada statement a 65.535 parâmetros; o INSERT em lote do
# _upsert fatia as linhas para ficar confortavelmente abaixo disso.
_LIMITE_PARAMETROS = 60000


def _upsert(session: Session, modelo, linhas: list[dict], chave: list[str]) -> int:
    """INSERT ... ON CONFLICT DO UPDATE em lotes.

    Um fato com a série longa passa de 6 mil linhas; num INSERT único isso
    estoura o limite de parâmetros do Postgres, então o lote é fatiado pelo
    número de colunas da linha.
    """
    if not linhas:
        return 0
    por_lote = max(1, _LIMITE_PARAMETROS // len(linhas[0]))
    total = 0
    for indice in range(0, len(linhas), por_lote):
        lote = linhas[indice : indice + por_lote]
        stmt = pg_insert(modelo).values(lote)
        atualizaveis = {c: stmt.excluded[c] for c in linhas[0] if c not in chave}
        if atualizaveis:
            stmt = stmt.on_conflict_do_update(index_elements=chave, set_=atualizaveis)
        else:
            stmt = stmt.on_conflict_do_nothing(index_elements=chave)
        session.execute(stmt)
        total += len(lote)
    return total


def _podar(session: Session, modelo, coluna_chave, presentes: set) -> None:
    """Remove do fato o que sumiu da origem — mantem a carga reexecutavel."""
    if presentes:
        session.execute(modelo.__table__.delete().where(coluna_chave.notin_(presentes)))
    else:
        session.execute(modelo.__table__.delete())


def _mapa(session: Session, modelo, coluna_chave, coluna_sk) -> dict:
    return {
        chave: sk
        for chave, sk in session.execute(select(coluna_chave, coluna_sk)).all()
    }


# ---------------------------------------------------------------------------
# Dimensoes
# ---------------------------------------------------------------------------


def _intervalo_do_calendario(session: Session) -> tuple[date, date]:
    """Menor e maior data relevante do operacional, para o calendario denso."""
    fontes: list[Select] = [
        select(func.min(OrdemServico.aberta_em), func.max(OrdemServico.aberta_em)),
        select(func.min(Coleta.coletada_em), func.max(Coleta.coletada_em)),
        select(func.min(Laudo.liberado_em), func.max(Laudo.liberado_em)),
        select(func.min(LoteFaturamento.criado_em), func.max(LoteFaturamento.fechado_em)),
        select(func.min(Glosa.criado_em), func.max(Glosa.criado_em)),
        select(func.min(MovimentoCaixa.ocorrido_em), func.max(MovimentoCaixa.ocorrido_em)),
        select(func.min(Malote.criado_em), func.max(Malote.despachado_em)),
        select(func.min(ProtocoloRecebimento.recebido_em), func.max(ProtocoloRecebimento.recebido_em)),
        select(func.min(TituloReceber.vencimento), func.max(TituloReceber.vencimento)),
        select(func.min(TituloPagar.vencimento), func.max(TituloPagar.vencimento)),
    ]

    hoje = datetime.now(timezone.utc).date()
    inicio, fim = hoje, hoje
    for consulta in fontes:
        minimo, maximo = session.execute(consulta).one()
        for bruto in (minimo, maximo):
            if bruto is None:
                continue
            valor = bruto.date() if isinstance(bruto, datetime) else bruto
            inicio = min(inicio, valor)
            fim = max(fim, valor)

    # Fecha o mes corrente inteiro: serie mensal sem cauda truncada.
    fim = max(fim, hoje)
    return inicio.replace(day=1), fim


def _carregar_dim_tempo(session: Session) -> dict[date, int]:
    """Calendario DENSO — sem buraco de dia, portanto sem buraco de mes."""
    inicio, fim = _intervalo_do_calendario(session)

    linhas = []
    atual = inicio
    while atual <= fim:
        iso = atual.isocalendar()
        linhas.append(
            {
                "data": atual,
                "ano": atual.year,
                "mes": atual.month,
                "dia": atual.day,
                "dia_semana": _DIAS_SEMANA[atual.weekday()],
                "dia_semana_num": atual.weekday(),
                "trimestre": (atual.month - 1) // 3 + 1,
                "semestre": 1 if atual.month <= 6 else 2,
                "semana_iso": iso.week,
                "nome_mes": _NOMES_MES[atual.month - 1],
                "ano_mes": f"{atual.year}-{atual.month:02d}",
                "competencia": atual.replace(day=1),
                "dia_util": atual.weekday() < 5,
            }
        )
        atual += timedelta(days=1)

    _upsert(session, DimTempo, linhas, ["data"])
    session.flush()
    return _mapa(session, DimTempo, DimTempo.data, DimTempo.sk_tempo)


def _carregar_dim_faixa_etaria(session: Session) -> dict[str, int]:
    linhas = [
        {"chave_natural": chave, "descricao": descricao, "ordem": ordem}
        for chave, descricao, ordem, _minimo, _maximo in _FAIXAS_ETARIAS
    ]
    _upsert(session, DimFaixaEtaria, linhas, ["chave_natural"])
    session.flush()
    return _mapa(session, DimFaixaEtaria, DimFaixaEtaria.chave_natural, DimFaixaEtaria.sk_faixa_etaria)


def _carregar_dim_unidade(session: Session) -> dict[uuid.UUID, int]:
    linhas = [
        {
            "id_origem": u.id,
            "nome": u.nome,
            "tipo": u.tipo.value if hasattr(u.tipo, "value") else str(u.tipo),
        }
        for u in session.scalars(select(Unidade)).all()
    ]
    _upsert(session, DimUnidade, linhas, ["id_origem"])
    session.flush()
    return _mapa(session, DimUnidade, DimUnidade.id_origem, DimUnidade.sk_unidade)


def _carregar_dim_convenio(session: Session) -> dict[uuid.UUID, int]:
    linhas = [
        {"id_origem": c.id, "nome": c.nome, "registro_ans": c.registro_ans}
        for c in session.scalars(select(Convenio)).all()
    ]
    _upsert(session, DimConvenio, linhas, ["id_origem"])
    session.flush()
    return _mapa(session, DimConvenio, DimConvenio.id_origem, DimConvenio.sk_convenio)


def _carregar_dim_setor(session: Session, procedimentos) -> dict[str, int]:
    vistos: dict[str, str] = {_SEM_SETOR: "Sem setor"}
    for proc in procedimentos:
        chave = _normalizar(proc.setor, _SEM_SETOR)
        if chave not in vistos:
            vistos[chave] = (proc.setor or "").strip() or "Sem setor"

    linhas = [{"chave_natural": chave, "nome": nome} for chave, nome in vistos.items()]
    _upsert(session, DimSetor, linhas, ["chave_natural"])
    session.flush()
    return _mapa(session, DimSetor, DimSetor.chave_natural, DimSetor.sk_setor)


def _carregar_dim_procedimento(session: Session, procedimentos, setores) -> dict[uuid.UUID, int]:
    linhas = [
        {
            "id_origem": p.id,
            "codigo_tuss": p.codigo_tuss,
            "nome": p.nome,
            # Antes era sempre NULL: a carga passava setor=None de proposito.
            "setor": p.setor,
            "sk_setor": setores.get(_normalizar(p.setor, _SEM_SETOR)),
            "ativo": bool(p.ativo),
        }
        for p in procedimentos
    ]
    _upsert(session, DimProcedimento, linhas, ["id_origem"])
    session.flush()
    return _mapa(session, DimProcedimento, DimProcedimento.id_origem, DimProcedimento.sk_procedimento)


def _carregar_dim_paciente(session: Session, pacientes) -> dict[uuid.UUID, int]:
    linhas = []
    por_uuid: dict[uuid.UUID, str] = {}
    for p in pacientes:
        chave = _hash_paciente(p.id)
        por_uuid[p.id] = chave
        sexo = p.sexo.value if hasattr(p.sexo, "value") else (str(p.sexo) if p.sexo else "NAO_INFORMADO")
        linhas.append({"id_origem": chave, "sexo": sexo})

    _upsert(session, DimPacienteAnon, linhas, ["id_origem"])
    session.flush()
    por_hash = _mapa(session, DimPacienteAnon, DimPacienteAnon.id_origem, DimPacienteAnon.sk_paciente)
    return {pid: por_hash[chave] for pid, chave in por_uuid.items() if chave in por_hash}


def _carregar_dim_motivo_glosa(session: Session) -> dict[str, int]:
    motivos = session.scalars(select(Glosa.motivo).distinct()).all()
    vistos: dict[str, str] = {_SEM_MOTIVO: "Nao informado"}
    for motivo in motivos:
        chave = _normalizar(motivo, _SEM_MOTIVO)
        if chave not in vistos:
            vistos[chave] = (motivo or "").strip() or "Nao informado"

    linhas = [{"chave_natural": chave, "descricao": descricao} for chave, descricao in vistos.items()]
    _upsert(session, DimMotivoGlosa, linhas, ["chave_natural"])
    session.flush()
    return _mapa(session, DimMotivoGlosa, DimMotivoGlosa.chave_natural, DimMotivoGlosa.sk_motivo_glosa)


def _carregar_dimensoes(session: Session) -> dict:
    procedimentos = session.scalars(select(Procedimento)).all()
    pacientes = session.scalars(select(Paciente)).all()

    setores = _carregar_dim_setor(session, procedimentos)
    return {
        "tempo": _carregar_dim_tempo(session),
        "faixa": _carregar_dim_faixa_etaria(session),
        "unidade": _carregar_dim_unidade(session),
        "convenio": _carregar_dim_convenio(session),
        "setor": setores,
        "procedimento": _carregar_dim_procedimento(session, procedimentos, setores),
        "paciente": _carregar_dim_paciente(session, pacientes),
        "motivo_glosa": _carregar_dim_motivo_glosa(session),
        "nascimento": {p.id: p.data_nascimento for p in pacientes},
        "setor_por_procedimento": {
            p.id: setores.get(_normalizar(p.setor, _SEM_SETOR)) for p in procedimentos
        },
    }


# ---------------------------------------------------------------------------
# Marcos temporais por Ordem de Servico e por amostra
# ---------------------------------------------------------------------------


def _marcos_por_os(session: Session) -> dict[uuid.UUID, dict]:
    """Coleta, recebimento e laudo por OS — tres queries agregadas, sem N+1."""
    marcos: dict[uuid.UUID, dict] = {}

    coletas = session.execute(
        select(Amostra.ordem_servico_id, func.min(Coleta.coletada_em))
        .join(Coleta, Coleta.amostra_id == Amostra.id)
        .group_by(Amostra.ordem_servico_id)
    ).all()
    for os_id, primeira in coletas:
        marcos.setdefault(os_id, {})["coleta"] = primeira

    recebimentos = session.execute(
        select(Amostra.ordem_servico_id, func.min(ProtocoloRecebimento.recebido_em))
        .join(MaloteAmostra, MaloteAmostra.amostra_id == Amostra.id)
        .join(ProtocoloRecebimento, ProtocoloRecebimento.malote_id == MaloteAmostra.malote_id)
        .group_by(Amostra.ordem_servico_id)
    ).all()
    for os_id, primeiro in recebimentos:
        marcos.setdefault(os_id, {})["recebimento"] = primeiro

    laudos = session.execute(
        select(OsItem.ordem_servico_id, func.max(Laudo.liberado_em))
        .join(Laudo, Laudo.os_item_id == OsItem.id)
        .where(Laudo.status == StatusLaudo.LIBERADO)
        .group_by(OsItem.ordem_servico_id)
    ).all()
    for os_id, ultimo in laudos:
        marcos.setdefault(os_id, {})["laudo"] = ultimo

    return marcos


def _marcos_por_amostra(session: Session) -> dict[uuid.UUID, dict]:
    """Coleta, despacho e recebimento por amostra.

    `tempo_transito_horas` sai daqui: `recebido_em - despachado_em`. As duas
    datas sempre existiram no OLTP e a coluna do fato nunca foi populada.
    """
    marcos: dict[uuid.UUID, dict] = {}

    for amostra_id, coletada_em in session.execute(
        select(Coleta.amostra_id, Coleta.coletada_em)
    ).all():
        marcos.setdefault(amostra_id, {})["coleta"] = coletada_em

    # `malotes_amostras.amostra_id` e UNIQUE e `protocolos_recebimento.malote_id`
    # tambem: a cadeia amostra -> malote -> protocolo e 1:1:1, entao nao ha o que
    # agregar aqui.
    transporte = session.execute(
        select(
            MaloteAmostra.amostra_id,
            Malote.despachado_em,
            ProtocoloRecebimento.recebido_em,
            Malote.unidade_destino_id,
        )
        .join(Malote, Malote.id == MaloteAmostra.malote_id)
        .join(
            ProtocoloRecebimento,
            ProtocoloRecebimento.malote_id == Malote.id,
            isouter=True,
        )
    ).all()
    for amostra_id, despachado, recebido, destino in transporte:
        registro = marcos.setdefault(amostra_id, {})
        registro["despacho"] = despachado
        registro["recebimento"] = recebido
        registro["destino"] = destino

    rejeicoes = session.execute(
        select(AmostraMovimentacao.amostra_id, func.count())
        .where(AmostraMovimentacao.status == "REJEITADA")
        .group_by(AmostraMovimentacao.amostra_id)
    ).all()
    for amostra_id, quantidade in rejeicoes:
        marcos.setdefault(amostra_id, {})["rejeicoes"] = quantidade

    return marcos


# ---------------------------------------------------------------------------
# Fatos
# ---------------------------------------------------------------------------


def _fato_ordem_servico(session: Session, dims: dict) -> int:
    marcos = _marcos_por_os(session)

    agregados = {
        os_id: (total, cancelados, _valor(soma))
        for os_id, total, cancelados, soma in session.execute(
            select(
                OsItem.ordem_servico_id,
                func.count(),
                func.count().filter(OsItem.status == "CANCELADO"),
                func.sum(OsItem.valor_negociado),
            ).group_by(OsItem.ordem_servico_id)
        ).all()
    }

    linhas, presentes = [], set()
    for ordem in session.scalars(select(OrdemServico)).all():
        if ordem.aberta_em is None:
            continue
        sk_tempo = dims["tempo"].get(ordem.aberta_em.date())
        sk_unidade = dims["unidade"].get(ordem.unidade_id)
        sk_paciente = dims["paciente"].get(ordem.paciente_id)
        if sk_tempo is None or sk_unidade is None or sk_paciente is None:
            continue

        marco = marcos.get(ordem.id, {})
        total, cancelados, soma = agregados.get(ordem.id, (0, 0, Decimal("0")))
        nascimento = dims["nascimento"].get(ordem.paciente_id)

        presentes.add(ordem.id)
        linhas.append(
            {
                "ordem_servico_id": ordem.id,
                "sk_tempo": sk_tempo,
                "sk_unidade": sk_unidade,
                "sk_convenio": dims["convenio"].get(ordem.convenio_id),
                "sk_paciente": sk_paciente,
                "sk_faixa_etaria": dims["faixa"][_faixa_etaria(nascimento, ordem.aberta_em.date())],
                "qtd_itens": total,
                "qtd_itens_cancelados": cancelados,
                "valor_total": soma,
                "tempo_ciclo_horas": _horas(marco.get("coleta"), marco.get("laudo")),
                "tempo_coleta_recebimento_horas": _horas(marco.get("coleta"), marco.get("recebimento")),
                "tempo_recebimento_laudo_horas": _horas(marco.get("recebimento"), marco.get("laudo")),
                "concluida": marco.get("laudo") is not None,
            }
        )

    _podar(session, FatoOrdemServico, FatoOrdemServico.ordem_servico_id, presentes)
    return _upsert(session, FatoOrdemServico, linhas, ["ordem_servico_id"])


def _fato_atendimento(session: Session, dims: dict) -> int:
    liberados = set(
        session.scalars(
            select(Laudo.os_item_id).where(Laudo.status == StatusLaudo.LIBERADO)
        ).all()
    )

    consulta = (
        select(
            OsItem.id,
            OsItem.procedimento_id,
            OsItem.valor_negociado,
            OsItem.status,
            OrdemServico.id.label("ordem_id"),
            OrdemServico.aberta_em,
            OrdemServico.unidade_id,
            OrdemServico.convenio_id,
            OrdemServico.paciente_id,
        )
        .join(OrdemServico, OrdemServico.id == OsItem.ordem_servico_id)
        .where(OrdemServico.aberta_em.is_not(None))
    )

    linhas, presentes = [], set()
    for r in session.execute(consulta).all():
        sk_tempo = dims["tempo"].get(r.aberta_em.date())
        sk_unidade = dims["unidade"].get(r.unidade_id)
        sk_paciente = dims["paciente"].get(r.paciente_id)
        sk_procedimento = dims["procedimento"].get(r.procedimento_id)
        if None in (sk_tempo, sk_unidade, sk_paciente, sk_procedimento):
            continue

        nascimento = dims["nascimento"].get(r.paciente_id)
        presentes.add(r.id)
        linhas.append(
            {
                "os_item_id": r.id,
                "sk_tempo": sk_tempo,
                "sk_unidade": sk_unidade,
                "sk_convenio": dims["convenio"].get(r.convenio_id),
                "sk_procedimento": sk_procedimento,
                "sk_paciente": sk_paciente,
                "sk_faixa_etaria": dims["faixa"][_faixa_etaria(nascimento, r.aberta_em.date())],
                "sk_setor": dims["setor_por_procedimento"].get(r.procedimento_id),
                "qtd_exames": 1,
                "valor_negociado": _valor(r.valor_negociado),
                "cancelado": str(r.status) == "CANCELADO",
                "laudo_liberado": r.id in liberados,
            }
        )

    _podar(session, FatoAtendimento, FatoAtendimento.os_item_id, presentes)
    return _upsert(session, FatoAtendimento, linhas, ["os_item_id"])


def _fato_faturamento(session: Session, dims: dict) -> int:
    """Item faturado, datado pelo FECHAMENTO do lote.

    Item de lote ainda ABERTO nao entra: antes ele caia em `date.today()` e
    migrava de bucket temporal a cada execucao do ETL.
    """
    glosado_por_item = {
        item_id: _valor(soma)
        for item_id, soma in session.execute(
            select(Glosa.guia_item_id, func.sum(Glosa.valor_glosado)).group_by(Glosa.guia_item_id)
        ).all()
    }

    consulta = (
        select(
            GuiaItem.id,
            GuiaItem.procedimento_id,
            GuiaItem.valor_faturado,
            LoteFaturamento.fechado_em,
            LoteFaturamento.convenio_id,
            OrdemServico.unidade_id,
            OrdemServico.paciente_id,
        )
        .join(GuiaTiss, GuiaTiss.id == GuiaItem.guia_tiss_id)
        .join(LoteFaturamento, LoteFaturamento.id == GuiaTiss.lote_faturamento_id)
        .join(Laudo, Laudo.id == GuiaItem.laudo_id)
        .join(OsItem, OsItem.id == Laudo.os_item_id)
        .join(OrdemServico, OrdemServico.id == OsItem.ordem_servico_id)
        .where(LoteFaturamento.fechado_em.is_not(None))
    )

    linhas, presentes = [], set()
    for r in session.execute(consulta).all():
        sk_tempo = dims["tempo"].get(r.fechado_em.date())
        sk_unidade = dims["unidade"].get(r.unidade_id)
        sk_procedimento = dims["procedimento"].get(r.procedimento_id)
        sk_paciente = dims["paciente"].get(r.paciente_id)
        if None in (sk_tempo, sk_unidade, sk_procedimento, sk_paciente):
            continue

        faturado = _valor(r.valor_faturado)
        glosado = glosado_por_item.get(r.id, Decimal("0"))
        presentes.add(r.id)
        linhas.append(
            {
                "guia_item_id": r.id,
                "sk_tempo": sk_tempo,
                # Unidade REAL da OS — antes era a unidade fake "consolidado".
                "sk_unidade": sk_unidade,
                "sk_convenio": dims["convenio"].get(r.convenio_id),
                "sk_procedimento": sk_procedimento,
                "sk_paciente": sk_paciente,
                "sk_setor": dims["setor_por_procedimento"].get(r.procedimento_id),
                "valor_faturado": faturado,
                "valor_glosado": glosado,
                "valor_liberado": faturado - glosado,
                "qtd_itens": 1,
            }
        )

    _podar(session, FatoFaturamento, FatoFaturamento.guia_item_id, presentes)
    return _upsert(session, FatoFaturamento, linhas, ["guia_item_id"])


def _fato_financeiro(session: Session, dims: dict) -> int:
    """Dois regimes na mesma tabela, separados pela coluna `regime`.

    PREVISTO = titulo, datado pelo vencimento (cronograma).
    CAIXA    = movimento, datado por `ocorrido_em` (dinheiro que entrou/saiu).

    Antes o ETL somava `titulo.valor` de TODO titulo em `valor_recebido`,
    independente do status: titulo ABERTO virava receita realizada na tela.

    `sk_unidade` aqui nao e atribuicao por unidade de coleta: 87,5% dos lotes
    de faturamento fechados hoje misturam itens de OSs de 2 a 4 unidades
    diferentes (`lotes_faturamento` nao tem `unidade_id`, e o fechamento so
    valida convenio), e `Usuario` nao tem coluna de unidade — nao ha unidade
    real recuperavel sem mudar o modelo de faturamento/RH. E caixa
    consolidado, entao aponta para a unidade CENTRAL (o Laboratorio, o
    "centro de resolucao") em vez de sortear a primeira unidade de coleta do
    dicionario, que era o bug antigo.
    """
    unidade_padrao = session.scalar(
        select(DimUnidade.sk_unidade).where(DimUnidade.tipo == "CENTRAL").limit(1)
    )
    if unidade_padrao is None:
        _podar(session, FatoFinanceiro, FatoFinanceiro.origem_id, set())
        return 0

    convenio_por_lote = {
        lote_id: convenio_id
        for lote_id, convenio_id in session.execute(
            select(LoteFaturamento.id, LoteFaturamento.convenio_id)
        ).all()
    }

    linhas, presentes = [], set()

    for titulo in session.scalars(select(TituloReceber)).all():
        sk_tempo = dims["tempo"].get(titulo.vencimento)
        if sk_tempo is None:
            continue
        convenio_id = convenio_por_lote.get(titulo.lote_faturamento_id)
        presentes.add(titulo.id)
        linhas.append(
            {
                "regime": "PREVISTO",
                "origem_tabela": "titulos_receber",
                "origem_id": titulo.id,
                "sk_tempo": sk_tempo,
                "sk_unidade": unidade_padrao,
                "sk_convenio": dims["convenio"].get(convenio_id),
                "fluxo": "ENTRADA",
                "valor_previsto": _valor(titulo.valor),
                "valor_realizado": Decimal("0"),
                "liquidado": str(titulo.status) == "PAGO",
            }
        )

    for titulo in session.scalars(select(TituloPagar)).all():
        sk_tempo = dims["tempo"].get(titulo.vencimento)
        if sk_tempo is None:
            continue
        presentes.add(titulo.id)
        linhas.append(
            {
                "regime": "PREVISTO",
                "origem_tabela": "titulos_pagar",
                "origem_id": titulo.id,
                "sk_tempo": sk_tempo,
                "sk_unidade": unidade_padrao,
                "sk_convenio": None,
                "fluxo": "SAIDA",
                "valor_previsto": _valor(titulo.valor),
                "valor_realizado": Decimal("0"),
                "liquidado": str(titulo.status) == "PAGO",
            }
        )

    for movimento in session.scalars(select(MovimentoCaixa)).all():
        sk_tempo = dims["tempo"].get(movimento.ocorrido_em.date())
        if sk_tempo is None:
            continue
        convenio_id = None
        if movimento.titulo_receber_id is not None:
            titulo = session.get(TituloReceber, movimento.titulo_receber_id)
            if titulo is not None:
                convenio_id = convenio_por_lote.get(titulo.lote_faturamento_id)
        presentes.add(movimento.id)
        linhas.append(
            {
                "regime": "CAIXA",
                "origem_tabela": "movimentos_caixa",
                "origem_id": movimento.id,
                "sk_tempo": sk_tempo,
                "sk_unidade": unidade_padrao,
                "sk_convenio": dims["convenio"].get(convenio_id),
                "fluxo": str(movimento.tipo),
                "valor_previsto": Decimal("0"),
                "valor_realizado": _valor(movimento.valor),
                "liquidado": True,
            }
        )

    _podar(session, FatoFinanceiro, FatoFinanceiro.origem_id, presentes)
    return _upsert(
        session, FatoFinanceiro, linhas, ["regime", "origem_tabela", "origem_id"]
    )


def _fato_logistica(session: Session, dims: dict) -> int:
    """Amostra datada pela COLETA — antes tudo caia numa barra unica em 'hoje'."""
    marcos = _marcos_por_amostra(session)

    consulta = (
        select(
            Amostra.id,
            Amostra.status,
            OrdemServico.unidade_id,
        )
        .join(OrdemServico, OrdemServico.id == Amostra.ordem_servico_id)
    )

    linhas, presentes = [], set()
    for r in session.execute(consulta).all():
        marco = marcos.get(r.id, {})
        coletada_em = marco.get("coleta")
        if coletada_em is None:
            # Sem coleta nao ha data de fato gerador. Datar em "hoje" e
            # exatamente o bug que este ETL corrige, entao a amostra fica fora.
            continue

        sk_tempo = dims["tempo"].get(coletada_em.date())
        sk_unidade = dims["unidade"].get(r.unidade_id)
        if sk_tempo is None or sk_unidade is None:
            continue

        rejeicoes = marco.get("rejeicoes", 0)
        presentes.add(r.id)
        linhas.append(
            {
                "amostra_id": r.id,
                "sk_tempo": sk_tempo,
                "sk_unidade": sk_unidade,
                "sk_unidade_destino": dims["unidade"].get(marco.get("destino")),
                "qtd_amostras": 1,
                "tempo_transito_horas": _horas(marco.get("despacho"), marco.get("recebimento")),
                "tempo_coleta_recebimento_horas": _horas(coletada_em, marco.get("recebimento")),
                "rejeitada": str(r.status) == "REJEITADA",
                "amostras_divergentes": rejeicoes,
                "status_atual": str(r.status),
            }
        )

    _podar(session, FatoLogistica, FatoLogistica.amostra_id, presentes)
    return _upsert(session, FatoLogistica, linhas, ["amostra_id"])


def _fato_glosa(session: Session, dims: dict) -> int:
    consulta = (
        select(
            Glosa.id,
            Glosa.motivo,
            Glosa.valor_glosado,
            Glosa.criado_em,
            Glosa.unidade_origem_id,
            GuiaItem.procedimento_id,
            GuiaItem.valor_faturado,
            LoteFaturamento.convenio_id,
        )
        .join(GuiaItem, GuiaItem.id == Glosa.guia_item_id)
        .join(GuiaTiss, GuiaTiss.id == GuiaItem.guia_tiss_id)
        .join(LoteFaturamento, LoteFaturamento.id == GuiaTiss.lote_faturamento_id)
    )

    linhas, presentes = [], set()
    for r in session.execute(consulta).all():
        sk_tempo = dims["tempo"].get(r.criado_em.date())
        sk_unidade = dims["unidade"].get(r.unidade_origem_id)
        sk_procedimento = dims["procedimento"].get(r.procedimento_id)
        if None in (sk_tempo, sk_unidade, sk_procedimento):
            continue

        presentes.add(r.id)
        linhas.append(
            {
                "glosa_id": r.id,
                "sk_tempo": sk_tempo,
                "sk_unidade": sk_unidade,
                "sk_convenio": dims["convenio"].get(r.convenio_id),
                "sk_procedimento": sk_procedimento,
                "sk_motivo_glosa": dims["motivo_glosa"][_normalizar(r.motivo, _SEM_MOTIVO)],
                "valor_glosado": _valor(r.valor_glosado),
                "valor_faturado_item": _valor(r.valor_faturado),
                "qtd_glosas": 1,
            }
        )

    _podar(session, FatoGlosa, FatoGlosa.glosa_id, presentes)
    return _upsert(session, FatoGlosa, linhas, ["glosa_id"])


def _carregar_fatos(session: Session, dims: dict) -> dict[str, int]:
    return {
        "fato_ordem_servico": _fato_ordem_servico(session, dims),
        "fato_atendimento": _fato_atendimento(session, dims),
        "fato_faturamento": _fato_faturamento(session, dims),
        "fato_financeiro": _fato_financeiro(session, dims),
        "fato_logistica": _fato_logistica(session, dims),
        "fato_glosa": _fato_glosa(session, dims),
    }


# ---------------------------------------------------------------------------
# Orquestracao
# ---------------------------------------------------------------------------


def executar_etl(modo: str = "FULL") -> dict[str, int]:
    """Carrega o esquema estrela e registra a execucao.

    Reexecutavel: rodar duas vezes sobre os mesmos dados de origem produz
    exatamente as mesmas linhas.
    """
    inicio = datetime.now(timezone.utc)
    execucao_id = uuid.uuid4()

    with session_scope() as session:
        session.add(EtlExecucao(id=execucao_id, iniciado_em=inicio, status="EXECUTANDO", modo=modo))
        session.commit()

        try:
            dims = _carregar_dimensoes(session)
            contagem = _carregar_fatos(session, dims)
            session.commit()
        except Exception as erro:
            session.rollback()
            registro = session.get(EtlExecucao, execucao_id)
            if registro is not None:
                registro.status = "ERRO"
                registro.finalizado_em = datetime.now(timezone.utc)
                registro.erro = str(erro)[:4000]
                session.commit()
            raise

        fim = datetime.now(timezone.utc)
        registro = session.get(EtlExecucao, execucao_id)
        registro.status = "SUCESSO"
        registro.finalizado_em = fim
        registro.linhas = contagem
        registro.duracao_seg = Decimal(str(round((fim - inicio).total_seconds(), 2)))
        session.commit()

    return contagem


def ultima_execucao(session: Session) -> EtlExecucao | None:
    """Alimenta o "dados atualizados em ..." dos dashboards."""
    return session.scalar(
        select(EtlExecucao)
        .where(EtlExecucao.status == "SUCESSO")
        .order_by(EtlExecucao.finalizado_em.desc())
        .limit(1)
    )


def main() -> None:
    contagem = executar_etl()
    print("ETL BI concluido.")
    for chave, valor in contagem.items():
        print(f"  {chave}: {valor}")


if __name__ == "__main__":
    main()
