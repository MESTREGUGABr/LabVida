"""Seed dos cadastros-base (unidades, convênios, procedimentos, médicos).

Idempotente por tabela: só insere quando a tabela está vazia, para não colidir
com FKs de OS/itens já existentes. É a fundação de todo o resto do seeder — sem
procedimento com valor vigente por convênio não se abre uma OS.
"""

import random
from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session

from src.cadastro.convenio import repository as convenio_repository
from src.cadastro.convenio.dtos import ConvenioCreate
from src.cadastro.convenio.service import criar_convenio
from src.cadastro.medico import repository as medico_repository
from src.cadastro.medico.dtos import MedicoCreate
from src.cadastro.medico.service import criar_medico
from src.cadastro.procedimento import repository as procedimento_repository
from src.cadastro.procedimento.dtos import ProcedimentoCreate, ProcedimentoValorCreate
from src.cadastro.procedimento.service import criar_procedimento, definir_valor
from src.cadastro.unidade import repository as unidade_repository
from src.cadastro.unidade.dtos import SetorCreate, UnidadeCreate
from src.cadastro.unidade.service import criar_setor, criar_unidade
from src.db import session_scope
from src.seeder.catalogo import CONVENIOS, MEDICOS, PROCEDIMENTOS, UNIDADES
from src.seeder.config import qtd
from src.seeder.documentos import gerar_cnpj, gerar_telefone


def executar_seeder_cadastros() -> dict[str, int]:
    contagem = {"unidades": 0, "setores": 0, "convenios": 0, "procedimentos": 0, "valores": 0, "medicos": 0}

    with session_scope() as session:
        contagem["unidades"], contagem["setores"] = _seed_unidades(session)
        convenios_ids = _seed_convenios(session)
        contagem["convenios"] = len(convenios_ids)
        procedimentos_ids = _seed_procedimentos(session)
        contagem["procedimentos"] = len(procedimentos_ids)
        contagem["valores"] = _seed_valores(session, procedimentos_ids, convenios_ids)
        contagem["medicos"] = _seed_medicos(session)

    return contagem


def _seed_unidades(session: Session) -> tuple[int, int]:
    if unidade_repository.listar_unidades_ativas(session):
        return 0, 0
    unidades = 0
    setores = 0
    for nome, tipo, nomes_setores in UNIDADES:
        unidade = criar_unidade(session, UnidadeCreate(nome=nome, tipo=tipo))
        unidades += 1
        for nome_setor in nomes_setores:
            criar_setor(session, SetorCreate(unidade_id=unidade.id, nome=nome_setor))
            setores += 1
    return unidades, setores


def _seed_convenios(session: Session) -> list:
    existentes = convenio_repository.listar_ativos(session)
    if existentes:
        return [c.id for c in existentes]

    cnpjs_usados: set[str] = set()
    ids = []
    for nome, registro_ans in CONVENIOS[: qtd(len(CONVENIOS))]:
        convenio = criar_convenio(
            session,
            ConvenioCreate(
                nome=nome,
                registro_ans=registro_ans,
                cnpj=gerar_cnpj(cnpjs_usados),
                telefone=gerar_telefone(),
                email=f"faturamento@{nome.split()[0].lower()}.com.br",
            ),
        )
        ids.append(convenio.id)
    return ids


def _seed_procedimentos(session: Session) -> list:
    existentes = procedimento_repository.listar_ativos(session)
    if existentes:
        return [p.id for p in existentes]
    return [
        criar_procedimento(
            session,
            ProcedimentoCreate(codigo_tuss=p.codigo_tuss, nome=p.nome, setor=p.setor),
        ).id
        for p in PROCEDIMENTOS[: qtd(len(PROCEDIMENTOS))]
    ]


def _seed_valores(session: Session, procedimentos_ids: list, convenios_ids: list) -> int:
    """Tabela de preços negociada: cada convênio paga um percentual do valor base."""
    valores_base = {p.codigo_tuss: p.valor_base for p in PROCEDIMENTOS}
    fatores = {cid: Decimal(str(round(random.uniform(0.82, 1.18), 2))) for cid in convenios_ids}
    inicio_vigencia = date(date.today().year, 1, 1)

    total = 0
    for procedimento_id in procedimentos_ids:
        procedimento = procedimento_repository.obter_por_id(session, procedimento_id)
        valor_base = valores_base.get(procedimento.codigo_tuss, Decimal("35.00")) if procedimento else Decimal("35.00")

        # `None` primeiro = TABELA PARTICULAR (balcao). Ate a fase F3 ela nao
        # existia: o valor do particular era digitado a mao na abertura da OS.
        # O balcao cobra o valor cheio; convenio negocia percentual sobre ele.
        for convenio_id in [None] + list(convenios_ids):
            if procedimento_repository.obter_valor_vigente(
                session, procedimento_id, convenio_id, date.today()
            ):
                continue
            valor = (
                valor_base
                if convenio_id is None
                else (valor_base * fatores[convenio_id]).quantize(Decimal("0.01"))
            )
            definir_valor(
                session,
                ProcedimentoValorCreate(
                    procedimento_id=procedimento_id,
                    convenio_id=convenio_id,
                    valor=valor,
                    vigencia_inicio=inicio_vigencia,
                ),
            )
            total += 1
    return total


def _seed_medicos(session: Session) -> int:
    if medico_repository.listar_ativos(session):
        return 0
    medicos = MEDICOS[: max(2, qtd(len(MEDICOS)))]
    for nome, crm, uf, responsavel in medicos:
        criar_medico(
            session,
            MedicoCreate(nome=nome, crm=crm, uf_crm=uf, responsavel_tecnico=responsavel),
        )
    return len(medicos)


def main() -> None:
    contagem = executar_seeder_cadastros()
    print("Seed de cadastros finalizado")
    for chave, valor in contagem.items():
        print(f"{chave}: {valor}")


if __name__ == "__main__":
    main()
