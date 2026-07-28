from decimal import Decimal

import pytest
from sqlalchemy.orm import Session

from src.faturamento.glosa.dtos import GlosaCreate
from src.faturamento.glosa.errors import ValorGlosaExcedeFaturado
from src.faturamento.glosa.service import registrar_glosa
from src.faturamento.lote_faturamento import repository
from src.faturamento.lote_faturamento.dtos import (
    GuiaItemCreate,
    LoteFaturamentoCreate,
    StatusGuiaItem,
)
from src.faturamento.lote_faturamento.service import adicionar_guia_item, criar_lote
from tests.faturamento._helpers import criar_laudo_liberado, montar_base


def _item_faturado(session: Session, valor: Decimal):
    base = montar_base(session, valor_tabela=valor)
    laudo = criar_laudo_liberado(session, base)
    lote = criar_lote(session, LoteFaturamentoCreate(convenio_id=base.convenio_id))
    adicionar_guia_item(
        session,
        lote.id,
        GuiaItemCreate(
            laudo_id=laudo.id,
            procedimento_id=base.procedimento_id,
            valor_faturado=float(valor),
        ),
    )
    return repository.obter_lote_por_id(session, lote.id).guias[0].itens[0]


def test_glosa_integral_de_valor_quebrado(session: Session) -> None:
    """Glosa do valor cheio é o padrão da tela e não pode ser recusada.

    Regressão: 30.87 não tem representação binária exata, então comparar o float
    do DTO com o Decimal da coluna reprovava a glosa integral.
    """
    item = _item_faturado(session, Decimal("30.87"))

    glosa = registrar_glosa(
        session,
        GlosaCreate(guia_item_id=item.id, motivo="Procedimento não coberto", valor_glosado=30.87),
    )

    assert Decimal(str(glosa.valor_glosado)) == Decimal("30.87")
    assert item.status == StatusGuiaItem.GLOSADO


def test_glosa_parcial_mantem_item_faturado(session: Session) -> None:
    item = _item_faturado(session, Decimal("30.87"))

    registrar_glosa(
        session,
        GlosaCreate(guia_item_id=item.id, motivo="Valor acima da tabela", valor_glosado=10.00),
    )

    assert item.status != StatusGuiaItem.GLOSADO


def test_glosa_acima_do_faturado_e_recusada(session: Session) -> None:
    item = _item_faturado(session, Decimal("30.87"))

    with pytest.raises(ValorGlosaExcedeFaturado):
        registrar_glosa(
            session,
            GlosaCreate(guia_item_id=item.id, motivo="Cobrança em duplicidade", valor_glosado=30.88),
        )
