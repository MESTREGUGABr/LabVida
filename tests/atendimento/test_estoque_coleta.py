from decimal import Decimal
import pytest
from sqlalchemy.orm import Session

from src.atendimento.amostra.dtos import ColetaCreate, TipoMaterial
from src.atendimento.amostra.errors import EstoqueInsuficienteError
from src.atendimento.amostra.service import registrar_coleta
from src.atendimento.ordem_servico.dtos import OrdemServicoCreate, OsItemInput
from src.atendimento.ordem_servico.service import abrir_os
from src.cadastro.procedimento.repository import vincular_insumo
from src.compras.insumo.dtos import InsumoCreate, TipoMovimentoEstoque
from src.compras.insumo.service import criar_insumo, listar_todos_movimentos, obter_insumo
from tests.atendimento._helpers import montar_base


def test_coleta_deduz_estoque_quando_procedimento_tem_insumo_vinculado(session: Session) -> None:
    base = montar_base(session)

    # 1. Criar insumo com estoque = 10
    insumo = criar_insumo(
        session,
        InsumoCreate(
            nome="Tubo Teste Coleta",
            finalidade="Teste Coleta",
            quantidade_estoque=10.0,
            estoque_minimo=2.0,
        ),
    )

    # 2. Vincular ao procedimento do teste (necessita 1.0)
    vincular_insumo(session, base.procedimento_id, insumo.id, quantidade_necessaria=1.0)
    session.commit()

    # 3. Abrir OS e registrar coleta
    ordem = abrir_os(
        session,
        OrdemServicoCreate(
            paciente_id=base.paciente_id,
            unidade_id=base.unidade_id,
            convenio_id=None,
            itens=[
                OsItemInput(
                    procedimento_id=base.procedimento_id,
                    valor_negociado=Decimal("50"),
                    motivo_excecao="Teste consumo estoque",
                )
            ],
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

    # 4. Verificar debito do estoque (10.0 - 1.0 = 9.0)
    insumo_atual = obter_insumo(session, insumo.id)
    assert insumo_atual.quantidade_estoque == 9.0

    movs = listar_todos_movimentos(session)
    mov_saida = [m for m in movs if m.insumo_material_id == insumo.id and m.tipo == TipoMovimentoEstoque.SAIDA]
    assert len(mov_saida) == 1
    assert Decimal(str(mov_saida[0].quantidade)) == Decimal("1.000")


def test_coleta_bloqueia_quando_estoque_insuficiente(session: Session) -> None:
    base = montar_base(session)

    # 1. Criar insumo com estoque = 0.5 (insuficiente para a necessidade 1.0)
    insumo = criar_insumo(
        session,
        InsumoCreate(
            nome="Tubo Escasso",
            finalidade="Teste Bloqueio",
            quantidade_estoque=0.5,
            estoque_minimo=2.0,
        ),
    )

    # 2. Vincular ao procedimento (necessita 1.0)
    vincular_insumo(session, base.procedimento_id, insumo.id, quantidade_necessaria=1.0)
    session.commit()

    # 3. Abrir OS
    ordem = abrir_os(
        session,
        OrdemServicoCreate(
            paciente_id=base.paciente_id,
            unidade_id=base.unidade_id,
            convenio_id=None,
            itens=[
                OsItemInput(
                    procedimento_id=base.procedimento_id,
                    valor_negociado=Decimal("50"),
                    motivo_excecao="Teste bloqueio estoque",
                )
            ],
        ),
        base.usuario_id,
    )

    # 4. Tentar registrar coleta -> deve levantar EstoqueInsuficienteError
    with pytest.raises(EstoqueInsuficienteError, match="Estoque insuficiente"):
        registrar_coleta(
            session,
            ColetaCreate(
                ordem_servico_id=ordem.id,
                tipo_material=TipoMaterial.SANGUE,
                coletor_usuario_id=base.usuario_id,
            ),
        )
