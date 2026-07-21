import streamlit as st
from sqlalchemy.orm import Session
from sqlalchemy import select

from src.db import session_scope
from src.atendimento.ordem_servico.models import OrdemServico, OsItem
from src.laboratorial.dtos import ResultadoCreate, ResultadoUpdate
from src.laboratorial.models import StatusResultado
from src.laboratorial.service import LaboratorialService
from src.usuario.service import listar_usuarios

st.set_page_config(page_title="Resultados de Exames", page_icon="🔬", layout="wide")

st.title("🔬 Digitação e Conferência de Resultados")
st.markdown("Selecione um item de Ordem de Serviço para lançar ou revisar resultados.")

def listar_os_itens(session: Session):
    return session.scalars(select(OsItem)).all()

with session_scope() as session:
    itens = listar_os_itens(session)
    if not itens:
        st.info("Nenhuma OS cadastrada no momento.")
    else:
        opcoes_itens = {f"OS {item.ordem_servico.id} - Proc {item.procedimento.nome}": item for item in itens if item.ordem_servico}
        escolha = st.selectbox("Selecione a Amostra / Item de OS", options=list(opcoes_itens.keys()))
        
        item_selecionado = opcoes_itens[escolha]
        
        st.subheader("Resultados do Exame")
        service = LaboratorialService(session)
        resultados_existentes = service.listar_resultados_por_os_item(item_selecionado.id)
        
        if resultados_existentes:
            for res in resultados_existentes:
                with st.expander(f"Analito: {res.analito} - Valor: {res.valor} ({res.status.value})"):
                    st.write(f"**Data da última alteração:** {res.importado_em}")
                    usuarios = listar_usuarios(session)
                    user_opts = {u.nome: u.id for u in usuarios}
                    revisor = st.selectbox("Usuário Revisor", options=list(user_opts.keys()), key=f"rev_{res.id}")
                    
                    novo_valor = st.text_input("Atualizar Valor", value=res.valor, key=f"val_{res.id}")
                    
                    if st.button("Revisar e Salvar", key=f"btn_{res.id}", type="primary"):
                        service.atualizar_resultado(
                            res.id,
                            ResultadoUpdate(
                                valor=novo_valor,
                                status=StatusResultado.REVISADO,
                                usuario_id=user_opts[revisor]
                            )
                        )
                        st.success("Resultado atualizado com sucesso!")
                        st.rerun()
                        
                    st.markdown("**Auditoria (Histórico):**")
                    auditoria = service.listar_auditoria_resultado(res.id)
                    for aud in auditoria:
                        st.caption(f"- {aud.ocorrido_em.strftime('%d/%m %H:%M')} | Valor: '{aud.valor_anterior}' -> '{aud.valor_novo}'")
                        
        st.divider()
        st.subheader("Inserir Novo Resultado")
        with st.form("form_resultado"):
            novo_analito = st.text_input("Analito")
            novo_valor = st.text_input("Valor Encontrado")
            
            usuarios = listar_usuarios(session)
            user_opts = {u.nome: u.id for u in usuarios}
            if not user_opts:
                st.warning("Cadastre um usuário primeiro.")
            else:
                digitador = st.selectbox("Usuário Digitador", options=list(user_opts.keys()))
                
                if st.form_submit_button("Registrar"):
                    service.registrar_resultado(
                        ResultadoCreate(
                            os_item_id=item_selecionado.id,
                            analito=novo_analito,
                            valor=novo_valor,
                            usuario_id=user_opts[digitador]
                        )
                    )
                    st.success("Resultado inserido com sucesso!")
                    st.rerun()
