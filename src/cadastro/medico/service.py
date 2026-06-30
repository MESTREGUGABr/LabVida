from sqlalchemy.orm import Session

from src.cadastro.medico import repository
from src.cadastro.medico.dtos import MedicoCreate, MedicoRead
from src.cadastro.medico.errors import CrmDuplicado
from src.cadastro.medico.models import Medico


def criar_medico(session: Session, dto: MedicoCreate) -> MedicoRead:
    if repository.obter_por_crm(session, dto.crm, dto.uf_crm):
        raise CrmDuplicado("Médico já cadastrado com este CRM/UF")

    medico = Medico(
        nome=dto.nome,
        crm=dto.crm,
        uf_crm=dto.uf_crm,
        responsavel_tecnico=dto.responsavel_tecnico,
        ativo=True,
    )
    repository.salvar(session, medico)
    session.commit()
    session.refresh(medico)
    return MedicoRead.model_validate(medico)


def listar_medicos_ativos(session: Session) -> list[MedicoRead]:
    return [MedicoRead.model_validate(m) for m in repository.listar_ativos(session)]
