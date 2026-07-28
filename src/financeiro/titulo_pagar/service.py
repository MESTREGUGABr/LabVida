from uuid import UUID

from sqlalchemy.orm import Session

from src.auditoria import registrar_auditoria
from src.financeiro.movimento_caixa.dtos import TipoMovimento
from src.financeiro.movimento_caixa.models import MovimentoCaixa
from src.financeiro.titulo_pagar import repository
from src.financeiro.titulo_pagar.dtos import StatusTitulo, TituloPagarRead
from src.financeiro.titulo_pagar.errors import TituloPagarJaBaixado, TituloPagarNaoEncontrado
from src.financeiro.titulo_receber.errors import FinanceiroError


def obter_titulo(session: Session, titulo_id: UUID) -> TituloPagarRead:
    titulo = repository.obter_por_id(session, titulo_id)
    if titulo is None:
        raise TituloPagarNaoEncontrado("Título a pagar não encontrado")
    return TituloPagarRead.model_validate(titulo)


def listar_todos(session: Session) -> list[TituloPagarRead]:
    return [TituloPagarRead.model_validate(t) for t in repository.listar_todos(session)]


def baixar_titulo(
    session: Session,
    titulo_id: UUID,
    observacao: str | None = None,
    usuario_id: UUID | None = None,
) -> TituloPagarRead:
    titulo = repository.obter_por_id(session, titulo_id)
    if titulo is None:
        raise TituloPagarNaoEncontrado("Título a pagar não encontrado")
    if titulo.status != StatusTitulo.PENDENTE:
        raise TituloPagarJaBaixado("Título já foi baixado ou cancelado")

    if usuario_id is not None:
        from sqlalchemy import select
        from src.rbac.models import Perfil
        from src.rbac.repository import usuario_tem_permissao
        if session.scalar(select(Perfil.id).limit(1)) is not None:
            if not usuario_tem_permissao(session, usuario_id, "financeiro:baixar_titulo"):
                from src.financeiro.titulo_receber.errors import FinanceiroError
                raise FinanceiroError("Usuário sem permissão para baixar título")

    titulo.status = StatusTitulo.PAGO

    movimento = MovimentoCaixa(
        titulo_pagar_id=titulo.id,
        tipo=TipoMovimento.SAIDA,
        valor=titulo.valor,
        descricao=observacao or f"Pagamento do título {titulo.id}",
    )
    session.add(movimento)

    if usuario_id is not None:
        registrar_auditoria(
            session,
            usuario_id,
            entidade="titulo_pagar",
            entidade_id=titulo.id,
            acao="BAIXAR_TITULO_PAGAR",
            dados={"valor": str(titulo.valor)},
        )

    session.commit()
    session.refresh(titulo)
    return TituloPagarRead.model_validate(titulo)
