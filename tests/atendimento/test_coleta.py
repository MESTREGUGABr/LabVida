from decimal import Decimal
from uuid import uuid4

import pytest
from sqlalchemy.orm import Session

from src.atendimento.amostra.dtos import ColetaCreate, StatusAmostra, TipoMaterial
from src.atendimento.amostra.errors import ColetorInvalido, ColetaNaoPermitida, OrdemServicoInexistente
from src.atendimento.amostra.service import listar_amostras, registrar_coleta
from src.atendimento.ordem_servico.dtos import (
    OrdemServicoCreate,
    OsItemInput,
    StatusOrdemServico,
)
from src.atendimento.ordem_servico.service import abrir_os, listar_historico, obter_os

from tests.atendimento._helpers import montar_base


def _abrir_os(session: Session, base) -> object:
    return abrir_os(
        session,
        OrdemServicoCreate(
            paciente_id=base.paciente_id,
            unidade_id=base.unidade_id,
            convenio_id=None,
            # Valor divergente da tabela: a regra do valor (F3) exige motivo.
            itens=[OsItemInput(
                procedimento_id=base.procedimento_id,
                valor_negociado=Decimal("50"),
                motivo_excecao="Acordo comercial do teste",
            )],
        ),
        base.usuario_id,
    )


def test_coleta_cria_amostra_e_transiciona_os(session: Session) -> None:
    base = montar_base(session)
    ordem = _abrir_os(session, base)

    amostra = registrar_coleta(
        session,
        ColetaCreate(
            ordem_servico_id=ordem.id,
            tipo_material=TipoMaterial.SANGUE,
            coletor_usuario_id=base.usuario_id,
        ),
    )

    assert amostra.codigo_barras.startswith("AM")
    assert amostra.status == StatusAmostra.COLETADA

    assert obter_os(session, ordem.id).status == StatusOrdemServico.COLETADA
    assert StatusOrdemServico.COLETADA in [h.status for h in listar_historico(session, ordem.id)]
    assert len(listar_amostras(session, ordem.id)) == 1


def test_coleta_rejeita_os_inexistente(session: Session) -> None:
    base = montar_base(session)

    with pytest.raises(OrdemServicoInexistente):
        registrar_coleta(
            session,
            ColetaCreate(
                ordem_servico_id=uuid4(),
                tipo_material=TipoMaterial.SANGUE,
                coletor_usuario_id=base.usuario_id,
            ),
        )


def test_coleta_rejeita_coletor_invalido(session: Session) -> None:
    base = montar_base(session)
    ordem = _abrir_os(session, base)

    with pytest.raises(ColetorInvalido):
        registrar_coleta(
            session,
            ColetaCreate(
                ordem_servico_id=ordem.id,
                tipo_material=TipoMaterial.SANGUE,
                coletor_usuario_id=uuid4(),
            ),
        )


def test_coleta_rejeita_os_convenio_sem_autorizacao_valida(session: Session) -> None:
    from src.atendimento.ordem_servico.dtos import OrdemServicoCreate as OSDto, OsItemInput as OI

    base = montar_base(session)
    ordem = abrir_os(
        session,
        OSDto(
            paciente_id=base.paciente_id,
            unidade_id=base.unidade_id,
            convenio_id=base.convenio_id,
            # Valor divergente da tabela: a regra do valor (F3) exige motivo.
            itens=[OI(
                procedimento_id=base.procedimento_id,
                valor_negociado=Decimal("50"),
                motivo_excecao="Acordo comercial do teste",
            )],
        ),
        base.usuario_id,
    )

    with pytest.raises(ColetaNaoPermitida, match="sem autorização válida"):
        registrar_coleta(
            session,
            ColetaCreate(
                ordem_servico_id=ordem.id,
                tipo_material=TipoMaterial.SANGUE,
                coletor_usuario_id=base.usuario_id,
            ),
        )


def test_coleta_rejeita_sem_permissao(session: Session) -> None:
    from src.rbac.models import Perfil
    from src.usuario.service import sincronizar_usuario

    base = montar_base(session)
    ordem = _abrir_os(session, base)

    perfil = Perfil(nome="coleta_test", descricao="Sem coleta")
    session.add(perfil)
    session.flush()

    coletor_sem_permissao = sincronizar_usuario(
        session, "semcoleta@labvida.test", "Sem Coleta"
    )
    coletor_sem_permissao.perfil_id = perfil.id
    session.flush()

    with pytest.raises(ColetorInvalido, match="sem permissão"):
        registrar_coleta(
            session,
            ColetaCreate(
                ordem_servico_id=ordem.id,
                tipo_material=TipoMaterial.SANGUE,
                coletor_usuario_id=coletor_sem_permissao.id,
            ),
        )

    session.query(Perfil).filter_by(id=perfil.id).delete()
    session.flush()
