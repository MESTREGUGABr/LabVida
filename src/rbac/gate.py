from uuid import UUID

from sqlalchemy.orm import Session

from src.rbac import repository
from src.rbac.errors import PermissaoNegada


def verificar_permissao(session: Session, usuario_id: UUID, codigo_permissao: str) -> bool:
    return repository.usuario_tem_permissao(session, usuario_id, codigo_permissao)


def exigir_permissao(session: Session, usuario_id: UUID, codigo_permissao: str) -> None:
    if not verificar_permissao(session, usuario_id, codigo_permissao):
        raise PermissaoNegada(
            f"Usuário {usuario_id} não possui a permissão '{codigo_permissao}'"
        )
