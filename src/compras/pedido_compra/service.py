from datetime import date, timedelta
from uuid import UUID

from sqlalchemy.orm import Session

from src.compras.fornecedor import repository as fornecedor_repository
from src.compras.fornecedor.dtos import StatusFornecedor
from src.compras.fornecedor.errors import FornecedorInativo, FornecedorNaoEncontrado
from src.compras.insumo import repository as insumo_repository
from src.compras.insumo.dtos import TipoMovimentoEstoque
from src.compras.insumo.errors import InsumoNaoEncontrado
from src.compras.insumo.models import EstoqueMovimento
from src.compras.pedido_compra import repository
from src.compras.pedido_compra.dtos import (
    PedidoCompraRead,
    PedidoItemRead,
    SolicitacaoCreate,
    StatusPedido,
)
from src.compras.pedido_compra.errors import (
    FornecedorInvalidoParaPedido,
    PedidoNaoEncontrado,
    PedidoNaoPodeSerAprovado,
    PedidoNaoPodeSerCancelado,
    PedidoNaoPodeSerRecebido,
    SolicitacaoSemItens,
)
from src.compras.pedido_compra.models import (
    PedidoCompra,
    PedidoItem,
    RecebimentoInsumo,
    SolicitacaoCompra,
)
from src.financeiro.titulo_pagar.models import TituloPagar


def criar_solicitacao(session: Session, dto: SolicitacaoCreate, usuario_id: UUID) -> PedidoCompraRead:
    if not dto.itens:
        raise SolicitacaoSemItens("Pedido deve conter ao menos um item")

    fornecedor = fornecedor_repository.obter_por_id(session, dto.fornecedor_id)
    if fornecedor is None:
        raise FornecedorNaoEncontrado("Fornecedor não encontrado")
    if fornecedor.status != StatusFornecedor.ATIVO:
        raise FornecedorInvalidoParaPedido("Fornecedor não está ativo")

    solicitacao = SolicitacaoCompra(solicitante_id=usuario_id)
    repository.salvar_solicitacao(session, solicitacao)
    session.flush()

    pedido = PedidoCompra(
        solicitacao_compra_id=solicitacao.id,
        fornecedor_id=dto.fornecedor_id,
        status=StatusPedido.RASCUNHO,
    )
    repository.salvar_pedido(session, pedido)
    session.flush()

    valor_total = 0.0
    for item_dto in dto.itens:
        if item_dto.quantidade <= 0 or item_dto.valor_unitario <= 0:
            raise SolicitacaoSemItens("Quantidade e valor unitário devem ser maiores que zero")
        insumo = insumo_repository.obter_insumo_por_id(session, item_dto.insumo_material_id)
        if insumo is None:
            raise InsumoNaoEncontrado(f"Insumo {item_dto.insumo_material_id} não encontrado")
        item = PedidoItem(
            pedido_compra_id=pedido.id,
            insumo_material_id=item_dto.insumo_material_id,
            quantidade=item_dto.quantidade,
            valor_unitario=item_dto.valor_unitario,
        )
        repository.salvar_item(session, item)
        valor_total += item_dto.quantidade * item_dto.valor_unitario

    pedido.valor_total = valor_total
    session.commit()
    session.refresh(pedido)
    return PedidoCompraRead.model_validate(pedido)


def aprovar_pedido(session: Session, pedido_id: UUID) -> PedidoCompraRead:
    pedido = repository.obter_pedido_por_id(session, pedido_id)
    if pedido is None:
        raise PedidoNaoEncontrado("Pedido não encontrado")
    if pedido.status != StatusPedido.RASCUNHO:
        raise PedidoNaoPodeSerAprovado("Apenas pedidos em RASCUNHO podem ser aprovados")

    pedido.status = StatusPedido.APROVADO

    titulo = TituloPagar(
        pedido_compra_id=pedido.id,
        valor=pedido.valor_total,
        vencimento=date.today() + timedelta(days=30),
        status="PENDENTE",
    )
    session.add(titulo)

    session.commit()
    session.refresh(pedido)
    return PedidoCompraRead.model_validate(pedido)


def receber_pedido(session: Session, pedido_id: UUID) -> PedidoCompraRead:
    pedido = repository.obter_pedido_por_id(session, pedido_id)
    if pedido is None:
        raise PedidoNaoEncontrado("Pedido não encontrado")
    if pedido.status != StatusPedido.APROVADO:
        raise PedidoNaoPodeSerRecebido("Apenas pedidos APROVADOS podem ser recebidos")

    pedido.status = StatusPedido.RECEBIDO

    recebimento = RecebimentoInsumo(pedido_compra_id=pedido.id, conferido=True)
    repository.salvar_recebimento(session, recebimento)

    for item in pedido.itens:
        insumo = insumo_repository.obter_insumo_por_id(session, item.insumo_material_id)
        if insumo is not None:
            insumo.quantidade_estoque += item.quantidade
            mov = EstoqueMovimento(
                insumo_material_id=insumo.id,
                tipo=TipoMovimentoEstoque.ENTRADA,
                quantidade=item.quantidade,
                observacao=f"Recebimento do pedido {pedido.id}",
            )
            insumo_repository.salvar_movimento(session, mov)

    session.commit()
    session.refresh(pedido)
    return PedidoCompraRead.model_validate(pedido)


def cancelar_pedido(session: Session, pedido_id: UUID) -> PedidoCompraRead:
    pedido = repository.obter_pedido_por_id(session, pedido_id)
    if pedido is None:
        raise PedidoNaoEncontrado("Pedido não encontrado")
    if pedido.status != StatusPedido.RASCUNHO:
        raise PedidoNaoPodeSerCancelado("Apenas pedidos em RASCUNHO podem ser cancelados")

    pedido.status = StatusPedido.CANCELADO
    session.commit()
    session.refresh(pedido)
    return PedidoCompraRead.model_validate(pedido)


def obter_pedido(session: Session, pedido_id: UUID) -> PedidoCompraRead:
    pedido = repository.obter_pedido_por_id(session, pedido_id)
    if pedido is None:
        raise PedidoNaoEncontrado("Pedido não encontrado")
    return PedidoCompraRead.model_validate(pedido)


def listar_pedidos(session: Session) -> list[PedidoCompraRead]:
    return [PedidoCompraRead.model_validate(p) for p in repository.listar_pedidos(session)]
