import time

import streamlit as st
from sqlalchemy.orm import Session
from sqlalchemy import select

from src.db import session_scope
from src.atendimento.ordem_servico.models import OsItem
from src.laboratorial.dtos import LaudoCreate, LaudoUpdate
from src.laboratorial.models import StatusLaudo, StatusResultado
from src.laboratorial.service import LaboratorialService
from src.cadastro.medico.service import listar_medicos_ativos

st.set_page_config(page_title="Emissão de Laudos", page_icon="📝", layout="wide")

st.title("📝 Laudos e Liberação")
st.markdown("Emita e assine digitalmente os laudos dos exames.")

def listar_os_itens(session: Session):
    return session.scalars(select(OsItem)).all()

with session_scope() as session:
    itens = listar_os_itens(session)
    if not itens:
        st.info("Nenhuma OS cadastrada no momento.")
    else:
        service = LaboratorialService(session)
        # Filtra apenas itens que têm resultados ou já têm laudo
        opcoes_itens = {
            f"OS {item.ordem_servico.id} - Proc {item.procedimento.nome}": item
            for item in itens if item.ordem_servico and 
            (service.listar_resultados_por_os_item(item.id) or service.obter_laudo_por_os_item(item.id))
        }
        
        if not opcoes_itens:
            st.info("Nenhuma OS possui resultados para emitir laudo.")
        else:
            escolha = st.selectbox("Selecione a OS / Exame para Laudo", options=list(opcoes_itens.keys()))
            item_selecionado = opcoes_itens[escolha]
            
            laudo = service.obter_laudo_por_os_item(item_selecionado.id)
            resultados = service.listar_resultados_por_os_item(item_selecionado.id)
            
            st.subheader("Resultados do Exame")
            todos_revisados = True
            if resultados:
                for res in resultados:
                    if res.status != StatusResultado.REVISADO:
                        todos_revisados = False
                    st.write(f"- **{res.analito}:** {res.valor} ({res.status.value})")
            else:
                st.warning("Nenhum resultado registrado ainda.")
                todos_revisados = False
                
            if not todos_revisados:
                st.warning("Atenção: Nem todos os resultados foram digitados e REVISADOS. Você não deve liberar o laudo ainda.")
                
            st.divider()
            
            if not laudo:
                st.info("Este exame ainda não tem Laudo. Clique abaixo para iniciar o Rascunho.")
                if st.button("Criar Rascunho de Laudo", type="primary"):
                    try:
                        service.criar_laudo(LaudoCreate(os_item_id=item_selecionado.id))
                        st.toast("Laudo criado como Rascunho.", icon="✅")
                        time.sleep(2.5)
                        st.rerun()
                    except ValueError as e:
                        st.error(str(e))
            else:
                st.subheader(f"Status do Laudo: {laudo.status.value}")
                
                if laudo.status == StatusLaudo.LIBERADO:
                    st.success(f"Laudo liberado em {laudo.liberado_em.strftime('%d/%m/%Y %H:%M')}")
                    st.write(f"**Assinatura Digital:** {laudo.assinatura_digital or 'Sem assinatura'}")
                else:
                    medicos = [medico for medico in listar_medicos_ativos(session) if medico.responsavel_tecnico]
                    medico_opts = {
                        f"{medico.nome} · CRM {medico.crm}/{medico.uf_crm}": medico.id
                        for medico in medicos
                    }

                    if not medico_opts:
                        st.warning("Nenhum médico responsável técnico ativo está cadastrado.")
                        st.stop()
                    
                    responsavel = st.selectbox("Responsável Técnico", options=list(medico_opts.keys()))
                    assinatura = st.text_input("Assinatura Digital (Hash/Chave)")
                    
                    if st.button("Salvar e LIBERAR Laudo", type="primary"):
                        try:
                            service.atualizar_laudo(
                                laudo.id,
                                LaudoUpdate(
                                    responsavel_tecnico_id=medico_opts[responsavel],
                                    assinatura_digital=assinatura if assinatura else None,
                                    status=StatusLaudo.LIBERADO,
                                )
                            )
                            st.toast("Laudo LIBERADO com sucesso!", icon="✅")
                            time.sleep(0.5)
                            st.rerun()
                        except ValueError as e:
                            st.error(str(e))
