"""Seed de Compras — fornecedores, insumos e pedidos (teste ponta a ponta)."""

from sqlalchemy.orm import Session

from src.compras.fornecedor import repository as fornecedor_repository
from src.compras.fornecedor.dtos import FornecedorCreate
from src.compras.fornecedor.service import criar_fornecedor
from src.compras.insumo import repository as insumo_repository
from src.compras.insumo.dtos import InsumoCreate
from src.compras.insumo.service import criar_insumo
from src.compras.pedido_compra import repository as pedido_repository
from src.compras.pedido_compra.dtos import PedidoItemCreate, SolicitacaoCreate
from src.compras.pedido_compra.service import aprovar_pedido, criar_solicitacao, receber_pedido
from src.db import session_scope
from src.usuario.repository import obter_por_email as obter_usuario


def executar_seeder_compras() -> dict[str, int]:
    contagem = {"fornecedores": 0, "insumos": 0, "pedidos": 0}

    with session_scope() as session:
        contagem["fornecedores"] = _seed_fornecedores(session)
        contagem["insumos"] = _seed_insumos(session)
        contagem["pedidos"] = _seed_pedidos(session)

    return contagem


def _seed_fornecedores(session: Session) -> int:
    existentes = fornecedor_repository.listar_todos(session)
    if existentes:
        return 0
    dados = [
        FornecedorCreate(nome="LabSupply Ltda", cnpj="11222333000181"),
        FornecedorCreate(nome="BioReagentes S.A.", cnpj="44555666000191"),
        FornecedorCreate(nome="MedInsumos Brasil", cnpj="77888999000101"),
    ]
    for dto in dados:
        criar_fornecedor(session, dto)
    session.flush()
    return len(dados)


def _seed_insumos(session: Session) -> int:
    existentes = insumo_repository.listar_insumos(session)
    if existentes:
        return 0
    dados = [
        InsumoCreate(nome="Reagente Hematologia", finalidade="Hemograma completo"),
        InsumoCreate(nome="Reagente Bioquímica", finalidade="Dosagem de glicose e colesterol"),
        InsumoCreate(nome="Tubo de Coleta EDTA", finalidade="Coleta de sangue para hematologia"),
        InsumoCreate(nome="Ponteira 100µL", finalidade="Pipetagem de amostras"),
        InsumoCreate(nome="Lâmina de Microscopia", finalidade="Análise microscópica"),
    ]
    for dto in dados:
        criar_insumo(session, dto)
    session.flush()
    return len(dados)


def _seed_pedidos(session: Session) -> int:
    existentes = pedido_repository.listar_pedidos(session)
    if existentes:
        return 0

    fornecedores = fornecedor_repository.listar_ativos(session)
    insumos = insumo_repository.listar_insumos(session)
    if len(fornecedores) < 1 or len(insumos) < 2:
        return 0

    usuario = obter_usuario(session, "seeder@labvida.com.br")
    if usuario is None:
        usuario = obter_usuario(session, "coletor@labvida.test")
    if usuario is None:
        return 0

    contagem = 0

    pedido1 = criar_solicitacao(
        session,
        SolicitacaoCreate(
            fornecedor_id=fornecedores[0].id,
            itens=[
                PedidoItemCreate(insumo_material_id=insumos[0].id, quantidade=10, valor_unitario=25.0),
                PedidoItemCreate(insumo_material_id=insumos[1].id, quantidade=5, valor_unitario=80.0),
            ],
        ),
        usuario.id,
    )
    aprovar_pedido(session, pedido1.id)
    contagem += 1

    pedido2 = criar_solicitacao(
        session,
        SolicitacaoCreate(
            fornecedor_id=fornecedores[0].id,
            itens=[
                PedidoItemCreate(insumo_material_id=insumos[2].id, quantidade=100, valor_unitario=1.50),
            ],
        ),
        usuario.id,
    )
    aprovar_pedido(session, pedido2.id)
    receber_pedido(session, pedido2.id)
    contagem += 1

    return contagem


def main() -> None:
    contagem = executar_seeder_compras()
    print("Seed compras finalizado")
    for chave, valor in contagem.items():
        print(f"{chave}: {valor}")


if __name__ == "__main__":
    main()
