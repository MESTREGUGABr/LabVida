import hashlib
from datetime import date
from decimal import Decimal

from sqlalchemy import func, select, text

from src.bi.models import (
    DimConvenio,
    DimPacienteAnon,
    DimProcedimento,
    DimTempo,
    DimUnidade,
    FatoAtendimento,
    FatoFaturamento,
    FatoFinanceiro,
    FatoLogistica,
)
from src.atendimento.amostra.models import Amostra
from src.atendimento.ordem_servico.models import OrdemServico, OsItem
from src.cadastro.convenio.models import Convenio
from src.cadastro.models import Paciente
from src.cadastro.procedimento.models import Procedimento
from src.cadastro.unidade.models import Unidade
from src.faturamento.glosa.models import Glosa
from src.faturamento.lote_faturamento.models import GuiaItem, GuiaTiss, LoteFaturamento
from src.financeiro.titulo_pagar.models import TituloPagar
from src.financeiro.titulo_receber.models import TituloReceber
from src.logistica.recebimento.models import AmostraMovimentacao
from src.db import session_scope

_DIAS_SEMANA = [
    "Segunda-feira", "Terca-feira", "Quarta-feira",
    "Quinta-feira", "Sexta-feira", "Sabado", "Domingo",
]


def _sk_tempo(session, data_ref: date) -> int:
    dim = session.scalar(select(DimTempo).where(DimTempo.data == data_ref))
    if dim:
        return dim.sk_tempo
    dim = DimTempo(
        data=data_ref, ano=data_ref.year, mes=data_ref.month, dia=data_ref.day,
        dia_semana=_DIAS_SEMANA[data_ref.weekday()],
        trimestre=(data_ref.month - 1) // 3 + 1,
    )
    session.add(dim)
    session.flush()
    return dim.sk_tempo


def _sk_unidade(session, uid, nome="", tipo="") -> int:
    dim = session.scalar(select(DimUnidade).where(DimUnidade.id_origem == uid))
    if dim:
        return dim.sk_unidade
    dim = DimUnidade(id_origem=uid, nome=nome, tipo=tipo)
    session.add(dim)
    session.flush()
    return dim.sk_unidade


def _sk_convenio(session, cid, nome="", ans=None) -> int | None:
    if cid is None:
        return None
    dim = session.scalar(select(DimConvenio).where(DimConvenio.id_origem == cid))
    if dim:
        return dim.sk_convenio
    dim = DimConvenio(id_origem=cid, nome=nome, registro_ans=ans)
    session.add(dim)
    session.flush()
    return dim.sk_convenio


def _sk_procedimento(session, pid, tuss="", nome="", setor=None) -> int:
    dim = session.scalar(select(DimProcedimento).where(DimProcedimento.id_origem == pid))
    if dim:
        return dim.sk_procedimento
    dim = DimProcedimento(id_origem=pid, codigo_tuss=tuss, nome=nome, setor=setor)
    session.add(dim)
    session.flush()
    return dim.sk_procedimento


def _hash_paciente(pid) -> str:
    """Pseudônimo determinístico do paciente para o BI (não reversível para PII)."""
    return hashlib.sha256(str(pid).encode()).hexdigest()


def _sk_paciente(session, pid, nasc=None, sexo=None) -> int:
    id_hash = _hash_paciente(pid)
    dim = session.scalar(select(DimPacienteAnon).where(DimPacienteAnon.id_origem == id_hash))
    if dim:
        return dim.sk_paciente
    faixa = "Desconhecida"
    if nasc:
        hoje = date.today()
        idade = hoje.year - nasc.year - ((hoje.month, hoje.day) < (nasc.month, nasc.day))
        if idade <= 12: faixa = "0-12 anos"
        elif idade <= 18: faixa = "13-18 anos"
        elif idade <= 30: faixa = "19-30 anos"
        elif idade <= 50: faixa = "31-50 anos"
        elif idade <= 65: faixa = "51-65 anos"
        else: faixa = "66+ anos"
    sexo_str = sexo.value if hasattr(sexo, 'value') else str(sexo) if sexo else "NAO_INFORMADO"
    dim = DimPacienteAnon(id_origem=id_hash, faixa_etaria=faixa, sexo=sexo_str)
    session.add(dim)
    session.flush()
    return dim.sk_paciente


def _carga_dimensoes(session):
    _sk_unidade(session, "00000000-0000-0000-0000-000000000000", "Consolidado", "SISTEMA")
    _sk_tempo(session, date.today())
    for u in session.scalars(select(Unidade)).all():
        _sk_unidade(session, u.id, u.nome, u.tipo.value if hasattr(u.tipo, 'value') else str(u.tipo))
    for c in session.scalars(select(Convenio)).all():
        _sk_convenio(session, c.id, c.nome, c.registro_ans)
    for p in session.scalars(select(Procedimento)).all():
        _sk_procedimento(session, p.id, p.codigo_tuss, p.nome, None)
    for p in session.scalars(select(Paciente)).all():
        _sk_paciente(session, p.id, p.data_nascimento, p.sexo)
    session.commit()


def _carga_fatos(session):
    session.execute(text("DELETE FROM bi_fato_logistica"))
    session.execute(text("DELETE FROM bi_fato_financeiro"))
    session.execute(text("DELETE FROM bi_fato_faturamento"))
    session.execute(text("DELETE FROM bi_fato_atendimento"))
    session.commit()

    su_consolidado = _sk_unidade(session, "00000000-0000-0000-0000-000000000000", "Consolidado", "SISTEMA")

    ordens = session.scalars(select(OrdemServico)).all()
    for os in ordens:
        if os.aberta_em is None:
            continue
        st = _sk_tempo(session, os.aberta_em.date())
        su = _sk_unidade(session, os.unidade_id)
        paciente = session.get(Paciente, os.paciente_id)
        if not paciente:
            continue
        sp = _sk_paciente(session, paciente.id, paciente.data_nascimento, paciente.sexo)
        sc = _sk_convenio(session, os.convenio_id)
        for item in session.scalars(select(OsItem).where(OsItem.ordem_servico_id == os.id)).all():
            spr = _sk_procedimento(session, item.procedimento_id)
            session.add(FatoAtendimento(sk_tempo=st, sk_unidade=su, sk_convenio=sc, sk_procedimento=spr, sk_paciente=sp, qtd_exames=1))
    session.commit()

    for gi in session.scalars(select(GuiaItem)).all():
        guia = session.get(GuiaTiss, gi.guia_tiss_id) if gi.guia_tiss_id else None
        if guia is None:
            continue
        lote = session.get(LoteFaturamento, guia.lote_faturamento_id)
        data_ref = lote.fechado_em.date() if lote and lote.fechado_em else date.today()
        st = _sk_tempo(session, data_ref)
        sc = _sk_convenio(session, lote.convenio_id) if lote else None
        spr = _sk_procedimento(session, gi.procedimento_id)
        glosa_total = Decimal("0")
        for g in session.scalars(select(Glosa).where(Glosa.guia_item_id == gi.id)).all():
            glosa_total += g.valor_glosado or Decimal("0")
        session.add(FatoFaturamento(sk_tempo=st, sk_unidade=su_consolidado, sk_convenio=sc, sk_procedimento=spr,
                                    valor_faturado=gi.valor_faturado or Decimal("0"), valor_glosado=glosa_total))
    session.commit()

    for t in session.scalars(select(TituloReceber)).all():
        data_ref = t.vencimento if t.vencimento else date.today()
        st = _sk_tempo(session, data_ref)
        session.add(FatoFinanceiro(sk_tempo=st, sk_unidade=su_consolidado, sk_convenio=None, valor_recebido=Decimal(str(t.valor or 0)), valor_pago=Decimal("0")))
    for t in session.scalars(select(TituloPagar)).all():
        data_ref = t.vencimento if t.vencimento else date.today()
        st = _sk_tempo(session, data_ref)
        session.add(FatoFinanceiro(sk_tempo=st, sk_unidade=su_consolidado, sk_convenio=None, valor_recebido=Decimal("0"), valor_pago=Decimal(str(t.valor or 0))))
    session.commit()

    for a in session.scalars(select(Amostra)).all():
        st = _sk_tempo(session, date.today())
        su = su_consolidado
        if a.ordem_servico_id:
            os_obj = session.get(OrdemServico, a.ordem_servico_id)
            if os_obj:
                su = _sk_unidade(session, os_obj.unidade_id)
        divergentes = 0
        movs = session.scalars(select(AmostraMovimentacao).where(AmostraMovimentacao.amostra_id == a.id)).all()
        for m in movs:
            if m.status == "REJEITADA":
                divergentes += 1
        session.add(FatoLogistica(sk_tempo=st, sk_unidade=su, qtd_amostras=1, amostras_divergentes=divergentes))
    session.commit()


def executar_etl() -> None:
    with session_scope() as session:
        _carga_dimensoes(session)
        _carga_fatos(session)
    print("ETL BI concluido.")


if __name__ == "__main__":
    executar_etl()
