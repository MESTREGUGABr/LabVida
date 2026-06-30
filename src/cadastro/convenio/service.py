from uuid import UUID

from sqlalchemy.orm import Session

from src.cadastro.convenio import repository
from src.cadastro.convenio.dtos import ConvenioCreate, ConvenioRead, StatusConvenio
from src.cadastro.convenio.errors import ConvenioNaoEncontrado
from src.cadastro.convenio.models import Convenio


def criar_convenio(session: Session, dto: ConvenioCreate) -> ConvenioRead:
    convenio = Convenio(
        nome=dto.nome,
        registro_ans=dto.registro_ans,
        status=StatusConvenio.ATIVO,
    )
    repository.salvar(session, convenio)
    session.commit()
    session.refresh(convenio)
    return ConvenioRead.model_validate(convenio)


def listar_convenios(session: Session) -> list[ConvenioRead]:
    return [ConvenioRead.model_validate(c) for c in repository.listar_ordenados_por_nome(session)]


def listar_convenios_ativos(session: Session) -> list[ConvenioRead]:
    return [ConvenioRead.model_validate(c) for c in repository.listar_ativos(session)]


def alternar_status(session: Session, convenio_id: UUID, ativo: bool) -> ConvenioRead:
    convenio = repository.obter_por_id(session, convenio_id)
    if convenio is None:
        raise ConvenioNaoEncontrado("Convênio não encontrado")
    convenio.status = StatusConvenio.ATIVO if ativo else StatusConvenio.INATIVO
    session.commit()
    session.refresh(convenio)
    return ConvenioRead.model_validate(convenio)
