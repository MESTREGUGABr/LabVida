from collections.abc import Iterator

import pytest
from sqlalchemy.orm import Session

from src.seeder import config
from src.seeder.atendimento import executar_seeder_atendimento
from src.seeder.cadastros import main as seed_cadastros
from src.seeder.pacientes import main as seed_pacientes
from src.seeder.rbac import main as seed_rbac


@pytest.fixture()
def escala_reduzida() -> Iterator[None]:
    """Roda o mesmo seeder da demo com uma fração do volume."""
    config.definir_escala(0.05)
    config.iniciar_rng()
    yield
    config.definir_escala(1.0)


def test_executar_seeder_atendimento(session: Session, escala_reduzida: None) -> None:
    # Garantir pré-requisitos do seeder
    seed_rbac()
    seed_cadastros()
    seed_pacientes()

    contagem = executar_seeder_atendimento()

    # O seeder distribui as OS pelos estágios do fluxo, então o que importa é a
    # coerência entre as etapas — não um número fixo de registros.
    assert contagem["ordens_servico"] > 0
    assert contagem["itens"] >= contagem["ordens_servico"]
    assert 0 < contagem["amostras"] <= contagem["ordens_servico"]
    assert contagem["malotes"] > 0
    assert contagem["recebimentos"] <= contagem["malotes"]
    assert contagem["ordens_canceladas"] <= contagem["ordens_servico"]


def test_seeder_atendimento_e_idempotente(session: Session, escala_reduzida: None) -> None:
    seed_rbac()
    seed_cadastros()
    seed_pacientes()
    executar_seeder_atendimento()

    segunda_execucao = executar_seeder_atendimento()

    assert segunda_execucao["ordens_servico"] == 0
    assert segunda_execucao["amostras"] == 0
