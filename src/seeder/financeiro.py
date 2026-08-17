"""Seed de Financeiro — despesas fixas, baixas de título, caixa e conciliação.

Os títulos a receber vêm do fechamento de lote (Faturamento) e os a pagar da
aprovação de pedido (Compras); aqui entram as despesas fixas do laboratório e a
liquidação de parte dessa carteira. As baixas passam pelo service, então cada
uma gera movimento de caixa — e quando o convênio paga a menor, a conciliação
registra a divergência sozinha.

Idempotente: só insere se não houver movimento de caixa no banco.
"""

import random
from datetime import date, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.db import session_scope
from src.financeiro.conciliacao_pagamento.models import ConciliacaoPagamento
from src.financeiro.movimento_caixa.models import MovimentoCaixa
from src.financeiro.titulo_pagar import repository as tp_repository
from src.financeiro.titulo_pagar.dtos import StatusTitulo
from src.financeiro.titulo_pagar.models import TituloPagar
from src.financeiro.titulo_pagar.service import baixar_titulo as baixar_titulo_pagar
from src.financeiro.titulo_receber import repository as tr_repository
from src.financeiro.titulo_receber.service import baixar_titulo as baixar_titulo_receber
from src.seeder.catalogo import INICIO_OPERACAO_UNIDADES
from src.seeder.config import JANELA_DIAS, agora, qtd
from src.usuario.models import Usuario

# Despesas fixas mensais do laboratório (descrição, valor médio).
_DESPESAS_FIXAS = (
    ("Aluguel do laboratório central", 1800.00),
    ("Energia elétrica", 720.00),
    ("Água e esgoto", 180.00),
    ("Licença do sistema LIS", 340.00),
    ("Manutenção preventiva de equipamentos", 260.00),
    ("Coleta de resíduos de serviço de saúde", 190.00),
    ("Internet e telefonia", 150.00),
)

# Cada unidade de coleta inaugurada durante a série adiciona custo fixo
# próprio — a estrutura de custos cresce junto com a rede.
_DESPESAS_POR_UNIDADE = (
    ("Aluguel da unidade de coleta", 900.00),
    ("Energia elétrica da unidade de coleta", 260.00),
)

# Reajuste anual dos contratos de despesa fixa (~6% ao ano). Os valores da
# tabela são os de HOJE; meses mais antigos saem mais baratos.
_INFLACAO_ANUAL = 1.06

_PROPORCAO_RECEBER_BAIXADOS = 0.62
_PROPORCAO_PAGAR_BAIXADOS = 0.58
_PROPORCAO_PAGAMENTO_DIVERGENTE = 0.25


def executar_seeder_financeiro() -> dict[str, int]:
    contagem = {
        "titulos_pagar_fixos": 0,
        "titulos_receber_baixados": 0,
        "titulos_pagar_baixados": 0,
        "conciliacoes": 0,
    }

    with session_scope() as session:
        if session.execute(select(MovimentoCaixa).limit(1)).first() is not None:
            return contagem

        financeiro = _usuario_financeiro(session)
        contagem["titulos_pagar_fixos"] = _seed_despesas_fixas(session)
        contagem["titulos_receber_baixados"], contagem["conciliacoes"] = _baixar_receber(session, financeiro)
        contagem["titulos_pagar_baixados"] = _baixar_pagar(session, financeiro)

    return contagem


def _seed_despesas_fixas(session: Session) -> int:
    """Contas recorrentes que não nascem de pedido de compra.

    A tabela de título a pagar ainda não guarda descrição; o rótulo de
    `_DESPESAS_FIXAS` serve para dar ordem de grandeza realista a cada valor.
    A conta mensal cresce com a empresa: inflação anual sobre os valores e
    custos fixos adicionais quando uma unidade de coleta é inaugurada.
    """
    meses = max(1, qtd(JANELA_DIAS // 30))
    hoje = date.today()
    total = 0

    for indice in range(meses):
        vencimento = (hoje - timedelta(days=30 * indice)).replace(day=10)
        idade_empresa = (meses - 1 - indice) / 12  # 0 no primeiro mês da série
        inflacao = _INFLACAO_ANUAL ** idade_empresa
        unidades_extras = sum(
            1 for inicio in INICIO_OPERACAO_UNIDADES.values() if inicio <= vencimento
        )
        despesas = _DESPESAS_FIXAS + _DESPESAS_POR_UNIDADE * unidades_extras
        for _rotulo, valor in despesas:
            session.add(
                TituloPagar(
                    pedido_compra_id=None,
                    valor=round(valor * inflacao * random.uniform(0.9, 1.12), 2),
                    vencimento=vencimento,
                    status="PENDENTE",
                )
            )
            total += 1

    session.commit()
    return total


def _baixar_receber(session: Session, financeiro: Usuario | None) -> tuple[int, int]:
    """Liquida os títulos já vencidos; parte deles com pagamento a menor."""
    baixados = 0
    conciliacoes = 0
    limite = date.today()

    for titulo in tr_repository.listar_pendentes(session):
        if titulo.vencimento > limite:
            continue
        if random.random() >= _PROPORCAO_RECEBER_BAIXADOS:
            continue

        valor = float(titulo.valor)
        divergente = random.random() < _PROPORCAO_PAGAMENTO_DIVERGENTE
        valor_pago = round(valor * random.uniform(0.72, 0.96), 2) if divergente else valor
        t_pagamento = _instante_do_pagamento(titulo.vencimento)

        baixar_titulo_receber(
            session,
            titulo.id,
            valor_pago,
            observacao="Repasse do convênio conciliado no extrato",
            usuario_id=financeiro.id if financeiro else None,
        )
        _retrodatar_baixa(session, titulo_receber_id=titulo.id, instante=t_pagamento)

        baixados += 1
        if divergente:
            conciliacoes += 1

    return baixados, conciliacoes


def _baixar_pagar(session: Session, financeiro: Usuario | None) -> int:
    baixados = 0
    limite = date.today()

    for titulo in tp_repository.listar_todos(session):
        if titulo.status != StatusTitulo.PENDENTE or titulo.vencimento > limite:
            continue
        if random.random() >= _PROPORCAO_PAGAR_BAIXADOS:
            continue

        t_pagamento = _instante_do_pagamento(titulo.vencimento)
        baixar_titulo_pagar(
            session,
            titulo.id,
            observacao="Pagamento liquidado em conta corrente",
            usuario_id=financeiro.id if financeiro else None,
        )
        _retrodatar_baixa(session, titulo_pagar_id=titulo.id, instante=t_pagamento)
        baixados += 1

    return baixados


def _instante_do_pagamento(vencimento: date) -> datetime:
    """Paga entre 3 dias antes e 10 dias depois do vencimento, nunca no futuro."""
    momento_pagamento = datetime.combine(
        vencimento + timedelta(days=random.randint(-3, 10)),
        datetime.min.time(),
        tzinfo=agora().tzinfo,
    ) + timedelta(hours=random.randint(8, 17))
    return min(momento_pagamento, agora())


def _retrodatar_baixa(
    session: Session,
    instante: datetime,
    titulo_receber_id=None,
    titulo_pagar_id=None,
) -> None:
    if titulo_receber_id is not None:
        filtro = MovimentoCaixa.titulo_receber_id == titulo_receber_id
    else:
        filtro = MovimentoCaixa.titulo_pagar_id == titulo_pagar_id

    for movimento in session.scalars(select(MovimentoCaixa).where(filtro)):
        movimento.ocorrido_em = instante

    if titulo_receber_id is not None:
        for conciliacao in session.scalars(
            select(ConciliacaoPagamento).where(
                ConciliacaoPagamento.titulo_receber_id == titulo_receber_id
            )
        ):
            conciliacao.conciliado_em = instante

    session.commit()


def _usuario_financeiro(session: Session) -> Usuario | None:
    for email in ("financeiro@labvida.com.br", "seeder@labvida.com.br"):
        usuario = session.scalar(select(Usuario).where(Usuario.email == email))
        if usuario is not None:
            return usuario
    return None


def main() -> None:
    contagem = executar_seeder_financeiro()
    print("Seed financeiro finalizado")
    for chave, valor in contagem.items():
        print(f"{chave}: {valor}")


if __name__ == "__main__":
    main()
