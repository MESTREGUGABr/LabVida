from uuid import UUID

from sqlalchemy.orm import Session

from src.cadastro.dtos import PacienteCreate, PacienteRead, PacienteUpdate
from src.cadastro.errors import CpfPacienteDuplicado, PacienteNaoEncontrado
from src.cadastro.models import Paciente
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
