"""Seed de Faturamento — lotes, guias e itens faturados a partir de laudos LIBERADOS.

Idempotente: só insere se não houver lotes no banco.
"""

import uuid
from datetime import datetime, timezone

from src.cadastro.convenio.repository import listar_ativos as listar_convenios
from src.db import session_scope
from src.faturamento.lote_faturamento.models import GuiaItem, GuiaTiss, LoteFaturamento
from src.faturamento.lote_faturamento.repository import (
    listar_laudos_liberados_por_convenio,
    listar_lotes,
    obter_lote_por_codigo,
    salvar_guia,
    salvar_guia_item,
    salvar_lote,
)


def _gerar_codigo_lote(session) -> str:
    ano = datetime.now(timezone.utc).year
    for _ in range(10):
        codigo = f"LT-{ano}-{uuid.uuid4().hex[:6].upper()}"
        if obter_lote_por_codigo(session, codigo) is None:
            return codigo
    raise RuntimeError("Não foi possível gerar código de lote único")


def _gerar_codigo_tiss() -> str:
    return f"TISS-{uuid.uuid4().hex[:12].upper()}"


def executar_seeder_faturamento() -> dict[str, int]:
    contagem = {"lotes": 0, "guias_itens": 0}

    with session_scope() as session:
        existentes = listar_lotes(session)
        if existentes:
            return contagem

        convenios = listar_convenios(session)
        if not convenios:
            return contagem

        for convenio in convenios[:2]:
            laudos = listar_laudos_liberados_por_convenio(session, convenio.id)
            if not laudos:
                continue

            lote = LoteFaturamento(
                codigo_lote=_gerar_codigo_lote(session),
                convenio_id=convenio.id,
                status="ABERTO",
            )
            salvar_lote(session, lote)
            session.flush()

            guia = GuiaTiss(
                lote_faturamento_id=lote.id,
                codigo_tiss=_gerar_codigo_tiss(),
            )
            salvar_guia(session, guia)
            session.flush()

            for laudo_info in laudos:
                item = GuiaItem(
                    guia_tiss_id=guia.id,
                    laudo_id=laudo_info["laudo_id"],
                    procedimento_id=laudo_info["procedimento_id"],
                    valor_faturado=50.00,
                )
                salvar_guia_item(session, item)
                lote.valor_total += 50.00
                contagem["guias_itens"] += 1

            session.flush()
            contagem["lotes"] += 1

        session.commit()

    return contagem


def main() -> None:
    contagem = executar_seeder_faturamento()
    print("Seed faturamento finalizado")
    for chave, valor in contagem.items():
        print(f"{chave}: {valor}")


if __name__ == "__main__":
    main()
