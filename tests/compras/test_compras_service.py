import pytest
from sqlalchemy.orm import Session

from src.compras.fornecedor.dtos import FornecedorCreate
from src.compras.fornecedor.errors import CnpjDuplicado
from src.compras.fornecedor.service import criar_fornecedor, listar_ativos
from src.compras.insumo.dtos import InsumoCreate
from src.compras.insumo.service import criar_insumo, listar_insumos
from src.compras.pedido_compra.dtos import PedidoItemCreate, SolicitacaoCreate
from src.compras.pedido_compra.errors import (
    PedidoError,
    PedidoNaoPodeSerAprovado,
    PedidoNaoPodeSerCancelado,
    PedidoNaoPodeSerRecebido,
    SolicitacaoSemItens,
)
from src.compras.pedido_compra.service import (
    aprovar_pedido,
    cancelar_pedido,
    criar_solicitacao,
    listar_pedidos,
    receber_pedido,
)
from src.usuario.service import sincronizar_usuario


def _montar_base(session: Session):
    fornecedor = criar_fornecedor(
        session, FornecedorCreate(nome="Fornecedor Teste", cnpj="11222333000181")
    )
    insumo = criar_insumo(
        session, InsumoCreate(nome="Insumo Teste", finalidade="Teste")
    )
    usuario = sincronizar_usuario(session, "teste@labvida.com", "Tester")
    return fornecedor.id, insumo.id, usuario.id


def test_criar_fornecedor(session: Session) -> None:
    f = criar_fornecedor(session, FornecedorCreate(nome="Teste", cnpj="11222333000181"))
    assert f.nome == "Teste"


def test_cnpj_duplicado(session: Session) -> None:
    criar_fornecedor(session, FornecedorCreate(nome="A", cnpj="11222333000181"))
    with pytest.raises(CnpjDuplicado):
        criar_fornecedor(session, FornecedorCreate(nome="B", cnpj="11222333000181"))


def test_criar_pedido(session: Session) -> None:
    forn_id, insumo_id, usuario_id = _montar_base(session)

    dto = SolicitacaoCreate(
        fornecedor_id=forn_id,
        itens=[PedidoItemCreate(insumo_material_id=insumo_id, quantidade=5, valor_unitario=10.0)],
    )
    pedido = criar_solicitacao(session, dto, usuario_id)
    assert pedido.valor_total == 50.0
    assert len(pedido.itens) == 1


def test_criar_pedido_sem_itens(session: Session) -> None:
    forn_id, _, usuario_id = _montar_base(session)
    dto = SolicitacaoCreate(fornecedor_id=forn_id, itens=[])
    with pytest.raises(SolicitacaoSemItens):
        criar_solicitacao(session, dto, usuario_id)


def test_aprovar_pedido_gera_titulo(session: Session) -> None:
    forn_id, insumo_id, usuario_id = _montar_base(session)

    dto = SolicitacaoCreate(
        fornecedor_id=forn_id,
        itens=[PedidoItemCreate(insumo_material_id=insumo_id, quantidade=2, valor_unitario=25.0)],
    )
    pedido = criar_solicitacao(session, dto, usuario_id)

    aprovado = aprovar_pedido(session, pedido.id)
    assert aprovado.status == "APROVADO"


def test_nao_pode_aprovar_duas_vezes(session: Session) -> None:
    forn_id, insumo_id, usuario_id = _montar_base(session)
    dto = SolicitacaoCreate(
        fornecedor_id=forn_id,
        itens=[PedidoItemCreate(insumo_material_id=insumo_id, quantidade=1, valor_unitario=10.0)],
    )
    pedido = criar_solicitacao(session, dto, usuario_id)
    aprovar_pedido(session, pedido.id)

    with pytest.raises(PedidoNaoPodeSerAprovado):
        aprovar_pedido(session, pedido.id)


def test_receber_pedido_atualiza_estoque(session: Session) -> None:
    forn_id, insumo_id, usuario_id = _montar_base(session)

    dto = SolicitacaoCreate(
        fornecedor_id=forn_id,
        itens=[PedidoItemCreate(insumo_material_id=insumo_id, quantidade=10, valor_unitario=5.0)],
    )
    pedido = criar_solicitacao(session, dto, usuario_id)
    aprovar_pedido(session, pedido.id)

    recebido = receber_pedido(session, pedido.id)
    assert recebido.status == "RECEBIDO"

    insumos = listar_insumos(session)
    assert insumos[0].quantidade_estoque == 10.0


def test_cancelar_pedido_rascunho(session: Session) -> None:
    forn_id, insumo_id, usuario_id = _montar_base(session)
    dto = SolicitacaoCreate(
        fornecedor_id=forn_id,
        itens=[PedidoItemCreate(insumo_material_id=insumo_id, quantidade=1, valor_unitario=10.0)],
    )
    pedido = criar_solicitacao(session, dto, usuario_id)

    cancelado = cancelar_pedido(session, pedido.id)
    assert cancelado.status == "CANCELADO"


def test_nao_pode_cancelar_aprovado(session: Session) -> None:
    forn_id, insumo_id, usuario_id = _montar_base(session)
    dto = SolicitacaoCreate(
        fornecedor_id=forn_id,
        itens=[PedidoItemCreate(insumo_material_id=insumo_id, quantidade=1, valor_unitario=10.0)],
    )
    pedido = criar_solicitacao(session, dto, usuario_id)
    aprovar_pedido(session, pedido.id)

    with pytest.raises(PedidoNaoPodeSerCancelado):
        cancelar_pedido(session, pedido.id)


def test_criar_solicitacao_rejeita_sem_permissao(session: Session) -> None:
    from src.rbac.models import Perfil
    from src.usuario.service import sincronizar_usuario as sync

    forn_id, insumo_id, _ = _montar_base(session)

    perfil = Perfil(nome="compras_test", descricao="Sem compras")
    session.add(perfil)
    session.flush()

    usuario_sem = sync(session, "semcompras@labvida.test", "Sem Compras")
    usuario_sem.perfil_id = perfil.id
    session.flush()

    dto = SolicitacaoCreate(
        fornecedor_id=forn_id,
        itens=[PedidoItemCreate(insumo_material_id=insumo_id, quantidade=1, valor_unitario=10.0)],
    )

    with pytest.raises(PedidoError, match="sem permissão"):
        criar_solicitacao(session, dto, usuario_sem.id)

    session.query(Perfil).filter_by(id=perfil.id).delete()
    session.flush()
