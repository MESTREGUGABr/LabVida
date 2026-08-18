"""Trajetória de crescimento da empresa simulada.

Uma base de demonstração não pode ter volume constante ao longo da janela:
uma empresa real cresce, sente sazonalidade, muda o mix e melhora o processo.
Este módulo concentra a curva que molda ONDE os eventos caem na linha do tempo
— é a única fonte desses fatores, usada por todos os seeders.

A história contada (com SEED_INICIO=2022-01-01):
- Recuperação pós-pandemia: a rede abre 2022 com a central + 2 unidades de
  coleta e cresce ~2%/mês (≈27% ao ano) conforme assina convênios e inaugura
  unidades (ciclo de vida no catálogo);
- Sazonalidade local: pico de demanda no inverno (jun-ago), vales no recesso
  de fim de ano e em janeiro;
- Movimento concentrado em dias úteis — sábado atende plantão, domingo é
  residual.
"""

import math
import random
from datetime import date, datetime, timedelta

from src.seeder.config import JANELA_DIAS, agora

# Sazonalidade por mês: multiplica o peso de um dia daquele mês.
SAZONALIDADE_MENSAL = {
    1: 0.88,   # férias de verão, movimento fraco
    2: 0.96,
    3: 1.08,   # check-ups de volta às aulas
    4: 1.04,
    5: 1.05,
    6: 1.06,
    7: 1.12,   # inverno: pico de demanda
    8: 1.10,
    9: 1.00,
    10: 1.02,
    11: 0.97,
    12: 0.82,  # recesso de fim de ano
}

# Crescimento mensal composto (~2%/mês ≈ 27%/ano).
CRESCIMENTO_MENSAL = 1.02

# Peso por dia da semana: dias úteis cheios, sábado plantão, domingo residual.
PESO_DIA_SEMANA = {0: 1.0, 1: 1.0, 2: 1.0, 3: 1.0, 4: 1.0, 5: 0.55, 6: 0.05}

_PESOS_CACHE: dict[tuple[int, int], tuple[list[int], list[float]]] = {}


def data_inicio() -> date:
    """Primeiro dia da janela simulada."""
    return (agora() - timedelta(days=JANELA_DIAS)).date()


def anos_de_operacao(instante: datetime) -> float:
    """Idade da empresa (em anos) no instante dado, contada do início da janela."""
    inicio = datetime.combine(data_inicio(), datetime.min.time(), tzinfo=instante.tzinfo)
    return max(0.0, (instante - inicio).total_seconds() / (86400 * 365.25))


def peso_do_dia(dia: date) -> float:
    """Peso relativo de um dia da série (crescimento × sazonalidade × dia da semana)."""
    inicio = data_inicio()
    meses = (dia.year - inicio.year) * 12 + (dia.month - inicio.month)
    crescimento = CRESCIMENTO_MENSAL ** max(0, meses)
    return crescimento * SAZONALIDADE_MENSAL[dia.month] * PESO_DIA_SEMANA[dia.weekday()]


def sortear_dias_atras(minimo: float, maximo: float) -> float:
    """Sorteia "dias atrás" respeitando a trajetória da empresa.

    Em vez de uma distribuição uniforme, a chance de um dia ser sorteado cresce
    com a maturidade da empresa e segue a sazonalidade — o volume mensal da
    base sai com a curva de evolução real, não uma linha reta.
    """
    inicio = math.floor(minimo)
    fim = math.floor(maximo)
    chave = (inicio, fim)
    if chave not in _PESOS_CACHE:
        hoje = data_inicio() + timedelta(days=JANELA_DIAS)
        dias = list(range(inicio, fim + 1))
        pesos = [peso_do_dia(hoje - timedelta(days=d)) for d in dias]
        _PESOS_CACHE[chave] = (dias, pesos)

    dias, pesos = _PESOS_CACHE[chave]
    return random.choices(dias, weights=pesos, k=1)[0] + random.random()


def proporcao_particular(instante: datetime) -> float:
    """Mix particular: cai conforme a rede cresce e assina convênios.

    No começo da série o balcão pesa (~30% das OS); com os contratos de
    convênio ao longo dos anos o particular recua até o piso (~12%).
    """
    anos = anos_de_operacao(instante)
    return max(0.12, 0.30 - 0.045 * anos)
