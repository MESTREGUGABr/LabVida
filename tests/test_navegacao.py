"""Regra de visibilidade do menu, filtrada por permissao.

`paginas_permitidas()` e logica pura (sem `st.Page`/`st.navigation`), reusada
tanto pelo menu HTML/CSS manual (`src/ui.py:renderizar_menu`, revertido da F1
a pedido do professor) quanto testavel isoladamente aqui.

O que precisa continuar valendo: o menu nunca mostra uma tela que o `shell()`
daquela pagina vai barrar — item visivel que responde "acesso negado" e pior do
que item ausente.
"""

from collections.abc import Iterator
from uuid import UUID

import pytest
from sqlalchemy.orm import Session

from src.db import session_scope
from src.rbac.models import Perfil, PerfilPermissao, Permissao
from src.ui import _MENU, paginas_permitidas
from src.usuario.models import Usuario
from src.usuario.service import sincronizar_usuario


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


def _usuario_com(session: Session, codigos: list[str]) -> UUID:
    perfil = Perfil(nome="perfil_teste", descricao="Perfil de teste")
    session.add(perfil)
    session.flush()

    for codigo in codigos:
        permissao = Permissao(codigo=codigo, descricao=codigo)
        session.add(permissao)
        session.flush()
        session.add(PerfilPermissao(perfil_id=perfil.id, permissao_id=permissao.id))

    # `sincronizar_usuario` devolve um DTO Pydantic: atribuir `perfil_id` nele
    # nao chega ao banco. O vinculo precisa ser feito na linha ORM.
    lido = sincronizar_usuario(session, "nav@labvida.test", "Nav Teste")
    usuario = session.get(Usuario, lido.id)
    usuario.perfil_id = perfil.id
    session.commit()
    return usuario.id


def _titulos(secoes: dict) -> set[str]:
    return {titulo for itens in secoes.values() for titulo, _caminho in itens}


def test_home_esta_sempre_disponivel(session: Session) -> None:
    usuario_id = _usuario_com(session, ["bi:visualizar"])

    navegacao = paginas_permitidas(usuario_id)

    assert "Inicio" in navegacao
    assert navegacao["Inicio"] == [("Home", "pages/home.py")]


def test_so_aparecem_as_secoes_permitidas(session: Session) -> None:
    usuario_id = _usuario_com(session, ["bi:visualizar"])

    navegacao = paginas_permitidas(usuario_id)

    assert "BI — Indicadores" in navegacao
    assert "Faturamento" not in navegacao
    assert "Compras" not in navegacao
    # "Meu Perfil" nao exige permissao: a secao Administracao aparece so com ele.
    assert _titulos(navegacao) >= {"Home", "Visao Executiva", "Meu Perfil"}


def test_secao_sem_nenhum_item_permitido_some(session: Session) -> None:
    """Secao vazia nao pode virar cabecalho orfao na barra lateral."""
    usuario_id = _usuario_com(session, ["compras:visualizar_estoque"])

    navegacao = paginas_permitidas(usuario_id)

    assert "Compras" in navegacao
    assert [titulo for titulo, _c in navegacao["Compras"]] == ["Estoque"]
    assert "Laboratorial" not in navegacao


def test_item_sem_permissao_e_visivel_para_todos(session: Session) -> None:
    usuario_id = _usuario_com(session, [])

    navegacao = paginas_permitidas(usuario_id)

    assert "Meu Perfil" in _titulos(navegacao)


def test_bootstrap_libera_tudo(session: Session) -> None:
    """Sem nenhum perfil cadastrado o acesso e plano (ADR 0002), senao a
    primeira pessoa a logar num banco novo nao configuraria nada."""
    usuario = sincronizar_usuario(session, "bootstrap@labvida.test", "Bootstrap")
    session.commit()

    navegacao = paginas_permitidas(usuario.id)

    esperadas = {titulo for _secao, itens in _MENU for titulo, _c, _p in itens} | {"Home"}
    assert _titulos(navegacao) == esperadas


def test_toda_pagina_do_menu_existe_em_disco(session: Session) -> None:
    """`st.Page` estoura no boot da aplicacao se o caminho nao existir — e
    seria no boot, nao num teste."""
    from pathlib import Path

    raiz = Path(__file__).parent.parent
    faltando = [caminho for _s, itens in _MENU for _t, caminho, _p in itens
                if not (raiz / caminho).is_file()]

    assert not faltando, f"paginas do menu ausentes: {faltando}"
