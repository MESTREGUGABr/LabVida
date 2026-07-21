from collections.abc import Sequence
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from src.laboratorial.dtos import (
    EquipamentoCreate,
    EquipamentoUpdate,
    LaudoCreate,
    LaudoUpdate,
    ResultadoCreate,
    ResultadoUpdate,
    ValorReferenciaCreate,
    ValorReferenciaUpdate,
)
from src.laboratorial.models import (
    Equipamento,
    Laudo,
    Resultado,
    ResultadoAuditoria,
    StatusLaudo,
    ValorReferencia,
)
from src.laboratorial.repository import LaboratorialRepository


class LaboratorialService:
    def __init__(self, session: Session) -> None:
        self.repository = LaboratorialRepository(session)

    # --- Equipamento ---
    def criar_equipamento(self, dto: EquipamentoCreate) -> Equipamento:
        equipamento = Equipamento(
            setor_id=dto.setor_id,
            nome=dto.nome,
            protocolo=dto.protocolo,
        )
        return self.repository.save_equipamento(equipamento)

    def atualizar_equipamento(
        self, equipamento_id: UUID, dto: EquipamentoUpdate
    ) -> Equipamento:
        equipamento = self.repository.get_equipamento(equipamento_id)
        if not equipamento:
            raise ValueError("Equipamento não encontrado")

        if dto.setor_id is not None:
            equipamento.setor_id = dto.setor_id
        if dto.nome is not None:
            equipamento.nome = dto.nome
        if dto.protocolo is not None:
            equipamento.protocolo = dto.protocolo

        return self.repository.save_equipamento(equipamento)

    def obter_equipamento(self, equipamento_id: UUID) -> Equipamento:
        equipamento = self.repository.get_equipamento(equipamento_id)
        if not equipamento:
            raise ValueError("Equipamento não encontrado")
        return equipamento

    def listar_equipamentos(self, setor_id: UUID | None = None) -> Sequence[Equipamento]:
        return self.repository.list_equipamentos(setor_id)

    # --- Valor Referencia ---
    def criar_valor_referencia(self, dto: ValorReferenciaCreate) -> ValorReferencia:
        if dto.minimo is None and dto.maximo is None and dto.valor_esperado_texto is None:
            raise ValueError("Deve ser fornecido pelo menos um valor de referência (min, max ou texto)")
            
        valor_ref = ValorReferencia(
            procedimento_id=dto.procedimento_id,
            analito=dto.analito,
            minimo=dto.minimo,
            maximo=dto.maximo,
            valor_esperado_texto=dto.valor_esperado_texto,
            unidade_medida=dto.unidade_medida,
        )
        return self.repository.save_valor_referencia(valor_ref)

    def atualizar_valor_referencia(
        self, valor_referencia_id: UUID, dto: ValorReferenciaUpdate
    ) -> ValorReferencia:
        valor_ref = self.repository.get_valor_referencia(valor_referencia_id)
        if not valor_ref:
            raise ValueError("Valor de Referência não encontrado")

        if dto.procedimento_id is not None:
            valor_ref.procedimento_id = dto.procedimento_id
        if dto.analito is not None:
            valor_ref.analito = dto.analito
        if dto.minimo is not None:
            valor_ref.minimo = dto.minimo
        if dto.maximo is not None:
            valor_ref.maximo = dto.maximo
        if dto.valor_esperado_texto is not None:
            valor_ref.valor_esperado_texto = dto.valor_esperado_texto
        if dto.unidade_medida is not None:
            valor_ref.unidade_medida = dto.unidade_medida

        return self.repository.save_valor_referencia(valor_ref)

    def listar_valores_referencia(
        self, procedimento_id: UUID | None = None
    ) -> Sequence[ValorReferencia]:
        return self.repository.list_valores_referencia(procedimento_id)
        
    def deletar_valor_referencia(self, valor_referencia_id: UUID) -> None:
        valor_ref = self.repository.get_valor_referencia(valor_referencia_id)
        if not valor_ref:
            raise ValueError("Valor de Referência não encontrado")
        self.repository.delete_valor_referencia(valor_ref)

    # --- Resultado ---
    def registrar_resultado(self, dto: ResultadoCreate) -> Resultado:
        # Criar resultado
        resultado = Resultado(
            os_item_id=dto.os_item_id,
            equipamento_id=dto.equipamento_id,
            analito=dto.analito,
            valor=dto.valor,
            status=dto.status,
        )
        resultado = self.repository.save_resultado(resultado)
        
        # Registrar auditoria
        auditoria = ResultadoAuditoria(
            resultado_id=resultado.id,
            usuario_id=dto.usuario_id,
            valor_anterior="",
            valor_novo=dto.valor
        )
        self.repository.save_auditoria(auditoria)
        return resultado

    def atualizar_resultado(self, resultado_id: UUID, dto: ResultadoUpdate) -> Resultado:
        resultado = self.repository.get_resultado(resultado_id)
        if not resultado:
            raise ValueError("Resultado não encontrado")
            
        valor_anterior = resultado.valor
        teve_alteracao = False

        if dto.equipamento_id is not None:
            resultado.equipamento_id = dto.equipamento_id
            teve_alteracao = True
        if dto.valor is not None and dto.valor != resultado.valor:
            resultado.valor = dto.valor
            teve_alteracao = True
        if dto.status is not None:
            resultado.status = dto.status
            teve_alteracao = True
            
        resultado = self.repository.save_resultado(resultado)
        
        if teve_alteracao and dto.valor is not None and valor_anterior != dto.valor:
            auditoria = ResultadoAuditoria(
                resultado_id=resultado.id,
                usuario_id=dto.usuario_id,
                valor_anterior=valor_anterior,
                valor_novo=dto.valor
            )
            self.repository.save_auditoria(auditoria)

        return resultado

    def listar_resultados_por_os_item(self, os_item_id: UUID) -> Sequence[Resultado]:
        return self.repository.get_resultados_by_os_item(os_item_id)
        
    def listar_auditoria_resultado(self, resultado_id: UUID) -> Sequence[ResultadoAuditoria]:
        return self.repository.list_auditoria_by_resultado(resultado_id)

    # --- Laudo ---
    def criar_laudo(self, dto: LaudoCreate) -> Laudo:
        existente = self.repository.get_laudo_by_os_item(dto.os_item_id)
        if existente:
            raise ValueError("Laudo já existe para este item de OS")
            
        laudo = Laudo(
            os_item_id=dto.os_item_id,
            responsavel_tecnico_id=dto.responsavel_tecnico_id,
        )
        return self.repository.save_laudo(laudo)

    def atualizar_laudo(self, laudo_id: UUID, dto: LaudoUpdate) -> Laudo:
        laudo = self.repository.get_laudo(laudo_id)
        if not laudo:
            raise ValueError("Laudo não encontrado")
            
        if laudo.status == StatusLaudo.LIBERADO:
            raise ValueError("Laudo liberado não pode ser alterado")

        if dto.responsavel_tecnico_id is not None:
            laudo.responsavel_tecnico_id = dto.responsavel_tecnico_id
        if dto.assinatura_digital is not None:
            laudo.assinatura_digital = dto.assinatura_digital
            
        if dto.status == StatusLaudo.LIBERADO:
            if not laudo.responsavel_tecnico_id:
                raise ValueError("Laudo precisa de um responsável técnico para ser liberado")
            laudo.status = StatusLaudo.LIBERADO
            laudo.liberado_em = datetime.now(timezone.utc)
            
        return self.repository.save_laudo(laudo)

    def obter_laudo_por_os_item(self, os_item_id: UUID) -> Laudo | None:
        return self.repository.get_laudo_by_os_item(os_item_id)
