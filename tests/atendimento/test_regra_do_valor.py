"""Regra do valor na abertura da OS (fase F3).

Apontamento do professor: "regra de negocio do valor pelos procedimentos".

Antes, qualquer valor digitado na abertura da OS **sobrescrevia a tabela sem
nenhuma checagem**, sem registrar o que a tabela dizia nem por que mudou. A
tabela de precos existia, mas nao mandava em nada.

A regra agora tem tres saidas, e a diferenca entre elas importa:

- valor omitido      -> usa a TABELA
- valor = tabela     -> usa a tabela (digitar o preco certo nao e excecao)
- valor != tabela    -> NEGOCIADO: exige permissao e motivo
- sem preco em tabela-> SEM_TABELA: passa, mas fica marcado

O ultimo caso e deliberado: bloquear a abertura da OS por causa de cadastro de
preco incompleto pararia o atendimento. A divergencia e responsabilidade da
pre-auditoria do faturamento, que e onde ela custa dinheiro.
"""

from datetime import date, timedelta
from decimal import Decimal

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.atendimento.ordem_servico.dtos import OrdemServicoCreate, OsItemInput
from src.atendimento.ordem_servico.errors import (
    MotivoDeExcecaoObrigatorio,
    ValorForaDaTabela,
    ValorItemNaoDefinido,
)
from src.atendimento.ordem_servico.models import OsItem
from src.atendimento.ordem_servico.service import abrir_os
from src.cadastro.procedimento.dtos import ProcedimentoCreate, ProcedimentoValorCreate
from src.cadastro.procedimento.service import criar_procedimento, definir_valor
from tests.atendimento._helpers import montar_base

# `montar_base` cadastra o procedimento com este preco de tabela.
VALOR_DE_TABELA = Decimal("42.00")


def _itens_da_os(session: Session, ordem_id) -> list[OsItem]:
    return list(
        session.scalars(select(OsItem).where(OsItem.ordem_servico_id == ordem_id)).all()
    )


def test_valor_omitido_usa_a_tabela(session: Session) -> None:
    base = montar_base(session)

    ordem = abrir_os(
        session,
        OrdemServicoCreate(
            paciente_id=base.paciente_id,
            unidade_id=base.unidade_id,
            convenio_id=base.convenio_id,
            itens=[OsItemInput(procedimento_id=base.procedimento_id)],
        ),
        base.usuario_id,
    )

    item = _itens_da_os(session, ordem.id)[0]
    assert item.valor_negociado == VALOR_DE_TABELA
    assert item.valor_tabela == VALOR_DE_TABELA
    assert item.origem_valor == "TABELA"
    assert item.motivo_excecao is None


def test_valor_igual_ao_da_tabela_nao_e_excecao(session: Session) -> None:
    """Digitar o preco certo nao pode exigir justificativa."""
    base = montar_base(session)

    ordem = abrir_os(
        session,
        OrdemServicoCreate(
            paciente_id=base.paciente_id,
            unidade_id=base.unidade_id,
            convenio_id=base.convenio_id,
            itens=[
                OsItemInput(
                    procedimento_id=base.procedimento_id, valor_negociado=VALOR_DE_TABELA
                )
            ],
        ),
        base.usuario_id,
    )

    item = _itens_da_os(session, ordem.id)[0]
    assert item.origem_valor == "TABELA"


def test_valor_divergente_exige_motivo(session: Session) -> None:
    base = montar_base(session)

    with pytest.raises(MotivoDeExcecaoObrigatorio):
        abrir_os(
            session,
            OrdemServicoCreate(
                paciente_id=base.paciente_id,
                unidade_id=base.unidade_id,
                convenio_id=base.convenio_id,
                itens=[
                    OsItemInput(
                        procedimento_id=base.procedimento_id, valor_negociado=Decimal("15.00")
                    )
                ],
            ),
            base.usuario_id,
        )


def test_valor_divergente_com_motivo_guarda_o_rastro(session: Session) -> None:
    """O ponto da regra: o que a TABELA dizia fica registrado ao lado do que foi
    cobrado, para a pre-auditoria e o BI poderem comparar depois."""
    base = montar_base(session)

    ordem = abrir_os(
        session,
        OrdemServicoCreate(
            paciente_id=base.paciente_id,
            unidade_id=base.unidade_id,
            convenio_id=base.convenio_id,
            itens=[
                OsItemInput(
                    procedimento_id=base.procedimento_id,
                    valor_negociado=Decimal("15.00"),
                    motivo_excecao="Campanha de outubro",
                )
            ],
        ),
        base.usuario_id,
    )

    item = _itens_da_os(session, ordem.id)[0]
    assert item.valor_negociado == Decimal("15.00")
    assert item.valor_tabela == VALOR_DE_TABELA
    assert item.origem_valor == "NEGOCIADO"
    assert item.motivo_excecao == "Campanha de outubro"


def test_sem_preco_em_tabela_passa_marcado(session: Session) -> None:
    """Cadastro de preco incompleto nao pode parar o atendimento."""
    base = montar_base(session)
    sem_preco = criar_procedimento(
        session, ProcedimentoCreate(codigo_tuss="40301010", nome="Glicose")
    )

    ordem = abrir_os(
        session,
        OrdemServicoCreate(
            paciente_id=base.paciente_id,
            unidade_id=base.unidade_id,
            convenio_id=base.convenio_id,
            itens=[OsItemInput(procedimento_id=sem_preco.id, valor_negociado=Decimal("33.00"))],
        ),
        base.usuario_id,
    )

    item = _itens_da_os(session, ordem.id)[0]
    assert item.origem_valor == "SEM_TABELA"
    assert item.valor_tabela is None
    assert item.valor_negociado == Decimal("33.00")


def test_sem_preco_e_sem_valor_e_recusado(session: Session) -> None:
    """Nao ha de onde tirar o valor: aqui bloquear e a unica saida honesta."""
    base = montar_base(session)
    sem_preco = criar_procedimento(
        session, ProcedimentoCreate(codigo_tuss="40301010", nome="Glicose")
    )

    with pytest.raises(ValorItemNaoDefinido):
        abrir_os(
            session,
            OrdemServicoCreate(
                paciente_id=base.paciente_id,
                unidade_id=base.unidade_id,
                convenio_id=base.convenio_id,
                itens=[OsItemInput(procedimento_id=sem_preco.id)],
            ),
            base.usuario_id,
        )


def test_os_particular_usa_a_tabela_particular(session: Session) -> None:
    """O ganho concreto do preco particular: o balcao deixa de ser digitado a mao."""
    base = montar_base(session)
    definir_valor(
        session,
        ProcedimentoValorCreate(
            procedimento_id=base.procedimento_id,
            convenio_id=None,
            valor=Decimal("99.00"),
            vigencia_inicio=date.today() - timedelta(days=1),
        ),
    )

    ordem = abrir_os(
        session,
        OrdemServicoCreate(
            paciente_id=base.paciente_id,
            unidade_id=base.unidade_id,
            convenio_id=None,
            itens=[OsItemInput(procedimento_id=base.procedimento_id)],
        ),
        base.usuario_id,
    )

    item = _itens_da_os(session, ordem.id)[0]
    assert item.valor_negociado == Decimal("99.00")
    assert item.origem_valor == "TABELA"


def test_sem_permissao_de_excecao_o_valor_divergente_e_barrado(session: Session) -> None:
    """Com RBAC configurado, negociar preco exige `faturamento:valor_excecao`.

    O bootstrap (tabela `perfis` vazia) libera, senao nao daria para abrir a
    primeira OS num banco novo — mesmo criterio dos outros gates (ADR 0002).
    """
    from src.rbac.models import Perfil, PerfilPermissao, Permissao
    from src.usuario.models import Usuario

    base = montar_base(session)

    perfil = Perfil(nome="atendente_sem_excecao", descricao="Sem excecao de valor")
    session.add(perfil)
    session.flush()
    permissao = Permissao(codigo="atendimento:abrir_os", descricao="Abrir OS")
    session.add(permissao)
    session.flush()
    session.add(PerfilPermissao(perfil_id=perfil.id, permissao_id=permissao.id))
    session.get(Usuario, base.usuario_id).perfil_id = perfil.id
    session.commit()

    with pytest.raises(ValorForaDaTabela, match="valor_excecao"):
        abrir_os(
            session,
            OrdemServicoCreate(
                paciente_id=base.paciente_id,
                unidade_id=base.unidade_id,
                convenio_id=base.convenio_id,
                itens=[
                    OsItemInput(
                        procedimento_id=base.procedimento_id,
                        valor_negociado=Decimal("15.00"),
                        motivo_excecao="Tentativa sem permissao",
                    )
                ],
            ),
            base.usuario_id,
        )
