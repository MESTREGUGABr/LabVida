from decimal import Decimal

import pytest
from sqlalchemy.orm import Session

from src.faturamento.lote_faturamento.dtos import (
    GuiaItemCreate,
    LoteFaturamentoCreate,
    StatusLote,
)
from src.faturamento.lote_faturamento.errors import (
    ConvenioInvalidoParaLote,
    LoteNaoEncontrado,
    LoteSemItens,
)
from src.faturamento.lote_faturamento.service import (
    adicionar_guia_item,
    adicionar_itens_ao_lote,
    criar_lote,
    fechar_lote,
    listar_lotes,
    obter_lote,
)
from tests.faturamento._helpers import criar_laudo_liberado, montar_base


def test_criar_lote(session: Session) -> None:
    base = montar_base(session)

    lote_dto = LoteFaturamentoCreate(convenio_id=base.convenio_id)
    lote = criar_lote(session, lote_dto)

    assert lote.status == StatusLote.ABERTO
    assert lote.valor_total == 0
    assert lote.codigo_lote.startswith("LT-")


def test_criar_lote_convenio_invalido(session: Session) -> None:
    from uuid import uuid4
    dto = LoteFaturamentoCreate(convenio_id=uuid4())

    with pytest.raises(ConvenioInvalidoParaLote):
        criar_lote(session, dto)


def test_fechar_lote_sem_itens_gera_erro(session: Session) -> None:
    base = montar_base(session)

    lote = criar_lote(session, LoteFaturamentoCreate(convenio_id=base.convenio_id))

    with pytest.raises(LoteSemItens):
        fechar_lote(session, lote.id, base.usuario_id)


def test_listar_lotes(session: Session) -> None:
    base = montar_base(session)

    criar_lote(session, LoteFaturamentoCreate(convenio_id=base.convenio_id))
    criar_lote(session, LoteFaturamentoCreate(convenio_id=base.convenio_id))

    lotes = listar_lotes(session)
    assert len(lotes) == 2


def test_obter_lote_inexistente_gera_erro(session: Session) -> None:
    from uuid import uuid4

    with pytest.raises(LoteNaoEncontrado):
        obter_lote(session, uuid4())


def test_adicionar_item_soma_no_valor_total(session: Session) -> None:
    base = montar_base(session)
    laudo = criar_laudo_liberado(session, base)
    lote = criar_lote(session, LoteFaturamentoCreate(convenio_id=base.convenio_id))

    atualizado = adicionar_guia_item(
        session,
        lote.id,
        GuiaItemCreate(
            laudo_id=laudo.id,
            procedimento_id=base.procedimento_id,
            valor_faturado=float(base.valor_tabela),
        ),
    )

    assert Decimal(str(atualizado.valor_total)) == base.valor_tabela


def test_adicionar_itens_em_lote_acumula_valor_total(session: Session) -> None:
    base = montar_base(session)
    laudos = [criar_laudo_liberado(session, base) for _ in range(3)]
    lote = criar_lote(session, LoteFaturamentoCreate(convenio_id=base.convenio_id))

    atualizado = adicionar_itens_ao_lote(
        session,
        lote.id,
        [
            GuiaItemCreate(
                laudo_id=laudo.id,
                procedimento_id=base.procedimento_id,
                valor_faturado=float(base.valor_tabela),
            )
            for laudo in laudos
        ],
    )

    assert Decimal(str(atualizado.valor_total)) == base.valor_tabela * 3
