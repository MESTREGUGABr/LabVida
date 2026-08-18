"""Regressões da trajetória de crescimento da base de demonstração.

A série histórica não pode ser uniforme: o volume precisa crescer com a
empresa, seguir a sazonalidade e respeitar o ciclo de vida das unidades e dos
contratos de convênio. Estes testes cobrem a curva sem tocar no banco.
"""

from datetime import date, datetime, timedelta, timezone
from types import SimpleNamespace

from src.seeder import config
from src.seeder import trajetoria
from src.seeder.atendimento import _escolher_convenio, _unidades_ativas_em


def _mesmo_dia_da_semana(referencia: date, alvo: date) -> date:
    """Desloca `alvo` para cair no mesmo dia da semana de `referencia`."""
    return alvo + timedelta(days=referencia.weekday() - alvo.weekday())


def test_peso_cresce_ano_a_ano() -> None:
    """Mesmo mês, mesmo dia da semana: um ano depois pesa mais (crescimento)."""
    inicio = trajetoria.data_inicio()
    ano_seguinte = _mesmo_dia_da_semana(inicio, inicio.replace(year=inicio.year + 1))
    assert trajetoria.peso_do_dia(ano_seguinte) > trajetoria.peso_do_dia(inicio)


def test_sazonalidade_inverno_mais_forte_que_recesso() -> None:
    """Julho (inverno, pico) pesa mais que dezembro (recesso), mesmo ano."""
    ano = trajetoria.data_inicio().year
    julho = date(ano, 7, 15)
    dezembro = _mesmo_dia_da_semana(julho, date(ano, 12, 15))
    assert trajetoria.peso_do_dia(julho) > trajetoria.peso_do_dia(dezembro)


def test_domingo_e_residual() -> None:
    """Domingo quase não tem movimento frente aos dias úteis."""
    inicio = trajetoria.data_inicio()
    segunda = inicio + timedelta(days=(0 - inicio.weekday()) % 7)
    domingo = segunda + timedelta(days=6)
    assert trajetoria.peso_do_dia(segunda) > trajetoria.peso_do_dia(domingo) * 10


def test_sortear_dias_atras_respeita_faixa() -> None:
    config.iniciar_rng()
    for _ in range(300):
        valor = trajetoria.sortear_dias_atras(10, 100)
        assert 10 <= valor < 101


def test_particular_cai_conforme_rede_assina_convenios() -> None:
    inicio = trajetoria.data_inicio()
    t_inicio = datetime.combine(inicio, datetime.min.time(), tzinfo=timezone.utc)
    t_cinco_anos = t_inicio + timedelta(days=round(365.25 * 5))

    assert trajetoria.proporcao_particular(t_inicio) == 0.30
    assert trajetoria.proporcao_particular(t_cinco_anos) < 0.30
    assert trajetoria.proporcao_particular(t_cinco_anos) >= 0.12


def test_unidade_so_recebe_movimento_depois_de_inaugurada() -> None:
    unidades = [
        SimpleNamespace(nome="Unidade de Coleta Centro"),
        SimpleNamespace(nome="Unidade de Coleta São José"),
    ]
    antes = _unidades_ativas_em(unidades, date(2023, 1, 15))
    depois = _unidades_ativas_em(unidades, date(2023, 8, 15))

    assert [u.nome for u in antes] == ["Unidade de Coleta Centro"]
    assert {u.nome for u in depois} == {u.nome for u in unidades}


def test_convenio_nao_entra_antes_do_contrato() -> None:
    contexto = SimpleNamespace(
        convenios=[SimpleNamespace(nome="Unimed"), SimpleNamespace(nome="Cassi")]
    )
    antes_do_contrato = datetime(2024, 6, 1, tzinfo=timezone.utc)

    config.iniciar_rng()
    nomes = {_escolher_convenio(contexto, antes_do_contrato).nome for _ in range(50)}

    assert nomes == {"Unimed"}
