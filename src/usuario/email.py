"""Validação de formato de e-mail no cadastro local.

Regex simples (`algo@algo.algo`) — suficiente para pegar erro de digitação
óbvio (`"abc"`, e-mail sem domínio). Não tenta validar RFC 5322 completo.
"""

import re

from src.usuario.errors import EmailInvalido

_PADRAO_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validar_email(email: str) -> None:
    if not email or not _PADRAO_EMAIL.match(email.strip()):
        raise EmailInvalido("E-mail inválido.")
