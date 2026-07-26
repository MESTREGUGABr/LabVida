import streamlit as st

from src.cadastro.procedimento.service import listar_procedimentos_ativos as listar_procedimentos
from src.cadastro.unidade.service import (
    listar_setores_ativos as listar_setores,
    listar_unidades_ativas as listar_unidades,
)
from src.db import session_scope
from src.laboratorial.dtos import (
    EquipamentoCreate,
    ProtocoloEquipamento,
    ValorReferenciaCreate,
)
from src.laboratorial.service import LaboratorialService
from src.ui import renderizar_menu, shell
from src.ui_components import renderizar_cabecalho, renderizar_secao
from src.ui_icons import ICONE_RESULTADO


def main() -> None:
    ctx = shell("Cadastros Laboratoriais", layout="wide", permissao="laboratorial:registrar_resultado")
    renderizar_menu(ctx["usuario_id"])

    renderizar_cabecalho(
        titulo="Cadastros Laboratoriais",
        subtitulo="Gerencie Equipamentos e Valores de Referencia",
        icone=ICONE_RESULTADO,
    )

    tab1, tab2 = st.tabs(["Equipamentos", "Valores de Referência"])

    with tab1:
        _render_equipamentos()

    with tab2:
        _render_valores_referencia()


def _render_equipamentos() -> None:
    renderizar_secao(titulo="Novo Equipamento")

    with session_scope() as session:
        unidades = listar_unidades(session)
        if not unidades:
            st.warning("Cadastre ao menos uma unidade central primeiro.")
            return

        setores = listar_setores(session, unidades[0].id)
        if not setores:
            st.warning("Cadastre ao menos um setor na unidade central.")
            return

        setor_opcoes = {s.nome: s.id for s in setores}
        setor_escolhido = st.selectbox("Setor", options=list(setor_opcoes.keys()))
        nome_eq = st.text_input("Nome do Equipamento")
        protocolo = st.selectbox(
            "Protocolo", options=[p.value for p in ProtocoloEquipamento]
        )

        if st.button("Salvar Equipamento", type="primary"):
            service = LaboratorialService(session)
            service.criar_equipamento(
                EquipamentoCreate(
                    setor_id=setor_opcoes[setor_escolhido],
                    nome=nome_eq,
                    protocolo=ProtocoloEquipamento(protocolo),
                )
            )
            st.success(f"Equipamento {nome_eq} salvo com sucesso!")

    st.divider()
    renderizar_secao(titulo="Equipamentos Cadastrados")
    with session_scope() as session:
        service = LaboratorialService(session)
        lista_eq = service.listar_equipamentos()
        if lista_eq:
            st.dataframe(
                [
                    {"ID": e.id, "Nome": e.nome, "Protocolo": e.protocolo.value}
                    for e in lista_eq
                ],
                width="stretch",
            )
        else:
            st.info("Nenhum equipamento cadastrado.")


def _render_valores_referencia() -> None:
    renderizar_secao(titulo="Novo Valor de Referencia")
    with session_scope() as session:
        procedimentos = listar_procedimentos(session)
        if not procedimentos:
            st.warning("Cadastre ao menos um procedimento primeiro.")
            return

        proc_opcoes = {p.nome: p.id for p in procedimentos}
        proc_escolhido = st.selectbox(
            "Procedimento", options=list(proc_opcoes.keys())
        )

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
                        unidade_medida=unid if unid else None,
                    )
                )
                st.success("Valor de Referência salvo com sucesso!")
            except ValueError as e:
                st.error(str(e))

    st.divider()
    renderizar_secao(titulo="Valores de Referencia Cadastrados")
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
                        "Texto": vr.valor_esperado_texto,
                    }
                    for vr in lista_vr
                ],
                width="stretch",
            )
        else:
            st.info("Nenhum valor de referência cadastrado.")


if __name__ == "__main__":
    main()
