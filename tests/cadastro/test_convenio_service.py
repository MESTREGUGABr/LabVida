from collections.abc import Iterator

import pytest
from sqlalchemy.orm import Session

from src.cadastro.dtos import ConvenioCreate, ConvenioUpdate
from src.cadastro.errors import CnpjConvenioDuplicado, ConvenioNaoEncontrado, NomeConvenioDuplicado
from src.cadastro.models import Convenio
from src.cadastro.service import (
    atualizar_convenio,
    criar_convenio,
    inativar_convenio,
    listar_convenios,
    obter_convenio_por_id,
)
from src.db import session_scope


@pytest.fixture()
def session() -> Iterator[Session]:
    with session_scope() as session:
        session.query(Convenio).delete()
        session.commit()
        yield session
        session.query(Convenio).delete()
        session.commit()


def _convenio_create(nome: str = "Unimed Recife") -> ConvenioCreate:
    return ConvenioCreate(
        nome=nome,
        cnpj="12.345.678/0001-95",
        telefone="(87) 99999-1234",
        email="financeiro@unimed.test",
    )


def test_cria_convenio_ativo(session: Session) -> None:
    convenio = criar_convenio(session, _convenio_create())

    assert convenio.id
    assert convenio.nome == "Unimed Recife"
    assert convenio.cnpj == "12345678000195"
    assert convenio.telefone == "87999991234"
    assert convenio.email == "financeiro@unimed.test"
    assert convenio.ativo is True


def test_rejeita_nome_duplicado_normalizado_mesmo_inativo(session: Session) -> None:
    convenio = criar_convenio(session, _convenio_create(nome="Unimed Recife"))
    inativar_convenio(session, convenio.id)

    with pytest.raises(NomeConvenioDuplicado, match="Convênio já cadastrado com este nome"):
        criar_convenio(session, _convenio_create(nome="  unimed   recife  "))


def test_rejeita_cnpj_duplicado_quando_preenchido(session: Session) -> None:
    criar_convenio(session, _convenio_create(nome="Unimed Recife"))

    with pytest.raises(CnpjConvenioDuplicado, match="Convênio já cadastrado com este CNPJ"):
        criar_convenio(session, _convenio_create(nome="Unimed Caruaru"))


def test_lista_convenios_ativos_e_inativos_ordenados_por_nome(session: Session) -> None:
    criar_convenio(session, _convenio_create(nome="Bradesco Saúde"))
    sulamerica = criar_convenio(
        session,
        ConvenioCreate(nome="SulAmérica", cnpj=None, telefone=None, email=None),
    )
    unimed = criar_convenio(
        session,
        ConvenioCreate(nome="Unimed Recife", cnpj=None, telefone=None, email=None),
    )
    inativar_convenio(session, sulamerica.id)

    convenios = listar_convenios(session)

    assert [(convenio.nome, convenio.ativo) for convenio in convenios] == [
        ("Bradesco Saúde", True),
        ("SulAmérica", False),
        ("Unimed Recife", True),
    ]
    assert unimed.id in [convenio.id for convenio in convenios]


def test_obtem_convenio_por_id_mesmo_inativo(session: Session) -> None:
    convenio = criar_convenio(session, _convenio_create())
    inativar_convenio(session, convenio.id)

    encontrado = obter_convenio_por_id(session, convenio.id)

    assert encontrado.id == convenio.id


def test_atualiza_convenio_parcialmente(session: Session) -> None:
    convenio = criar_convenio(session, _convenio_create())

    atualizado = atualizar_convenio(session, convenio.id, ConvenioUpdate(nome="  Unimed   Agreste  ", cnpj=None))

    assert atualizado.nome == "Unimed Agreste"
    assert atualizado.cnpj is None
    assert atualizado.telefone == "87999991234"


def test_atualizar_nome_rejeita_nome_de_outro_convenio(session: Session) -> None:
    convenio = criar_convenio(session, _convenio_create(nome="Unimed Recife"))
    criar_convenio(session, ConvenioCreate(nome="Bradesco Saúde", cnpj=None, telefone=None, email=None))

    with pytest.raises(NomeConvenioDuplicado, match="Convênio já cadastrado com este nome"):
        atualizar_convenio(session, convenio.id, ConvenioUpdate(nome="bradesco saúde"))


def test_atualizar_cnpj_rejeita_cnpj_de_outro_convenio(session: Session) -> None:
    convenio = criar_convenio(session, ConvenioCreate(nome="Unimed Recife", cnpj=None, telefone=None, email=None))
    criar_convenio(session, _convenio_create(nome="Bradesco Saúde"))

    with pytest.raises(CnpjConvenioDuplicado, match="Convênio já cadastrado com este CNPJ"):
        atualizar_convenio(session, convenio.id, ConvenioUpdate(cnpj="12.345.678/0001-95"))


def test_inativar_convenio_eh_idempotente(session: Session) -> None:
    convenio = criar_convenio(session, _convenio_create())

    inativar_convenio(session, convenio.id)
    inativar_convenio(session, convenio.id)

    assert obter_convenio_por_id(session, convenio.id).ativo is False


def test_convenio_nao_encontrado(session: Session) -> None:
    from uuid import uuid4

    with pytest.raises(ConvenioNaoEncontrado, match="Convênio não encontrado"):
        obter_convenio_por_id(session, uuid4())
