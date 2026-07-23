from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.atendimento.ordem_servico.models import OrdemServico, OsItem
from src.cadastro.convenio.models import Convenio
from src.cadastro.procedimento.models import Procedimento
from src.cadastro.unidade.models import Unidade
from src.faturamento.glosa.models import Glosa
from src.faturamento.lote_faturamento.models import GuiaItem, GuiaTiss, LoteFaturamento
from src.laboratorial.models import Laudo


def salvar_glosa(session: Session, glosa: Glosa) -> Glosa:
    session.add(glosa)
    return glosa


def obter_glosa_por_id(session: Session, glosa_id: UUID) -> Glosa | None:
    return session.get(Glosa, glosa_id)


def listar_glosas_por_unidade(session: Session, unidade_origem_id: UUID) -> list[Glosa]:
    stmt = select(Glosa).where(Glosa.unidade_origem_id == unidade_origem_id).order_by(Glosa.criado_em.desc())
    return list(session.scalars(stmt).all())


def listar_glosas_por_guia_item(session: Session, guia_item_id: UUID) -> list[Glosa]:
    stmt = select(Glosa).where(Glosa.guia_item_id == guia_item_id).order_by(Glosa.criado_em.desc())
    return list(session.scalars(stmt).all())


def listar_guias_itens_faturados(session: Session) -> list[dict]:
    stmt = (
        select(
            GuiaItem.id,
            GuiaItem.laudo_id,
            GuiaItem.valor_faturado,
            LoteFaturamento.codigo_lote,
            LoteFaturamento.convenio_id,
            Convenio.nome.label("convenio_nome"),
            Procedimento.nome.label("procedimento_nome"),
            OrdemServico.unidade_id,
            Unidade.nome.label("unidade_nome"),
        )
        .join(GuiaTiss, GuiaItem.guia_tiss_id == GuiaTiss.id)
        .join(LoteFaturamento, GuiaTiss.lote_faturamento_id == LoteFaturamento.id)
        .join(Convenio, LoteFaturamento.convenio_id == Convenio.id)
        .join(Procedimento, GuiaItem.procedimento_id == Procedimento.id)
        .join(Laudo, GuiaItem.laudo_id == Laudo.id)
        .join(OsItem, Laudo.os_item_id == OsItem.id)
        .join(OrdemServico, OsItem.ordem_servico_id == OrdemServico.id)
        .join(Unidade, OrdemServico.unidade_id == Unidade.id)
        .order_by(GuiaItem.criado_em.desc())
    )
    results = session.execute(stmt).all()
    return [
        {
            "guia_item_id": r.id,
            "laudo_id": r.laudo_id,
            "valor_faturado": r.valor_faturado,
            "codigo_lote": r.codigo_lote,
            "convenio_id": r.convenio_id,
            "convenio_nome": r.convenio_nome,
            "procedimento_nome": r.procedimento_nome,
            "unidade_id": r.unidade_id,
            "unidade_nome": r.unidade_nome,
        }
        for r in results
    ]


def listar_glosas_com_contexto(session: Session) -> list[dict]:
    stmt = (
        select(
            Glosa.id,
            Glosa.guia_item_id,
            Glosa.motivo,
            Glosa.valor_glosado,
            Glosa.criado_em,
            GuiaItem.valor_faturado,
            LoteFaturamento.codigo_lote,
            Convenio.nome.label("convenio_nome"),
            Procedimento.nome.label("procedimento_nome"),
            Unidade.nome.label("unidade_nome"),
        )
        .join(GuiaItem, Glosa.guia_item_id == GuiaItem.id)
        .join(GuiaTiss, GuiaItem.guia_tiss_id == GuiaTiss.id)
        .join(LoteFaturamento, GuiaTiss.lote_faturamento_id == LoteFaturamento.id)
        .join(Convenio, LoteFaturamento.convenio_id == Convenio.id)
        .join(Procedimento, GuiaItem.procedimento_id == Procedimento.id)
        .join(Laudo, GuiaItem.laudo_id == Laudo.id)
        .join(OsItem, Laudo.os_item_id == OsItem.id)
        .join(OrdemServico, OsItem.ordem_servico_id == OrdemServico.id)
        .join(Unidade, OrdemServico.unidade_id == Unidade.id)
        .order_by(Glosa.criado_em.desc())
    )
    results = session.execute(stmt).all()
    return [
        {
            "glosa_id": r.id,
            "guia_item_id": r.guia_item_id,
            "motivo": r.motivo,
            "valor_glosado": r.valor_glosado,
            "criado_em": r.criado_em,
            "valor_faturado": r.valor_faturado,
            "codigo_lote": r.codigo_lote,
            "convenio_nome": r.convenio_nome,
            "procedimento_nome": r.procedimento_nome,
            "unidade_nome": r.unidade_nome,
        }
        for r in results
    ]
