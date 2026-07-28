"""Seed de Faturamento — lotes, guias TISS, itens faturados e glosas.

Fatura os laudos liberados agrupando-os por convênio em lotes mensais, fecha a
maior parte deles (o que dispara a pré-auditoria e gera o título a receber) e
deixa alguns abertos para a tela ter o que fechar. Sobre os lotes fechados
aplica glosas parciais e totais, com os motivos que os convênios usam de fato.

Idempotente: só insere se não houver lotes no banco.
"""

import random
from datetime import datetime, timedelta
from decimal import ROUND_DOWN, Decimal
from uuid import UUID

from sqlalchemy.orm import Session

from src.cadastro.convenio.repository import listar_ativos as listar_convenios
from src.db import session_scope
from src.faturamento.glosa.dtos import GlosaCreate
from src.faturamento.glosa.service import registrar_glosa
from src.faturamento.lote_faturamento import repository
from src.faturamento.lote_faturamento.dtos import GuiaItemCreate, LoteFaturamentoCreate
from src.faturamento.lote_faturamento.service import (
    adicionar_itens_ao_lote,
    criar_lote,
    fechar_lote,
)
from src.faturamento.lote_faturamento.models import LoteFaturamento
from src.financeiro.titulo_receber.models import TituloReceber
from src.seeder.catalogo import MOTIVOS_GLOSA
from src.seeder.config import agora, somar_horas
from src.usuario.models import Usuario

_LAUDOS_POR_LOTE = (8, 18)
_PROPORCAO_LOTES_FECHADOS = 0.7
_PROPORCAO_ITENS_GLOSADOS = 0.12
_PRAZO_PAGAMENTO_DIAS = 30


def executar_seeder_faturamento() -> dict[str, int]:
    contagem = {"lotes": 0, "lotes_fechados": 0, "guias_itens": 0, "glosas": 0}

    with session_scope() as session:
        if repository.listar_lotes(session):
            return contagem

        faturista = _faturista(session)
        convenios_ids: list[UUID | None] = [c.id for c in listar_convenios(session)]
        convenios_ids.append(None)  # OS particular também é faturada, em lote próprio

        for convenio_id in convenios_ids:
            laudos = repository.listar_laudos_liberados_por_convenio(session, convenio_id)
            if not laudos:
                continue

            laudos.sort(key=lambda item: item["liberado_em"] or agora())
            for bloco in _blocos(laudos):
                _faturar_bloco(session, convenio_id, bloco, faturista, contagem)

    return contagem


def _blocos(laudos: list[dict]) -> list[list[dict]]:
    blocos = []
    inicio = 0
    while inicio < len(laudos):
        tamanho = random.randint(*_LAUDOS_POR_LOTE)
        blocos.append(laudos[inicio : inicio + tamanho])
        inicio += tamanho
    return blocos


def _faturar_bloco(
    session: Session,
    convenio_id: UUID | None,
    bloco: list[dict],
    faturista: Usuario | None,
    contagem: dict[str, int],
) -> None:
    lote = criar_lote(session, LoteFaturamentoCreate(convenio_id=convenio_id))
    adicionar_itens_ao_lote(
        session,
        lote.id,
        [
            GuiaItemCreate(
                laudo_id=item["laudo_id"],
                procedimento_id=item["procedimento_id"],
                valor_faturado=item["valor_negociado"],
            )
            for item in bloco
        ],
    )

    contagem["lotes"] += 1
    contagem["guias_itens"] += len(bloco)

    ultimo_laudo = max((item["liberado_em"] for item in bloco if item["liberado_em"]), default=agora())
    t_criacao = somar_horas(ultimo_laudo, 2, 24)

    if random.random() >= _PROPORCAO_LOTES_FECHADOS:
        _retrodatar_lote(session, lote.id, t_criacao, None)
        return

    t_fechamento = somar_horas(t_criacao, 12, 72)
    fechar_lote(session, lote.id, faturista.id if faturista else None)
    _retrodatar_lote(session, lote.id, t_criacao, t_fechamento)
    contagem["lotes_fechados"] += 1

    contagem["glosas"] += _glosar(session, lote.id, faturista)


def _glosar(session: Session, lote_id: UUID, faturista: Usuario | None) -> int:
    """Convênio recusa parte do lote: glosa parcial (revisável) ou total."""
    lote = repository.obter_lote_por_id(session, lote_id)
    if lote is None:
        return 0

    total = 0
    for guia in lote.guias:
        for item in guia.itens:
            if random.random() >= _PROPORCAO_ITENS_GLOSADOS:
                continue
            proporcao = Decimal(random.choice(["0.3", "0.5", "1.0"]))
            valor_glosado = (Decimal(str(item.valor_faturado)) * proporcao).quantize(
                Decimal("0.01"), rounding=ROUND_DOWN
            )
            registrar_glosa(
                session,
                GlosaCreate(
                    guia_item_id=item.id,
                    motivo=random.choice(MOTIVOS_GLOSA),
                    valor_glosado=float(valor_glosado),
                ),
                faturista.id if faturista else None,
            )
            total += 1
    return total


def _retrodatar_lote(
    session: Session, lote_id: UUID, criado: datetime, fechado: datetime | None
) -> None:
    """Alinha lote, guias e título a receber à data real do faturamento."""
    lote = session.get(LoteFaturamento, lote_id)
    if lote is None:
        return

    lote.criado_em = criado
    for guia in lote.guias:
        guia.criado_em = criado
        for item in guia.itens:
            item.criado_em = criado

    if fechado is not None:
        lote.fechado_em = fechado
        titulo = session.query(TituloReceber).filter(TituloReceber.lote_faturamento_id == lote.id).first()
        if titulo is not None:
            titulo.criado_em = fechado
            titulo.vencimento = (fechado + timedelta(days=_PRAZO_PAGAMENTO_DIAS)).date()

    session.commit()


def _faturista(session: Session) -> Usuario | None:
    return session.query(Usuario).filter(Usuario.email == "faturamento@labvida.com.br").first()


def main() -> None:
    contagem = executar_seeder_faturamento()
    print("Seed faturamento finalizado")
    for chave, valor in contagem.items():
        print(f"{chave}: {valor}")


if __name__ == "__main__":
    main()
