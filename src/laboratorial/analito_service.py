"""Catalogo de analitos e faixa de referencia aplicavel (fase F3).

O ganho concreto: a bancada passa a saber a faixa de referencia do que acabou de
digitar, e o laudo pode marcar resultado ALTERADO.

Antes isso era impossivel. `Resultado.analito` e `ValorReferencia.analito` eram
duas strings livres sem FK entre si — "Hemoglobina" e "hemoglobina" eram coisas
diferentes para o banco, e nenhum codigo tentava casar as duas.
"""

from __future__ import annotations

import re
import uuid
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from src.laboratorial.models import Analito, ProcedimentoAnalito, ValorReferencia

_NAO_ALFANUMERICO = re.compile(r"[^a-zA-Z0-9]")
_ESPACOS = re.compile(r"\s+")


def normalizar_nome(nome: str) -> str:
    """Chave de comparacao entre as duas pontas. Mesma regra do backfill."""
    return _ESPACOS.sub(" ", (nome or "").strip()).lower()


def codigo_de(nome: str) -> str:
    """Codigo interno deterministico — a chave natural do catalogo."""
    return _NAO_ALFANUMERICO.sub("", normalizar_nome(nome)).upper()[:30]


def obter_ou_criar_analito(
    session: Session, nome: str, *, unidade_medida: str | None = None
) -> Analito:
    """Analito pelo nome, criando se ainda nao existir.

    A busca e pelo CODIGO normalizado, nao pelo nome digitado: e o que impede
    "Hemoglobina" e "hemoglobina " de virarem duas linhas.
    """
    if not (nome or "").strip():
        raise ValueError("Nome do analito nao pode ser vazio")

    codigo = codigo_de(nome)
    analito = session.scalar(select(Analito).where(Analito.codigo == codigo))
    if analito is not None:
        return analito

    analito = Analito(
        id=uuid.uuid4(),
        codigo=codigo,
        nome=nome.strip(),
        unidade_medida=unidade_medida,
    )
    session.add(analito)
    session.flush()
    return analito


def vincular_ao_procedimento(
    session: Session, procedimento_id: uuid.UUID, analito_id: uuid.UUID, ordem: int = 1
) -> None:
    """Monta o painel do exame. Hemograma e um painel de analitos."""
    ja_existe = session.get(ProcedimentoAnalito, (procedimento_id, analito_id))
    if ja_existe is not None:
        return
    session.add(
        ProcedimentoAnalito(procedimento_id=procedimento_id, analito_id=analito_id, ordem=ordem)
    )
    session.flush()


def listar_analitos_do_procedimento(session: Session, procedimento_id: uuid.UUID) -> list[Analito]:
    """O que a bancada precisa digitar para este exame."""
    return list(
        session.scalars(
            select(Analito)
            .join(ProcedimentoAnalito, ProcedimentoAnalito.analito_id == Analito.id)
            .where(ProcedimentoAnalito.procedimento_id == procedimento_id)
            .order_by(ProcedimentoAnalito.ordem, Analito.nome)
        ).all()
    )


def idade_em(nascimento: date | None, referencia: date | None = None) -> int | None:
    if nascimento is None:
        return None
    hoje = referencia or date.today()
    return hoje.year - nascimento.year - (
        (hoje.month, hoje.day) < (nascimento.month, nascimento.day)
    )


def obter_faixa_referencia(
    session: Session,
    procedimento_id: uuid.UUID,
    analito_id: uuid.UUID,
    *,
    sexo: str | None = None,
    idade: int | None = None,
) -> ValorReferencia | None:
    """Faixa aplicavel ao paciente.

    Prefere a faixa MAIS ESPECIFICA que serve: uma cadastrada para o sexo e a
    idade do paciente ganha de uma generica. Faixa de outro sexo ou de outra
    idade nunca e devolvida — devolver a generica nesses casos seria pior do que
    nao devolver nada, porque parece certo.
    """
    consulta = select(ValorReferencia).where(
        ValorReferencia.procedimento_id == procedimento_id,
        ValorReferencia.analito_id == analito_id,
    )

    if sexo is not None:
        consulta = consulta.where(
            or_(ValorReferencia.sexo.is_(None), ValorReferencia.sexo == sexo)
        )
    else:
        consulta = consulta.where(ValorReferencia.sexo.is_(None))

    if idade is not None:
        consulta = consulta.where(
            or_(ValorReferencia.idade_min.is_(None), ValorReferencia.idade_min <= idade),
            or_(ValorReferencia.idade_max.is_(None), ValorReferencia.idade_max >= idade),
        )
    else:
        consulta = consulta.where(
            ValorReferencia.idade_min.is_(None), ValorReferencia.idade_max.is_(None)
        )

    faixas = list(session.scalars(consulta).all())
    if not faixas:
        return None

    def especificidade(faixa: ValorReferencia) -> int:
        pontos = 0
        if faixa.sexo is not None:
            pontos += 2
        if faixa.idade_min is not None or faixa.idade_max is not None:
            pontos += 1
        return pontos

    return max(faixas, key=especificidade)


def para_numero(valor: str | None) -> Decimal | None:
    """Converte o texto do resultado em numero quando ele for numerico.

    Exame qualitativo ("Nao Reagente") continua so no texto — e o correto, nao
    uma limitacao.
    """
    if valor is None:
        return None
    texto = str(valor).strip().replace(",", ".")
    if not texto:
        return None
    try:
        return Decimal(texto)
    except (InvalidOperation, ValueError):
        return None


@dataclass(frozen=True)
class AvaliacaoResultado:
    """Como o resultado se posiciona frente a faixa de referencia."""

    situacao: str  # NORMAL | BAIXO | ALTO | NAO_AVALIAVEL
    faixa: ValorReferencia | None
    valor_numerico: Decimal | None

    @property
    def alterado(self) -> bool:
        return self.situacao in ("BAIXO", "ALTO")


def avaliar_resultado(
    session: Session,
    *,
    procedimento_id: uuid.UUID,
    analito_id: uuid.UUID | None,
    valor: str | None,
    sexo: str | None = None,
    idade: int | None = None,
) -> AvaliacaoResultado:
    """Compara o resultado com a faixa aplicavel.

    `NAO_AVALIAVEL` cobre tres casos honestos: analito sem catalogo, resultado
    qualitativo e faixa nao cadastrada. Nenhum deles pode virar "normal" por
    omissao — dizer que esta normal sem ter com o que comparar seria pior do que
    admitir que nao da para avaliar.
    """
    numero = para_numero(valor)
    if analito_id is None or numero is None:
        return AvaliacaoResultado("NAO_AVALIAVEL", None, numero)

    faixa = obter_faixa_referencia(
        session, procedimento_id, analito_id, sexo=sexo, idade=idade
    )
    if faixa is None or (faixa.minimo is None and faixa.maximo is None):
        return AvaliacaoResultado("NAO_AVALIAVEL", faixa, numero)

    if faixa.minimo is not None and numero < Decimal(str(faixa.minimo)):
        return AvaliacaoResultado("BAIXO", faixa, numero)
    if faixa.maximo is not None and numero > Decimal(str(faixa.maximo)):
        return AvaliacaoResultado("ALTO", faixa, numero)
    return AvaliacaoResultado("NORMAL", faixa, numero)
