import streamlit as st
from sqlalchemy.orm import Session
from sqlalchemy import select

from src.db import session_scope
from src.atendimento.ordem_servico.models import OsItem
from src.laboratorial.dtos import LaudoCreate, LaudoUpdate
from src.laboratorial.models import StatusLaudo, StatusResultado
from src.laboratorial.service import LaboratorialService
from src.usuario.service import listar_usuarios

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
                    service.criar_laudo(LaudoCreate(os_item_id=item_selecionado.id))
                    st.success("Laudo criado como Rascunho.")
                    st.rerun()
            else:
                st.subheader(f"Status do Laudo: {laudo.status.value}")
                
                if laudo.status == StatusLaudo.LIBERADO:
                    st.success(f"Laudo liberado em {laudo.liberado_em.strftime('%d/%m/%Y %H:%M')}")
                    st.write(f"**Assinatura Digital:** {laudo.assinatura_digital or 'Sem assinatura'}")
                else:
                    usuarios = listar_usuarios(session)
                    user_opts = {u.nome: u.id for u in usuarios}
                    
                    responsavel = st.selectbox("Responsável Técnico (Biomédico/Médico)", options=list(user_opts.keys()))
                    assinatura = st.text_input("Assinatura Digital (Hash/Chave)")
                    
                    if st.button("Salvar e LIBERAR Laudo", type="primary"):
                        try:
                            # 1. Update with responsavel and assinatura
                            service.atualizar_laudo(
                                laudo.id, 
                                LaudoUpdate(
                                    responsavel_tecnico_id=user_opts[responsavel],
                                    assinatura_digital=assinatura if assinatura else None
                                )
                            )
                            # 2. Update status to LIBERADO
                            service.atualizar_laudo(laudo.id, LaudoUpdate(status=StatusLaudo.LIBERADO))
                            st.success("Laudo LIBERADO com sucesso!")
                            st.rerun()
                        except ValueError as e:
                            st.error(str(e))
