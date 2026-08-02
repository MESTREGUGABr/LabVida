"""Regressão: o repositório de laudos pendentes não pode inventar valor.

`listar_laudos_liberados_por_convenio` trazia
`float(r.valor_negociado) if r.valor_negociado else 50.0`. Como
`os_itens.valor_negociado` é NOT NULL, o ramo do fallback nunca cobria NULL —
ele só reescrevia silenciosamente item de valor **zero** para R$ 50,00, criando
receita do nada na tela de faturamento.
"""

import uuid
from decimal import Decimal

from sqlalchemy.orm import Session

from src.atendimento.ordem_servico.dtos import StatusOrdemServico, StatusOsItem
from src.atendimento.ordem_servico.models import OrdemServico, OsItem
from src.faturamento.lote_faturamento.repository import (
    listar_laudos_liberados_por_convenio,
)
from src.laboratorial.models import Laudo, StatusLaudo
from tests.faturamento._helpers import Base, montar_base


def _laudo_liberado_com_valor(session: Session, base: Base, valor: Decimal) -> Laudo:
    ordem = OrdemServico(
        codigo_os=f"OS-TESTE-{uuid.uuid4().hex[:6].upper()}",
        paciente_id=base.paciente_id,
        convenio_id=base.convenio_id,
        unidade_id=base.unidade_id,
        status=StatusOrdemServico.EM_ANALISE,
    )
    session.add(ordem)
    session.flush()

    item = OsItem(
        ordem_servico_id=ordem.id,
        procedimento_id=base.procedimento_id,
        valor_negociado=valor,
        status=StatusOsItem.COLETADO,
    )
    session.add(item)
    session.flush()

    laudo = Laudo(os_item_id=item.id, status=StatusLaudo.LIBERADO)
    session.add(laudo)
    session.commit()
    return laudo


def test_valor_zero_nao_vira_cinquenta(session: Session) -> None:
    base = montar_base(session)
    _laudo_liberado_com_valor(session, base, Decimal("0.00"))

    pendentes = listar_laudos_liberados_por_convenio(session, base.convenio_id)

    assert len(pendentes) == 1
    assert pendentes[0]["valor_negociado"] == 0.0


def test_valor_real_e_preservado(session: Session) -> None:
    base = montar_base(session)
    _laudo_liberado_com_valor(session, base, Decimal("137.45"))

    pendentes = listar_laudos_liberados_por_convenio(session, base.convenio_id)

    assert len(pendentes) == 1
    assert pendentes[0]["valor_negociado"] == 137.45
