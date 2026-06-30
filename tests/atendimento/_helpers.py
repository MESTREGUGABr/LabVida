from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session

from src.cadastro.convenio.dtos import ConvenioCreate
from src.cadastro.convenio.service import criar_convenio
from src.cadastro.dtos import PacienteCreate, SexoPaciente
from src.cadastro.procedimento.dtos import ProcedimentoCreate, ProcedimentoValorCreate
from src.cadastro.procedimento.service import criar_procedimento, definir_valor
from src.cadastro.service import criar_paciente
from src.cadastro.unidade.dtos import TipoUnidade, UnidadeCreate
from src.cadastro.unidade.service import criar_unidade
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
