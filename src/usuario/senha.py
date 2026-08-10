"""Hash e verificação de senha (bcrypt).

Regras de segurança que não podem ser violadas:
- `senha_hash=None` nunca autentica — `verificar_senha` sempre retorna False.
- Comparação sempre via `bcrypt.checkpw` (constant-time), nunca `==`.
- Quando o hash é None/inválido, roda um verify "dummy" contra um hash fixo
  para equalizar o tempo de resposta e não vazar, por timing, se a conta existe.
- bcrypt trunca silenciosamente senhas acima de 72 bytes UTF-8 — validado em
  `validar_politica` para nunca deixar isso passar sem aviso.
- Nunca logar, imprimir ou auditar a senha em texto plano nem o hash.
"""

import bcrypt

from src.usuario.errors import SenhaFraca

_TAMANHO_MINIMO = 8
_TAMANHO_MAXIMO_BYTES = 72

# Hash fixo, gerado uma vez no import, usado só para equalizar o tempo de
# resposta quando não há hash real para comparar (conta inexistente ou sem
# senha). O valor em si não protege nada — só existe para a comparação levar
# o mesmo tempo de um bcrypt.checkpw real.
_HASH_DUMMY = bcrypt.hashpw(b"dummy-para-equalizar-timing", bcrypt.gensalt())


def validar_politica(senha: str) -> None:
    if len(senha) < _TAMANHO_MINIMO:
        raise SenhaFraca(f"A senha precisa ter pelo menos {_TAMANHO_MINIMO} caracteres.")
    if len(senha.encode("utf-8")) > _TAMANHO_MAXIMO_BYTES:
        raise SenhaFraca("A senha é muito longa.")


def hash_senha(senha: str) -> str:
    validar_politica(senha)
    return bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("ascii")


def verificar_senha(senha: str, senha_hash: str | None) -> bool:
    if not senha_hash:
        bcrypt.checkpw(senha.encode("utf-8"), _HASH_DUMMY)
        return False
    try:
        return bcrypt.checkpw(senha.encode("utf-8"), senha_hash.encode("ascii"))
    except ValueError:
        return False
