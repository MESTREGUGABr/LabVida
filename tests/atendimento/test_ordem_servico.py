from decimal import Decimal
from uuid import uuid4

import pytest
from pydantic import ValidationError
from sqlalchemy.orm import Session

from src.atendimento.ordem_servico.dtos import (
    OrdemServicoCreate,
    OsItemInput,
    StatusOrdemServico,
    StatusOsItem,
)
from src.atendimento.ordem_servico.errors import (
    ConvenioInvalidoParaOS,
    ItemNaoPodeSerCancelado,
    OrdemServicoNaoPodeSerCancelada,
    PacienteInvalidoParaOS,
    UsuarioNaoAutorizadoParaCancelamento,
    ValorItemNaoDefinido,
)
from src.atendimento.ordem_servico.models import OrdemServico, OsItem, OsStatusHistorico
from src.atendimento.ordem_servico.service import (
    abrir_os,
    cancelar_item_os,
    cancelar_os,
    listar_historico,
    listar_itens,
)
from src.cadastro.convenio.service import alternar_status
from src.cadastro.procedimento.dtos import ProcedimentoCreate
from src.cadastro.procedimento.service import criar_procedimento
from src.laboratorial.models import Laudo, StatusLaudo
from src.usuario.models import Usuario

from tests.atendimento._helpers import montar_base


def _abrir_os_com_dois_itens(session: Session):
    base = montar_base(session)
    segundo = criar_procedimento(
        session, ProcedimentoCreate(codigo_tuss="40302024", nome="Glicemia")
    )
    ordem = abrir_os(
        session,
        OrdemServicoCreate(
            paciente_id=base.paciente_id,
            unidade_id=base.unidade_id,
            itens=[
                OsItemInput(procedimento_id=base.procedimento_id, valor_negociado=Decimal("80")),
                OsItemInput(procedimento_id=segundo.id, valor_negociado=Decimal("50")),
            ],
        ),
        base.usuario_id,
    )
    itens = listar_itens(session, ordem.id)
    return base, ordem, itens


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


def test_cancelar_item_mantem_os_aberta_enquanto_houver_item_ativo(session: Session) -> None:
    base, ordem, itens = _abrir_os_com_dois_itens(session)

    cancelar_item_os(session, itens[0].id, base.usuario_id)

    assert listar_itens(session, ordem.id)[0].status == StatusOsItem.CANCELADO
    assert listar_itens(session, ordem.id)[0].cancelado_por_usuario_id == base.usuario_id
    assert session.get(OrdemServico, ordem.id).status == StatusOrdemServico.ABERTA
    assert listar_historico(session, ordem.id)[-1].status == StatusOrdemServico.ABERTA


def test_cancelar_ultimo_item_cancela_os_e_audita_ator(session: Session) -> None:
    base, ordem, itens = _abrir_os_com_dois_itens(session)

    cancelar_item_os(session, itens[0].id, base.usuario_id)
    cancelar_item_os(session, itens[1].id, base.usuario_id)
    ordem_atual = session.get(OrdemServico, ordem.id)

    assert ordem_atual.status == StatusOrdemServico.CANCELADA
    historico = session.query(OsStatusHistorico).filter_by(ordem_servico_id=ordem.id).all()
    assert [registro.status for registro in historico] == [
        StatusOrdemServico.ABERTA,
        StatusOrdemServico.CANCELADA,
    ]
    assert historico[-1].usuario_id == base.usuario_id


def test_cancelar_item_com_outro_laudo_liberado_conclui_os(session: Session) -> None:
    base, ordem, itens = _abrir_os_com_dois_itens(session)
    laudo = Laudo(os_item_id=itens[1].id, status=StatusLaudo.LIBERADO)
    session.add(laudo)
    session.flush()

    cancelar_item_os(session, itens[0].id, base.usuario_id)
    ordem_atual = session.get(OrdemServico, ordem.id)

    assert ordem_atual.status == StatusOrdemServico.CONCLUIDA
    assert listar_historico(session, ordem.id)[-1].usuario_id == base.usuario_id


def test_nao_cancela_item_com_laudo_liberado(session: Session) -> None:
    base, ordem, itens = _abrir_os_com_dois_itens(session)
    session.add(Laudo(os_item_id=itens[0].id, status=StatusLaudo.LIBERADO))
    session.flush()

    with pytest.raises(ItemNaoPodeSerCancelado):
        cancelar_item_os(session, itens[0].id, base.usuario_id)

    assert listar_itens(session, ordem.id)[0].status == StatusOsItem.SOLICITADO
    assert session.get(OrdemServico, ordem.id).status == StatusOrdemServico.ABERTA
    assert len(listar_historico(session, ordem.id)) == 1


def test_cancelamento_integral_bloqueado_com_item_concluido(session: Session) -> None:
    base, ordem, itens = _abrir_os_com_dois_itens(session)
    session.add(Laudo(os_item_id=itens[0].id, status=StatusLaudo.LIBERADO))
    session.flush()

    with pytest.raises(OrdemServicoNaoPodeSerCancelada):
        cancelar_os(session, ordem.id, base.usuario_id)

    assert listar_itens(session, ordem.id)[0].status == StatusOsItem.SOLICITADO
    assert session.get(OrdemServico, ordem.id).status == StatusOrdemServico.ABERTA


def test_nao_cancela_item_faturado(session: Session) -> None:
    base, ordem, itens = _abrir_os_com_dois_itens(session)
    session.get(OsItem, itens[0].id).status = StatusOsItem.FATURADO
    session.flush()

    with pytest.raises(ItemNaoPodeSerCancelado):
        cancelar_item_os(session, itens[0].id, base.usuario_id)

    assert listar_itens(session, ordem.id)[0].status == StatusOsItem.FATURADO
    assert len(listar_historico(session, ordem.id)) == 1


def test_repetir_cancelamento_nao_cria_nova_transicao(session: Session) -> None:
    base, ordem, itens = _abrir_os_com_dois_itens(session)
    cancelar_item_os(session, itens[0].id, base.usuario_id)

    with pytest.raises(ItemNaoPodeSerCancelado):
        cancelar_item_os(session, itens[0].id, base.usuario_id)

    assert len(listar_historico(session, ordem.id)) == 1


def test_usuario_inativo_nao_pode_cancelar_item(session: Session) -> None:
    base, ordem, itens = _abrir_os_com_dois_itens(session)
    session.get(Usuario, base.usuario_id).ativo = False
    session.flush()

    with pytest.raises(UsuarioNaoAutorizadoParaCancelamento):
        cancelar_item_os(session, itens[0].id, base.usuario_id)
