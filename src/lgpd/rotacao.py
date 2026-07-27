"""Rotação da chave de criptografia LGPD.

Re-criptografa o CPF de todos os pacientes de uma chave Fernet **antiga** para a
**nova** (a que passa a valer no ambiente). O `cpf_hash` (SHA-256 do CPF em claro)
não muda — só o `cpf_encrypted`.

Uso (CLI): defina a NOVA chave no ambiente e informe a ANTIGA como argumento:

    LGPD_ENCRYPTION_KEY=<chave_nova> python -m src.lgpd.rotacao <chave_antiga>

Programático: `rotacionar_chave(session, chave_antiga, chave_nova)`.
"""
import os
import sys

from cryptography.fernet import Fernet
from sqlalchemy.orm import Session

from src.cadastro.models import Paciente
from src.db import session_scope


def rotacionar_chave(session: Session, chave_antiga: str, chave_nova: str) -> int:
    """Re-criptografa os CPFs; devolve quantos pacientes foram processados."""
    fernet_antiga = Fernet(chave_antiga.encode())
    fernet_nova = Fernet(chave_nova.encode())

    pacientes = session.query(Paciente).all()
    for paciente in pacientes:
        cpf = fernet_antiga.decrypt(paciente.cpf_encrypted).decode()
        paciente.cpf_encrypted = fernet_nova.encrypt(cpf.encode())

    session.commit()
    return len(pacientes)


def main(argv: list[str] | None = None) -> None:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        raise SystemExit(
            "Uso: LGPD_ENCRYPTION_KEY=<chave_nova> python -m src.lgpd.rotacao <chave_antiga>"
        )

    chave_antiga = argv[0]
    chave_nova = os.environ.get("LGPD_ENCRYPTION_KEY", "")
    if not chave_nova:
        raise SystemExit("Defina LGPD_ENCRYPTION_KEY (a nova chave) no ambiente antes de rotacionar.")
    if chave_nova == chave_antiga:
        raise SystemExit("A chave nova é igual à antiga — nada a rotacionar.")

    with session_scope() as session:
        total = rotacionar_chave(session, chave_antiga, chave_nova)
    print(f"Rotação concluída: {total} CPF(s) re-criptografados com a nova chave.")


if __name__ == "__main__":
    main()
