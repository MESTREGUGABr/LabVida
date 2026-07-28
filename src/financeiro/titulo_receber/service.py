from uuid import UUID
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from src.auditoria import registrar_auditoria
from src.financeiro.conciliacao_pagamento.models import ConciliacaoPagamento
from src.financeiro.movimento_caixa.dtos import TipoMovimento
from src.financeiro.movimento_caixa.models import MovimentoCaixa
from src.financeiro.titulo_receber import repository
from src.financeiro.titulo_receber.dtos import StatusTitulo, TituloReceberRead
from src.financeiro.titulo_receber.errors import (
    TituloReceberJaBaixado,
    TituloReceberNaoEncontrado,
)


def obter_titulo(session: Session, titulo_id: UUID) -> TituloReceberRead:
    titulo = repository.obter_por_id(session, titulo_id)
    if titulo is None:
        raise TituloReceberNaoEncontrado("Título a receber não encontrado")
    return TituloReceberRead.model_validate(titulo)


def listar_todos(session: Session) -> list[TituloReceberRead]:
    return [TituloReceberRead.model_validate(t) for t in repository.listar_todos(session)]


def listar_pendentes(session: Session) -> list[TituloReceberRead]:
    return [TituloReceberRead.model_validate(t) for t in repository.listar_pendentes(session)]


def baixar_titulo(
    session: Session,
    titulo_id: UUID,
    valor_pago: float,
    observacao: str | None = None,
    usuario_id: UUID | None = None,
) -> TituloReceberRead:
    titulo = repository.obter_por_id(session, titulo_id)
    if titulo is None:
        raise TituloReceberNaoEncontrado("Título a receber não encontrado")
    if titulo.status != StatusTitulo.PENDENTE:
        raise TituloReceberJaBaixado("Título já foi baixado ou cancelado")

    if usuario_id is not None:
        from sqlalchemy import select
        from src.rbac.models import Perfil
        from src.rbac.repository import usuario_tem_permissao
        if session.scalar(select(Perfil.id).limit(1)) is not None:
            if not usuario_tem_permissao(session, usuario_id, "financeiro:baixar_titulo"):
                from src.financeiro.titulo_receber.errors import FinanceiroError
                raise FinanceiroError("Usuário sem permissão para baixar título")

    divergencia = titulo.valor - valor_pago

    titulo.status = StatusTitulo.PAGO

    movimento = MovimentoCaixa(
        titulo_receber_id=titulo.id,
        tipo=TipoMovimento.ENTRADA,
        valor=valor_pago,
        descricao=observacao or f"Recebimento do título {titulo.id}",
    )
    session.add(movimento)

    if divergencia > 0:
        conciliacao = ConciliacaoPagamento(
            titulo_receber_id=titulo.id,
            valor_recebido=valor_pago,
            divergencia=divergencia,
            observacao=f"Divergência de R$ {divergencia:.2f} — valor esperado: R$ {titulo.valor:.2f}",
        )
        session.add(conciliacao)

    if usuario_id is not None:
        registrar_auditoria(
            session,
            usuario_id,
            entidade="titulo_receber",
            entidade_id=titulo.id,
            acao="BAIXAR_TITULO_RECEBER",
            dados={"valor_pago": str(valor_pago), "divergencia": str(divergencia)},
        )

    session.commit()
    session.refresh(titulo)
    return TituloReceberRead.model_validate(titulo)
