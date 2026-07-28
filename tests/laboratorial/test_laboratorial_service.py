from datetime import date, timedelta
from decimal import Decimal

import pytest
from sqlalchemy.orm import Session

from src.atendimento.amostra.dtos import StatusAmostra
from src.atendimento.amostra.models import Amostra
from src.atendimento.ordem_servico.dtos import StatusOrdemServico, StatusOsItem
from src.atendimento.ordem_servico.models import OrdemServico, OsItem, OsStatusHistorico
from src.cadastro.dtos import SexoPaciente
from src.cadastro.medico.models import Medico
from src.cadastro.models import Paciente
from src.cadastro.procedimento.models import Procedimento
from src.cadastro.unidade.models import Unidade
from src.laboratorial.dtos import LaudoCreate, LaudoUpdate, ResultadoCreate, ResultadoUpdate
from src.laboratorial.models import StatusLaudo, StatusResultado
from src.usuario.models import Usuario
from src.laboratorial.service import LaboratorialService


def _criar_amostra_recebida(session: Session, ordem_servico_id) -> Amostra:
    import uuid

    amostra = Amostra(
        ordem_servico_id=ordem_servico_id,
        codigo_barras=f"AM{uuid.uuid4().hex[:12]}",
        tipo_material="Sangue",
        status=StatusAmostra.RECEBIDA,
    )
    session.add(amostra)
    session.flush()
    return amostra


def _registrar_resultado_revisado(service, os_item_id, usuario_id, analito="Hemoglobina") -> None:
    """Registra um resultado ja REVISADO para o item (pre-requisito da liberacao de laudo)."""
    service.registrar_resultado(
        ResultadoCreate(
            os_item_id=os_item_id,
            analito=analito,
            valor="14.2",
            status=StatusResultado.REVISADO,
            usuario_id=usuario_id,
        )
    )


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
    _criar_amostra_recebida(session, ordem.id)
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
    _registrar_resultado_revisado(service, item.id, usuario.id)
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
    _criar_amostra_recebida(session, ordem.id)
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
    _registrar_resultado_revisado(service, item_1.id, usuario.id)
    _registrar_resultado_revisado(service, item_2.id, usuario.id)

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


def _montar_cenario_laudo(
    session: Session,
    *,
    responsavel_tecnico: bool = True,
    medico_ativo: bool = True,
):
    """Monta OS/item/laudo + medico + usuario e devolve as pecas para os testes de liberacao."""
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
    medico = Medico(
        nome="Dr. Joao",
        crm="12345",
        uf_crm="SP",
        responsavel_tecnico=responsavel_tecnico,
        ativo=medico_ativo,
    )
    usuario = Usuario(email="tecnico@labvida.test", nome="Tecnico", ativo=True)
    session.add_all([paciente, unidade, procedimento, medico, usuario])
    session.flush()

    ordem = OrdemServico(
        codigo_os="OS-2026-REGRA",
        paciente_id=paciente.id,
        unidade_id=unidade.id,
        status=StatusOrdemServico.EM_ANALISE,
    )
    session.add(ordem)
    session.flush()
    _criar_amostra_recebida(session, ordem.id)
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
    return service, item, laudo, medico, usuario


def test_nao_libera_laudo_sem_resultados(session: Session) -> None:
    service, item, laudo, medico, usuario = _montar_cenario_laudo(session)

    with pytest.raises(ValueError, match="sem resultados"):
        service.atualizar_laudo(
            laudo.id,
            LaudoUpdate(responsavel_tecnico_id=medico.id, status=StatusLaudo.LIBERADO),
            usuario_id=usuario.id,
        )

    session.rollback()
    session.refresh(laudo)
    assert laudo.status == StatusLaudo.RASCUNHO


def test_nao_libera_laudo_com_resultado_nao_revisado(session: Session) -> None:
    service, item, laudo, medico, usuario = _montar_cenario_laudo(session)
    service.registrar_resultado(
        ResultadoCreate(
            os_item_id=item.id,
            analito="Hemoglobina",
            valor="14.2",
            status=StatusResultado.AGUARDANDO_REVISAO,
            usuario_id=usuario.id,
        )
    )

    with pytest.raises(ValueError, match="REVISADOS"):
        service.atualizar_laudo(
            laudo.id,
            LaudoUpdate(responsavel_tecnico_id=medico.id, status=StatusLaudo.LIBERADO),
            usuario_id=usuario.id,
        )

    session.rollback()
    session.refresh(laudo)
    assert laudo.status == StatusLaudo.RASCUNHO


def test_nao_libera_laudo_com_medico_nao_responsavel_tecnico(session: Session) -> None:
    service, item, laudo, medico, usuario = _montar_cenario_laudo(
        session, responsavel_tecnico=False
    )
    _registrar_resultado_revisado(service, item.id, usuario.id)

    with pytest.raises(ValueError, match="responsável técnico"):
        service.atualizar_laudo(
            laudo.id,
            LaudoUpdate(responsavel_tecnico_id=medico.id, status=StatusLaudo.LIBERADO),
            usuario_id=usuario.id,
        )

    session.rollback()
    session.refresh(laudo)
    assert laudo.status == StatusLaudo.RASCUNHO


def test_nao_libera_laudo_com_medico_inativo(session: Session) -> None:
    service, item, laudo, medico, usuario = _montar_cenario_laudo(session, medico_ativo=False)
    _registrar_resultado_revisado(service, item.id, usuario.id)

    with pytest.raises(ValueError, match="responsável técnico"):
        service.atualizar_laudo(
            laudo.id,
            LaudoUpdate(responsavel_tecnico_id=medico.id, status=StatusLaudo.LIBERADO),
            usuario_id=usuario.id,
        )

    session.rollback()
    session.refresh(laudo)
    assert laudo.status == StatusLaudo.RASCUNHO


def test_laudo_liberado_nao_pode_ser_alterado(session: Session) -> None:
    service, item, laudo, medico, usuario = _montar_cenario_laudo(session)
    _registrar_resultado_revisado(service, item.id, usuario.id)
    service.atualizar_laudo(
        laudo.id,
        LaudoUpdate(responsavel_tecnico_id=medico.id, status=StatusLaudo.LIBERADO),
        usuario_id=usuario.id,
    )

    with pytest.raises(ValueError, match="liberado"):
        service.atualizar_laudo(
            laudo.id,
            LaudoUpdate(assinatura_digital="assinatura-nova"),
            usuario_id=usuario.id,
        )


def test_criar_laudo_duplicado_falha(session: Session) -> None:
    service, item, laudo, medico, usuario = _montar_cenario_laudo(session)

    with pytest.raises(ValueError, match="já existe"):
        service.criar_laudo(LaudoCreate(os_item_id=item.id))


def test_atualizar_resultado_gera_auditoria(session: Session) -> None:
    service, item, laudo, medico, usuario = _montar_cenario_laudo(session)
    resultado = service.registrar_resultado(
        ResultadoCreate(
            os_item_id=item.id,
            analito="Hemoglobina",
            valor="10.0",
            status=StatusResultado.AGUARDANDO_REVISAO,
            usuario_id=usuario.id,
        )
    )

    service.atualizar_resultado(
        resultado.id,
        ResultadoUpdate(valor="14.2", status=StatusResultado.REVISADO, usuario_id=usuario.id),
    )

    auditorias = service.listar_auditoria_resultado(resultado.id)
    pares = {(a.valor_anterior, a.valor_novo) for a in auditorias}
    assert ("", "10.0") in pares  # criação
    assert ("10.0", "14.2") in pares  # atualização
