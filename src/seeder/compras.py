"""Seed de Compras — fornecedores, insumos, pedidos e movimentação de estoque.

Percorre o ciclo inteiro respeitando a segregação de funções: quem solicita não
é quem aprova, e quem aprova não é quem dá entrada no almoxarifado. Os pedidos
ficam distribuídos entre rascunho, aprovado, recebido e cancelado, e o estoque
recebe tanto as entradas dos recebimentos quanto as saídas de consumo da
bancada — sem isso o saldo ficaria só subindo.
"""

import random
from datetime import datetime, timedelta
from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session

from src.compras.fornecedor import repository as fornecedor_repository
from src.compras.fornecedor.dtos import FornecedorCreate
from src.compras.fornecedor.service import criar_fornecedor
from src.compras.insumo import repository as insumo_repository
from src.compras.insumo.dtos import InsumoCreate, TipoMovimentoEstoque
from src.compras.insumo.models import EstoqueMovimento
from src.compras.insumo.service import criar_insumo
from src.compras.pedido_compra import repository as pedido_repository
from src.compras.pedido_compra.dtos import PedidoItemCreate, SolicitacaoCreate
from src.compras.pedido_compra.models import PedidoCompra, RecebimentoInsumo, SolicitacaoCompra
from src.compras.pedido_compra.service import (
    aprovar_pedido,
    cancelar_pedido,
    criar_solicitacao,
    receber_pedido,
)
from src.db import session_scope
from src.financeiro.titulo_pagar.models import TituloPagar
from src.seeder.catalogo import FORNECEDORES, INSUMOS
from src.seeder.config import JANELA_DIAS, momento, qtd
from src.seeder.documentos import gerar_cnpj
from src.usuario.models import Usuario
from src.usuario.repository import obter_por_email as obter_usuario

PEDIDOS_PADRAO = 28

# Situação dos pedidos ao final do período (soma 1.0).
_PESOS_STATUS = {
    "recebido": 0.55,   # ciclo completo: entrada no estoque + título a pagar
    "aprovado": 0.22,   # aguardando entrega do fornecedor
    "rascunho": 0.15,   # solicitação aguardando aprovação
    "cancelado": 0.08,
}
_PRAZO_PAGAMENTO_DIAS = 30
_CONSUMOS_POR_INSUMO = (4, 10)
# Estoque inicial generoso (multiplo do pedido tipico) e minimo bem mais baixo
# — margem grande o suficiente pra sobreviver ao consumo simulado sem disparar
# o alerta de estoque baixo por acaso (ver pages/compras_estoque.py).
_ESTOQUE_INICIAL_FATOR = (4.0, 8.0)
_ESTOQUE_MINIMO_FATOR = (0.3, 0.6)


def executar_seeder_compras() -> dict[str, int]:
    contagem = {
        "fornecedores": 0,
        "insumos": 0,
        "pedidos": 0,
        "pedidos_recebidos": 0,
        "movimentos_estoque": 0,
    }

    with session_scope() as session:
        contagem["fornecedores"] = _seed_fornecedores(session)
        contagem["insumos"] = _seed_insumos(session)
        pedidos, recebidos = _seed_pedidos(session)
        contagem["pedidos"] = pedidos
        contagem["pedidos_recebidos"] = recebidos
        contagem["movimentos_estoque"] = _seed_consumo(session)

    return contagem


def _seed_fornecedores(session: Session) -> int:
    if fornecedor_repository.listar_todos(session):
        return 0

    cnpjs_usados: set[str] = set()
    nomes = FORNECEDORES[: qtd(len(FORNECEDORES))]
    for nome in nomes:
        criar_fornecedor(session, FornecedorCreate(nome=nome, cnpj=gerar_cnpj(cnpjs_usados)))
    session.flush()
    return len(nomes)


def _seed_insumos(session: Session) -> int:
    if insumo_repository.listar_insumos(session):
        return 0

    itens = INSUMOS[: qtd(len(INSUMOS))]
    for nome, finalidade, _valor, quantidade_tipica in itens:
        criar_insumo(
            session,
            InsumoCreate(
                nome=nome,
                finalidade=finalidade,
                quantidade_estoque=round(quantidade_tipica * random.uniform(*_ESTOQUE_INICIAL_FATOR), 3),
                estoque_minimo=round(quantidade_tipica * random.uniform(*_ESTOQUE_MINIMO_FATOR), 3),
            ),
        )
    session.flush()
    return len(itens)


def _seed_pedidos(session: Session) -> tuple[int, int]:
    if pedido_repository.listar_pedidos(session):
        return 0, 0

    fornecedores = fornecedor_repository.listar_ativos(session)
    insumos = insumo_repository.listar_insumos(session)
    solicitante = _solicitante(session)
    if not fornecedores or len(insumos) < 2 or solicitante is None:
        return 0, 0

    tabela = {nome: (valor, quantidade) for nome, _f, valor, quantidade in INSUMOS}
    criados = 0
    recebidos = 0

    for _ in range(qtd(PEDIDOS_PADRAO)):
        t_pedido = momento(random.uniform(2, JANELA_DIAS))
        itens = random.sample(insumos, k=min(len(insumos), random.randint(1, 3)))

        pedido = criar_solicitacao(
            session,
            SolicitacaoCreate(
                fornecedor_id=random.choice(fornecedores).id,
                itens=[_item_do_pedido(insumo, tabela) for insumo in itens],
            ),
            solicitante.id,
        )
        criados += 1

        status = random.choices(list(_PESOS_STATUS), weights=list(_PESOS_STATUS.values()))[0]
        if status == "cancelado":
            cancelar_pedido(session, pedido.id)
            _retrodatar_pedido(session, pedido.id, t_pedido, None)
            continue
        if status == "rascunho":
            _retrodatar_pedido(session, pedido.id, t_pedido, None)
            continue

        aprovar_pedido(session, pedido.id)
        t_entrega = None

        if status == "recebido":
            receber_pedido(session, pedido.id)
            t_entrega = t_pedido + timedelta(days=random.randint(2, 12))
            recebidos += 1

        _retrodatar_pedido(session, pedido.id, t_pedido, t_entrega)

    return criados, recebidos


def _item_do_pedido(insumo, tabela: dict) -> PedidoItemCreate:
    """Quantidade e preço vêm do catálogo, com a variação normal de negociação."""
    valor_base, quantidade_tipica = tabela.get(insumo.nome, (Decimal("25.00"), 10))
    return PedidoItemCreate(
        insumo_material_id=insumo.id,
        quantidade=max(1, round(quantidade_tipica * random.uniform(0.7, 1.3))),
        valor_unitario=float((valor_base * Decimal(str(round(random.uniform(0.92, 1.12), 2)))).quantize(Decimal("0.01"))),
    )


def _seed_consumo(session: Session) -> int:
    """Baixa de estoque pelo uso na bancada — o contrapeso das entradas."""
    movimentos = 0

    for insumo in insumo_repository.listar_insumos(session):
        saldo = float(insumo.quantidade_estoque or 0)
        if saldo <= 0:
            continue

        for _ in range(random.randint(*_CONSUMOS_POR_INSUMO)):
            if saldo <= 1:
                break
            quantidade = round(min(saldo * random.uniform(0.05, 0.25), saldo - 1), 3)
            if quantidade <= 0:
                break

            session.add(
                EstoqueMovimento(
                    insumo_material_id=insumo.id,
                    tipo=TipoMovimentoEstoque.SAIDA,
                    quantidade=quantidade,
                    ocorrido_em=momento(random.uniform(1, JANELA_DIAS / 2)),
                    observacao="Consumo na bancada",
                )
            )
            saldo -= quantidade
            movimentos += 1

        insumo.quantidade_estoque = round(saldo, 3)

    session.commit()
    return movimentos


def _retrodatar_pedido(
    session: Session, pedido_id: UUID, criado: datetime, recebido: datetime | None
) -> None:
    """Alinha pedido, solicitação, recebimento, estoque e título a pagar à data real."""
    pedido = session.get(PedidoCompra, pedido_id)
    if pedido is None:
        return

    pedido.criado_em = criado
    solicitacao = session.get(SolicitacaoCompra, pedido.solicitacao_compra_id)
    if solicitacao is not None:
        solicitacao.criada_em = criado

    titulo = session.query(TituloPagar).filter(TituloPagar.pedido_compra_id == pedido.id).first()
    if titulo is not None:
        titulo.criado_em = criado
        titulo.vencimento = (criado + timedelta(days=_PRAZO_PAGAMENTO_DIAS)).date()

    if recebido is not None:
        recebimento = (
            session.query(RecebimentoInsumo).filter(RecebimentoInsumo.pedido_compra_id == pedido.id).first()
        )
        if recebimento is not None:
            recebimento.recebido_em = recebido
        for movimento in session.query(EstoqueMovimento).filter(
            EstoqueMovimento.observacao == f"Recebimento do pedido {pedido.id}"
        ):
            movimento.ocorrido_em = recebido

    session.commit()


def _solicitante(session: Session) -> Usuario | None:
    for email in ("compras@labvida.com.br", "seeder@labvida.com.br"):
        usuario = obter_usuario(session, email)
        if usuario is not None:
            return usuario
    return None


def main() -> None:
    contagem = executar_seeder_compras()
    print("Seed compras finalizado")
    for chave, valor in contagem.items():
        print(f"{chave}: {valor}")


if __name__ == "__main__":
    main()
