"""Seed dos cadastros-base (unidades, convênios, procedimentos, médicos).

Idempotente por tabela: só insere quando a tabela está vazia, para não colidir
com FKs de OS/itens já existentes. Habilita abrir uma OS ponta a ponta na demo.
"""

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
from src.cadastro.unidade.dtos import SetorCreate, TipoUnidade, UnidadeCreate
from src.cadastro.unidade.service import criar_setor, criar_unidade
from src.db import session_scope


_UNIDADES = [
    ("Laboratório Central Garanhuns", TipoUnidade.CENTRAL, ["Bioquímica", "Hematologia", "Recepção"]),
    ("Unidade de Coleta Centro", TipoUnidade.COLETA, ["Coleta"]),
    ("Unidade de Coleta Heliópolis", TipoUnidade.COLETA, ["Coleta"]),
    ("Unidade de Coleta São José", TipoUnidade.COLETA, ["Coleta"]),
    ("Unidade de Coleta Boa Vista", TipoUnidade.COLETA, ["Coleta"]),
]

_CONVENIOS = [("Unimed", "417033"), ("Bradesco Saúde", "005711"), ("Hapvida", "368253")]

_PROCEDIMENTOS = [
    ("40302016", "Hemograma completo", "Hematologia"),
    ("40301630", "Glicose", "Bioquímica"),
    ("40301770", "Colesterol total", "Bioquímica"),
    ("40311902", "TSH", "Bioquímica"),
    ("40307450", "Urina tipo I (EAS)", "Bioquímica"),
]

_MEDICOS = [
    ("Dra. Helena Vasconcelos", "12345", "PE", True),
    ("Dr. Rafael Lins", "54321", "PE", False),
]


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
    for nome, tipo, nomes_setores in _UNIDADES:
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
    return [criar_convenio(session, ConvenioCreate(nome=nome, registro_ans=ans)).id for nome, ans in _CONVENIOS]


def _seed_procedimentos(session: Session) -> list:
    existentes = procedimento_repository.listar_ativos(session)
    if existentes:
        return [p.id for p in existentes]
    return [
        criar_procedimento(
            session, ProcedimentoCreate(codigo_tuss=tuss, nome=nome, setor=setor)
        ).id
        for tuss, nome, setor in _PROCEDIMENTOS
    ]


def _seed_valores(session: Session, procedimentos_ids: list, convenios_ids: list) -> int:
    total = 0
    for procedimento_id in procedimentos_ids:
        for convenio_id in convenios_ids:
            if procedimento_repository.obter_valor_vigente(
                session, procedimento_id, convenio_id, date.today()
            ):
                continue
            definir_valor(
                session,
                ProcedimentoValorCreate(
                    procedimento_id=procedimento_id,
                    convenio_id=convenio_id,
                    valor=Decimal("35.00"),
                    vigencia_inicio=date(date.today().year, 1, 1),
                ),
            )
            total += 1
    return total


def _seed_medicos(session: Session) -> int:
    if medico_repository.listar_ativos(session):
        return 0
    for nome, crm, uf, responsavel in _MEDICOS:
        criar_medico(
            session,
            MedicoCreate(nome=nome, crm=crm, uf_crm=uf, responsavel_tecnico=responsavel),
        )
    return len(_MEDICOS)


def main() -> None:
    contagem = executar_seeder_cadastros()
    print("Seed de cadastros finalizado")
    for chave, valor in contagem.items():
        print(f"{chave}: {valor}")


if __name__ == "__main__":
    main()
