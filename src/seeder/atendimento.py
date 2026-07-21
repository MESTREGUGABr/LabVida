"""Seed de Ordens de Serviço, Coletas, Malotes e Recebimentos (vários status de amostra).

Cria cenários práticos para testes na interface Streamlit:
- OS e Amostra COLETADA (aguardando malote)
- Malote e Amostras EM_TRANSITO (aguardando recepção no central)
- Malote e Amostras RECEBIDAS (OS em EM_ANALISE no central)
- Amostras REJEITADAS por avaria no transporte
"""

from decimal import Decimal

from sqlalchemy.orm import Session

from src.atendimento.amostra.dtos import ColetaCreate, TipoMaterial
from src.atendimento.amostra.service import registrar_coleta
from src.atendimento.ordem_servico import repository as os_repository
from src.atendimento.ordem_servico.dtos import OrdemServicoCreate, OsItemInput
from src.atendimento.ordem_servico.service import abrir_os
from src.cadastro.convenio.repository import listar_ativos as listar_convenios
from src.cadastro.medico.repository import listar_ativos as listar_medicos
from src.cadastro.procedimento.repository import listar_ativos as listar_procedimentos
from src.cadastro.service import listar_pacientes_ativos as listar_pacientes
from src.cadastro.unidade.repository import listar_unidades_ativas
from src.db import session_scope
from src.logistica.malote.dtos import MaloteCreate
from src.logistica.malote.service import (
    adicionar_amostra_ao_malote,
    criar_malote,
    despachar_malote,
)
from src.logistica.recebimento.dtos import ProtocoloRecebimentoCreate
from src.logistica.recebimento.service import receber_malote
from src.usuario.models import Usuario


def executar_seeder_atendimento() -> dict[str, int]:
    contagem = {"ordens_servico": 0, "amostras": 0, "malotes": 0, "recebimentos": 0}

    with session_scope() as session:
        if os_repository.listar_os(session):
            return contagem

        pacientes = listar_pacientes(session)
        medicos = listar_medicos(session)
        convenios = listar_convenios(session)
        procedimentos = listar_procedimentos(session)
        unidades = listar_unidades_ativas(session)

        usuario = session.query(Usuario).first()
        if not usuario:
            usuario = Usuario(email="seeder@labvida.com.br", nome="Seeder do Sistema", ativo=True)
            session.add(usuario)
            session.flush()

        if not (pacientes and procedimentos and unidades):
            return contagem

        unidades_coleta = [u for u in unidades if u.tipo == "COLETA"] or unidades
        unidades_central = [u for u in unidades if u.tipo == "CENTRAL"] or unidades

        coleta_unit = unidades_coleta[0]
        central_unit = unidades_central[0]
        medico = medicos[0] if medicos else None
        convenio = convenios[0] if convenios else None
        procedimento = procedimentos[0]

        # Cenário 1: OS + Amostra COLETADA (Pendente de malote)
        ordem1 = abrir_os(
            session,
            OrdemServicoCreate(
                paciente_id=pacientes[0].id,
                unidade_id=coleta_unit.id,
                medico_id=medico.id if medico else None,
                convenio_id=convenio.id if convenio else None,
                itens=[OsItemInput(procedimento_id=procedimento.id, valor_negociado=Decimal("50.00"))],
            ),
            usuario.id,
        )
        amostra1 = registrar_coleta(
            session,
            ColetaCreate(
                ordem_servico_id=ordem1.id,
                tipo_material=TipoMaterial.SANGUE,
                coletor_usuario_id=usuario.id,
            ),
        )
        contagem["ordens_servico"] += 1
        contagem["amostras"] += 1

        # Cenário 2: Malote + Amostra EM_TRANSITO
        if len(pacientes) > 1:
            ordem2 = abrir_os(
                session,
                OrdemServicoCreate(
                    paciente_id=pacientes[1].id,
                    unidade_id=coleta_unit.id,
                    medico_id=medico.id if medico else None,
                    convenio_id=convenio.id if convenio else None,
                    itens=[OsItemInput(procedimento_id=procedimento.id, valor_negociado=Decimal("50.00"))],
                ),
                usuario.id,
            )
            amostra2 = registrar_coleta(
                session,
                ColetaCreate(
                    ordem_servico_id=ordem2.id,
                    tipo_material=TipoMaterial.URINA,
                    coletor_usuario_id=usuario.id,
                ),
            )
            malote2 = criar_malote(
                session,
                MaloteCreate(
                    unidade_origem_id=coleta_unit.id,
                    unidade_destino_id=central_unit.id,
                    enviado_por_usuario_id=usuario.id,
                ),
            )
            adicionar_amostra_ao_malote(session, malote2.id, amostra2.id)
            despachar_malote(session, malote2.id, usuario.id)

            contagem["ordens_servico"] += 1
            contagem["amostras"] += 1
            contagem["malotes"] += 1

        # Cenário 3: Malote + Amostra RECEBIDA (OS em EM_ANALISE)
        if len(pacientes) > 2:
            ordem3 = abrir_os(
                session,
                OrdemServicoCreate(
                    paciente_id=pacientes[2].id,
                    unidade_id=coleta_unit.id,
                    medico_id=medico.id if medico else None,
                    convenio_id=convenio.id if convenio else None,
                    itens=[OsItemInput(procedimento_id=procedimento.id, valor_negociado=Decimal("50.00"))],
                ),
                usuario.id,
            )
            amostra3 = registrar_coleta(
                session,
                ColetaCreate(
                    ordem_servico_id=ordem3.id,
                    tipo_material=TipoMaterial.SANGUE,
                    coletor_usuario_id=usuario.id,
                ),
            )
            malote3 = criar_malote(
                session,
                MaloteCreate(
                    unidade_origem_id=coleta_unit.id,
                    unidade_destino_id=central_unit.id,
                    enviado_por_usuario_id=usuario.id,
                ),
            )
            adicionar_amostra_ao_malote(session, malote3.id, amostra3.id)
            despachar_malote(session, malote3.id, usuario.id)
            receber_malote(
                session,
                ProtocoloRecebimentoCreate(
                    malote_id=malote3.id,
                    recebido_por_usuario_id=usuario.id,
                    integridade_ok=True,
                    observacao="Amostra recebida sem ranhuras ou fraturas",
                ),
            )

            contagem["ordens_servico"] += 1
            contagem["amostras"] += 1
            contagem["malotes"] += 1
            contagem["recebimentos"] += 1

        # Cenário 4: Amostra REJEITADA por avaria
        if len(pacientes) > 3:
            ordem4 = abrir_os(
                session,
                OrdemServicoCreate(
                    paciente_id=pacientes[3].id,
                    unidade_id=coleta_unit.id,
                    medico_id=medico.id if medico else None,
                    convenio_id=convenio.id if convenio else None,
                    itens=[OsItemInput(procedimento_id=procedimento.id, valor_negociado=Decimal("50.00"))],
                ),
                usuario.id,
            )
            amostra4 = registrar_coleta(
                session,
                ColetaCreate(
                    ordem_servico_id=ordem4.id,
                    tipo_material=TipoMaterial.FEZES,
                    coletor_usuario_id=usuario.id,
                ),
            )
            malote4 = criar_malote(
                session,
                MaloteCreate(
                    unidade_origem_id=coleta_unit.id,
                    unidade_destino_id=central_unit.id,
                    enviado_por_usuario_id=usuario.id,
                ),
            )
            adicionar_amostra_ao_malote(session, malote4.id, amostra4.id)
            despachar_malote(session, malote4.id, usuario.id)
            receber_malote(
                session,
                ProtocoloRecebimentoCreate(
                    malote_id=malote4.id,
                    recebido_por_usuario_id=usuario.id,
                    integridade_ok=False,
                    observacao="Frasco trincado e material extravasado",
                ),
            )

            contagem["ordens_servico"] += 1
            contagem["amostras"] += 1
            contagem["malotes"] += 1
            contagem["recebimentos"] += 1

    return contagem


def main() -> None:
    contagem = executar_seeder_atendimento()
    print("Seed de atendimento e logística finalizado")
    for chave, valor in contagem.items():
        print(f"{chave}: {valor}")


if __name__ == "__main__":
    main()
