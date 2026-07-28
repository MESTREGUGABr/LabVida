"""Seed do fluxo operacional: OS → coleta → malote → recebimento no central.

As Ordens de Serviço são distribuídas ao longo da janela de operação e por
estágio do fluxo, de modo que toda tela tenha volume real para trabalhar:
aguardando coleta, coletada sem malote, em trânsito, recebida no central,
rejeitada por avaria e cancelada.

Os marcos de cada OS são retrodatados depois de gravados pelos services — as
regras de negócio continuam sendo validadas normalmente, e a base fica com
histórico de meses (o que o BI precisa para ter série temporal).
"""

import random
from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.atendimento.amostra.dtos import ColetaCreate, TipoMaterial
from src.atendimento.amostra.models import Amostra, Coleta
from src.atendimento.amostra.service import registrar_coleta
from src.atendimento.autorizacao.dtos import AutorizacaoCreate, StatusAutorizacao
from src.atendimento.autorizacao.service import registrar_autorizacao
from src.atendimento.ordem_servico import repository as os_repository
from src.atendimento.ordem_servico.dtos import OrdemServicoCreate, OsItemInput
from src.atendimento.ordem_servico.service import abrir_os, cancelar_os
from src.cadastro.convenio.repository import listar_ativos as listar_convenios
from src.cadastro.medico.repository import listar_ativos as listar_medicos
from src.cadastro.procedimento.repository import listar_ativos as listar_procedimentos
from src.cadastro.service import listar_pacientes_ativos as listar_pacientes
from src.cadastro.unidade.repository import listar_unidades_ativas
from src.db import session_scope
from src.logistica.malote.dtos import MaloteCreate
from src.logistica.malote.models import Malote
from src.logistica.malote.service import (
    adicionar_amostra_ao_malote,
    criar_malote,
    despachar_malote,
)
from src.logistica.recebimento.dtos import ProtocoloRecebimentoCreate
from src.logistica.recebimento.models import AmostraMovimentacao, ProtocoloRecebimento
from src.logistica.recebimento.service import receber_malote
from src.seeder.catalogo import MOTIVOS_REJEICAO, PROCEDIMENTOS
from src.seeder.config import JANELA_DIAS, agora, momento, qtd, somar_horas
from src.usuario.models import Usuario

ORDENS_PADRAO = 400
_ATENDIMENTOS_POR_JORNADA = (2, 6)
_EXAMES_POR_OS = (2, 6)

# Uma parte das OS fica na operação corrente (últimos dias) e o resto compõe o
# histórico do período. É o que dá volume às telas de pendência sem inventar
# malote parado em trânsito desde o começo do ano.
_DIAS_OPERACAO_CORRENTE = 10
_PROPORCAO_OPERACAO_CORRENTE = 0.30

# Estágio do fluxo por idade da OS (cada dicionário soma 1.0).
_PESOS_ESTAGIO_CORRENTE = {
    "aberta": 0.15,       # aguardando autorização/coleta
    "coletada": 0.22,     # coletada, aguardando malote
    "em_transito": 0.18,  # malote despachado, a caminho do central
    "recebida": 0.45,     # recebida no central (vira insumo do laboratório)
}
_PESOS_ESTAGIO_HISTORICO = {
    "aberta": 0.05,       # ficou pendente e será cancelada
    "recebida": 0.95,
}

# Boa parte das OS que travam na autorização acaba cancelada pela recepção.
_PROPORCAO_ABERTAS_CANCELADAS = 0.45
_PROPORCAO_REJEITADAS = 0.06
_PROPORCAO_PARTICULAR = 0.18
_CAPACIDADE_MALOTE = (4, 9)


@dataclass
class _Contexto:
    pacientes: list
    medicos: list
    convenios: list
    procedimentos: list
    unidades_coleta: list
    central: object
    atendentes: list
    coletores: list
    recebedores: list
    admin: object
    materiais: dict


@dataclass
class _Jornada:
    """Movimento de um dia numa unidade de coleta.

    As OS nascem agrupadas assim — e não espalhadas aleatoriamente — porque é o
    que faz o malote do dia sair com várias amostras, como na operação real.
    """

    unidade: object
    instantes: list[datetime]


@dataclass
class _Bucket:
    """Amostras do dia aguardando fechamento de malote numa unidade de coleta.

    O malote fecha quando enche ou quando vira o dia — malote não acumula
    amostra de meses diferentes, e é isso que mantém a linha do tempo coerente.
    """

    dia: date
    amostras: list = field(default_factory=list)
    instantes: list = field(default_factory=list)


def executar_seeder_atendimento() -> dict[str, int]:
    contagem = {
        "ordens_servico": 0,
        "itens": 0,
        "amostras": 0,
        "malotes": 0,
        "recebimentos": 0,
        "amostras_rejeitadas": 0,
        "ordens_canceladas": 0,
    }

    with session_scope() as session:
        if os_repository.listar(session):
            return contagem

        contexto = _montar_contexto(session)
        if contexto is None:
            return contagem

        buckets: dict[tuple[UUID, str], _Bucket] = {}
        abertas_para_cancelar: list[UUID] = []

        # Em ordem cronológica: é o que permite fechar o malote na virada do dia.
        for jornada in _planejar_jornadas(contexto, qtd(ORDENS_PADRAO)):
            for t_abertura in jornada.instantes:
                plano = _criar_ordem(session, contexto, contagem, t_abertura, jornada.unidade)
                if plano is None:
                    continue

                ordem_id, estagio = plano
                if estagio == "aberta":
                    abertas_para_cancelar.append(ordem_id)
                    continue

                amostra_id, t_coleta = _coletar(session, contexto, ordem_id, t_abertura)
                contagem["amostras"] += 1
                if estagio == "coletada":
                    continue

                chave = (jornada.unidade.id, "recebida" if estagio == "recebida" else "transito")
                bucket = _bucket_do_dia(session, contexto, buckets, chave, t_coleta.date(), contagem)
                bucket.amostras.append(amostra_id)
                bucket.instantes.append(t_coleta)

                if len(bucket.amostras) >= random.randint(*_CAPACIDADE_MALOTE):
                    _fechar_malote(session, contexto, chave, bucket, contagem)
                    del buckets[chave]

        for chave, bucket in list(buckets.items()):
            if bucket.amostras:
                _fechar_malote(session, contexto, chave, bucket, contagem)

        _cancelar_algumas(session, contexto, abertas_para_cancelar, contagem)

    return contagem


def _planejar_jornadas(contexto: _Contexto, total: int) -> list[_Jornada]:
    """Distribui os atendimentos em dias de movimento por unidade."""
    jornadas: list[_Jornada] = []
    emitidos = 0

    while emitidos < total:
        dias_atras = _sortear_dias_atras()
        quantidade = min(random.randint(*_ATENDIMENTOS_POR_JORNADA), total - emitidos)
        jornadas.append(
            _Jornada(
                unidade=random.choice(contexto.unidades_coleta),
                instantes=sorted(momento(dias_atras) for _ in range(quantidade)),
            )
        )
        emitidos += quantidade

    jornadas.sort(key=lambda jornada: jornada.instantes[0])
    return jornadas


def _sortear_dias_atras() -> float:
    """Concentra parte do movimento nos últimos dias e espalha o resto no período."""
    if random.random() < _PROPORCAO_OPERACAO_CORRENTE:
        return random.uniform(0.2, _DIAS_OPERACAO_CORRENTE)
    return random.uniform(_DIAS_OPERACAO_CORRENTE, JANELA_DIAS)


def _sortear_estagio(t_abertura: datetime) -> str:
    """OS antiga já rodou o fluxo inteiro; só a recente fica no meio do caminho."""
    dias = (agora() - t_abertura).days
    pesos = _PESOS_ESTAGIO_CORRENTE if dias <= _DIAS_OPERACAO_CORRENTE else _PESOS_ESTAGIO_HISTORICO
    return random.choices(list(pesos), weights=list(pesos.values()))[0]


def _bucket_do_dia(
    session: Session,
    contexto: _Contexto,
    buckets: dict[tuple[UUID, str], _Bucket],
    chave: tuple[UUID, str],
    dia: date,
    contagem: dict[str, int],
) -> _Bucket:
    bucket = buckets.get(chave)
    if bucket is not None and bucket.dia == dia:
        return bucket

    if bucket is not None:
        _fechar_malote(session, contexto, chave, bucket, contagem)

    buckets[chave] = _Bucket(dia=dia)
    return buckets[chave]


def _montar_contexto(session: Session) -> _Contexto | None:
    pacientes = listar_pacientes(session)
    procedimentos = listar_procedimentos(session)
    unidades = listar_unidades_ativas(session)
    if not (pacientes and procedimentos and unidades):
        return None

    unidades_coleta = [u for u in unidades if u.tipo == "COLETA"] or unidades
    central = next((u for u in unidades if u.tipo == "CENTRAL"), unidades[0])

    return _Contexto(
        pacientes=pacientes,
        medicos=listar_medicos(session),
        convenios=listar_convenios(session),
        procedimentos=procedimentos,
        unidades_coleta=unidades_coleta,
        central=central,
        atendentes=_usuarios_do_perfil(session, "atendente"),
        coletores=_usuarios_do_perfil(session, "coletador"),
        recebedores=_usuarios_do_perfil(session, "tecnico_laboratorio"),
        admin=_usuario_admin(session),
        materiais={p.codigo_tuss: p.material for p in PROCEDIMENTOS},
    )


def _criar_ordem(
    session: Session,
    contexto: _Contexto,
    contagem: dict[str, int],
    t_abertura: datetime,
    unidade,
) -> tuple[UUID, str] | None:
    convenio = None if random.random() < _PROPORCAO_PARTICULAR else _escolher(contexto.convenios)
    medico = _escolher(contexto.medicos) if random.random() < 0.85 else None
    itens = random.sample(
        contexto.procedimentos,
        k=min(len(contexto.procedimentos), random.randint(*_EXAMES_POR_OS)),
    )

    dto = OrdemServicoCreate(
        paciente_id=random.choice(contexto.pacientes).id,
        unidade_id=unidade.id,
        medico_id=medico.id if medico else None,
        convenio_id=convenio.id if convenio else None,
        itens=[
            OsItemInput(
                procedimento_id=p.id,
                valor_negociado=None if convenio else _valor_particular(p.codigo_tuss),
            )
            for p in itens
        ],
    )

    solicitante = _escolher(contexto.atendentes) or contexto.admin
    try:
        ordem = abrir_os(session, dto, solicitante.id if solicitante else None)
    except Exception:
        return None

    contagem["ordens_servico"] += 1
    contagem["itens"] += len(itens)

    estagio = _sortear_estagio(t_abertura)

    # OS de convênio só avança com autorização válida; as que ficam em "aberta"
    # representam a fila de validação junto à operadora.
    if convenio is not None and estagio != "aberta":
        registrar_autorizacao(
            session,
            AutorizacaoCreate(
                ordem_servico_id=ordem.id,
                numero_guia=f"GUIA-{ordem.codigo_os[-6:]}",
                status=StatusAutorizacao.VALIDA,
            ),
        )

    _retrodatar_ordem(session, ordem.id, t_abertura)
    return ordem.id, estagio


def _coletar(
    session: Session, contexto: _Contexto, ordem_id: UUID, t_abertura: datetime
) -> tuple[UUID, datetime]:
    coletor = _escolher(contexto.coletores) or contexto.admin
    t_coleta = somar_horas(t_abertura, 0.3, 3)

    amostra = registrar_coleta(
        session,
        ColetaCreate(
            ordem_servico_id=ordem_id,
            tipo_material=_material_da_ordem(session, contexto, ordem_id),
            coletor_usuario_id=coletor.id,
        ),
    )

    _retrodatar_coleta(session, amostra.id, ordem_id, t_coleta)
    return amostra.id, t_coleta


def _fechar_malote(
    session: Session,
    contexto: _Contexto,
    chave: tuple[UUID, str],
    bucket: _Bucket,
    contagem: dict[str, int],
) -> None:
    unidade_id, modo = chave
    coletor = _escolher(contexto.coletores) or contexto.admin
    t_despacho = somar_horas(max(bucket.instantes), 1, 6)

    malote = criar_malote(
        session,
        MaloteCreate(
            unidade_origem_id=unidade_id,
            unidade_destino_id=contexto.central.id,
            enviado_por_usuario_id=coletor.id,
        ),
    )
    for amostra_id in bucket.amostras:
        adicionar_amostra_ao_malote(session, malote.id, amostra_id)
    despachar_malote(session, malote.id, coletor.id)
    _retrodatar_malote(session, malote.id, bucket.amostras, min(bucket.instantes), t_despacho)
    contagem["malotes"] += 1

    if modo != "recebida":
        return

    rejeitadas = {a for a in bucket.amostras if random.random() < _PROPORCAO_REJEITADAS}
    recebedor = _escolher(contexto.recebedores) or contexto.admin
    t_recebimento = somar_horas(t_despacho, 1, 5)

    receber_malote(
        session,
        ProtocoloRecebimentoCreate(
            malote_id=malote.id,
            recebido_por_usuario_id=recebedor.id,
            integridade_ok=not rejeitadas,
            amostras_rejeitadas=rejeitadas,
            observacao=random.choice(MOTIVOS_REJEICAO) if rejeitadas else "Amostras recebidas íntegras",
        ),
    )
    _retrodatar_recebimento(session, malote.id, bucket.amostras, t_recebimento)

    contagem["recebimentos"] += 1
    contagem["amostras_rejeitadas"] += len(rejeitadas)


def _cancelar_algumas(
    session: Session, contexto: _Contexto, candidatas: list[UUID], contagem: dict[str, int]
) -> None:
    """Cancela parte das OS que nunca saíram do estágio aberto."""
    if contexto.admin is None or not candidatas:
        return

    total = max(1, round(len(candidatas) * _PROPORCAO_ABERTAS_CANCELADAS))
    for ordem_id in random.sample(candidatas, k=min(len(candidatas), total)):
        try:
            cancelar_os(session, ordem_id, contexto.admin.id)
            contagem["ordens_canceladas"] += 1
        except Exception:
            continue


# --- Retrodatação dos marcos ---------------------------------------------


def _retrodatar_ordem(session: Session, ordem_id: UUID, instante: datetime) -> None:
    ordem = os_repository.obter_por_id(session, ordem_id)
    if ordem is not None:
        ordem.aberta_em = instante
    for historico in os_repository.listar_historico(session, ordem_id):
        historico.ocorrido_em = instante
    session.commit()


def _retrodatar_coleta(session: Session, amostra_id: UUID, ordem_id: UUID, instante: datetime) -> None:
    coleta = session.scalar(select(Coleta).where(Coleta.amostra_id == amostra_id))
    if coleta is not None:
        coleta.coletada_em = instante
    _retrodatar_movimentacoes(session, [amostra_id], "COLETADA", instante)
    _retrodatar_transicao(session, ordem_id, "COLETADA", instante)
    session.commit()


def _retrodatar_malote(
    session: Session, malote_id: UUID, amostras: list[UUID], criado: datetime, despachado: datetime
) -> None:
    malote = session.get(Malote, malote_id)
    if malote is not None:
        malote.criado_em = criado
        malote.despachado_em = despachado
    _retrodatar_movimentacoes(session, amostras, "EM_TRANSITO", despachado)
    session.commit()


def _retrodatar_recebimento(
    session: Session, malote_id: UUID, amostras: list[UUID], instante: datetime
) -> None:
    protocolo = session.scalar(
        select(ProtocoloRecebimento).where(ProtocoloRecebimento.malote_id == malote_id)
    )
    if protocolo is not None:
        protocolo.recebido_em = instante

    for status in ("RECEBIDA", "REJEITADA"):
        _retrodatar_movimentacoes(session, amostras, status, instante)

    # O recebimento leva a OS para EM_ANALISE — o histórico acompanha a data.
    ordens = session.scalars(select(Amostra.ordem_servico_id).where(Amostra.id.in_(amostras))).all()
    for ordem_id in set(ordens):
        _retrodatar_transicao(session, ordem_id, "EM_ANALISE", instante)

    session.commit()


def _retrodatar_movimentacoes(
    session: Session, amostras: list[UUID], status: str, instante: datetime
) -> None:
    movimentacoes = session.scalars(
        select(AmostraMovimentacao).where(
            AmostraMovimentacao.amostra_id.in_(amostras),
            AmostraMovimentacao.status == status,
        )
    ).all()
    for movimentacao in movimentacoes:
        movimentacao.ocorrido_em = instante


def _retrodatar_transicao(session: Session, ordem_id: UUID, status: str, instante: datetime) -> None:
    for historico in os_repository.listar_historico(session, ordem_id):
        if historico.status == status:
            historico.ocorrido_em = instante


# --- Auxiliares ------------------------------------------------------------


def _usuarios_do_perfil(session: Session, nome_perfil: str) -> list:
    from src.rbac.models import Perfil

    perfil = session.scalar(select(Perfil).where(Perfil.nome == nome_perfil))
    if perfil is None:
        return []
    return list(session.scalars(select(Usuario).where(Usuario.perfil_id == perfil.id, Usuario.ativo.is_(True))))


def _usuario_admin(session: Session) -> Usuario | None:
    admin = session.scalar(select(Usuario).where(Usuario.email == "seeder@labvida.com.br"))
    return admin or session.scalar(select(Usuario).limit(1))


def _escolher(itens: list):
    return random.choice(itens) if itens else None


def _material_da_ordem(session: Session, contexto: _Contexto, ordem_id: UUID) -> TipoMaterial:
    """Material coletado segue o primeiro procedimento da OS (sangue na maioria)."""
    itens = os_repository.listar_itens(session, ordem_id)
    for item in itens:
        procedimento = next((p for p in contexto.procedimentos if p.id == item.procedimento_id), None)
        if procedimento is None:
            continue
        material = contexto.materiais.get(procedimento.codigo_tuss)
        if material is not None:
            return material
    return TipoMaterial.SANGUE


def _valor_particular(codigo_tuss: str) -> Decimal:
    """Particular paga a tabela cheia, com um acréscimo de balcão."""
    base = next((p.valor_base for p in PROCEDIMENTOS if p.codigo_tuss == codigo_tuss), Decimal("50.00"))
    return (base * Decimal("1.35")).quantize(Decimal("0.01"))


def main() -> None:
    contagem = executar_seeder_atendimento()
    print("Seed de atendimento e logística finalizado")
    for chave, valor in contagem.items():
        print(f"{chave}: {valor}")


if __name__ == "__main__":
    main()
