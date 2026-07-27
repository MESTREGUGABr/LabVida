from collections.abc import Iterator
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal

import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.atendimento.amostra.models import Amostra, Coleta
from src.atendimento.ordem_servico.models import OrdemServico, OsItem
from src.bi.etl import _tempo_ciclo_os
from src.cadastro.dtos import SexoPaciente
from src.cadastro.models import Paciente
from src.cadastro.procedimento.models import Procedimento
from src.cadastro.unidade.models import Unidade
from src.db import session_scope
from src.laboratorial.models import Laudo, StatusLaudo
from src.usuario.models import Usuario

_TABELAS = (
    "auditoria_log",
    "resultados_auditoria",
    "laudos",
    "resultados",
    "coletas",
    "amostras",
    "os_status_historico",
    "os_itens",
    "ordens_servico",
    "medicos",
    "procedimentos",
    "unidades",
    "usuarios",
    "pacientes",
)


@pytest.fixture()
def session() -> Iterator[Session]:
    with session_scope() as s:
        s.execute(text("TRUNCATE " + ", ".join(_TABELAS) + " RESTART IDENTITY CASCADE"))
        s.commit()
        yield s
        s.execute(text("TRUNCATE " + ", ".join(_TABELAS) + " RESTART IDENTITY CASCADE"))
        s.commit()


def _montar_os_com_ciclo(session: Session, *, coletada_em, liberado_em) -> OrdemServico:
    paciente = Paciente(
        cpf="52998224725",
        nome="Ana Ciclo",
        data_nascimento=date(1990, 1, 1),
        telefone="87999991234",
        sexo=SexoPaciente.FEMININO,
        ativo=True,
    )
    unidade = Unidade(nome="Central Ciclo", tipo="CENTRAL", ativo=True)
    procedimento = Procedimento(codigo_tuss="40302016", nome="Hemograma", ativo=True)
    usuario = Usuario(email="coletor.ciclo@labvida.test", nome="Coletor", ativo=True)
    session.add_all([paciente, unidade, procedimento, usuario])
    session.flush()

    ordem = OrdemServico(
        codigo_os="OS-CICLO-1",
        paciente_id=paciente.id,
        unidade_id=unidade.id,
        status="CONCLUIDA",
    )
    session.add(ordem)
    session.flush()
    item = OsItem(
        ordem_servico_id=ordem.id,
        procedimento_id=procedimento.id,
        valor_negociado=Decimal("100"),
        status="RESULTADO_LIBERADO",
    )
    amostra = Amostra(
        ordem_servico_id=ordem.id,
        codigo_barras="AMCICLO0001",
        tipo_material="SANGUE",
        status="RECEBIDA",
    )
    session.add_all([item, amostra])
    session.flush()
    session.add(Coleta(amostra_id=amostra.id, coletor_id=usuario.id, coletada_em=coletada_em))
    session.add(
        Laudo(
            os_item_id=item.id,
            status=StatusLaudo.LIBERADO,
            liberado_em=liberado_em,
        )
    )
    session.flush()
    return ordem


def test_tempo_ciclo_os_calcula_horas(session: Session) -> None:
    t0 = datetime(2026, 1, 1, 8, 0, tzinfo=timezone.utc)
    ordem = _montar_os_com_ciclo(session, coletada_em=t0, liberado_em=t0 + timedelta(hours=5, minutes=30))

    ciclo = _tempo_ciclo_os(session, ordem.id)

    assert ciclo == Decimal("5.50")


def test_tempo_ciclo_os_sem_laudo_liberado_retorna_none(session: Session) -> None:
    paciente = Paciente(
        cpf="52998224725",
        nome="Sem Laudo",
        data_nascimento=date(1990, 1, 1),
        telefone="87999991234",
        sexo=SexoPaciente.FEMININO,
        ativo=True,
    )
    unidade = Unidade(nome="Central Sem", tipo="CENTRAL", ativo=True)
    session.add_all([paciente, unidade])
    session.flush()
    ordem = OrdemServico(
        codigo_os="OS-SEM-LAUDO",
        paciente_id=paciente.id,
        unidade_id=unidade.id,
        status="ABERTA",
    )
    session.add(ordem)
    session.flush()

    assert _tempo_ciclo_os(session, ordem.id) is None
