"""Regressão N13: o seed de RBAC precisa ser idempotente linha a linha.

Antes, `_seed_perfis` fazia early-return se a tabela `permissoes` tivesse
qualquer linha. Efeito: toda base já semeada ficava congelada na primeira versão
do RBAC — permissão adicionada depois nunca chegava, e a tela que dependesse dela
ficava inacessível para todo mundo, inclusive admin.
"""

from collections.abc import Iterator

import pytest
from sqlalchemy.orm import Session

from src.db import session_scope
from src.rbac import repository
from src.rbac.models import Perfil, PerfilPermissao, Permissao
from src.seeder.rbac import executar_seeder_rbac
from src.usuario.models import Usuario


def _limpar(session: Session) -> None:
    session.query(Usuario).update({"perfil_id": None})
    session.commit()
    for tabela in (PerfilPermissao, Permissao, Perfil):
        session.query(tabela).delete()
    session.commit()
    session.query(Usuario).delete()
    session.commit()


@pytest.fixture()
def session() -> Iterator[Session]:
    with session_scope() as s:
        _limpar(s)
        yield s
        _limpar(s)


def test_segunda_execucao_nao_duplica(session: Session) -> None:
    primeira = executar_seeder_rbac()
    assert primeira["permissoes"] > 0
    assert primeira["perfis"] > 0

    total_permissoes = len(repository.listar_permissoes(session))
    total_perfis = len(repository.listar_perfis(session))

    segunda = executar_seeder_rbac()

    # Nada novo a criar, e nada duplicado.
    assert segunda == {"perfis": 0, "permissoes": 0, "usuarios": 0}
    assert len(repository.listar_permissoes(session)) == total_permissoes
    assert len(repository.listar_perfis(session)) == total_perfis


def test_permissao_faltante_e_reposta_em_base_ja_semeada(session: Session) -> None:
    """O caso que o early-return quebrava: base existente ganhando permissão nova."""
    executar_seeder_rbac()

    alvo = repository.obter_permissao_por_codigo(session, "bi:visualizar")
    assert alvo is not None
    session.query(PerfilPermissao).filter(PerfilPermissao.permissao_id == alvo.id).delete()
    session.delete(alvo)
    session.commit()

    assert repository.obter_permissao_por_codigo(session, "bi:visualizar") is None

    contagem = executar_seeder_rbac()

    assert contagem["permissoes"] == 1
    reposta = repository.obter_permissao_por_codigo(session, "bi:visualizar")
    assert reposta is not None

    # E o vínculo com quem devia tê-la também volta — repor a permissão órfã
    # sem religar o perfil deixaria a tela igualmente inacessível.
    admin = repository.obter_perfil_por_nome(session, "admin")
    codigos_admin = {p.codigo for p in repository.listar_permissoes_por_perfil(session, admin.id)}
    assert "bi:visualizar" in codigos_admin


def test_vinculo_removido_e_restaurado(session: Session) -> None:
    executar_seeder_rbac()

    faturista = repository.obter_perfil_por_nome(session, "faturista")
    alvo = repository.obter_permissao_por_codigo(session, "faturamento:gerenciar_lotes")
    repository.remover_permissao(session, faturista.id, alvo.id)
    session.commit()

    codigos = {p.codigo for p in repository.listar_permissoes_por_perfil(session, faturista.id)}
    assert "faturamento:gerenciar_lotes" not in codigos

    executar_seeder_rbac()

    codigos = {p.codigo for p in repository.listar_permissoes_por_perfil(session, faturista.id)}
    assert "faturamento:gerenciar_lotes" in codigos
