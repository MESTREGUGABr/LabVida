"""Seed laboratorial — equipamentos, valores de referência, resultados e laudos.

Trabalha só sobre as OS cuja amostra foi recebida no central (é o que o service
exige para registrar resultado), e distribui a bancada em três situações:
laudo liberado, laudo em rascunho e resultado aguardando revisão. As liberações
alimentam o faturamento; as pendências dão o que fazer nas telas do módulo.

Idempotente: só insere se não houver laudos nem resultados no banco.
"""

import random
from datetime import datetime, timedelta
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.atendimento.amostra.models import Amostra
from src.atendimento.ordem_servico import repository as os_repository
from src.atendimento.ordem_servico.dtos import StatusOsItem
from src.atendimento.ordem_servico.models import OrdemServico
from src.cadastro.medico.repository import listar_ativos as listar_medicos
from src.cadastro.procedimento.repository import listar_ativos as listar_procedimentos
from src.cadastro.unidade.repository import listar_setores_ativos, listar_unidades_ativas
from src.db import session_scope
from src.laboratorial.dtos import LaudoCreate, LaudoUpdate, ResultadoCreate, ValorReferenciaCreate
from src.laboratorial.models import (
    Equipamento,
    ProtocoloEquipamento,
    Resultado,
    StatusLaudo,
    StatusResultado,
)
from src.laboratorial.service import LaboratorialService
from src.logistica.recebimento.models import AmostraMovimentacao
from src.seeder.catalogo import EQUIPAMENTOS, PROCEDIMENTOS
from src.seeder.config import somar_horas
from src.seeder.trajetoria import anos_de_operacao
from src.usuario.models import Usuario

# Situação da bancada por OS recebida (soma 1.0).
_PESOS_BANCADA = {
    "liberado": 0.72,   # todos os laudos liberados → OS concluída, pronta para faturar
    "parcial": 0.10,    # parte liberada, parte em rascunho
    "aguardando": 0.18, # resultado digitado, ainda sem revisão
}
_PROPORCAO_FORA_DA_FAIXA = 0.22
_COMMIT_A_CADA = 25


def executar_seeder_laboratorial() -> dict[str, int]:
    contagem = {"equipamentos": 0, "valores_referencia": 0, "resultados": 0, "laudos": 0, "laudos_liberados": 0}

    with session_scope() as session:
        if session.execute(select(Resultado).limit(1)).first() is not None:
            return contagem

        medicos = listar_medicos(session)
        responsaveis = [m for m in medicos if m.responsavel_tecnico]
        if not responsaveis:
            return contagem

        servico = LaboratorialService(session)
        equipamentos, contagem["equipamentos"] = _seed_equipamentos(session)

        procedimentos = {p.id: p for p in listar_procedimentos(session)}
        catalogo = {p.codigo_tuss: p for p in PROCEDIMENTOS}

        contagem["valores_referencia"] = _seed_valores_referencia(servico, procedimentos, catalogo)
        session.commit()

        tecnico = session.scalar(
            select(Usuario).where(Usuario.email == "bancada.hematologia@labvida.com.br")
        ) or session.scalar(select(Usuario).limit(1))

        # Commit em lotes: com a janela longa (SEED_INICIO) o seeder processa
        # milhares de OS e um commit por OS dominaria o tempo de execução.
        for indice, (ordem_id, recebido_em) in enumerate(_ordens_recebidas(session)):
            _processar_ordem(
                session,
                servico,
                ordem_id,
                recebido_em,
                procedimentos,
                catalogo,
                equipamentos,
                responsaveis,
                tecnico,
                contagem,
            )
            if (indice + 1) % _COMMIT_A_CADA == 0:
                session.commit()

        session.commit()

    return contagem


def _seed_equipamentos(session: Session) -> tuple[dict[str, Equipamento], int]:
    """Parque de equipamentos do laboratório central, por setor e protocolo.

    Devolve o índice usado para associar resultado a equipamento (o primeiro de
    cada setor) junto do total efetivamente criado — um setor pode ter mais de
    um analisador.
    """
    unidades = listar_unidades_ativas(session)
    central = next((u for u in unidades if u.tipo == "CENTRAL"), unidades[0] if unidades else None)
    if central is None:
        return {}, 0

    setores = {s.nome: s for s in listar_setores_ativos(session, central.id)}
    por_setor: dict[str, Equipamento] = {}
    criados = 0

    for nome, setor_nome, protocolo in EQUIPAMENTOS:
        setor = setores.get(setor_nome)
        if setor is None:
            continue
        equipamento = Equipamento(
            setor_id=setor.id,
            nome=nome,
            protocolo=ProtocoloEquipamento(protocolo),
        )
        session.add(equipamento)
        por_setor.setdefault(setor_nome, equipamento)
        criados += 1

    session.flush()
    return por_setor, criados


def _seed_valores_referencia(servico: LaboratorialService, procedimentos: dict, catalogo: dict) -> int:
    total = 0
    for procedimento in procedimentos.values():
        entrada = catalogo.get(procedimento.codigo_tuss)
        if entrada is None:
            continue
        for analito in entrada.analitos:
            servico.criar_valor_referencia(
                ValorReferenciaCreate(
                    procedimento_id=procedimento.id,
                    analito=analito.nome,
                    minimo=analito.minimo,
                    maximo=analito.maximo,
                    unidade_medida=analito.unidade or None,
                )
            )
            total += 1
    return total


def _ordens_recebidas(session: Session) -> list[tuple[UUID, datetime]]:
    """OS com amostra recebida no central, junto do instante do recebimento."""
    ordens = session.execute(
        select(OrdemServico.id, Amostra.id)
        .join(Amostra, Amostra.ordem_servico_id == OrdemServico.id)
        .where(Amostra.status == "RECEBIDA")
    ).all()

    resultado = []
    for ordem_id, amostra_id in ordens:
        recebido_em = session.scalar(
            select(AmostraMovimentacao.ocorrido_em).where(
                AmostraMovimentacao.amostra_id == amostra_id,
                AmostraMovimentacao.status == "RECEBIDA",
            )
        )
        resultado.append((ordem_id, recebido_em))
    return resultado


def _processar_ordem(
    session: Session,
    servico: LaboratorialService,
    ordem_id: UUID,
    recebido_em: datetime | None,
    procedimentos: dict,
    catalogo: dict,
    equipamentos: dict,
    responsaveis: list,
    tecnico: Usuario | None,
    contagem: dict[str, int],
) -> None:
    itens = [i for i in os_repository.listar_itens(session, ordem_id) if i.status != StatusOsItem.CANCELADO]
    if not itens or tecnico is None:
        return

    situacao = random.choices(list(_PESOS_BANCADA), weights=list(_PESOS_BANCADA.values()))[0]
    base = recebido_em or _agora_fallback()
    t_resultado, t_laudo = _atrasos_da_bancada(base)
    revisado = situacao != "aguardando"

    for indice, item in enumerate(itens):
        procedimento = procedimentos.get(item.procedimento_id)
        entrada = catalogo.get(procedimento.codigo_tuss) if procedimento else None
        if entrada is None:
            continue

        equipamento = equipamentos.get(entrada.setor)
        for analito in entrada.analitos:
            resultado = servico.registrar_resultado(
                ResultadoCreate(
                    os_item_id=item.id,
                    equipamento_id=equipamento.id if equipamento else None,
                    analito=analito.nome,
                    valor=_valor_medido(analito),
                    status=StatusResultado.REVISADO if revisado else StatusResultado.AGUARDANDO_REVISAO,
                    usuario_id=tecnico.id,
                )
            )
            resultado.importado_em = t_resultado
            contagem["resultados"] += 1

        if not revisado:
            continue

        # No cenário parcial só a primeira metade dos exames sai do rascunho.
        liberar = situacao == "liberado" or indice < len(itens) // 2 + len(itens) % 2
        responsavel = random.choice(responsaveis)
        laudo = servico.criar_laudo(LaudoCreate(os_item_id=item.id, responsavel_tecnico_id=responsavel.id))
        contagem["laudos"] += 1

        if not liberar:
            continue

        servico.atualizar_laudo(
            laudo.id,
            LaudoUpdate(
                status=StatusLaudo.LIBERADO,
                assinatura_digital=f"CRM {responsavel.crm}/{responsavel.uf_crm}",
            ),
            tecnico.id,
        )
        laudo.liberado_em = t_laudo
        contagem["laudos_liberados"] += 1

    _retrodatar_conclusao(session, ordem_id, t_laudo)


def _atrasos_da_bancada(recebido_em: datetime) -> tuple[datetime, datetime]:
    """Resultado e laudo saem mais rápido conforme o processo amadurece.

    No começo da série a bancada demora mais (processo novo); com os anos o
    laboratório automatiza e o TAT melhora até ~55% do atraso inicial — o que
    aparece no BI como ganho real de tempo de atendimento.
    """
    fator = max(0.55, 1.0 - 0.12 * anos_de_operacao(recebido_em))
    t_resultado = somar_horas(recebido_em, 1 * fator, 10 * fator)
    t_laudo = somar_horas(t_resultado, 1 * fator, 14 * fator)
    return t_resultado, t_laudo


def _retrodatar_conclusao(session: Session, ordem_id: UUID, instante: datetime) -> None:
    for historico in os_repository.listar_historico(session, ordem_id):
        if historico.status == "CONCLUIDA":
            historico.ocorrido_em = instante


def _valor_medido(analito) -> str:
    """Valor plausível: a maior parte dentro da faixa, o resto alterado."""
    amplitude = analito.maximo - analito.minimo
    if random.random() < _PROPORCAO_FORA_DA_FAIXA:
        if random.random() < 0.5:
            valor = analito.minimo - amplitude * random.uniform(0.05, 0.30)
        else:
            valor = analito.maximo + amplitude * random.uniform(0.05, 0.45)
    else:
        valor = random.uniform(analito.minimo, analito.maximo)

    valor = max(valor, 0)
    if analito.maximo >= 1000:
        return str(int(round(valor, -1)))
    if analito.maximo >= 100:
        return str(int(round(valor)))
    return f"{valor:.2f}"


def _agora_fallback() -> datetime:
    from src.seeder.config import agora

    return agora() - timedelta(days=1)


def main() -> None:
    contagem = executar_seeder_laboratorial()
    print("Seed laboratorial finalizado")
    for chave, valor in contagem.items():
        print(f"{chave}: {valor}")


if __name__ == "__main__":
    main()
