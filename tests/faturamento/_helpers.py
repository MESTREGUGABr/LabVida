import uuid
from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session

from src.atendimento.ordem_servico.dtos import StatusOrdemServico, StatusOsItem
from src.atendimento.ordem_servico.models import OrdemServico, OsItem
from src.cadastro.convenio.dtos import ConvenioCreate
from src.cadastro.convenio.service import criar_convenio
from src.cadastro.dtos import PacienteCreate, SexoPaciente
from src.cadastro.procedimento.dtos import ProcedimentoCreate, ProcedimentoValorCreate
from src.cadastro.procedimento.service import criar_procedimento, definir_valor
from src.cadastro.service import criar_paciente
from src.cadastro.unidade.dtos import TipoUnidade, UnidadeCreate
from src.cadastro.unidade.service import criar_unidade
from src.laboratorial.models import Laudo, StatusLaudo
from src.usuario.service import sincronizar_usuario


@dataclass
class Base:
    paciente_id: UUID
    unidade_id: UUID
    convenio_id: UUID
    procedimento_id: UUID
    usuario_id: UUID
    valor_tabela: Decimal


def montar_base(session: Session, valor_tabela: Decimal = Decimal("42.00")) -> Base:
    paciente = criar_paciente(
        session,
        PacienteCreate(
            cpf="52998224725",
            nome="Ana Maria",
            data_nascimento=date.today() - timedelta(days=10000),
            telefone="87999991234",
            sexo=SexoPaciente.FEMININO,
        ),
    )
    unidade = criar_unidade(session, UnidadeCreate(nome="Central", tipo=TipoUnidade.CENTRAL))
    convenio = criar_convenio(session, ConvenioCreate(nome="Unimed"))
    procedimento = criar_procedimento(
        session, ProcedimentoCreate(codigo_tuss="40302016", nome="Hemograma")
    )
    definir_valor(
        session,
        ProcedimentoValorCreate(
            procedimento_id=procedimento.id,
            convenio_id=convenio.id,
            valor=valor_tabela,
            vigencia_inicio=date.today() - timedelta(days=1),
        ),
    )
    usuario = sincronizar_usuario(session, "coletor@labvida.test", "Coletor Teste")

    return Base(
        paciente_id=paciente.id,
        unidade_id=unidade.id,
        convenio_id=convenio.id,
        procedimento_id=procedimento.id,
        usuario_id=usuario.id,
        valor_tabela=valor_tabela,
    )


def criar_laudo_liberado(session: Session, base: Base) -> Laudo:
    """Laudo pronto para faturar, sem depender do fluxo inteiro da bancada."""
    ordem = OrdemServico(
        codigo_os=f"OS-TESTE-{uuid.uuid4().hex[:6].upper()}",
        paciente_id=base.paciente_id,
        convenio_id=base.convenio_id,
        unidade_id=base.unidade_id,
        status=StatusOrdemServico.EM_ANALISE,
    )
    session.add(ordem)
    session.flush()

    item = OsItem(
        ordem_servico_id=ordem.id,
        procedimento_id=base.procedimento_id,
        valor_negociado=base.valor_tabela,
        status=StatusOsItem.COLETADO,
    )
    session.add(item)
    session.flush()

    laudo = Laudo(os_item_id=item.id, status=StatusLaudo.LIBERADO)
    session.add(laudo)
    session.commit()
    return laudo
