from decimal import Decimal
from uuid import uuid4

import pytest
from sqlalchemy.orm import Session

from src.atendimento.amostra.dtos import ColetaCreate, StatusAmostra, TipoMaterial
from src.atendimento.amostra.service import registrar_coleta
from src.atendimento.ordem_servico.dtos import OrdemServicoCreate, OsItemInput, StatusOrdemServico
from src.atendimento.ordem_servico.service import abrir_os, obter_os
from src.cadastro.unidade.dtos import UnidadeCreate
from src.cadastro.unidade.service import criar_unidade
from src.logistica.malote.dtos import MaloteCreate, StatusMalote
from src.logistica.malote.errors import AmostraInvalidaParaMalote, MaloteFechadoOuInvalido
from src.logistica.malote.service import (
    adicionar_amostra_ao_malote,
    criar_malote,
    despachar_malote,
    obter_malote,
)
from src.logistica.recebimento.dtos import ProtocoloRecebimentoCreate
from src.logistica.recebimento.service import (
    listar_historico_amostra,
    obter_protocolo,
    receber_malote,
)
from tests.atendimento._helpers import montar_base


def test_fluxo_completo_logistica(session: Session) -> None:
    base = montar_base(session)

    # 1. Criar unidade central para ser o destino do malote
    central = criar_unidade(session, UnidadeCreate(nome="Laboratório Central", tipo="CENTRAL"))

    # 2. Abrir OS e registrar coleta na unidade de origem
    ordem = abrir_os(
        session,
        OrdemServicoCreate(
            paciente_id=base.paciente_id,
            unidade_id=base.unidade_id,
            convenio_id=None,
            itens=[OsItemInput(procedimento_id=base.procedimento_id, valor_negociado=Decimal("100"))],
        ),
        base.usuario_id,
    )
    amostra = registrar_coleta(
        session,
        ColetaCreate(
            ordem_servico_id=ordem.id,
            tipo_material=TipoMaterial.SANGUE,
            coletor_usuario_id=base.usuario_id,
        ),
    )
    assert amostra.status == StatusAmostra.COLETADA

    # 3. Criar malote da Unidade de Coleta -> Central
    malote = criar_malote(
        session,
        MaloteCreate(
            unidade_origem_id=base.unidade_id,
            unidade_destino_id=central.id,
            enviado_por_usuario_id=base.usuario_id,
        ),
    )
    assert malote.status == StatusMalote.ABERTO

    # 4. Adicionar amostra ao malote e despachar
    adicionar_amostra_ao_malote(session, malote.id, amostra.id)
    malote_despachado = despachar_malote(session, malote.id, base.usuario_id)
    assert malote_despachado.status == StatusMalote.EM_TRANSITO

    # 5. Receber malote no Central
    protocolo = receber_malote(
        session,
        ProtocoloRecebimentoCreate(
            malote_id=malote.id,
            recebido_por_usuario_id=base.usuario_id,
            integridade_ok=True,
            observacao="Tubo sem ranhuras ou vazamentos",
        ),
    )
    assert protocolo.integridade_ok is True

    # 6. Verificações ponta a ponta
    malote_final = obter_malote(session, malote.id)
    assert malote_final.status == StatusMalote.RECEBIDO

    # OS deve ter transicionado para EM_ANALISE
    os_atual = obter_os(session, ordem.id)
    assert os_atual.status == StatusOrdemServico.EM_ANALISE

    # Cadeia de custódia da amostra
    historico = listar_historico_amostra(session, amostra.id)
    assert len(historico) == 3
    assert historico[0].status == StatusAmostra.COLETADA
    assert historico[1].status == StatusAmostra.EM_TRANSITO
    assert historico[2].status == StatusAmostra.RECEBIDA


def test_recebimento_com_integridade_falsa_rejeita_amostra(session: Session) -> None:
    base = montar_base(session)
    central = criar_unidade(session, UnidadeCreate(nome="Laboratório Central", tipo="CENTRAL"))

    ordem = abrir_os(
        session,
        OrdemServicoCreate(
            paciente_id=base.paciente_id,
            unidade_id=base.unidade_id,
            convenio_id=None,
            itens=[OsItemInput(procedimento_id=base.procedimento_id, valor_negociado=Decimal("100"))],
        ),
        base.usuario_id,
    )
    amostra = registrar_coleta(
        session,
        ColetaCreate(
            ordem_servico_id=ordem.id,
            tipo_material=TipoMaterial.SANGUE,
            coletor_usuario_id=base.usuario_id,
        ),
    )

    malote = criar_malote(
        session,
        MaloteCreate(
            unidade_origem_id=base.unidade_id,
            unidade_destino_id=central.id,
            enviado_por_usuario_id=base.usuario_id,
        ),
    )
    adicionar_amostra_ao_malote(session, malote.id, amostra.id)
    despachar_malote(session, malote.id, base.usuario_id)

    receber_malote(
        session,
        ProtocoloRecebimentoCreate(
            malote_id=malote.id,
            recebido_por_usuario_id=base.usuario_id,
            integridade_ok=False,
            observacao="Tubo quebrado no transporte",
        ),
    )

    historico = listar_historico_amostra(session, amostra.id)
    assert len(historico) == 3
    assert historico[0].status == StatusAmostra.COLETADA
    assert historico[1].status == StatusAmostra.EM_TRANSITO
    assert historico[2].status == StatusAmostra.REJEITADA


def test_nao_permite_despachar_malote_sem_amostras(session: Session) -> None:
    base = montar_base(session)
    central = criar_unidade(session, UnidadeCreate(nome="Laboratório Central", tipo="CENTRAL"))

    malote = criar_malote(
        session,
        MaloteCreate(
            unidade_origem_id=base.unidade_id,
            unidade_destino_id=central.id,
            enviado_por_usuario_id=base.usuario_id,
        ),
    )

    with pytest.raises(MaloteFechadoOuInvalido):
        despachar_malote(session, malote.id, base.usuario_id)
