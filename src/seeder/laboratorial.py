"""Seed laboratorial — equipamentos, resultados e laudos LIBERADOS.

Cria dados de teste para destravar o fluxo de faturamento.
Idempotente: só insere se não houver laudos no banco.
"""

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from src.atendimento.ordem_servico import repository as os_repository
from src.cadastro.unidade.repository import listar_unidades_ativas
from src.db import session_scope
from src.laboratorial.models import (
    Equipamento,
    Laudo,
    ProtocoloEquipamento,
    Resultado,
    StatusLaudo,
    StatusResultado,
)


def _agora() -> datetime:
    return datetime.now(timezone.utc)


def executar_seeder_laboratorial() -> dict[str, int]:
    contagem = {"equipamentos": 0, "resultados": 0, "laudos": 0}

    with session_scope() as session:
        from sqlalchemy import select
        existentes = session.execute(select(Laudo).limit(1)).first()
        if existentes is not None:
            return contagem

        from src.cadastro.medico.repository import listar_ativos as listar_medicos
        medicos = listar_medicos(session)
        medicos = listar_medicos(session)
        responsavel = next((m for m in medicos if m.responsavel_tecnico), medicos[0] if medicos else None)
        if responsavel is None:
            return contagem

        equipamento = _criar_equipamento(session)
        contagem["equipamentos"] = 1

        ordens = os_repository.listar(session)
        for ordem in ordens:
            itens = os_repository.listar_itens(session, ordem.id)
            for item in itens:
                resultado = Resultado(
                    os_item_id=item.id,
                    equipamento_id=equipamento.id,
                    analito="Hemoglobina",
                    valor="14.5",
                    status=StatusResultado.REVISADO,
                )
                session.add(resultado)
                session.flush()

                laudo = Laudo(
                    os_item_id=item.id,
                    responsavel_tecnico_id=responsavel.id,
                    status=StatusLaudo.LIBERADO,
                    liberado_em=_agora(),
                    assinatura_digital="seed_laboratorial",
                )
                session.add(laudo)

                contagem["resultados"] += 1
                contagem["laudos"] += 1

        session.commit()

    return contagem


def _criar_equipamento(session: Session) -> Equipamento:
    from src.cadastro.unidade.repository import listar_setores_ativos
    from src.laboratorial.repository import LaboratorialRepository
    repo = LaboratorialRepository(session)
    unidades = listar_unidades_ativas(session)
    unidade = next((u for u in unidades if u.tipo == "CENTRAL"), unidades[0] if unidades else None)
    setor_id = None
    if unidade is not None:
        setores = listar_setores_ativos(session, unidade.id)
        if setores:
            setor_id = setores[0].id
    eq = Equipamento(
        setor_id=setor_id,
        nome="Analisador Automático X-2000",
        protocolo=ProtocoloEquipamento.HL7,
    )
    repo.save_equipamento(eq)
    session.flush()
    return eq


def main() -> None:
    contagem = executar_seeder_laboratorial()
    print("Seed laboratorial finalizado")
    for chave, valor in contagem.items():
        print(f"{chave}: {valor}")


if __name__ == "__main__":
    main()
