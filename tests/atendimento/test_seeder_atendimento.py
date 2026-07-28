from sqlalchemy.orm import Session

from src.seeder.atendimento import executar_seeder_atendimento
from src.seeder.cadastros import main as seed_cadastros
from src.seeder.pacientes import main as seed_pacientes
from src.seeder.rbac import main as seed_rbac


def test_executar_seeder_atendimento(session: Session) -> None:
    # Garantir pré-requisitos do seeder
    seed_rbac()
    seed_cadastros()
    seed_pacientes()

    contagem = executar_seeder_atendimento()

    assert contagem["ordens_servico"] == 4
    assert contagem["amostras"] == 4
    assert contagem["malotes"] == 3
    assert contagem["recebimentos"] == 2
