"""add laboratorial models

Revision ID: f6ccac7706b1
Revises: 0005_stack_b_logistica
Create Date: 2026-07-21 14:59:05.239945

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'f6ccac7706b1'
down_revision: Union[str, None] = '0005_stack_b_logistica'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'equipamentos',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True),
        sa.Column('setor_id', sa.UUID(as_uuid=True), sa.ForeignKey('setores.id'), nullable=False),
        sa.Column('nome', sa.String(120), nullable=False),
        sa.Column('protocolo', sa.Enum('HL7', 'ASTM', name='protocolo_equipamento'), nullable=False)
    )
    op.create_table(
        'valores_referencia',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True),
        sa.Column('procedimento_id', sa.UUID(as_uuid=True), sa.ForeignKey('procedimentos.id'), nullable=False),
        sa.Column('analito', sa.String(120), nullable=False),
        sa.Column('minimo', sa.Numeric(10, 4), nullable=True),
        sa.Column('maximo', sa.Numeric(10, 4), nullable=True),
        sa.Column('valor_esperado_texto', sa.String(255), nullable=True),
        sa.Column('unidade_medida', sa.String(50), nullable=True)
    )
    op.create_table(
        'resultados',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True),
        sa.Column('os_item_id', sa.UUID(as_uuid=True), sa.ForeignKey('os_itens.id'), nullable=False, index=True),
        sa.Column('equipamento_id', sa.UUID(as_uuid=True), sa.ForeignKey('equipamentos.id'), nullable=True),
        sa.Column('analito', sa.String(120), nullable=False),
        sa.Column('valor', sa.String(255), nullable=False),
        sa.Column('status', sa.Enum('AGUARDANDO_REVISAO', 'REVISADO', name='status_resultado'), nullable=False, server_default='AGUARDANDO_REVISAO'),
        sa.Column('importado_em', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()'))
    )
    op.create_table(
        'laudos',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True),
        sa.Column('os_item_id', sa.UUID(as_uuid=True), sa.ForeignKey('os_itens.id'), nullable=False, unique=True),
        sa.Column('responsavel_tecnico_id', sa.UUID(as_uuid=True), sa.ForeignKey('medicos.id'), nullable=True),
        sa.Column('status', sa.Enum('RASCUNHO', 'LIBERADO', name='status_laudo'), nullable=False, server_default='RASCUNHO'),
        sa.Column('liberado_em', sa.DateTime(timezone=True), nullable=True),
        sa.Column('assinatura_digital', sa.Text(), nullable=True)
    )
    op.create_table(
        'resultados_auditoria',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True),
        sa.Column('resultado_id', sa.UUID(as_uuid=True), sa.ForeignKey('resultados.id'), nullable=False, index=True),
        sa.Column('usuario_id', sa.UUID(as_uuid=True), sa.ForeignKey('usuarios.id'), nullable=False),
        sa.Column('valor_anterior', sa.String(255), nullable=False),
        sa.Column('valor_novo', sa.String(255), nullable=False),
        sa.Column('ocorrido_em', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()'))
    )


def downgrade() -> None:
    op.drop_table('resultados_auditoria')
    op.drop_table('laudos')
    op.drop_table('resultados')
    op.drop_table('valores_referencia')
    op.drop_table('equipamentos')
    
    # Drop enums
    op.execute("DROP TYPE IF EXISTS protocolo_equipamento")
    op.execute("DROP TYPE IF EXISTS status_resultado")
    op.execute("DROP TYPE IF EXISTS status_laudo")
