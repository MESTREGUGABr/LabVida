from decimal import Decimal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.auditoria import registrar_auditoria
from src.atendimento.ordem_servico.models import OrdemServico, OsItem
from src.faturamento.glosa import repository
from src.faturamento.glosa.dtos import GlosaCreate, GlosaListagemRead, GlosaRead
from src.faturamento.glosa.errors import GuiaItemNaoEncontrado, ValorGlosaExcedeFaturado
from src.faturamento.glosa.models import Glosa
from src.faturamento.lote_faturamento import repository as faturamento_repository
from src.faturamento.lote_faturamento.dtos import StatusGuiaItem
from src.laboratorial.models import Laudo


def registrar_glosa(
    session: Session, dto: GlosaCreate, usuario_id: UUID | None = None
) -> GlosaRead:
    guia_item = faturamento_repository.obter_guia_item_por_id(session, dto.guia_item_id)
    if guia_item is None:
        raise GuiaItemNaoEncontrado("Guia Item não encontrado")

    # O DTO traz float e a coluna é Numeric: comparar direto reprova a glosa
    # integral, porque float(30.87) é maior que Decimal("30.87").
    valor_glosado = Decimal(str(dto.valor_glosado))
    valor_faturado = Decimal(str(guia_item.valor_faturado))

    if valor_glosado <= 0:
        raise ValueError("Valor da glosa deve ser maior que zero")
    if valor_glosado > valor_faturado:
        raise ValorGlosaExcedeFaturado("Valor da glosa excede o valor faturado do item")

    unidade_id = _unidade_do_guia_item(session, guia_item.laudo_id)
    if unidade_id is None:
        raise GuiaItemNaoEncontrado("Não foi possível determinar a unidade de origem do item")

    glosa = Glosa(
        guia_item_id=dto.guia_item_id,
        motivo=dto.motivo,
        valor_glosado=valor_glosado,
        unidade_origem_id=unidade_id,
    )
    repository.salvar_glosa(session, glosa)

    if valor_glosado >= valor_faturado:
        guia_item.status = StatusGuiaItem.GLOSADO

    if usuario_id is not None:
        registrar_auditoria(
            session,
            usuario_id,
            entidade="glosa",
            entidade_id=guia_item.id,
            acao="REGISTRAR_GLOSA",
            dados={
                "guia_item_id": str(dto.guia_item_id),
                "valor_glosado": str(dto.valor_glosado),
                "motivo": dto.motivo,
            },
        )

    session.commit()
    session.refresh(glosa)
    return GlosaRead.model_validate(glosa)


def listar_glosas_por_unidade(session: Session, unidade_origem_id: UUID) -> list[GlosaRead]:
    return [GlosaRead.model_validate(g) for g in repository.listar_glosas_por_unidade(session, unidade_origem_id)]


def listar_glosas_por_guia_item(session: Session, guia_item_id: UUID) -> list[GlosaRead]:
    return [GlosaRead.model_validate(g) for g in repository.listar_glosas_por_guia_item(session, guia_item_id)]


def listar_guias_itens_faturados(session: Session) -> list[dict]:
    return repository.listar_guias_itens_faturados(session)


def listar_glosas_com_contexto(session: Session) -> list[GlosaListagemRead]:
    resultados = repository.listar_glosas_com_contexto(session)
    return [
        GlosaListagemRead(
            id=r["glosa_id"],
            guia_item_id=r["guia_item_id"],
            codigo_lote=r["codigo_lote"],
            convenio_nome=r["convenio_nome"],
            procedimento_nome=r["procedimento_nome"],
            motivo=r["motivo"],
            valor_glosado=r["valor_glosado"],
            valor_faturado=r["valor_faturado"],
            criado_em=r["criado_em"],
        )
        for r in resultados
    ]


def _unidade_do_guia_item(session: Session, laudo_id: UUID) -> UUID | None:
    stmt = (
        select(OrdemServico.unidade_id)
        .join(OsItem, OsItem.ordem_servico_id == OrdemServico.id)
        .join(Laudo, Laudo.os_item_id == OsItem.id)
        .where(Laudo.id == laudo_id)
    )
    return session.execute(stmt).scalar_one_or_none()
