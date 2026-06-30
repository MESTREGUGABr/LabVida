from collections.abc import Iterator
from uuid import uuid4

import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.cadastro.convenio.dtos import ConvenioCreate, StatusConvenio
from src.cadastro.convenio.service import alternar_status, criar_convenio
from src.cadastro.medico.dtos import MedicoCreate
from src.cadastro.medico.errors import CrmDuplicado
from src.cadastro.medico.service import criar_medico
from src.cadastro.procedimento.dtos import ProcedimentoCreate
from src.cadastro.procedimento.errors import CodigoTussDuplicado
from src.cadastro.procedimento.service import criar_procedimento
from src.cadastro.unidade.dtos import SetorCreate, TipoUnidade, UnidadeCreate
from src.cadastro.unidade.errors import UnidadeNaoEncontrada
from src.cadastro.unidade.service import criar_setor, criar_unidade, listar_setores_ativos
from src.db import session_scope


_TABELAS = ("procedimento_valores", "procedimentos", "medicos", "convenios", "setores", "unidades")


@pytest.fixture()
def session() -> Iterator[Session]:
    with session_scope() as session:
        session.execute(text("TRUNCATE " + ", ".join(_TABELAS) + " RESTART IDENTITY CASCADE"))
        session.commit()
        yield session
        session.execute(text("TRUNCATE " + ", ".join(_TABELAS) + " RESTART IDENTITY CASCADE"))
        session.commit()


def test_procedimento_rejeita_tuss_duplicado(session: Session) -> None:
    criar_procedimento(session, ProcedimentoCreate(codigo_tuss="40302016", nome="Hemograma"))

    with pytest.raises(CodigoTussDuplicado):
        criar_procedimento(session, ProcedimentoCreate(codigo_tuss="40302016", nome="Outro"))


def test_medico_rejeita_crm_uf_duplicado(session: Session) -> None:
    criar_medico(session, MedicoCreate(nome="Dra. Helena", crm="12345", uf_crm="PE"))

    with pytest.raises(CrmDuplicado):
        criar_medico(session, MedicoCreate(nome="Outro", crm="12345", uf_crm="PE"))


def test_medico_mesmo_crm_uf_diferente_e_permitido(session: Session) -> None:
    criar_medico(session, MedicoCreate(nome="Dra. Helena", crm="12345", uf_crm="PE"))
    medico = criar_medico(session, MedicoCreate(nome="Dr. João", crm="12345", uf_crm="SP"))

    assert medico.uf_crm == "SP"


def test_convenio_alternar_status(session: Session) -> None:
    convenio = criar_convenio(session, ConvenioCreate(nome="Unimed"))
    assert convenio.status == StatusConvenio.ATIVO

    inativado = alternar_status(session, convenio.id, ativo=False)
    assert inativado.status == StatusConvenio.INATIVO


def test_setor_exige_unidade_existente(session: Session) -> None:
    with pytest.raises(UnidadeNaoEncontrada):
        criar_setor(session, SetorCreate(unidade_id=uuid4(), nome="Coleta"))


def test_setor_vinculado_a_unidade(session: Session) -> None:
    unidade = criar_unidade(session, UnidadeCreate(nome="Central", tipo=TipoUnidade.CENTRAL))
    criar_setor(session, SetorCreate(unidade_id=unidade.id, nome="Hematologia"))

    setores = listar_setores_ativos(session, unidade.id)
    assert [s.nome for s in setores] == ["Hematologia"]
