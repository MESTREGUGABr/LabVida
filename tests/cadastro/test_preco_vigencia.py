"""Preco particular e vigencia com fim (fase F3).

Duas coisas que nao existiam antes e que a tabela de precos precisava para ser
fonte da verdade:

1. **Preco particular.** `convenio_id` era NOT NULL, entao nao havia tabela de
   balcao — o valor do particular era digitado a mao na abertura da OS, sem
   governanca e sem historico.
2. **Fim de vigencia.** Sem ele, inserir um preco retroativo mudava
   silenciosamente o resultado de consultas historicas, e nao havia como
   encerrar nem corrigir um preco.
"""

from collections.abc import Iterator
from datetime import date, timedelta
from decimal import Decimal

import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.db import session_scope

from src.cadastro.convenio.dtos import ConvenioCreate
from src.cadastro.convenio.service import criar_convenio
from src.cadastro.procedimento.dtos import ProcedimentoCreate, ProcedimentoValorCreate
from src.cadastro.procedimento.models import ProcedimentoValor
from src.cadastro.procedimento.service import (
    criar_procedimento,
    definir_valor,
    obter_valor_vigente,
)

ONTEM = date.today() - timedelta(days=1)
HOJE = date.today()
AMANHA = date.today() + timedelta(days=1)


_TABELAS = ("procedimento_valores", "procedimentos", "convenios")


@pytest.fixture()
def session() -> Iterator[Session]:
    with session_scope() as sessao:
        sessao.execute(text("TRUNCATE " + ", ".join(_TABELAS) + " RESTART IDENTITY CASCADE"))
        sessao.commit()
        yield sessao
        sessao.rollback()
        sessao.execute(text("TRUNCATE " + ", ".join(_TABELAS) + " RESTART IDENTITY CASCADE"))
        sessao.commit()


@pytest.fixture()
def procedimento(session: Session):
    return criar_procedimento(
        session, ProcedimentoCreate(codigo_tuss="40302016", nome="Hemograma")
    )


@pytest.fixture()
def convenio(session: Session):
    return criar_convenio(session, ConvenioCreate(nome="Unimed Preco"))


def test_preco_particular_dispensa_convenio(session: Session, procedimento) -> None:
    """`convenio_id=None` e a tabela de balcao — antes era impossivel."""
    definir_valor(
        session,
        ProcedimentoValorCreate(
            procedimento_id=procedimento.id,
            convenio_id=None,
            valor=Decimal("80.00"),
            vigencia_inicio=ONTEM,
        ),
    )

    assert obter_valor_vigente(session, procedimento.id, None) == Decimal("80.00")


def test_particular_e_convenio_sao_tabelas_independentes(
    session: Session, procedimento, convenio
) -> None:
    definir_valor(session, ProcedimentoValorCreate(
        procedimento_id=procedimento.id, convenio_id=None,
        valor=Decimal("100.00"), vigencia_inicio=ONTEM,
    ))
    definir_valor(session, ProcedimentoValorCreate(
        procedimento_id=procedimento.id, convenio_id=convenio.id,
        valor=Decimal("60.00"), vigencia_inicio=ONTEM,
    ))

    assert obter_valor_vigente(session, procedimento.id, None) == Decimal("100.00")
    assert obter_valor_vigente(session, procedimento.id, convenio.id) == Decimal("60.00")


def test_novo_preco_encerra_a_vigencia_anterior(session: Session, procedimento, convenio) -> None:
    """Sem encerrar a anterior, o EXCLUDE do banco rejeitaria a insercao — e
    estaria certo: duas faixas sobrepostas sao dois precos validos na mesma data."""
    antigo = date.today() - timedelta(days=30)
    definir_valor(session, ProcedimentoValorCreate(
        procedimento_id=procedimento.id, convenio_id=convenio.id,
        valor=Decimal("50.00"), vigencia_inicio=antigo,
    ))
    definir_valor(session, ProcedimentoValorCreate(
        procedimento_id=procedimento.id, convenio_id=convenio.id,
        valor=Decimal("75.00"), vigencia_inicio=HOJE,
    ))

    precos = session.query(ProcedimentoValor).order_by(ProcedimentoValor.vigencia_inicio).all()
    assert len(precos) == 2
    assert precos[0].vigencia_fim == HOJE - timedelta(days=1)
    assert precos[1].vigencia_fim is None


def test_consulta_historica_devolve_o_preco_da_epoca(
    session: Session, procedimento, convenio
) -> None:
    """O ponto do fim de vigencia: preco novo nao reescreve o passado."""
    antigo = date.today() - timedelta(days=30)
    definir_valor(session, ProcedimentoValorCreate(
        procedimento_id=procedimento.id, convenio_id=convenio.id,
        valor=Decimal("50.00"), vigencia_inicio=antigo,
    ))
    definir_valor(session, ProcedimentoValorCreate(
        procedimento_id=procedimento.id, convenio_id=convenio.id,
        valor=Decimal("75.00"), vigencia_inicio=HOJE,
    ))

    assert obter_valor_vigente(session, procedimento.id, convenio.id, antigo) == Decimal("50.00")
    assert obter_valor_vigente(session, procedimento.id, convenio.id, HOJE) == Decimal("75.00")


def test_preco_retroativo_e_recusado(session: Session, procedimento, convenio) -> None:
    """Vigencia nova nao pode comecar antes da que esta aberta."""
    definir_valor(session, ProcedimentoValorCreate(
        procedimento_id=procedimento.id, convenio_id=convenio.id,
        valor=Decimal("50.00"), vigencia_inicio=HOJE,
    ))

    with pytest.raises(ValueError, match="precisa comecar depois"):
        definir_valor(session, ProcedimentoValorCreate(
            procedimento_id=procedimento.id, convenio_id=convenio.id,
            valor=Decimal("60.00"), vigencia_inicio=ONTEM,
        ))


def test_banco_recusa_vigencias_sobrepostas(session: Session, procedimento, convenio) -> None:
    """A garantia nao pode depender so do service.

    Escrita direta na tabela, contornando `definir_valor`, tem que esbarrar no
    `EXCLUDE ... USING gist` da migration 0015.
    """
    session.add(ProcedimentoValor(
        procedimento_id=procedimento.id, convenio_id=convenio.id,
        valor=Decimal("50.00"), vigencia_inicio=ONTEM, vigencia_fim=None,
    ))
    session.commit()

    session.add(ProcedimentoValor(
        procedimento_id=procedimento.id, convenio_id=convenio.id,
        valor=Decimal("70.00"), vigencia_inicio=HOJE, vigencia_fim=None,
    ))
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()


def test_banco_recusa_sobreposicao_no_particular(session: Session, procedimento) -> None:
    """O caso que um unique comum NAO pega: em SQL `NULL <> NULL`, entao sem
    `NULLS NOT DISTINCT` e sem o COALESCE do EXCLUDE o particular duplicaria."""
    session.add(ProcedimentoValor(
        procedimento_id=procedimento.id, convenio_id=None,
        valor=Decimal("90.00"), vigencia_inicio=ONTEM, vigencia_fim=None,
    ))
    session.commit()

    session.add(ProcedimentoValor(
        procedimento_id=procedimento.id, convenio_id=None,
        valor=Decimal("95.00"), vigencia_inicio=HOJE, vigencia_fim=None,
    ))
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()


def test_sem_preco_cadastrado_devolve_none(session: Session, procedimento) -> None:
    assert obter_valor_vigente(session, procedimento.id, None) is None


def test_preco_futuro_nao_vale_hoje(session: Session, procedimento, convenio) -> None:
    definir_valor(session, ProcedimentoValorCreate(
        procedimento_id=procedimento.id, convenio_id=convenio.id,
        valor=Decimal("120.00"), vigencia_inicio=AMANHA,
    ))

    assert obter_valor_vigente(session, procedimento.id, convenio.id, HOJE) is None
    assert obter_valor_vigente(session, procedimento.id, convenio.id, AMANHA) == Decimal("120.00")
