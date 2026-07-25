import pytest
from sqlalchemy.orm import Session

from src.faturamento.lote_faturamento.dtos import LoteFaturamentoCreate, StatusLote
from src.faturamento.lote_faturamento.errors import (
    ConvenioInvalidoParaLote,
    LoteNaoEncontrado,
    LoteSemItens,
)
from src.faturamento.lote_faturamento.service import (
    criar_lote,
    fechar_lote,
    listar_lotes,
    obter_lote,
)
from tests.faturamento._helpers import montar_base


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
