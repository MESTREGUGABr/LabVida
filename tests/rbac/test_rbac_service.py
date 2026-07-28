from collections.abc import Iterator
from uuid import uuid4

import pytest
from sqlalchemy.orm import Session

from src.db import session_scope
from src.rbac import repository, service
from src.rbac.dtos import PerfilCreate
from src.rbac.errors import PerfilDuplicado, PerfilNaoEncontrado, PermissaoNegada
from src.rbac.gate import exigir_permissao, verificar_permissao
from src.rbac.models import Perfil, Permissao, PerfilPermissao
from src.usuario.service import sincronizar_usuario


@pytest.fixture()
def session() -> Iterator[Session]:
    with session_scope() as s:
        from src.usuario.models import Usuario
        s.query(Usuario).update({"perfil_id": None})
        s.commit()
        for t in [PerfilPermissao, Permissao, Perfil]:
            s.query(t).delete()
        s.commit()
        yield s
        from src.usuario.models import Usuario
        s.query(Usuario).update({"perfil_id": None})
        for t in [PerfilPermissao, Permissao, Perfil]:
            s.query(t).delete()
        s.commit()


def _criar_permissao(session: Session, codigo: str) -> Permissao:
    p = Permissao(codigo=codigo, descricao=f"Permissão {codigo}")
    repository.salvar_permissao(session, p)
    session.commit()
    return p


def test_criar_perfil(session: Session) -> None:
    perfil = service.criar_perfil(session, PerfilCreate(nome="atendente", descricao="Atendente de balcão"))
    assert perfil.id
    assert perfil.nome == "atendente"


def test_rejeita_perfil_duplicado(session: Session) -> None:
    service.criar_perfil(session, PerfilCreate(nome="admin"))
    with pytest.raises(PerfilDuplicado):
        service.criar_perfil(session, PerfilCreate(nome="admin"))


def test_listar_perfis(session: Session) -> None:
    service.criar_perfil(session, PerfilCreate(nome="admin"))
    service.criar_perfil(session, PerfilCreate(nome="atendente"))
    perfis = service.listar_perfis(session)
    assert len(perfis) == 2


def test_atribuir_permissao_ao_perfil(session: Session) -> None:
    p = _criar_permissao(session, "atendimento:abrir_os")
    perfil = service.criar_perfil(session, PerfilCreate(nome="atendente"))
    service.atribuir_permissao_ao_perfil(session, perfil.id, p.id)
    permissoes = service.listar_permissoes_do_perfil(session, perfil.id)
    assert len(permissoes) == 1
    assert permissoes[0].codigo == "atendimento:abrir_os"


def test_vincular_usuario_ao_perfil(session: Session) -> None:
    p = _criar_permissao(session, "atendimento:abrir_os")
    perfil = service.criar_perfil(session, PerfilCreate(nome="atendente"))
    service.atribuir_permissao_ao_perfil(session, perfil.id, p.id)

    usuario = sincronizar_usuario(session, "teste@labvida.test", "Teste")
    service.vincular_usuario_ao_perfil(session, usuario.id, perfil.id)

    assert verificar_permissao(session, usuario.id, "atendimento:abrir_os") is True


def test_usuario_sem_perfil_sem_permissao(session: Session) -> None:
    usuario = sincronizar_usuario(session, "semperfil@labvida.test", "Sem Perfil")
    assert verificar_permissao(session, usuario.id, "atendimento:abrir_os") is False


def test_gate_exigir_permissao_autorizado(session: Session) -> None:
    p = _criar_permissao(session, "atendimento:abrir_os")
    perfil = service.criar_perfil(session, PerfilCreate(nome="atendente"))
    service.atribuir_permissao_ao_perfil(session, perfil.id, p.id)
    usuario = sincronizar_usuario(session, "autorizado@labvida.test", "Autorizado")
    service.vincular_usuario_ao_perfil(session, usuario.id, perfil.id)

    exigir_permissao(session, usuario.id, "atendimento:abrir_os")


def test_gate_exigir_permissao_negado(session: Session) -> None:
    usuario = sincronizar_usuario(session, "negado@labvida.test", "Negado")

    with pytest.raises(PermissaoNegada):
        exigir_permissao(session, usuario.id, "laboratorial:liberar_laudo")


def test_gate_e_granular_por_permissao(session: Session) -> None:
    # Perfil com apenas UMA permissão é autorizado nela e negado nas demais.
    p = _criar_permissao(session, "atendimento:abrir_os")
    _criar_permissao(session, "laboratorial:liberar_laudo")
    perfil = service.criar_perfil(session, PerfilCreate(nome="atendente"))
    service.atribuir_permissao_ao_perfil(session, perfil.id, p.id)
    usuario = sincronizar_usuario(session, "granular@labvida.test", "Granular")
    service.vincular_usuario_ao_perfil(session, usuario.id, perfil.id)

    assert verificar_permissao(session, usuario.id, "atendimento:abrir_os") is True
    assert verificar_permissao(session, usuario.id, "laboratorial:liberar_laudo") is False
    with pytest.raises(PermissaoNegada):
        exigir_permissao(session, usuario.id, "laboratorial:liberar_laudo")


def test_trocar_perfil_muda_permissoes(session: Session) -> None:
    abrir = _criar_permissao(session, "atendimento:abrir_os")
    liberar = _criar_permissao(session, "laboratorial:liberar_laudo")
    perfil_atend = service.criar_perfil(session, PerfilCreate(nome="atendente"))
    perfil_lab = service.criar_perfil(session, PerfilCreate(nome="laboratorio"))
    service.atribuir_permissao_ao_perfil(session, perfil_atend.id, abrir.id)
    service.atribuir_permissao_ao_perfil(session, perfil_lab.id, liberar.id)

    usuario = sincronizar_usuario(session, "troca@labvida.test", "Troca")
    service.vincular_usuario_ao_perfil(session, usuario.id, perfil_atend.id)
    assert verificar_permissao(session, usuario.id, "atendimento:abrir_os") is True

    # Ao trocar de perfil, as permissões acompanham.
    service.vincular_usuario_ao_perfil(session, usuario.id, perfil_lab.id)
    assert verificar_permissao(session, usuario.id, "atendimento:abrir_os") is False
    assert verificar_permissao(session, usuario.id, "laboratorial:liberar_laudo") is True


def test_listar_permissoes_do_usuario(session: Session) -> None:
    p1 = _criar_permissao(session, "atendimento:abrir_os")
    p2 = _criar_permissao(session, "atendimento:coletar")
    perfil = service.criar_perfil(session, PerfilCreate(nome="atendente"))
    service.atribuir_permissao_ao_perfil(session, perfil.id, p1.id)
    service.atribuir_permissao_ao_perfil(session, perfil.id, p2.id)
    usuario = sincronizar_usuario(session, "atendente@labvida.test", "Atendente")
    service.vincular_usuario_ao_perfil(session, usuario.id, perfil.id)

    permissoes = service.listar_permissoes_do_usuario(session, usuario.id)
    assert len(permissoes) == 2
    codigos = {p.codigo for p in permissoes}
    assert "atendimento:abrir_os" in codigos
    assert "atendimento:coletar" in codigos


def test_remover_permissao_do_perfil(session: Session) -> None:
    p1 = _criar_permissao(session, "atendimento:abrir_os")
    p2 = _criar_permissao(session, "atendimento:coletar")
    perfil = service.criar_perfil(session, PerfilCreate(nome="atendente"))
    service.atribuir_permissao_ao_perfil(session, perfil.id, p1.id)
    service.atribuir_permissao_ao_perfil(session, perfil.id, p2.id)

    assert len(service.listar_permissoes_do_perfil(session, perfil.id)) == 2

    service.remover_permissao_do_perfil(session, perfil.id, p1.id)
    permissoes = service.listar_permissoes_do_perfil(session, perfil.id)

    assert len(permissoes) == 1
    assert permissoes[0].codigo == "atendimento:coletar"


def test_desvincular_usuario_do_perfil(session: Session) -> None:
    p = _criar_permissao(session, "atendimento:abrir_os")
    perfil = service.criar_perfil(session, PerfilCreate(nome="atendente"))
    service.atribuir_permissao_ao_perfil(session, perfil.id, p.id)
    usuario = sincronizar_usuario(session, "desvincular@labvida.test", "Desvincular")
    service.vincular_usuario_ao_perfil(session, usuario.id, perfil.id)

    assert verificar_permissao(session, usuario.id, "atendimento:abrir_os") is True

    service.desvincular_usuario_do_perfil(session, usuario.id)
    assert verificar_permissao(session, usuario.id, "atendimento:abrir_os") is False
    assert len(service.listar_permissoes_do_usuario(session, usuario.id)) == 0


def test_remover_permissao_inexistente_nao_quebra(session: Session) -> None:
    p = _criar_permissao(session, "atendimento:abrir_os")
    perfil = service.criar_perfil(session, PerfilCreate(nome="atendente"))
    service.atribuir_permissao_ao_perfil(session, perfil.id, p.id)
    service.remover_permissao_do_perfil(session, perfil.id, p.id)

    service.remover_permissao_do_perfil(session, perfil.id, p.id)

    assert len(service.listar_permissoes_do_perfil(session, perfil.id)) == 0


def test_desvincular_bloqueia_acesso_quando_existem_perfis(session: Session) -> None:
    p = _criar_permissao(session, "atendimento:abrir_os")
    perfil = service.criar_perfil(session, PerfilCreate(nome="atendente"))
    service.atribuir_permissao_ao_perfil(session, perfil.id, p.id)
    usuario = sincronizar_usuario(session, "bloqueado@labvida.test", "Bloqueado")
    service.vincular_usuario_ao_perfil(session, usuario.id, perfil.id)

    assert verificar_permissao(session, usuario.id, "atendimento:abrir_os") is True

    service.desvincular_usuario_do_perfil(session, usuario.id)

    assert verificar_permissao(session, usuario.id, "atendimento:abrir_os") is False
    assert len(service.listar_permissoes_do_usuario(session, usuario.id)) == 0

    with pytest.raises(PermissaoNegada):
        exigir_permissao(session, usuario.id, "atendimento:abrir_os")
