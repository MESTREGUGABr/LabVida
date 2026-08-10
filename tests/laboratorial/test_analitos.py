"""Catalogo de analitos e faixa de referencia aplicavel (fase F3).

O que estes testes protegem: a faixa de referencia deixou de ser dado morto.
Antes, `Resultado.analito` e `ValorReferencia.analito` eram duas strings livres
sem FK entre si — a bancada digitava "Hemoglobina", a faixa estava cadastrada
como "hemoglobina", e nenhum codigo casava as duas.
"""

from collections.abc import Iterator
from datetime import date
from decimal import Decimal

import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.cadastro.procedimento.dtos import ProcedimentoCreate
from src.cadastro.procedimento.service import criar_procedimento
from src.db import session_scope
from src.laboratorial.analito_service import (
    avaliar_resultado,
    codigo_de,
    idade_em,
    listar_analitos_do_procedimento,
    obter_faixa_referencia,
    obter_ou_criar_analito,
    para_numero,
    vincular_ao_procedimento,
)
from src.laboratorial.models import ValorReferencia

_TABELAS = (
    "resultados_auditoria", "resultados", "valores_referencia",
    "procedimento_analitos", "analitos",
    "laudos", "os_itens", "ordens_servico", "procedimento_valores", "procedimentos",
)


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
def hemograma(session: Session):
    return criar_procedimento(
        session, ProcedimentoCreate(codigo_tuss="40302016", nome="Hemograma")
    )


def _faixa(session: Session, procedimento_id, analito_id, **campos) -> ValorReferencia:
    faixa = ValorReferencia(
        procedimento_id=procedimento_id,
        analito_id=analito_id,
        analito=campos.pop("analito", "Hemoglobina"),
        **campos,
    )
    session.add(faixa)
    session.commit()
    return faixa


# ------------------------------------------------------------------ catalogo


def test_variacoes_do_mesmo_nome_viram_um_analito_so(session: Session) -> None:
    """O bug que o catalogo existe para matar."""
    primeiro = obter_ou_criar_analito(session, "Hemoglobina")
    segundo = obter_ou_criar_analito(session, "  hemoglobina  ")
    terceiro = obter_ou_criar_analito(session, "HEMOGLOBINA")

    assert primeiro.id == segundo.id == terceiro.id
    assert primeiro.nome == "Hemoglobina"  # mantem a grafia do primeiro cadastro


def test_codigo_e_deterministico_e_sem_acento_de_digitacao(session: Session) -> None:
    assert codigo_de("Hemoglobina") == codigo_de("hemoglobina ")
    assert codigo_de("Volume Corpuscular Medio") == "VOLUMECORPUSCULARMEDIO"


def test_analitos_diferentes_nao_colidem(session: Session) -> None:
    hemoglobina = obter_ou_criar_analito(session, "Hemoglobina")
    hematocrito = obter_ou_criar_analito(session, "Hematocrito")

    assert hemoglobina.id != hematocrito.id


def test_painel_lista_os_analitos_do_exame(session: Session, hemograma) -> None:
    """Sem isso a bancada nao sabe o que digitar para o exame."""
    for ordem, nome in enumerate(["Hemoglobina", "Hematocrito", "Leucocitos"], start=1):
        analito = obter_ou_criar_analito(session, nome)
        vincular_ao_procedimento(session, hemograma.id, analito.id, ordem=ordem)
    session.commit()

    painel = listar_analitos_do_procedimento(session, hemograma.id)

    assert [a.nome for a in painel] == ["Hemoglobina", "Hematocrito", "Leucocitos"]


def test_vincular_duas_vezes_nao_duplica(session: Session, hemograma) -> None:
    analito = obter_ou_criar_analito(session, "Hemoglobina")
    vincular_ao_procedimento(session, hemograma.id, analito.id)
    vincular_ao_procedimento(session, hemograma.id, analito.id)
    session.commit()

    assert len(listar_analitos_do_procedimento(session, hemograma.id)) == 1


# ------------------------------------------------------- faixa de referencia


def test_faixa_especifica_ganha_da_generica(session: Session, hemograma) -> None:
    """Hemoglobina normal de homem adulto nao e a de crianca."""
    analito = obter_ou_criar_analito(session, "Hemoglobina")
    _faixa(session, hemograma.id, analito.id, minimo=12, maximo=16)  # generica
    _faixa(session, hemograma.id, analito.id, minimo=13, maximo=17, sexo="MASCULINO")

    faixa = obter_faixa_referencia(session, hemograma.id, analito.id, sexo="MASCULINO")

    assert faixa.sexo == "MASCULINO"
    assert faixa.minimo == 13


def test_faixa_de_outro_sexo_nunca_e_devolvida(session: Session, hemograma) -> None:
    """Devolver a faixa errada e pior do que nao devolver nada: parece certo."""
    analito = obter_ou_criar_analito(session, "Hemoglobina")
    _faixa(session, hemograma.id, analito.id, minimo=13, maximo=17, sexo="MASCULINO")

    assert obter_faixa_referencia(session, hemograma.id, analito.id, sexo="FEMININO") is None


def test_faixa_por_idade(session: Session, hemograma) -> None:
    analito = obter_ou_criar_analito(session, "Hemoglobina")
    _faixa(session, hemograma.id, analito.id, minimo=11, maximo=14, idade_min=0, idade_max=12)
    _faixa(session, hemograma.id, analito.id, minimo=13, maximo=17, idade_min=13, idade_max=120)

    crianca = obter_faixa_referencia(session, hemograma.id, analito.id, idade=8)
    adulto = obter_faixa_referencia(session, hemograma.id, analito.id, idade=30)

    assert crianca.maximo == 14
    assert adulto.maximo == 17


def test_idade_em_calcula_com_aniversario_nao_feito(session: Session) -> None:
    assert idade_em(date(2000, 12, 31), date(2026, 6, 15)) == 25
    assert idade_em(date(2000, 1, 1), date(2026, 6, 15)) == 26
    assert idade_em(None) is None


# ------------------------------------------------------ avaliacao do resultado


def test_resultado_dentro_da_faixa_e_normal(session: Session, hemograma) -> None:
    analito = obter_ou_criar_analito(session, "Hemoglobina")
    _faixa(session, hemograma.id, analito.id, minimo=13, maximo=17)

    avaliacao = avaliar_resultado(
        session, procedimento_id=hemograma.id, analito_id=analito.id, valor="14.5"
    )

    assert avaliacao.situacao == "NORMAL"
    assert avaliacao.alterado is False
    assert avaliacao.valor_numerico == Decimal("14.5")


def test_resultado_fora_da_faixa_e_marcado(session: Session, hemograma) -> None:
    """O laudo poder marcar resultado ALTERADO e o ganho clinico da fase."""
    analito = obter_ou_criar_analito(session, "Hemoglobina")
    _faixa(session, hemograma.id, analito.id, minimo=13, maximo=17)

    baixo = avaliar_resultado(
        session, procedimento_id=hemograma.id, analito_id=analito.id, valor="9,2"
    )
    alto = avaliar_resultado(
        session, procedimento_id=hemograma.id, analito_id=analito.id, valor="21"
    )

    assert baixo.situacao == "BAIXO" and baixo.alterado
    assert alto.situacao == "ALTO" and alto.alterado
    # Aceita virgula: e assim que o tecnico digita.
    assert baixo.valor_numerico == Decimal("9.2")


def test_resultado_qualitativo_nao_vira_normal_por_omissao(session: Session, hemograma) -> None:
    """"Nao Reagente" nao e numero. Dizer que esta normal sem ter com o que
    comparar seria pior do que admitir que nao da para avaliar."""
    analito = obter_ou_criar_analito(session, "VDRL")
    _faixa(session, hemograma.id, analito.id, valor_esperado_texto="Nao Reagente")

    avaliacao = avaliar_resultado(
        session, procedimento_id=hemograma.id, analito_id=analito.id, valor="Nao Reagente"
    )

    assert avaliacao.situacao == "NAO_AVALIAVEL"
    assert avaliacao.alterado is False


def test_sem_faixa_cadastrada_nao_avalia(session: Session, hemograma) -> None:
    analito = obter_ou_criar_analito(session, "Hemoglobina")

    avaliacao = avaliar_resultado(
        session, procedimento_id=hemograma.id, analito_id=analito.id, valor="14.5"
    )

    assert avaliacao.situacao == "NAO_AVALIAVEL"


def test_analito_fora_do_catalogo_nao_avalia(session: Session, hemograma) -> None:
    avaliacao = avaliar_resultado(
        session, procedimento_id=hemograma.id, analito_id=None, valor="14.5"
    )

    assert avaliacao.situacao == "NAO_AVALIAVEL"


def test_para_numero_aceita_virgula_e_recusa_texto() -> None:
    assert para_numero("1234,56") == Decimal("1234.56")
    assert para_numero(" 42 ") == Decimal("42")
    assert para_numero("Nao Reagente") is None
    assert para_numero("") is None
    assert para_numero(None) is None
