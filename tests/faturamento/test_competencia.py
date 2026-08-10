"""Competencia como eixo de apuracao (fase F4).

Responde a dois apontamentos do professor: "colocar mes do faturamento" e
"por que lotes e nao periodos". A resposta e que competencia e o eixo; o lote e
so o envelope enviado ao convenio.
"""

from datetime import date, datetime, timedelta, timezone
from decimal import Decimal

import pytest
from sqlalchemy.orm import Session

from src.faturamento.competencia.errors import (
    CompetenciaAnteriorAberta,
    CompetenciaFechada,
    CompetenciaJaFechada,
    JustificativaObrigatoria,
)
from src.faturamento.competencia.service import (
    apurar,
    competencia_de,
    competencia_de_lancamento,
    exigir_aberta,
    fechar,
    obter_ou_criar,
    reabrir,
)
from src.faturamento.lote_faturamento.dtos import GuiaItemCreate, LoteFaturamentoCreate
from src.faturamento.lote_faturamento.service import adicionar_guia_item, criar_lote
from tests.faturamento._helpers import criar_laudo_liberado, montar_base

JANEIRO = date(2026, 1, 1)
FEVEREIRO = date(2026, 2, 1)


# ------------------------------------------------------------ fuso (ADR 0007)


def test_fuso_de_operacao_decide_o_mes() -> None:
    """O caso que o ADR 0007 existe para resolver.

    Um laudo liberado as 22h de 28/02 em Garanhuns e `2026-03-01T01:00Z`.
    Apurar em UTC jogaria essa receita para marco — mes errado para quem assina
    o balanco.
    """
    assert competencia_de(datetime(2026, 3, 1, 1, 0, tzinfo=timezone.utc)) == FEVEREIRO
    assert competencia_de(datetime(2026, 3, 15, 12, 0, tzinfo=timezone.utc)) == date(2026, 3, 1)


def test_instante_sem_fuso_e_tratado_como_utc() -> None:
    """Datetime ingenuo nao pode ser interpretado como hora local por acidente."""
    assert competencia_de(datetime(2026, 3, 1, 1, 0)) == FEVEREIRO


def test_competencia_e_sempre_o_primeiro_dia_do_mes(session: Session) -> None:
    registro = obter_ou_criar(session, date(2026, 5, 17))

    assert registro.competencia == date(2026, 5, 1)


# --------------------------------------------------------------- ciclo de vida


def test_competencia_nasce_aberta(session: Session) -> None:
    registro = obter_ou_criar(session, JANEIRO)

    assert registro.aberta is True
    assert registro.fechada_em is None


def test_fechar_congela_a_apuracao(session: Session) -> None:
    """O total do periodo tem que parar de mudar quando o gestor fecha — senao
    o numero que ele viu no fechamento nao e o que aparece depois."""
    base = montar_base(session, valor_tabela=Decimal("100.00"))
    laudo = criar_laudo_liberado(session, base)
    lote = criar_lote(session, LoteFaturamentoCreate(convenio_id=base.convenio_id))
    adicionar_guia_item(
        session,
        lote.id,
        GuiaItemCreate(
            laudo_id=laudo.id, procedimento_id=base.procedimento_id, valor_faturado=100.00
        ),
    )
    competencia = competencia_de(laudo.liberado_em)
    obter_ou_criar(session, competencia)
    session.commit()

    antes = apurar(session, competencia)
    assert antes.valor_faturado == Decimal("100.00")

    fechada = fechar(session, competencia, base.usuario_id)

    assert fechada.status == "FECHADA"
    assert fechada.fechada_em is not None
    assert fechada.valor_faturado == Decimal("100.00")
    # A apuracao de uma competencia fechada devolve o CONGELADO, nao um
    # recalculo que poderia divergir.
    assert apurar(session, competencia).valor_faturado == Decimal("100.00")


def test_nao_fecha_duas_vezes(session: Session) -> None:
    obter_ou_criar(session, JANEIRO)
    session.commit()
    fechar(session, JANEIRO)

    with pytest.raises(CompetenciaJaFechada):
        fechar(session, JANEIRO)


def test_nao_fecha_marco_com_fevereiro_aberto(session: Session) -> None:
    """Fechar fora de ordem permitiria lancar no mes anterior depois que o
    posterior ja congelou — o balanco nunca mais fecharia."""
    obter_ou_criar(session, JANEIRO)
    obter_ou_criar(session, FEVEREIRO)
    session.commit()

    with pytest.raises(CompetenciaAnteriorAberta, match="01/2026"):
        fechar(session, FEVEREIRO)


def test_competencia_fechada_barra_lancamento(session: Session) -> None:
    obter_ou_criar(session, JANEIRO)
    session.commit()
    fechar(session, JANEIRO)

    with pytest.raises(CompetenciaFechada):
        exigir_aberta(session, JANEIRO)


def test_reabrir_exige_justificativa(session: Session) -> None:
    """Reabertura desfaz um fechamento contabil: nao pode ser silenciosa."""
    obter_ou_criar(session, JANEIRO)
    session.commit()
    fechar(session, JANEIRO)

    with pytest.raises(JustificativaObrigatoria):
        reabrir(session, JANEIRO, justificativa="   ")

    reaberta = reabrir(session, JANEIRO, justificativa="Glosa retroativa do convenio")

    assert reaberta.aberta is True
    assert reaberta.reaberta_em is not None
    assert reaberta.justificativa == "Glosa retroativa do convenio"


# ------------------------------------------------------ lancamento retroativo


def test_lancamento_em_competencia_aberta_usa_a_propria(session: Session) -> None:
    instante = datetime(2026, 1, 15, 12, 0, tzinfo=timezone.utc)
    obter_ou_criar(session, JANEIRO)
    session.commit()

    efetiva, original = competencia_de_lancamento(session, instante)

    assert efetiva == JANEIRO
    assert original is None


def test_lancamento_retroativo_cai_na_corrente_e_guarda_a_original(session: Session) -> None:
    """Fechado e imutavel; retroativo e rastreavel. As duas coisas so cabem
    juntas se o desvio ficar registrado."""
    instante = datetime(2026, 1, 15, 12, 0, tzinfo=timezone.utc)
    obter_ou_criar(session, JANEIRO)
    session.commit()
    fechar(session, JANEIRO)

    efetiva, original = competencia_de_lancamento(session, instante)

    assert original == JANEIRO
    assert efetiva != JANEIRO
    assert efetiva == date.today().replace(day=1)


# ------------------------------------------------------------------ apuracao


def test_apuracao_conta_laudo_do_mes_do_fato_gerador(session: Session) -> None:
    """Competencia e carimbada no FATO GERADOR, nao no ato de faturar."""
    base = montar_base(session, valor_tabela=Decimal("100.00"))
    laudo = criar_laudo_liberado(session, base)
    competencia = competencia_de(laudo.liberado_em)

    apuracao = apurar(session, competencia)

    assert apuracao.qtd_laudos == 1
    # Ainda nao faturado: e exatamente o numero que o gestor precisa ver.
    assert apuracao.laudos_nao_faturados == 1
    assert apuracao.valor_faturado == Decimal("0")


def test_apuracao_calcula_liberado_e_taxa_de_glosa(session: Session) -> None:
    from src.faturamento.glosa.dtos import GlosaCreate
    from src.faturamento.glosa.service import registrar_glosa
    from src.faturamento.lote_faturamento import repository

    base = montar_base(session, valor_tabela=Decimal("200.00"))
    laudo = criar_laudo_liberado(session, base)
    lote = criar_lote(session, LoteFaturamentoCreate(convenio_id=base.convenio_id))
    adicionar_guia_item(
        session,
        lote.id,
        GuiaItemCreate(
            laudo_id=laudo.id, procedimento_id=base.procedimento_id, valor_faturado=200.00
        ),
    )
    item = repository.obter_lote_por_id(session, lote.id).guias[0].itens[0]
    registrar_glosa(
        session, GlosaCreate(guia_item_id=item.id, motivo="Sem senha", valor_glosado=50.00)
    )

    apuracao = apurar(session, competencia_de(laudo.liberado_em))

    assert apuracao.valor_faturado == Decimal("200.00")
    assert apuracao.valor_glosado == Decimal("50.00")
    assert apuracao.valor_liberado == Decimal("150.00")
    assert apuracao.taxa_glosa == pytest.approx(25.0)


def test_laudo_de_outro_mes_nao_entra_na_apuracao(session: Session) -> None:
    """A separacao por periodo so vale se ela realmente separar."""
    base = montar_base(session, valor_tabela=Decimal("100.00"))
    laudo = criar_laudo_liberado(session, base)
    competencia = competencia_de(laudo.liberado_em)

    mes_anterior = (competencia - timedelta(days=1)).replace(day=1)
    apuracao = apurar(session, mes_anterior)

    assert apuracao.qtd_laudos == 0
    assert apuracao.valor_faturado == Decimal("0")
