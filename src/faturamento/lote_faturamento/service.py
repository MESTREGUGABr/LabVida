import uuid
from datetime import date, datetime, timedelta, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from src.cadastro.convenio import repository as convenio_repository
from src.cadastro.convenio.dtos import StatusConvenio
from src.faturamento.lote_faturamento import repository
from src.faturamento.lote_faturamento.dtos import (
    GuiaItemCreate,
    LoteFaturamentoCreate,
    LoteFaturamentoRead,
    StatusLote,
)
from src.faturamento.lote_faturamento.errors import (
    ConvenioInvalidoParaLote,
    ConvenioNaoConfereComLaudo,
    LaudoJaFaturado,
    LaudoNaoLiberado,
    LoteJaFechado,
    LoteNaoEncontrado,
    LoteSemItens,
    ValorFaturadoInvalido,
)
from src.faturamento.lote_faturamento.models import GuiaItem, GuiaTiss, LoteFaturamento
from src.financeiro.titulo_receber.models import TituloReceber
from src.laboratorial.models import Laudo, StatusLaudo


def _agora() -> datetime:
    return datetime.now(timezone.utc)


def criar_lote(session: Session, dto: LoteFaturamentoCreate) -> LoteFaturamentoRead:
    convenio = convenio_repository.obter_por_id(session, dto.convenio_id)
    if convenio is None or convenio.status != StatusConvenio.ATIVO:
        raise ConvenioInvalidoParaLote("Convênio inválido ou inativo")

    lote = LoteFaturamento(
        codigo_lote=_gerar_codigo_lote(session),
        convenio_id=dto.convenio_id,
        status=StatusLote.ABERTO,
    )
    repository.salvar_lote(session, lote)
    session.commit()
    session.refresh(lote)
    return LoteFaturamentoRead.model_validate(lote)


def adicionar_guia_item(session: Session, lote_id: UUID, dto: GuiaItemCreate) -> LoteFaturamentoRead:
    if dto.valor_faturado <= 0:
        raise ValorFaturadoInvalido("Valor faturado deve ser maior que zero")

    lote = repository.obter_lote_por_id(session, lote_id)
    if lote is None:
        raise LoteNaoEncontrado("Lote de faturamento não encontrado")
    if lote.status != StatusLote.ABERTO:
        raise LoteJaFechado("Não é possível adicionar itens a um lote fechado")

    existente = repository.obter_item_por_laudo(session, dto.laudo_id)
    if existente is not None:
        raise LaudoJaFaturado("Este laudo já foi faturado")

    laudo = session.get(Laudo, dto.laudo_id)
    if laudo is None or laudo.status != StatusLaudo.LIBERADO:
        raise LaudoNaoLiberado("Apenas laudos com status LIBERADO podem ser faturados")

    convenio_do_laudo = _convenio_do_laudo(session, laudo)
    if convenio_do_laudo is None or convenio_do_laudo != lote.convenio_id:
        raise ConvenioNaoConfereComLaudo(
            "O convênio do laudo não confere com o convênio do lote de faturamento"
        )

    guia = _obter_ou_criar_guia(session, lote)

    item = GuiaItem(
        guia_tiss_id=guia.id,
        laudo_id=dto.laudo_id,
        procedimento_id=dto.procedimento_id,
        valor_faturado=dto.valor_faturado,
    )
    repository.salvar_guia_item(session, item)

    lote.valor_total += dto.valor_faturado

    session.commit()
    session.refresh(lote)
    return LoteFaturamentoRead.model_validate(lote)


def fechar_lote(session: Session, lote_id: UUID, usuario_id: UUID | None = None) -> LoteFaturamentoRead:
    lote = repository.obter_lote_por_id(session, lote_id)
    if lote is None:
        raise LoteNaoEncontrado("Lote de faturamento não encontrado")
    if lote.status != StatusLote.ABERTO:
        raise LoteJaFechado("Lote já foi fechado")

    tem_itens = any(len(g.itens) > 0 for g in lote.guias)
    if not tem_itens:
        raise LoteSemItens("Não é possível fechar um lote sem itens faturados")

    lote.status = StatusLote.FECHADO
    lote.fechado_em = _agora()

    titulo = TituloReceber(
        lote_faturamento_id=lote.id,
        valor=lote.valor_total,
        vencimento=date.today() + timedelta(days=30),
        status="PENDENTE",
    )
    session.add(titulo)

    session.commit()
    session.refresh(lote)
    return LoteFaturamentoRead.model_validate(lote)


def obter_lote(session: Session, lote_id: UUID) -> LoteFaturamentoRead:
    lote = repository.obter_lote_por_id(session, lote_id)
    if lote is None:
        raise LoteNaoEncontrado("Lote de faturamento não encontrado")
    return LoteFaturamentoRead.model_validate(lote)


def adicionar_itens_ao_lote(session: Session, lote_id: UUID, itens: list[GuiaItemCreate]) -> LoteFaturamentoRead:
    lote = repository.obter_lote_por_id(session, lote_id)
    if lote is None:
        raise LoteNaoEncontrado("Lote de faturamento não encontrado")
    if lote.status != StatusLote.ABERTO:
        raise LoteJaFechado("Não é possível adicionar itens a um lote fechado")

    guia = _obter_ou_criar_guia(session, lote)

    for dto in itens:
        if dto.valor_faturado <= 0:
            raise ValorFaturadoInvalido(f"Valor faturado inválido: {dto.valor_faturado}")
        existente = repository.obter_item_por_laudo(session, dto.laudo_id)
        if existente is not None:
            raise LaudoJaFaturado(f"Laudo {dto.laudo_id} já foi faturado")
        laudo = session.get(Laudo, dto.laudo_id)
        if laudo is None or laudo.status != StatusLaudo.LIBERADO:
            raise LaudoNaoLiberado(f"Laudo {dto.laudo_id} não está liberado")
        convenio_do_laudo = _convenio_do_laudo(session, laudo)
        if convenio_do_laudo is None or convenio_do_laudo != lote.convenio_id:
            raise ConvenioNaoConfereComLaudo(
                f"Convênio do laudo {dto.laudo_id} não confere com o convênio do lote"
            )
        item = GuiaItem(
            guia_tiss_id=guia.id,
            laudo_id=dto.laudo_id,
            procedimento_id=dto.procedimento_id,
            valor_faturado=dto.valor_faturado,
        )
        repository.salvar_guia_item(session, item)
        lote.valor_total += dto.valor_faturado

    session.commit()
    session.refresh(lote)
    return LoteFaturamentoRead.model_validate(lote)


def listar_lotes(session: Session) -> list[LoteFaturamentoRead]:
    return [LoteFaturamentoRead.model_validate(l) for l in repository.listar_lotes(session)]


def contar_laudos_pendentes(session: Session, convenio_id: UUID) -> int:
    return repository.contar_laudos_pendentes_por_convenio(session, convenio_id)


def listar_laudos_pendentes_por_convenio(session: Session, convenio_id: UUID) -> list[dict]:
    return repository.listar_laudos_liberados_por_convenio(session, convenio_id)


def _convenio_do_laudo(session: Session, laudo: Laudo) -> UUID | None:
    from src.atendimento.ordem_servico.models import OrdemServico, OsItem

    stmt = (
        select(OrdemServico.convenio_id)
        .join(OsItem, OsItem.ordem_servico_id == OrdemServico.id)
        .where(OsItem.id == laudo.os_item_id)
    )
    return session.execute(stmt).scalar_one_or_none()


def _obter_ou_criar_guia(session: Session, lote: LoteFaturamento) -> GuiaTiss:
    if lote.guias:
        return lote.guias[0]
    guia = GuiaTiss(
        lote_faturamento_id=lote.id,
        codigo_tiss=_gerar_codigo_tiss(session),
    )
    repository.salvar_guia(session, guia)
    session.flush()
    return guia


def _gerar_codigo_lote(session: Session) -> str:
    ano = datetime.now(timezone.utc).year
    for _ in range(10):
        codigo = f"LT-{ano}-{uuid.uuid4().hex[:6].upper()}"
        if repository.obter_lote_por_codigo(session, codigo) is None:
            return codigo
    raise RuntimeError("Não foi possível gerar um código de lote único")


def _gerar_codigo_tiss(session: Session) -> str:
    return f"TISS-{uuid.uuid4().hex[:12].upper()}"
