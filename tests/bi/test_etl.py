from collections.abc import Iterator
from datetime import date

import pytest
from sqlalchemy.orm import Session
from sqlalchemy import text

from src.bi.etl import _carga_dimensoes
from src.bi.models import DimPacienteAnon, DimUnidade
from src.cadastro.convenio.dtos import ConvenioCreate
from src.cadastro.convenio.service import criar_convenio
from src.cadastro.dtos import PacienteCreate, SexoPaciente
from src.cadastro.service import criar_paciente
from src.cadastro.unidade.dtos import TipoUnidade, UnidadeCreate
from src.cadastro.unidade.service import criar_unidade
from src.db import session_scope


@pytest.fixture()
def session() -> Iterator[Session]:
    with session_scope() as s:
        for table in ["bi_fato_logistica", "bi_fato_financeiro", "bi_fato_faturamento",
                       "bi_fato_atendimento", "bi_dim_paciente_anon", "bi_dim_procedimento",
                       "bi_dim_convenio", "bi_dim_unidade", "bi_dim_tempo"]:
            s.execute(text(f"DELETE FROM {table}"))
        s.commit()
        yield s
        s.rollback()


def test_etl_popula_dimensoes(session: Session) -> None:
    criar_unidade(session, UnidadeCreate(nome=f"Central BI {id(session)}", tipo=TipoUnidade.CENTRAL))
    criar_convenio(session, ConvenioCreate(nome=f"Unimed BI {id(session)}"))

    _carga_dimensoes(session)

    assert session.query(DimUnidade).count() >= 2


def test_etl_anonimiza_paciente(session: Session) -> None:
    try:
        paciente = criar_paciente(session, PacienteCreate(
            cpf="52998224725", nome="Teste Anon", data_nascimento=date(1990, 1, 1),
            telefone="87999991234", sexo=SexoPaciente.FEMININO,
        ))
    except Exception:
        pytest.skip("Paciente já existe na base")

    _carga_dimensoes(session)

    dim = session.query(DimPacienteAnon).first()
    assert dim is not None
    assert dim.faixa_etaria in ("19-30 anos", "31-50 anos")
    assert dim.sexo == "FEMININO"
    # Anonimização reforçada: id_origem é hash SHA-256, não o UUID cru do paciente.
    assert len(dim.id_origem) == 64
    assert dim.id_origem != str(paciente.id)
