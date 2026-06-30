from uuid import UUID

from sqlalchemy.orm import Session

from src.cadastro.dtos import ConvenioCreate, ConvenioRead, ConvenioUpdate, PacienteCreate, PacienteRead, PacienteUpdate
from src.cadastro.errors import (
    CnpjConvenioDuplicado,
    ConvenioNaoEncontrado,
    CpfPacienteDuplicado,
    NomeConvenioDuplicado,
    PacienteNaoEncontrado,
)
from src.cadastro.models import Convenio, Paciente
from src.cadastro import repository


def criar_paciente(session: Session, dto: PacienteCreate) -> PacienteRead:
    if repository.obter_por_cpf(session, dto.cpf):
        raise CpfPacienteDuplicado("Paciente já cadastrado com este CPF")

    paciente = Paciente(
        cpf=dto.cpf,
        nome=dto.nome,
        data_nascimento=dto.data_nascimento,
        telefone=dto.telefone,
        sexo=dto.sexo,
        ativo=True,
    )
    repository.salvar(session, paciente)
    session.commit()
    session.refresh(paciente)
    return PacienteRead.model_validate(paciente)


def listar_pacientes_ativos(session: Session) -> list[PacienteRead]:
    return [PacienteRead.model_validate(paciente) for paciente in repository.listar_ativos_ordenados_por_nome(session)]


def obter_paciente_por_id(session: Session, paciente_id: UUID) -> PacienteRead:
    paciente = _obter_paciente_ou_falhar(session, paciente_id)
    return PacienteRead.model_validate(paciente)


def atualizar_paciente(session: Session, paciente_id: UUID, dto: PacienteUpdate) -> PacienteRead:
    paciente = _obter_paciente_ou_falhar(session, paciente_id)

    if dto.cpf is not None and dto.cpf != paciente.cpf:
        paciente_com_cpf = repository.obter_por_cpf(session, dto.cpf)
        if paciente_com_cpf and paciente_com_cpf.id != paciente.id:
            raise CpfPacienteDuplicado("Paciente já cadastrado com este CPF")
        paciente.cpf = dto.cpf

    if dto.nome is not None:
        paciente.nome = dto.nome
    if dto.data_nascimento is not None:
        paciente.data_nascimento = dto.data_nascimento
    if dto.telefone is not None:
        paciente.telefone = dto.telefone
    if dto.sexo is not None:
        paciente.sexo = dto.sexo

    session.commit()
    session.refresh(paciente)
    return PacienteRead.model_validate(paciente)


def inativar_paciente(session: Session, paciente_id: UUID) -> None:
    paciente = _obter_paciente_ou_falhar(session, paciente_id)
    paciente.ativo = False
    session.commit()


def _obter_paciente_ou_falhar(session: Session, paciente_id: UUID) -> Paciente:
    paciente = repository.obter_por_id(session, paciente_id)
    if not paciente:
        raise PacienteNaoEncontrado("Paciente não encontrado")
    return paciente


def criar_convenio(session: Session, dto: ConvenioCreate) -> ConvenioRead:
    nome_normalizado = _normalizar_nome_unico(dto.nome)
    if repository.obter_convenio_por_nome_normalizado(session, nome_normalizado):
        raise NomeConvenioDuplicado("Convênio já cadastrado com este nome")
    if dto.cnpj and repository.obter_convenio_por_cnpj(session, dto.cnpj):
        raise CnpjConvenioDuplicado("Convênio já cadastrado com este CNPJ")

    convenio = Convenio(
        nome=dto.nome,
        nome_normalizado=nome_normalizado,
        cnpj=dto.cnpj,
        telefone=dto.telefone,
        email=dto.email,
        ativo=True,
    )
    repository.salvar_convenio(session, convenio)
    session.commit()
    session.refresh(convenio)
    return ConvenioRead.model_validate(convenio)


def listar_convenios(session: Session) -> list[ConvenioRead]:
    return [ConvenioRead.model_validate(convenio) for convenio in repository.listar_convenios_ordenados_por_nome(session)]


def obter_convenio_por_id(session: Session, convenio_id: UUID) -> ConvenioRead:
    convenio = _obter_convenio_ou_falhar(session, convenio_id)
    return ConvenioRead.model_validate(convenio)


def atualizar_convenio(session: Session, convenio_id: UUID, dto: ConvenioUpdate) -> ConvenioRead:
    convenio = _obter_convenio_ou_falhar(session, convenio_id)

    if dto.nome is not None:
        nome_normalizado = _normalizar_nome_unico(dto.nome)
        convenio_com_nome = repository.obter_convenio_por_nome_normalizado(session, nome_normalizado)
        if convenio_com_nome and convenio_com_nome.id != convenio.id:
            raise NomeConvenioDuplicado("Convênio já cadastrado com este nome")
        convenio.nome = dto.nome
        convenio.nome_normalizado = nome_normalizado

    if "cnpj" in dto.model_fields_set and dto.cnpj != convenio.cnpj:
        if dto.cnpj is not None:
            convenio_com_cnpj = repository.obter_convenio_por_cnpj(session, dto.cnpj)
            if convenio_com_cnpj and convenio_com_cnpj.id != convenio.id:
                raise CnpjConvenioDuplicado("Convênio já cadastrado com este CNPJ")
        convenio.cnpj = dto.cnpj

    if "telefone" in dto.model_fields_set:
        convenio.telefone = dto.telefone
    if "email" in dto.model_fields_set:
        convenio.email = dto.email
    if "ativo" in dto.model_fields_set:
        convenio.ativo = dto.ativo

    session.commit()
    session.refresh(convenio)
    return ConvenioRead.model_validate(convenio)


def inativar_convenio(session: Session, convenio_id: UUID) -> None:
    convenio = _obter_convenio_ou_falhar(session, convenio_id)
    convenio.ativo = False
    session.commit()


def _obter_convenio_ou_falhar(session: Session, convenio_id: UUID) -> Convenio:
    convenio = repository.obter_convenio_por_id(session, convenio_id)
    if not convenio:
        raise ConvenioNaoEncontrado("Convênio não encontrado")
    return convenio


def _normalizar_nome_unico(nome: str) -> str:
    return nome.casefold()
