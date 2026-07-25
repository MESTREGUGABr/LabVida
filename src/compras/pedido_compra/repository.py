from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.compras.pedido_compra.models import PedidoCompra, PedidoItem, RecebimentoInsumo, SolicitacaoCompra


def salvar_solicitacao(session: Session, sol: SolicitacaoCompra) -> SolicitacaoCompra:
    session.add(sol)
    return sol


def obter_solicitacao(session: Session, sol_id: UUID) -> SolicitacaoCompra | None:
    return session.get(SolicitacaoCompra, sol_id)


def salvar_pedido(session: Session, pedido: PedidoCompra) -> PedidoCompra:
    session.add(pedido)
    return pedido


def salvar_item(session: Session, item: PedidoItem) -> PedidoItem:
    session.add(item)
    return item


def obter_pedido_por_id(session: Session, pedido_id: UUID) -> PedidoCompra | None:
    return session.get(PedidoCompra, pedido_id)


def listar_pedidos(session: Session) -> list[PedidoCompra]:
    stmt = select(PedidoCompra).order_by(PedidoCompra.criado_em.desc())
    return list(session.scalars(stmt).all())


def listar_pedidos_rascunho(session: Session) -> list[PedidoCompra]:
    stmt = select(PedidoCompra).where(PedidoCompra.status == "RASCUNHO").order_by(PedidoCompra.criado_em.desc())
    return list(session.scalars(stmt).all())


def salvar_recebimento(session: Session, rec: RecebimentoInsumo) -> RecebimentoInsumo:
    session.add(rec)
    return rec
