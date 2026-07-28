from uuid import UUID

from sqlalchemy.orm import Session

from src.cadastro.convenio import repository
from src.cadastro.convenio.dtos import ConvenioCreate, ConvenioRead, ConvenioUpdate, StatusConvenio
from src.cadastro.convenio.errors import ConvenioNaoEncontrado
from src.cadastro.convenio.models import Convenio
from src.cadastro.errors import CnpjConvenioDuplicado, NomeConvenioDuplicado
from src.cadastro.repository import obter_convenio_por_cnpj, obter_convenio_por_nome_normalizado
from src.auditoria import registrar_auditoria


def criar_convenio(session: Session, dto: ConvenioCreate, usuario_id: UUID | None = None) -> ConvenioRead:
    nome_normalizado = dto.nome.casefold()

    if obter_convenio_por_nome_normalizado(session, nome_normalizado):
        raise NomeConvenioDuplicado("Convênio já cadastrado com este nome")

    if dto.cnpj and obter_convenio_por_cnpj(session, dto.cnpj):
        raise CnpjConvenioDuplicado("Convênio já cadastrado com este CNPJ")

    convenio = Convenio(
        nome=dto.nome,
        nome_normalizado=nome_normalizado,
        cnpj=dto.cnpj,
        telefone=dto.telefone,
        email=dto.email,
        registro_ans=dto.registro_ans,
        ativo=True,
        status=StatusConvenio.ATIVO,
    )
    repository.salvar(session, convenio)
    session.commit()
    session.refresh(convenio)

    if usuario_id is not None:
        registrar_auditoria(session, usuario_id, entidade="convenio",
            entidade_id=convenio.id, acao="CRIAR_CONVENIO",
            dados={"nome": convenio.nome})

    return ConvenioRead.model_validate(convenio)


def listar_convenios(session: Session) -> list[ConvenioRead]:
    return [ConvenioRead.model_validate(c) for c in repository.listar_ordenados_por_nome(session)]


def listar_convenios_ativos(session: Session) -> list[ConvenioRead]:
    return [ConvenioRead.model_validate(c) for c in repository.listar_ativos(session)]


def obter_convenio_por_id(session: Session, convenio_id: UUID) -> ConvenioRead:
    convenio = _obter_convenio_ou_falhar(session, convenio_id)
    return ConvenioRead.model_validate(convenio)


def alternar_status(session: Session, convenio_id: UUID, ativo: bool, usuario_id: UUID | None = None) -> ConvenioRead:
    convenio = _obter_convenio_ou_falhar(session, convenio_id)
    convenio.ativo = ativo
    convenio.status = StatusConvenio.ATIVO if ativo else StatusConvenio.INATIVO
    session.commit()
    session.refresh(convenio)

    if usuario_id is not None:
        registrar_auditoria(session, usuario_id, entidade="convenio",
            entidade_id=convenio.id, acao="ALTERAR_STATUS_CONVENIO",
            dados={"nome": convenio.nome, "ativo": ativo})

    return ConvenioRead.model_validate(convenio)


def atualizar_convenio(session: Session, convenio_id: UUID, dto: ConvenioUpdate) -> ConvenioRead:
    convenio = _obter_convenio_ou_falhar(session, convenio_id)

    if dto.nome is not None:
        nome_normalizado = dto.nome.casefold()
        convenio_com_nome = obter_convenio_por_nome_normalizado(session, nome_normalizado)
        if convenio_com_nome and convenio_com_nome.id != convenio.id:
            raise NomeConvenioDuplicado("Convênio já cadastrado com este nome")
        convenio.nome = dto.nome
        convenio.nome_normalizado = nome_normalizado

    if "cnpj" in dto.model_fields_set:
        if dto.cnpj is not None:
            convenio_com_cnpj = obter_convenio_por_cnpj(session, dto.cnpj)
            if convenio_com_cnpj and convenio_com_cnpj.id != convenio.id:
                raise CnpjConvenioDuplicado("Convênio já cadastrado com este CNPJ")
        convenio.cnpj = dto.cnpj

    if "telefone" in dto.model_fields_set:
        convenio.telefone = dto.telefone
    if "email" in dto.model_fields_set:
        convenio.email = dto.email
    if dto.ativo is not None:
        convenio.ativo = dto.ativo
        convenio.status = StatusConvenio.ATIVO if dto.ativo else StatusConvenio.INATIVO

    session.commit()
    session.refresh(convenio)
    return ConvenioRead.model_validate(convenio)


def inativar_convenio(session: Session, convenio_id: UUID) -> None:
    convenio = _obter_convenio_ou_falhar(session, convenio_id)
    convenio.ativo = False
    convenio.status = StatusConvenio.INATIVO
    session.commit()


def _obter_convenio_ou_falhar(session: Session, convenio_id: UUID) -> Convenio:
    convenio = repository.obter_por_id(session, convenio_id)
    if convenio is None:
        raise ConvenioNaoEncontrado("Convênio não encontrado")
    return convenio
