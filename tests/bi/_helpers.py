"""Cenario operacional controlado para os testes de BI.

O ETL le o OLTP inteiro, entao testar a carga exige montar um operacional com
datas conhecidas — nao serve criar via services, que carimbam `now()`.
"""

import uuid
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal

from sqlalchemy.orm import Session

from src.atendimento.amostra.models import Amostra, Coleta
from src.atendimento.ordem_servico.models import OrdemServico, OsItem
from src.cadastro.convenio.models import Convenio
from src.cadastro.dtos import SexoPaciente
from src.cadastro.models import Paciente
from src.cadastro.procedimento.models import Procedimento
from src.cadastro.unidade.models import Unidade
from src.faturamento.glosa.models import Glosa
from src.faturamento.lote_faturamento.models import GuiaItem, GuiaTiss, LoteFaturamento
from src.financeiro.movimento_caixa.models import MovimentoCaixa
from src.financeiro.titulo_receber.models import TituloReceber
from src.laboratorial.models import Laudo, StatusLaudo
from src.logistica.malote.models import Malote, MaloteAmostra
from src.logistica.recebimento.models import ProtocoloRecebimento
from src.usuario.models import Usuario

# CPFs validos e distintos (o model valida digito verificador na origem).
_CPFS = ["52998224725", "11144477735", "19100000000", "12345678909"]


def utc(ano: int, mes: int, dia: int, hora: int = 8, minuto: int = 0) -> datetime:
    return datetime(ano, mes, dia, hora, minuto, tzinfo=timezone.utc)


@dataclass
class Cenario:
    unidade_coleta: uuid.UUID
    unidade_central: uuid.UUID
    convenio: uuid.UUID
    procedimento_bioquimica: uuid.UUID
    procedimento_hematologia: uuid.UUID
    usuario: uuid.UUID
    pacientes: list[uuid.UUID] = field(default_factory=list)


def montar_cadastros(session: Session) -> Cenario:
    coleta = Unidade(nome="Posto Garanhuns", tipo="COLETA", ativo=True)
    central = Unidade(nome="Laboratorio Central", tipo="CENTRAL", ativo=True)
    convenio = Convenio(
        nome="Unimed BI",
        nome_normalizado="unimed bi",  # NOT NULL: o service normaliza, aqui e na mao
        status="ATIVO",
        ativo=True,
    )
    # Setores diferentes: o `setor` da dimensao era sempre NULL antes (bug B4).
    bioquimica = Procedimento(
        codigo_tuss="40301010", nome="Glicose", setor="Bioquimica", ativo=True
    )
    hematologia = Procedimento(
        codigo_tuss="40302016", nome="Hemograma", setor="Hematologia", ativo=True
    )
    usuario = Usuario(email=f"bi.{uuid.uuid4().hex[:8]}@labvida.test", nome="Operador BI", ativo=True)
    session.add_all([coleta, central, convenio, bioquimica, hematologia, usuario])
    session.flush()

    cenario = Cenario(
        unidade_coleta=coleta.id,
        unidade_central=central.id,
        convenio=convenio.id,
        procedimento_bioquimica=bioquimica.id,
        procedimento_hematologia=hematologia.id,
        usuario=usuario.id,
    )

    for indice, cpf in enumerate(_CPFS[:2]):
        paciente = Paciente(
            cpf=cpf,
            nome=f"Paciente BI {indice}",
            data_nascimento=date(1990, 6, 15),
            telefone="87999990000",
            sexo=SexoPaciente.FEMININO if indice % 2 == 0 else SexoPaciente.MASCULINO,
            ativo=True,
        )
        session.add(paciente)
        session.flush()
        cenario.pacientes.append(paciente.id)

    session.commit()
    return cenario


def criar_os(
    session: Session,
    cenario: Cenario,
    *,
    aberta_em: datetime,
    paciente_id: uuid.UUID | None = None,
    convenio_id: uuid.UUID | None = ...,
    procedimentos: list[uuid.UUID] | None = None,
    valor: Decimal = Decimal("50.00"),
) -> OrdemServico:
    ordem = OrdemServico(
        codigo_os=f"OS-BI-{uuid.uuid4().hex[:8].upper()}",
        paciente_id=paciente_id or cenario.pacientes[0],
        convenio_id=cenario.convenio if convenio_id is ... else convenio_id,
        unidade_id=cenario.unidade_coleta,
        status="EM_ANALISE",
        aberta_em=aberta_em,
    )
    session.add(ordem)
    session.flush()

    for procedimento_id in procedimentos or [cenario.procedimento_bioquimica]:
        session.add(
            OsItem(
                ordem_servico_id=ordem.id,
                procedimento_id=procedimento_id,
                valor_negociado=valor,
                status="COLETADO",
            )
        )
    session.flush()
    session.commit()
    return ordem


def coletar(session: Session, cenario: Cenario, ordem: OrdemServico, *, coletada_em: datetime) -> Amostra:
    amostra = Amostra(
        ordem_servico_id=ordem.id,
        codigo_barras=f"AM{uuid.uuid4().hex[:10].upper()}",
        tipo_material="SANGUE",
        status="COLETADA",
    )
    session.add(amostra)
    session.flush()
    session.add(Coleta(amostra_id=amostra.id, coletor_id=cenario.usuario, coletada_em=coletada_em))
    session.commit()
    return amostra


def transportar(
    session: Session,
    cenario: Cenario,
    amostra: Amostra,
    *,
    despachado_em: datetime,
    recebido_em: datetime,
) -> None:
    """Malote despachado e recebido — a origem do `tempo_transito_horas`."""
    malote = Malote(
        codigo_malote=f"ML{uuid.uuid4().hex[:8].upper()}",
        unidade_origem_id=cenario.unidade_coleta,
        unidade_destino_id=cenario.unidade_central,
        enviado_por_usuario_id=cenario.usuario,
        status="RECEBIDO",
        criado_em=despachado_em - timedelta(hours=1),
        despachado_em=despachado_em,
    )
    session.add(malote)
    session.flush()
    session.add(MaloteAmostra(malote_id=malote.id, amostra_id=amostra.id))
    session.add(
        ProtocoloRecebimento(
            malote_id=malote.id,
            recebido_por_usuario_id=cenario.usuario,
            integridade_ok=True,
            recebido_em=recebido_em,
        )
    )
    amostra.status = "RECEBIDA"
    session.commit()


def liberar_laudos(session: Session, ordem: OrdemServico, *, liberado_em: datetime) -> list[Laudo]:
    laudos = []
    itens = session.query(OsItem).filter(OsItem.ordem_servico_id == ordem.id).all()
    for item in itens:
        laudo = Laudo(os_item_id=item.id, status=StatusLaudo.LIBERADO, liberado_em=liberado_em)
        session.add(laudo)
        laudos.append(laudo)
    session.flush()
    session.commit()
    return laudos


def faturar(
    session: Session,
    cenario: Cenario,
    laudos: list[Laudo],
    *,
    fechado_em: datetime | None,
    convenio_id: uuid.UUID | None = ...,
    valor: Decimal = Decimal("50.00"),
) -> LoteFaturamento:
    """Lote com guia e itens. `fechado_em=None` deixa o lote ABERTO."""
    lote = LoteFaturamento(
        codigo_lote=f"LT{uuid.uuid4().hex[:8].upper()}",
        convenio_id=cenario.convenio if convenio_id is ... else convenio_id,
        status="FECHADO" if fechado_em else "ABERTO",
        valor_total=valor * len(laudos),
        criado_em=(fechado_em or utc(2026, 1, 1)) - timedelta(days=1),
        fechado_em=fechado_em,
    )
    session.add(lote)
    session.flush()

    guia = GuiaTiss(lote_faturamento_id=lote.id, codigo_tiss="TISS-BI", status_pre_auditoria="APROVADA")
    session.add(guia)
    session.flush()

    for laudo in laudos:
        item_os = session.get(OsItem, laudo.os_item_id)
        session.add(
            GuiaItem(
                guia_tiss_id=guia.id,
                laudo_id=laudo.id,
                procedimento_id=item_os.procedimento_id,
                valor_faturado=valor,
                status="FATURADO",
            )
        )
    session.flush()
    session.commit()
    return lote


def glosar(
    session: Session,
    cenario: Cenario,
    lote: LoteFaturamento,
    *,
    valor: Decimal,
    motivo: str,
    criado_em: datetime,
) -> Glosa:
    item = lote.guias[0].itens[0]
    glosa = Glosa(
        guia_item_id=item.id,
        motivo=motivo,
        valor_glosado=valor,
        unidade_origem_id=cenario.unidade_coleta,
        criado_em=criado_em,
    )
    session.add(glosa)
    session.commit()
    return glosa


def titulo_receber(
    session: Session,
    lote: LoteFaturamento,
    *,
    valor: Decimal,
    vencimento: date,
    status: str = "PENDENTE",
) -> TituloReceber:
    titulo = TituloReceber(
        lote_faturamento_id=lote.id,
        valor=valor,
        vencimento=vencimento,
        status=status,
    )
    session.add(titulo)
    session.commit()
    return titulo


def receber_em_caixa(
    session: Session,
    titulo: TituloReceber,
    *,
    valor: Decimal,
    ocorrido_em: datetime,
) -> MovimentoCaixa:
    movimento = MovimentoCaixa(
        titulo_receber_id=titulo.id,
        tipo="ENTRADA",
        valor=valor,
        ocorrido_em=ocorrido_em,
        descricao="Recebimento BI",
    )
    session.add(movimento)
    titulo.status = "PAGO"
    session.commit()
    return movimento
