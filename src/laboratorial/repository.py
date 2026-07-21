from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.laboratorial.models import (
    Equipamento,
    Laudo,
    Resultado,
    ResultadoAuditoria,
    ValorReferencia,
)


class LaboratorialRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    # --- Equipamento ---
    def get_equipamento(self, equipamento_id: UUID) -> Equipamento | None:
        return self.session.get(Equipamento, equipamento_id)

    def list_equipamentos(self, setor_id: UUID | None = None) -> Sequence[Equipamento]:
        stmt = select(Equipamento)
        if setor_id:
            stmt = stmt.where(Equipamento.setor_id == setor_id)
        return self.session.scalars(stmt).all()

    def save_equipamento(self, equipamento: Equipamento) -> Equipamento:
        self.session.add(equipamento)
        self.session.flush()
        return equipamento

    def delete_equipamento(self, equipamento: Equipamento) -> None:
        self.session.delete(equipamento)
        self.session.flush()

    # --- Valor Referencia ---
    def get_valor_referencia(self, valor_referencia_id: UUID) -> ValorReferencia | None:
        return self.session.get(ValorReferencia, valor_referencia_id)

    def list_valores_referencia(
        self, procedimento_id: UUID | None = None
    ) -> Sequence[ValorReferencia]:
        stmt = select(ValorReferencia)
        if procedimento_id:
            stmt = stmt.where(ValorReferencia.procedimento_id == procedimento_id)
        return self.session.scalars(stmt).all()

    def save_valor_referencia(
        self, valor_referencia: ValorReferencia
    ) -> ValorReferencia:
        self.session.add(valor_referencia)
        self.session.flush()
        return valor_referencia

    def delete_valor_referencia(self, valor_referencia: ValorReferencia) -> None:
        self.session.delete(valor_referencia)
        self.session.flush()

    # --- Resultado ---
    def get_resultado(self, resultado_id: UUID) -> Resultado | None:
        return self.session.get(Resultado, resultado_id)

    def get_resultados_by_os_item(self, os_item_id: UUID) -> Sequence[Resultado]:
        stmt = select(Resultado).where(Resultado.os_item_id == os_item_id)
        return self.session.scalars(stmt).all()

    def save_resultado(self, resultado: Resultado) -> Resultado:
        self.session.add(resultado)
        self.session.flush()
        return resultado

    def save_auditoria(self, auditoria: ResultadoAuditoria) -> ResultadoAuditoria:
        self.session.add(auditoria)
        self.session.flush()
        return auditoria
        
    def list_auditoria_by_resultado(self, resultado_id: UUID) -> Sequence[ResultadoAuditoria]:
        stmt = select(ResultadoAuditoria).where(ResultadoAuditoria.resultado_id == resultado_id).order_by(ResultadoAuditoria.ocorrido_em.desc())
        return self.session.scalars(stmt).all()

    # --- Laudo ---
    def get_laudo(self, laudo_id: UUID) -> Laudo | None:
        return self.session.get(Laudo, laudo_id)

    def get_laudo_by_os_item(self, os_item_id: UUID) -> Laudo | None:
        stmt = select(Laudo).where(Laudo.os_item_id == os_item_id)
        return self.session.scalars(stmt).first()

    def save_laudo(self, laudo: Laudo) -> Laudo:
        self.session.add(laudo)
        self.session.flush()
        return laudo
