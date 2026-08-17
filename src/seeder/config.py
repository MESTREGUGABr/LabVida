"""Volume, determinismo e janela temporal da base de demonstração.

O seeder monta um laboratório com meses de operação já rodada. Todo volume
passa por `qtd()`, então `definir_escala()` encolhe (ou amplia) a carga inteira
de forma proporcional — é o que permite os testes exercitarem exatamente o
mesmo código com uma fração dos dados.

Variáveis de ambiente:
    SEED_INICIO       data ISO (ex.: 2022-01-01) de início da operação simulada;
                      tem precedência sobre SEED_JANELA_DIAS e vira a janela
                      inteira (da data até hoje)
    SEED_JANELA_DIAS  período de operação simulado, em dias (padrão 90)
    SEED_ESCALA       multiplicador de volume (padrão 1.0)
    SEED_SEMENTE      semente do RNG; fixa deixa a base reproduzível
"""

import os
import random
from datetime import date, datetime, timedelta, timezone

from faker import Faker

SEMENTE = int(os.environ.get("SEED_SEMENTE", "20261"))


def _resolver_janela_dias() -> int:
    """Janela de operação simulada, em dias, contados a partir de hoje.

    Uma data em `SEED_INICIO` define a janela inteira — o que permite estender
    a série temporal do BI para anos (ex.: base de 2022 até hoje). O fallback
    continua sendo `SEED_JANELA_DIAS`.
    """
    inicio = os.environ.get("SEED_INICIO", "").strip()
    if inicio:
        try:
            dias = (date.today() - date.fromisoformat(inicio)).days
            if dias > 0:
                return dias
        except ValueError:
            pass
    return int(os.environ.get("SEED_JANELA_DIAS", "90"))


JANELA_DIAS = _resolver_janela_dias()

fake = Faker("pt_BR")

_escala = float(os.environ.get("SEED_ESCALA", "1"))


def definir_escala(valor: float) -> None:
    """Redefine o multiplicador de volume (usado pelos testes)."""
    global _escala
    _escala = max(0.0, valor)


def escala() -> float:
    return _escala


def qtd(base: int) -> int:
    """Volume escalado, com piso de 1 para nunca zerar um módulo inteiro."""
    return max(1, round(base * _escala))


def iniciar_rng() -> None:
    """Fixa as sementes do RNG.

    Mantém a base equivalente entre execuções, não idêntica: parte das
    consultas do seeder não impõe ordenação, então a ordem em que o Postgres
    devolve as linhas ainda desloca alguns sorteios.
    """
    random.seed(SEMENTE)
    Faker.seed(SEMENTE)


def agora() -> datetime:
    return datetime.now(timezone.utc)


def momento(dias_atras: float) -> datetime:
    """Instante em horário de expediente, `dias_atras` dias no passado."""
    base = agora() - timedelta(days=dias_atras)
    return base.replace(
        hour=random.randint(6, 17),
        minute=random.randint(0, 59),
        second=random.randint(0, 59),
        microsecond=0,
    )


def somar_horas(instante: datetime, minimo: float, maximo: float) -> datetime:
    """Avança o relógio dentro de uma faixa, para encadear etapas do fluxo."""
    return instante + timedelta(hours=random.uniform(minimo, maximo))
