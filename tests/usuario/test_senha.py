import pytest

from src.usuario.errors import SenhaFraca
from src.usuario.senha import hash_senha, validar_politica, verificar_senha


def test_hash_nao_e_a_senha_em_claro() -> None:
    h = hash_senha("senha-forte-123")
    assert h != "senha-forte-123"


def test_dois_hashes_da_mesma_senha_diferem() -> None:
    assert hash_senha("senha-forte-123") != hash_senha("senha-forte-123")


def test_verificar_senha_aceita_a_correta() -> None:
    h = hash_senha("senha-forte-123")
    assert verificar_senha("senha-forte-123", h) is True


def test_verificar_senha_recusa_a_errada() -> None:
    h = hash_senha("senha-forte-123")
    assert verificar_senha("senha-errada-000", h) is False


def test_verificar_senha_com_hash_none_recusa() -> None:
    assert verificar_senha("qualquer-coisa", None) is False


def test_verificar_senha_com_hash_vazio_recusa() -> None:
    assert verificar_senha("qualquer-coisa", "") is False


def test_verificar_senha_com_hash_corrompido_nao_lanca() -> None:
    assert verificar_senha("qualquer-coisa", "isto-nao-e-um-hash-bcrypt") is False


def test_validar_politica_recusa_senha_curta() -> None:
    with pytest.raises(SenhaFraca):
        validar_politica("1234567")


def test_validar_politica_aceita_oito_caracteres() -> None:
    validar_politica("12345678")


def test_validar_politica_recusa_senha_maior_que_72_bytes() -> None:
    with pytest.raises(SenhaFraca):
        validar_politica("á" * 40)  # 'á' em UTF-8 ocupa 2 bytes -> 80 bytes


def test_hash_senha_recusa_senha_fraca() -> None:
    with pytest.raises(SenhaFraca):
        hash_senha("curta")
