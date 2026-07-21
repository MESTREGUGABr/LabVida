import streamlit as st
from sqlalchemy.orm import Session

from src.db import session_scope
from src.laboratorial.dtos import EquipamentoCreate, ProtocoloEquipamento, ValorReferenciaCreate
from src.laboratorial.service import LaboratorialService
from src.cadastro.unidade.service import listar_unidades, listar_setores
from src.cadastro.procedimento.service import listar_procedimentos

st.set_page_config(page_title="Cadastros Laboratoriais", page_icon="⚙️", layout="wide")

st.title("⚙️ Cadastros Laboratoriais")
st.markdown("Gerencie Equipamentos e Valores de Referência.")

tab1, tab2 = st.tabs(["Equipamentos", "Valores de Referência"])

with tab1:
    st.header("Novo Equipamento")
    
    with session_scope() as session:
        unidades = listar_unidades(session)
        if not unidades:
            st.warning("Cadastre ao menos uma unidade central primeiro.")
        else:
            setores = listar_setores(session, unidades[0].id)
            if not setores:
                st.warning("Cadastre ao menos um setor na unidade central.")
            else:
                setor_opcoes = {s.nome: s.id for s in setores}
                setor_escolhido = st.selectbox("Setor", options=list(setor_opcoes.keys()))
                nome_eq = st.text_input("Nome do Equipamento")
                protocolo = st.selectbox("Protocolo", options=[p.value for p in ProtocoloEquipamento])
                
                if st.button("Salvar Equipamento", type="primary"):
                    service = LaboratorialService(session)
                    service.criar_equipamento(
                        EquipamentoCreate(
                            setor_id=setor_opcoes[setor_escolhido],
                            nome=nome_eq,
                            protocolo=ProtocoloEquipamento(protocolo)
                        )
                    )
                    st.success(f"Equipamento {nome_eq} salvo com sucesso!")

    st.divider()
    st.header("Equipamentos Cadastrados")
    with session_scope() as session:
        service = LaboratorialService(session)
        lista_eq = service.listar_equipamentos()
        if lista_eq:
            st.dataframe(
                [{"ID": e.id, "Nome": e.nome, "Protocolo": e.protocolo.value} for e in lista_eq],
                use_container_width=True
            )
        else:
            st.info("Nenhum equipamento cadastrado.")

with tab2:
    st.header("Novo Valor de Referência")
    with session_scope() as session:
        procedimentos = listar_procedimentos(session)
        if not procedimentos:
            st.warning("Cadastre ao menos um procedimento primeiro.")
        else:
            proc_opcoes = {p.nome: p.id for p in procedimentos}
            proc_escolhido = st.selectbox("Procedimento", options=list(proc_opcoes.keys()))
            
            analito = st.text_input("Analito")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                minimo = st.number_input("Valor Mínimo", value=0.0, format="%f")
            with col2:
                maximo = st.number_input("Valor Máximo", value=0.0, format="%f")
            with col3:
                unid = st.text_input("Unidade de Medida (ex: mg/dL)")
                
            valor_esperado = st.text_input("Valor Esperado (Texto / Qualitativo)")
            
            if st.button("Salvar Valor Referência", type="primary"):
                service = LaboratorialService(session)
                try:
                    service.criar_valor_referencia(
                        ValorReferenciaCreate(
                            procedimento_id=proc_opcoes[proc_escolhido],
                            analito=analito,
                            minimo=minimo if minimo != 0.0 else None,
                            maximo=maximo if maximo != 0.0 else None,
                            valor_esperado_texto=valor_esperado if valor_esperado else None,
                            unidade_medida=unid if unid else None
                        )
                    )
                    st.success("Valor de Referência salvo com sucesso!")
                except ValueError as e:
                    st.error(str(e))
    
    st.divider()
    st.header("Valores de Referência Cadastrados")
    with session_scope() as session:
        service = LaboratorialService(session)
        lista_vr = service.listar_valores_referencia()
        if lista_vr:
            st.dataframe(
                [
                    {
                        "ID": vr.id, 
                        "Analito": vr.analito, 
                        "Min": vr.minimo, 
                        "Max": vr.maximo, 
                        "Texto": vr.valor_esperado_texto
                    } for vr in lista_vr
                ],
                use_container_width=True
            )
        else:
            st.info("Nenhum valor de referência cadastrado.")
