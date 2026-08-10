import pytest

from src.usuario.email import validar_email
from src.usuario.errors import EmailInvalido


@pytest.mark.parametrize(
    "email",
    ["usuario@labvida.com.br", "a@b.co", "nome.sobrenome@dominio.com"],
)
def test_validar_email_aceita_formatos_validos(email: str) -> None:
    validar_email(email)  # não lança


@pytest.mark.parametrize(
    "email",
    ["abc", "sem-arroba.com", "@sem-usuario.com", "usuario@sem-ponto", "", "  "],
)
def test_validar_email_recusa_formatos_invalidos(email: str) -> None:
    with pytest.raises(EmailInvalido):
        validar_email(email)
