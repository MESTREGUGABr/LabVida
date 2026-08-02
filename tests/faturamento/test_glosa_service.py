import uuid
from decimal import Decimal

import pytest
from sqlalchemy.orm import Session

from src.atendimento.ordem_servico.dtos import StatusOrdemServico, StatusOsItem
from src.atendimento.ordem_servico.models import OrdemServico, OsItem
from src.faturamento.glosa.dtos import GlosaCreate
from src.laboratorial.models import Laudo, StatusLaudo
from src.faturamento.glosa.errors import ValorGlosaExcedeFaturado
from src.faturamento.glosa.service import (
    listar_glosas_com_contexto,
    listar_guias_itens_faturados,
    registrar_glosa,
)
from src.faturamento.lote_faturamento import repository
from src.faturamento.lote_faturamento.dtos import (
    GuiaItemCreate,
    LoteFaturamentoCreate,
    StatusGuiaItem,
)
from src.faturamento.lote_faturamento.service import adicionar_guia_item, criar_lote
from tests.faturamento._helpers import criar_laudo_liberado, montar_base


def _laudo_liberado_particular(session: Session, base, valor: Decimal) -> Laudo:
    """Laudo de OS sem convênio — o caso que o INNER JOIN fazia sumir."""
    ordem = OrdemServico(
        codigo_os=f"OS-PART-{uuid.uuid4().hex[:6].upper()}",
        paciente_id=base.paciente_id,
        convenio_id=None,
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


def test_glosas_cumulativas_nao_podem_exceder_o_faturado(session: Session) -> None:
    """Regressão N3: a validação compara o ACUMULADO, não cada glosa isolada.

    Antes, duas glosas de 60% passavam — nenhuma delas sozinha atingia o valor
    faturado — e o convênio glosava 120% de um item que continuava FATURADO.
    """
    item = _item_faturado(session, Decimal("100.00"))

    registrar_glosa(
        session,
        GlosaCreate(guia_item_id=item.id, motivo="Divergência de senha", valor_glosado=60.00),
    )

    with pytest.raises(ValorGlosaExcedeFaturado) as excecao:
        registrar_glosa(
            session,
            GlosaCreate(guia_item_id=item.id, motivo="Segunda glosa indevida", valor_glosado=60.00),
        )

    # A mensagem precisa dizer quanto ainda cabe, senão o faturista fica no escuro.
    assert "disponível" in str(excecao.value)
    assert item.status == StatusGuiaItem.FATURADO


def test_glosas_parciais_somando_o_total_fecham_o_item(session: Session) -> None:
    """Duas glosas de 50% fecham o item: o status olha o acumulado."""
    item = _item_faturado(session, Decimal("100.00"))

    registrar_glosa(
        session,
        GlosaCreate(guia_item_id=item.id, motivo="Primeira parcial", valor_glosado=50.00),
    )
    assert item.status == StatusGuiaItem.FATURADO

    registrar_glosa(
        session,
        GlosaCreate(guia_item_id=item.id, motivo="Segunda parcial", valor_glosado=50.00),
    )
    assert item.status == StatusGuiaItem.GLOSADO


def test_lote_particular_aparece_nas_telas_de_glosa(session: Session) -> None:
    """Regressão N7: `INNER JOIN Convenio` sumia com todo lote particular.

    Lote particular tem `convenio_id IS NULL`; com INNER JOIN ele não retornava
    em nenhuma das duas listagens, então glosa de particular era invisível na UI.
    """
    base = montar_base(session, valor_tabela=Decimal("80.00"))
    # OS particular: sem convênio na origem, senão `adicionar_guia_item` recusa o
    # item por divergência entre o convênio do laudo e o do lote.
    laudo = _laudo_liberado_particular(session, base, Decimal("80.00"))
    lote = criar_lote(session, LoteFaturamentoCreate(convenio_id=None))
    adicionar_guia_item(
        session,
        lote.id,
        GuiaItemCreate(
            laudo_id=laudo.id,
            procedimento_id=base.procedimento_id,
            valor_faturado=80.00,
        ),
    )

    faturados = listar_guias_itens_faturados(session)
    assert len(faturados) == 1
    assert faturados[0]["convenio_id"] is None
    assert faturados[0]["convenio_nome"] == "Particular"

    item = repository.obter_lote_por_id(session, lote.id).guias[0].itens[0]
    registrar_glosa(
        session,
        GlosaCreate(guia_item_id=item.id, motivo="Paciente contestou", valor_glosado=80.00),
    )

    glosas = listar_glosas_com_contexto(session)
    assert len(glosas) == 1
    assert glosas[0].convenio_nome == "Particular"
