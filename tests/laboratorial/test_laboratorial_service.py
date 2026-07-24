from datetime import date, timedelta
from decimal import Decimal

from sqlalchemy.orm import Session

from src.atendimento.ordem_servico.dtos import StatusOrdemServico, StatusOsItem
from src.atendimento.ordem_servico.models import OrdemServico, OsItem
from src.cadastro.dtos import SexoPaciente
from src.cadastro.models import Paciente
from src.cadastro.procedimento.models import Procedimento
from src.cadastro.unidade.models import Unidade
from src.laboratorial.dtos import LaudoCreate
from src.laboratorial.service import LaboratorialService


def test_criar_rascunho_de_laudo_resolve_fk_de_medico(session: Session) -> None:
    paciente = Paciente(
        cpf="52998224725",
        nome="Ana Maria",
        data_nascimento=date.today() - timedelta(days=10000),
        telefone="87999991234",
        sexo=SexoPaciente.FEMININO,
        ativo=True,
    )
    unidade = Unidade(nome="Central", tipo="CENTRAL", ativo=True)
    procedimento = Procedimento(codigo_tuss="40302016", nome="Hemograma", ativo=True)
    session.add_all([paciente, unidade, procedimento])
    session.flush()

    ordem = OrdemServico(
        codigo_os="OS-2026-TESTE",
        paciente_id=paciente.id,
        unidade_id=unidade.id,
        status=StatusOrdemServico.EM_ANALISE,
    )
    session.add(ordem)
    session.flush()
    item = OsItem(
        ordem_servico_id=ordem.id,
        procedimento_id=procedimento.id,
        valor_negociado=Decimal("100"),
        status=StatusOsItem.COLETADO,
    )
    session.add(item)
    session.flush()

    laudo = LaboratorialService(session).criar_laudo(LaudoCreate(os_item_id=item.id))

    assert laudo.os_item_id == item.id
