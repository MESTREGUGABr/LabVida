from decimal import Decimal

from sqlalchemy.orm import Session

from src.atendimento.ordem_servico.dtos import OrdemServicoCreate, OsItemInput
from src.atendimento.ordem_servico.service import (
    abrir_os,
    cancelar_item_os,
    cancelar_os,
    listar_itens,
)
from src.auditoria.models import AuditoriaLog

from tests.atendimento._helpers import montar_base


def _abrir_os(session: Session, base):
    return abrir_os(
        session,
        OrdemServicoCreate(
            paciente_id=base.paciente_id,
            unidade_id=base.unidade_id,
            convenio_id=None,
            itens=[OsItemInput(procedimento_id=base.procedimento_id, valor_negociado=Decimal("80.00"))],
        ),
        base.usuario_id,
    )


def _logs(session: Session, acao: str) -> list[AuditoriaLog]:
    return session.query(AuditoriaLog).filter_by(acao=acao).all()


def test_abrir_os_registra_auditoria(session: Session) -> None:
    base = montar_base(session)

    ordem = _abrir_os(session, base)

    logs = _logs(session, "ABRIR_OS")
    assert len(logs) == 1
    assert logs[0].entidade == "ordem_servico"
    assert logs[0].entidade_id == ordem.id
    assert logs[0].usuario_id == base.usuario_id
    assert logs[0].dados["codigo_os"] == ordem.codigo_os
    assert logs[0].dados["itens"] == 1


def test_abrir_os_sem_usuario_nao_registra_auditoria(session: Session) -> None:
    base = montar_base(session)

    abrir_os(
        session,
        OrdemServicoCreate(
            paciente_id=base.paciente_id,
            unidade_id=base.unidade_id,
            convenio_id=None,
            itens=[OsItemInput(procedimento_id=base.procedimento_id, valor_negociado=Decimal("80.00"))],
        ),
    )

    assert _logs(session, "ABRIR_OS") == []


def test_cancelar_item_registra_auditoria(session: Session) -> None:
    base = montar_base(session)
    ordem = _abrir_os(session, base)
    item = listar_itens(session, ordem.id)[0]

    cancelar_item_os(session, item.id, base.usuario_id)

    logs = _logs(session, "CANCELAR_ITEM")
    assert len(logs) == 1
    assert logs[0].entidade == "os_item"
    assert logs[0].entidade_id == item.id
    assert logs[0].usuario_id == base.usuario_id


def test_cancelar_os_registra_auditoria(session: Session) -> None:
    base = montar_base(session)
    ordem = _abrir_os(session, base)

    cancelar_os(session, ordem.id, base.usuario_id)

    logs = _logs(session, "CANCELAR_OS")
    assert len(logs) == 1
    assert logs[0].entidade == "ordem_servico"
    assert logs[0].entidade_id == ordem.id
    assert logs[0].dados["codigo_os"] == ordem.codigo_os
