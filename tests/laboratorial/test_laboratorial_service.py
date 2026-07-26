from datetime import date, timedelta
from decimal import Decimal

from sqlalchemy.orm import Session

from src.atendimento.ordem_servico.dtos import StatusOrdemServico, StatusOsItem
from src.atendimento.ordem_servico.models import OrdemServico, OsItem, OsStatusHistorico
from src.cadastro.dtos import SexoPaciente
from src.cadastro.medico.models import Medico
from src.cadastro.models import Paciente
from src.cadastro.procedimento.models import Procedimento
from src.cadastro.unidade.models import Unidade
from src.laboratorial.dtos import LaudoCreate, LaudoUpdate
from src.laboratorial.models import StatusLaudo
from src.usuario.models import Usuario
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


def test_liberar_laudo_atualiza_os_item_para_resultado_liberado(session: Session) -> None:
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
    medico = Medico(nome="Dr. Joao", crm="12345", uf_crm="SP", responsavel_tecnico=True, ativo=True)
    usuario = Usuario(email="tecnico@labvida.test", nome="Tecnico", ativo=True)
    session.add_all([paciente, unidade, procedimento, medico, usuario])
    session.flush()

    ordem = OrdemServico(
        codigo_os="OS-2026-LIBERAR",
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

    service = LaboratorialService(session)
    laudo = service.criar_laudo(LaudoCreate(os_item_id=item.id))
    service.atualizar_laudo(
        laudo.id,
        LaudoUpdate(
            responsavel_tecnico_id=medico.id,
            status=StatusLaudo.LIBERADO,
        ),
        usuario_id=usuario.id,
    )

    session.refresh(item)
    session.refresh(ordem)
    assert item.status == StatusOsItem.RESULTADO_LIBERADO
    assert ordem.status == StatusOrdemServico.CONCLUIDA

    historico = session.query(OsStatusHistorico).filter_by(ordem_servico_id=ordem.id).all()
    assert [registro.status for registro in historico] == [StatusOrdemServico.CONCLUIDA]
    assert historico[0].usuario_id == usuario.id


def test_os_com_varios_itens_so_conclui_apos_liberar_todos_os_laudos(
    session: Session,
) -> None:
    paciente = Paciente(
        cpf="52998224725",
        nome="Ana Maria",
        data_nascimento=date.today() - timedelta(days=10000),
        telefone="87999991234",
        sexo=SexoPaciente.FEMININO,
        ativo=True,
    )
    unidade = Unidade(nome="Central", tipo="CENTRAL", ativo=True)
    procedimento_1 = Procedimento(codigo_tuss="40302016", nome="Hemograma", ativo=True)
    procedimento_2 = Procedimento(codigo_tuss="40302024", nome="Glicemia", ativo=True)
    procedimento_3 = Procedimento(codigo_tuss="40302032", nome="Colesterol", ativo=True)
    medico = Medico(nome="Dr. Joao", crm="12345", uf_crm="SP", responsavel_tecnico=True, ativo=True)
    usuario = Usuario(email="tecnico@labvida.test", nome="Tecnico", ativo=True)
    session.add_all(
        [paciente, unidade, procedimento_1, procedimento_2, procedimento_3, medico, usuario]
    )
    session.flush()

    ordem = OrdemServico(
        codigo_os="OS-2026-DOIS-ITENS",
        paciente_id=paciente.id,
        unidade_id=unidade.id,
        status=StatusOrdemServico.EM_ANALISE,
    )
    session.add(ordem)
    session.flush()
    item_1 = OsItem(
        ordem_servico_id=ordem.id,
        procedimento_id=procedimento_1.id,
        valor_negociado=Decimal("100"),
        status=StatusOsItem.COLETADO,
    )
    item_2 = OsItem(
        ordem_servico_id=ordem.id,
        procedimento_id=procedimento_2.id,
        valor_negociado=Decimal("50"),
        status=StatusOsItem.COLETADO,
    )
    item_3 = OsItem(
        ordem_servico_id=ordem.id,
        procedimento_id=procedimento_3.id,
        valor_negociado=Decimal("75"),
        status=StatusOsItem.CANCELADO,
    )
    session.add_all([item_1, item_2, item_3])
    session.flush()

    service = LaboratorialService(session)
    laudo_1 = service.criar_laudo(LaudoCreate(os_item_id=item_1.id))
    laudo_2 = service.criar_laudo(LaudoCreate(os_item_id=item_2.id))

    service.atualizar_laudo(
        laudo_1.id,
        LaudoUpdate(responsavel_tecnico_id=medico.id, status=StatusLaudo.LIBERADO),
        usuario_id=usuario.id,
    )
    session.refresh(ordem)
    assert ordem.status == StatusOrdemServico.EM_ANALISE

    service.atualizar_laudo(
        laudo_2.id,
        LaudoUpdate(responsavel_tecnico_id=medico.id, status=StatusLaudo.LIBERADO),
        usuario_id=usuario.id,
    )
    session.refresh(ordem)

    assert ordem.status == StatusOrdemServico.CONCLUIDA
    historico = session.query(OsStatusHistorico).filter_by(ordem_servico_id=ordem.id).all()
    assert [registro.status for registro in historico] == [StatusOrdemServico.CONCLUIDA]
