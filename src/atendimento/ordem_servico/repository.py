from uuid import UUID

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from src.atendimento.ordem_servico.models import OrdemServico, OsItem, OsStatusHistorico
from src.cadastro.models import Paciente
from src.faturamento.lote_faturamento.models import GuiaItem
from src.laboratorial.models import Laudo, StatusLaudo


def obter_por_id(session: Session, ordem_servico_id: UUID) -> OrdemServico | None:
    return session.get(OrdemServico, ordem_servico_id)


def obter_por_codigo(session: Session, codigo_os: str) -> OrdemServico | None:
    return session.scalar(select(OrdemServico).where(OrdemServico.codigo_os == codigo_os))


def obter_item_por_id(session: Session, os_item_id: UUID) -> OsItem | None:
    return session.get(OsItem, os_item_id)


def listar(session: Session, limite: int = 100) -> list[OrdemServico]:
    return list(
        session.scalars(select(OrdemServico).order_by(OrdemServico.aberta_em.desc()).limit(limite))
    )


def _filtro_os(stmt, busca: str | None, status: str | None):
    """Aplica busca (código da OS ou nome do paciente) e filtro de status a um select."""
    if busca:
        termo = f"%{busca.strip()}%"
        stmt = stmt.outerjoin(Paciente, Paciente.id == OrdemServico.paciente_id).where(
            or_(OrdemServico.codigo_os.ilike(termo), Paciente.nome.ilike(termo))
        )
    if status:
        stmt = stmt.where(OrdemServico.status == status)
    return stmt


def contar_filtrado(session: Session, busca: str | None = None, status: str | None = None) -> int:
    stmt = _filtro_os(select(func.count(OrdemServico.id)).select_from(OrdemServico), busca, status)
    return session.scalar(stmt) or 0


def listar_filtrado(
    session: Session,
    busca: str | None = None,
    status: str | None = None,
    limite: int = 20,
    offset: int = 0,
) -> list[OrdemServico]:
    stmt = _filtro_os(select(OrdemServico), busca, status)
    stmt = stmt.order_by(OrdemServico.aberta_em.desc()).limit(limite).offset(offset)
    return list(session.scalars(stmt))


def listar_por_status(session: Session, status: str) -> list[OrdemServico]:
    return list(
        session.scalars(
            select(OrdemServico)
            .where(OrdemServico.status == status)
            .order_by(OrdemServico.aberta_em.desc())
        )
    )


def salvar(session: Session, ordem_servico: OrdemServico) -> None:
    session.add(ordem_servico)


def salvar_item(session: Session, item: OsItem) -> None:
    session.add(item)


def listar_itens(session: Session, ordem_servico_id: UUID) -> list[OsItem]:
    return list(
        session.scalars(select(OsItem).where(OsItem.ordem_servico_id == ordem_servico_id))
    )


def item_tem_laudo_liberado(session: Session, os_item_id: UUID) -> bool:
    return session.scalar(
        select(Laudo.id).where(
            Laudo.os_item_id == os_item_id,
            Laudo.status == StatusLaudo.LIBERADO,
        )
    ) is not None


def item_faturado(session: Session, item: OsItem) -> bool:
    return item.status == "FATURADO" or session.scalar(
        select(GuiaItem.id).where(
            GuiaItem.status == "FATURADO",
            GuiaItem.laudo_id.in_(select(Laudo.id).where(Laudo.os_item_id == item.id)),
        )
    ) is not None


def salvar_historico(session: Session, historico: OsStatusHistorico) -> None:
    session.add(historico)


def listar_historico(session: Session, ordem_servico_id: UUID) -> list[OsStatusHistorico]:
    return list(
        session.scalars(
            select(OsStatusHistorico)
            .where(OsStatusHistorico.ordem_servico_id == ordem_servico_id)
            .order_by(OsStatusHistorico.ocorrido_em)
        )
    )
