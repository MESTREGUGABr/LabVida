"""Metricas de estoque — consulta direta a `InsumoMaterial`/`EstoqueMovimento`.

`movimentacao_estoque_por_mes` depende de `DimTempo` (calendario denso), entao
o teste roda o ETL para popular a dimensao — as demais filtram/comparam direto
contra as tabelas operacionais.
"""

from datetime import date

from sqlalchemy.orm import Session

from src.bi import metricas
from src.bi.etl import executar_etl
from src.bi.metricas import Periodo
from src.compras.insumo.dtos import InsumoCreate, TipoMovimentoEstoque
from src.compras.insumo.models import EstoqueMovimento
from src.compras.insumo.service import criar_insumo
from tests.bi._helpers import coletar, criar_os, montar_cadastros, utc

JANEIRO = Periodo(date(2026, 1, 1), date(2026, 1, 31), "Janeiro")


def _com_calendario(session: Session):
    """So para o calendario do BI (`DimTempo`) cobrir janeiro."""
    cenario = montar_cadastros(session)
    ordem = criar_os(session, cenario, aberta_em=utc(2026, 1, 10))
    coletar(session, cenario, ordem, coletada_em=utc(2026, 1, 10, 8))
    return cenario


def test_estoque_kpis_conta_criticos_e_total(session: Session) -> None:
    criar_insumo(session, InsumoCreate(nome="Tubo A", finalidade="x", quantidade_estoque=5, estoque_minimo=10))
    criar_insumo(session, InsumoCreate(nome="Tubo B", finalidade="x", quantidade_estoque=50, estoque_minimo=10))
    session.commit()

    indicadores = metricas.estoque_kpis(session)
    assert indicadores["total_insumos"] == 2
    assert indicadores["insumos_criticos"] == 1


def test_insumos_criticos_retorna_so_abaixo_do_minimo_ordenado_por_deficit(session: Session) -> None:
    criar_insumo(session, InsumoCreate(nome="Deficit pequeno", finalidade="x", quantidade_estoque=9, estoque_minimo=10))
    criar_insumo(session, InsumoCreate(nome="Deficit grande", finalidade="x", quantidade_estoque=1, estoque_minimo=20))
    criar_insumo(session, InsumoCreate(nome="Ok", finalidade="x", quantidade_estoque=100, estoque_minimo=10))
    session.commit()

    df = metricas.insumos_criticos(session)

    assert list(df["nome"]) == ["Deficit grande", "Deficit pequeno"]
    assert "Ok" not in set(df["nome"])


def test_movimentacao_estoque_por_mes_calendario_denso(session: Session) -> None:
    cenario = _com_calendario(session)
    insumo = criar_insumo(
        session, InsumoCreate(nome="Reagente", finalidade="x", quantidade_estoque=100, estoque_minimo=10)
    )
    session.add(
        EstoqueMovimento(
            insumo_material_id=insumo.id, tipo=TipoMovimentoEstoque.ENTRADA,
            quantidade=50, ocorrido_em=utc(2026, 1, 5),
        )
    )
    session.add(
        EstoqueMovimento(
            insumo_material_id=insumo.id, tipo=TipoMovimentoEstoque.SAIDA,
            quantidade=20, ocorrido_em=utc(2026, 1, 15),
        )
    )
    session.commit()
    executar_etl()

    trimestre = Periodo(date(2026, 1, 1), date(2026, 3, 31), "1o trimestre")
    df = metricas.movimentacao_estoque_por_mes(session, trimestre)

    janeiro = df[df["mes"] == "2026-01"].iloc[0]
    assert float(janeiro["entradas"]) == 50
    assert float(janeiro["saidas"]) == 20
    # Mes sem movimento entra com zero (calendario denso), nao some da serie.
    fevereiro = df[df["mes"] == "2026-02"].iloc[0]
    assert float(fevereiro["entradas"]) == 0
    assert float(fevereiro["saidas"]) == 0


def test_insumos_maior_consumo_filtra_por_periodo(session: Session) -> None:
    insumo = criar_insumo(
        session, InsumoCreate(nome="Reagente", finalidade="x", quantidade_estoque=100, estoque_minimo=10)
    )
    session.add(
        EstoqueMovimento(
            insumo_material_id=insumo.id, tipo=TipoMovimentoEstoque.SAIDA,
            quantidade=15, ocorrido_em=utc(2026, 1, 10),
        )
    )
    session.add(
        EstoqueMovimento(
            insumo_material_id=insumo.id, tipo=TipoMovimentoEstoque.SAIDA,
            quantidade=999, ocorrido_em=utc(2026, 2, 1),
        )
    )
    session.commit()

    df = metricas.insumos_maior_consumo(session, JANEIRO)

    assert len(df) == 1
    assert float(df.iloc[0]["saida_total"]) == 15


def test_cobertura_dias_saldo_sobre_consumo_diario_medio(session: Session) -> None:
    criar_insumo(session, InsumoCreate(nome="Reagente", finalidade="x", quantidade_estoque=100, estoque_minimo=10))
    insumo = criar_insumo(
        session, InsumoCreate(nome="Outro", finalidade="x", quantidade_estoque=0, estoque_minimo=10)
    )
    session.add(
        EstoqueMovimento(
            insumo_material_id=insumo.id, tipo=TipoMovimentoEstoque.SAIDA,
            quantidade=31, ocorrido_em=utc(2026, 1, 15),
        )
    )
    session.commit()

    # Saldo total = 100 (o segundo insumo esta zerado); consumo diario medio
    # em janeiro (31 dias) = 31/31 = 1 -> cobertura = 100 dias.
    assert metricas.cobertura_dias(session, JANEIRO) == 100.0


def test_cobertura_dias_sem_consumo_e_none(session: Session) -> None:
    """`None` = sem base para estimar (nao houve saida no periodo) — nao pode
    ser confundido com "0 dias" (estoque zerado com consumo ativo)."""
    criar_insumo(session, InsumoCreate(nome="Reagente", finalidade="x", quantidade_estoque=100, estoque_minimo=10))
    session.commit()

    assert metricas.cobertura_dias(session, JANEIRO) is None


def test_cobertura_dias_estoque_zerado_com_consumo_e_zero_nao_none(session: Session) -> None:
    """Caso mais grave: acabou o estoque e ainda ha consumo registrado no
    periodo — tem que aparecer como "0 dias" (alerta), nao como "sem dado"."""
    insumo = criar_insumo(
        session, InsumoCreate(nome="Reagente", finalidade="x", quantidade_estoque=0, estoque_minimo=10)
    )
    session.add(
        EstoqueMovimento(
            insumo_material_id=insumo.id, tipo=TipoMovimentoEstoque.SAIDA,
            quantidade=5, ocorrido_em=utc(2026, 1, 15),
        )
    )
    session.commit()

    assert metricas.cobertura_dias(session, JANEIRO) == 0.0
