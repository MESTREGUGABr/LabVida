"""Metricas de auditoria — consulta direta a `auditoria_log`, sem ETL/fato.

`ocorrencias_por_mes` ainda depende de `DimTempo` (so para o calendario denso
e o rotulo `ano_mes`), entao o teste roda o ETL para popular a dimensao — as
demais funcoes filtram a data direto contra `AuditoriaLog.ocorrido_em`.
"""

from datetime import date

from sqlalchemy.orm import Session

from src.auditoria.models import AuditoriaLog
from src.bi import metricas
from src.bi.etl import executar_etl
from src.bi.metricas import Periodo
from tests.bi._helpers import coletar, criar_os, montar_cadastros, utc

JANEIRO = Periodo(date(2026, 1, 1), date(2026, 1, 31), "Janeiro")
FEVEREIRO = Periodo(date(2026, 2, 1), date(2026, 2, 28), "Fevereiro")


def _cenario_com_calendario(session: Session):
    """Uma OS em janeiro e uma em fevereiro — so para o calendario do BI
    (`DimTempo`) cobrir os dois meses; a auditoria em si nao depende disso."""
    cenario = montar_cadastros(session)
    ordem_jan = criar_os(session, cenario, aberta_em=utc(2026, 1, 10))
    coletar(session, cenario, ordem_jan, coletada_em=utc(2026, 1, 10, 8))
    ordem_fev = criar_os(session, cenario, aberta_em=utc(2026, 2, 5))
    coletar(session, cenario, ordem_fev, coletada_em=utc(2026, 2, 5, 8))
    return cenario


def _log(session: Session, usuario_id, *, entidade: str, acao: str, quando) -> None:
    session.add(
        AuditoriaLog(
            usuario_id=usuario_id,
            entidade=entidade,
            acao=acao,
            dados={},
            ocorrido_em=quando,
        )
    )


def test_auditoria_kpis_filtra_por_periodo(session: Session) -> None:
    cenario = _cenario_com_calendario(session)
    _log(session, cenario.usuario, entidade="paciente", acao="CRIAR_PACIENTE", quando=utc(2026, 1, 5))
    _log(session, cenario.usuario, entidade="paciente", acao="CRIAR_PACIENTE", quando=utc(2026, 1, 6))
    _log(session, cenario.usuario, entidade="ordem_servico", acao="ABRIR_OS", quando=utc(2026, 2, 10))
    session.commit()

    assert metricas.auditoria_kpis(session, JANEIRO)["ocorrencias"] == 2
    assert metricas.auditoria_kpis(session, FEVEREIRO)["ocorrencias"] == 1


def test_ocorrencias_por_mes_calendario_denso(session: Session) -> None:
    cenario = _cenario_com_calendario(session)
    _log(session, cenario.usuario, entidade="paciente", acao="CRIAR_PACIENTE", quando=utc(2026, 1, 5))
    session.commit()
    executar_etl()

    trimestre = Periodo(date(2026, 1, 1), date(2026, 3, 31), "1o trimestre")
    df = metricas.ocorrencias_por_mes(session, trimestre)

    meses = dict(zip(df["mes"], df["ocorrencias"]))
    assert meses.get("2026-01") == 1
    # Mes sem ocorrencia entra com zero (calendario denso), nao some da serie.
    assert meses.get("2026-02") == 0
    assert meses.get("2026-03") == 0


def test_ocorrencias_por_acao_e_por_entidade(session: Session) -> None:
    cenario = _cenario_com_calendario(session)
    _log(session, cenario.usuario, entidade="paciente", acao="CRIAR_PACIENTE", quando=utc(2026, 1, 5))
    _log(session, cenario.usuario, entidade="paciente", acao="CRIAR_PACIENTE", quando=utc(2026, 1, 6))
    _log(session, cenario.usuario, entidade="ordem_servico", acao="ABRIR_OS", quando=utc(2026, 1, 7))
    session.commit()

    por_acao = dict(zip(*[metricas.ocorrencias_por_acao(session, JANEIRO)[c] for c in ("acao", "ocorrencias")]))
    assert por_acao["Criar paciente"] == 2
    assert por_acao["Abrir OS"] == 1

    por_entidade = dict(
        zip(*[metricas.ocorrencias_por_entidade(session, JANEIRO)[c] for c in ("entidade", "ocorrencias")])
    )
    assert por_entidade["Paciente"] == 2
    assert por_entidade["Ordem servico"] == 1


def test_ocorrencias_recentes_traz_nome_do_usuario_e_ordena_desc(session: Session) -> None:
    cenario = _cenario_com_calendario(session)
    _log(session, cenario.usuario, entidade="paciente", acao="CRIAR_PACIENTE", quando=utc(2026, 1, 5))
    _log(session, cenario.usuario, entidade="ordem_servico", acao="ABRIR_OS", quando=utc(2026, 1, 20))
    session.commit()

    df = metricas.ocorrencias_recentes(session, JANEIRO)

    assert list(df["acao"]) == ["Abrir OS", "Criar paciente"]
    assert (df["usuario_nome"] == "Operador BI").all()
