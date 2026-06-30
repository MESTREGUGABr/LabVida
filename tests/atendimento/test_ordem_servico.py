from decimal import Decimal
from uuid import uuid4

import pytest
from pydantic import ValidationError
from sqlalchemy.orm import Session

from src.atendimento.ordem_servico.dtos import (
    OrdemServicoCreate,
    OsItemInput,
    StatusOrdemServico,
)
from src.atendimento.ordem_servico.errors import (
    ConvenioInvalidoParaOS,
    PacienteInvalidoParaOS,
    ValorItemNaoDefinido,
)
from src.atendimento.ordem_servico.service import abrir_os, listar_historico, listar_itens
from src.cadastro.convenio.service import alternar_status

from tests.atendimento._helpers import montar_base


def test_abre_os_particular_com_valor_explicito(session: Session) -> None:
    base = montar_base(session)

    ordem = abrir_os(
        session,
        OrdemServicoCreate(
            paciente_id=base.paciente_id,
            unidade_id=base.unidade_id,
            convenio_id=None,
            itens=[OsItemInput(procedimento_id=base.procedimento_id, valor_negociado=Decimal("80.00"))],
        ),
        base.usuario_id,
    )

    assert ordem.codigo_os.startswith("OS-")
    assert ordem.status == StatusOrdemServico.ABERTA

    itens = listar_itens(session, ordem.id)
    assert len(itens) == 1
    assert itens[0].valor_negociado == Decimal("80.00")

    historico = listar_historico(session, ordem.id)
    assert [h.status for h in historico] == [StatusOrdemServico.ABERTA]


def test_abre_os_conveniada_deriva_valor_de_tabela(session: Session) -> None:
    base = montar_base(session, valor_tabela=Decimal("42.00"))

    ordem = abrir_os(
        session,
        OrdemServicoCreate(
            paciente_id=base.paciente_id,
            unidade_id=base.unidade_id,
            convenio_id=base.convenio_id,
            itens=[OsItemInput(procedimento_id=base.procedimento_id, valor_negociado=None)],
        ),
        base.usuario_id,
    )

    itens = listar_itens(session, ordem.id)
    assert itens[0].valor_negociado == Decimal("42.00")


def test_rejeita_convenio_inativo(session: Session) -> None:
    base = montar_base(session)
    alternar_status(session, base.convenio_id, ativo=False)

    with pytest.raises(ConvenioInvalidoParaOS):
        abrir_os(
            session,
            OrdemServicoCreate(
                paciente_id=base.paciente_id,
                unidade_id=base.unidade_id,
                convenio_id=base.convenio_id,
                itens=[OsItemInput(procedimento_id=base.procedimento_id, valor_negociado=None)],
            ),
            base.usuario_id,
        )


def test_rejeita_valor_nao_definido_para_particular(session: Session) -> None:
    base = montar_base(session)

    with pytest.raises(ValorItemNaoDefinido):
        abrir_os(
            session,
            OrdemServicoCreate(
                paciente_id=base.paciente_id,
                unidade_id=base.unidade_id,
                convenio_id=None,
                itens=[OsItemInput(procedimento_id=base.procedimento_id, valor_negociado=None)],
            ),
            base.usuario_id,
        )


def test_rejeita_paciente_inexistente(session: Session) -> None:
    base = montar_base(session)

    with pytest.raises(PacienteInvalidoParaOS):
        abrir_os(
            session,
            OrdemServicoCreate(
                paciente_id=uuid4(),
                unidade_id=base.unidade_id,
                convenio_id=None,
                itens=[OsItemInput(procedimento_id=base.procedimento_id, valor_negociado=Decimal("10"))],
            ),
            base.usuario_id,
        )


def test_os_sem_itens_e_invalida(session: Session) -> None:
    base = montar_base(session)

    with pytest.raises(ValidationError):
        OrdemServicoCreate(
            paciente_id=base.paciente_id,
            unidade_id=base.unidade_id,
            convenio_id=None,
            itens=[],
        )
