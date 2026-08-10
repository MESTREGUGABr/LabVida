import uuid
from uuid import UUID

from sqlalchemy.orm import Session

from src.auditoria import registrar_auditoria
from src.atendimento.amostra import repository
from src.atendimento.amostra.dtos import AmostraRead, ColetaCreate, StatusAmostra
from src.atendimento.amostra.errors import ColetaNaoPermitida, ColetorInvalido, OrdemServicoInexistente
from src.atendimento.amostra.models import Amostra, Coleta
from src.atendimento.ordem_servico import repository as os_repository
from src.atendimento.ordem_servico import service as os_service
from src.atendimento.ordem_servico.dtos import StatusOrdemServico
from src.usuario import repository as usuario_repository


_STATUS_OS_BLOQUEIA_COLETA = {StatusOrdemServico.CONCLUIDA, StatusOrdemServico.CANCELADA}


def registrar_coleta(session: Session, dto: ColetaCreate) -> AmostraRead:
    """Registra a coleta: cria a amostra (cadeia de custódia) e vincula o coletor.

    Numa transação só: gera a amostra COLETADA com código de barras, grava a
    coleta com o usuário coletor e transiciona a OS para COLETADA (com histórico).
    A pendência logística (amostra_movimentacao) é aberta pela Stack B a partir
    daqui.
    """
    ordem = os_repository.obter_por_id(session, dto.ordem_servico_id)
    if ordem is None:
        raise OrdemServicoInexistente("Ordem de Serviço não encontrada")
    if ordem.status in _STATUS_OS_BLOQUEIA_COLETA:
        raise ColetaNaoPermitida("Ordem de Serviço não permite novas coletas")

    from src.atendimento.autorizacao.service import possui_autorizacao_valida
    if ordem.convenio_id is not None and not possui_autorizacao_valida(session, ordem.id):
        raise ColetaNaoPermitida("OS de convênio sem autorização válida")

    coletor = usuario_repository.obter_por_id(session, dto.coletor_usuario_id)
    if coletor is None or not coletor.ativo:
        raise ColetorInvalido("Coletor inválido ou inativo")

    from sqlalchemy import select
    from src.rbac.models import Perfil
    from src.rbac.repository import usuario_tem_permissao
    if session.scalar(select(Perfil.id).limit(1)) is not None:
        if not usuario_tem_permissao(session, coletor.id, "atendimento:coletar"):
            raise ColetorInvalido("Coletor sem permissão para registrar coleta")

    _processar_consumo_estoque(session, ordem)

    amostra = Amostra(
        ordem_servico_id=ordem.id,
        codigo_barras=_gerar_codigo_barras(session),
        tipo_material=dto.tipo_material,
        status=StatusAmostra.COLETADA,
    )
    repository.salvar_amostra(session, amostra)
    session.flush()

    repository.salvar_coleta(
        session, Coleta(amostra_id=amostra.id, coletor_id=coletor.id)
    )

    from src.logistica.recebimento.models import AmostraMovimentacao
    mov = AmostraMovimentacao(
        amostra_id=amostra.id,
        status=StatusAmostra.COLETADA,
        usuario_id=coletor.id,
        unidade_id=ordem.unidade_id,
        observacao="Coleta realizada na unidade",
    )
    session.add(mov)

    if ordem.status != StatusOrdemServico.COLETADA:
        os_service.registrar_transicao(session, ordem, StatusOrdemServico.COLETADA, coletor.id)

    registrar_auditoria(
        session,
        coletor.id,
        entidade="amostra",
        entidade_id=amostra.id,
        acao="REGISTRAR_COLETA",
        dados={
            "ordem_servico_id": str(ordem.id),
            "codigo_barras": amostra.codigo_barras,
        },
    )

    session.commit()
    session.refresh(amostra)
    return AmostraRead.model_validate(amostra)


def listar_amostras(session: Session, ordem_servico_id: UUID) -> list[AmostraRead]:
    return [AmostraRead.model_validate(a) for a in repository.listar_por_os(session, ordem_servico_id)]


def listar_amostras_coletadas(session: Session) -> list[AmostraRead]:
    return [AmostraRead.model_validate(a) for a in repository.listar_por_status(session, StatusAmostra.COLETADA)]


def _gerar_codigo_barras(session: Session) -> str:
    for _ in range(10):
        codigo = f"AM{uuid.uuid4().hex[:12].upper()}"
        if repository.obter_por_codigo_barras(session, codigo) is None:
            return codigo
    raise RuntimeError("Não foi possível gerar um código de barras único")


def _processar_consumo_estoque(session: Session, ordem) -> None:
    from collections import defaultdict
    from decimal import Decimal
    from sqlalchemy import select
    from src.atendimento.amostra.errors import EstoqueInsuficienteError
    from src.atendimento.ordem_servico.dtos import StatusOsItem
    from src.atendimento.ordem_servico import repository as os_repository
    from src.cadastro.procedimento.models import ProcedimentoInsumo
    from src.compras.insumo.dtos import TipoMovimentoEstoque
    from src.compras.insumo.models import EstoqueMovimento, InsumoMaterial

    itens = os_repository.listar_itens(session, ordem.id)
    itens_ativos = [i for i in itens if i.status != StatusOsItem.CANCELADO]
    if not itens_ativos:
        return

    insumos_necessarios: dict[UUID, Decimal] = defaultdict(Decimal)

    for item in itens_ativos:
        links = session.scalars(
            select(ProcedimentoInsumo).where(ProcedimentoInsumo.procedimento_id == item.procedimento_id)
        ).all()
        for link in links:
            insumos_necessarios[link.insumo_material_id] += link.quantidade_necessaria

    if not insumos_necessarios:
        return

    insumos_objs: dict[UUID, InsumoMaterial] = {}
    for insumo_id, qtd_nec in insumos_necessarios.items():
        insumo = session.get(InsumoMaterial, insumo_id)
        if insumo is not None:
            insumos_objs[insumo_id] = insumo
            if Decimal(str(insumo.quantidade_estoque)) < qtd_nec:
                raise EstoqueInsuficienteError(
                    f"Estoque insuficiente para o insumo '{insumo.nome}': necessário {qtd_nec}, disponível {insumo.quantidade_estoque}"
                )

    for insumo_id, qtd_nec in insumos_necessarios.items():
        insumo = insumos_objs.get(insumo_id)
        if insumo is not None:
            novo_estoque = Decimal(str(insumo.quantidade_estoque)) - qtd_nec
            insumo.quantidade_estoque = float(novo_estoque)
            session.add(
                EstoqueMovimento(
                    insumo_material_id=insumo.id,
                    tipo=TipoMovimentoEstoque.SAIDA,
                    quantidade=qtd_nec,
                    observacao=f"Consumo automático - Coleta OS {ordem.codigo_os}",
                )
            )

