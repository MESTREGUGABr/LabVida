"""Stack C — Faturamento, Financeiro e Compras

Revision ID: 0006_stack_c
Revises: f6ccac7706b1
Create Date: 2026-07-23

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '0006_stack_c'
down_revision: Union[str, None] = 'f6ccac7706b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'fornecedores',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True),
        sa.Column('nome', sa.String(150), nullable=False),
        sa.Column('cnpj', sa.String(14), nullable=False, unique=True),
        sa.Column('status', sa.String(20), nullable=False, server_default='ATIVO'),
        sa.Column('criado_em', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
    )
    op.create_table(
        'insumos_materiais',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True),
        sa.Column('nome', sa.String(150), nullable=False),
        sa.Column('finalidade', sa.String(255), nullable=False),
        sa.Column('quantidade_estoque', sa.Numeric(12, 3), nullable=False, server_default='0'),
        sa.Column('criado_em', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
    )
    op.create_table(
        'lotes_faturamento',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True),
        sa.Column('codigo_lote', sa.String(20), nullable=False, unique=True, index=True),
        sa.Column('convenio_id', sa.UUID(as_uuid=True), sa.ForeignKey('convenios.id'), nullable=False),
        sa.Column('status', sa.String(20), nullable=False, server_default='ABERTO'),
        sa.Column('valor_total', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('criado_em', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('fechado_em', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_table(
        'solicitacoes_compra',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True),
        sa.Column('solicitante_id', sa.UUID(as_uuid=True), sa.ForeignKey('usuarios.id'), nullable=False),
        sa.Column('status', sa.String(20), nullable=False, server_default='ABERTA'),
        sa.Column('criada_em', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
    )
    op.create_table(
        'guias_tiss',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True),
        sa.Column('lote_faturamento_id', sa.UUID(as_uuid=True), sa.ForeignKey('lotes_faturamento.id'), nullable=False),
        sa.Column('codigo_tiss', sa.String(30), nullable=False),
        sa.Column('status_pre_auditoria', sa.String(30), nullable=False, server_default='PENDENTE'),
        sa.Column('xml_tiss', sa.Text(), nullable=True),
        sa.Column('criado_em', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
    )
    op.create_table(
        'pedidos_compra',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True),
        sa.Column('solicitacao_compra_id', sa.UUID(as_uuid=True), sa.ForeignKey('solicitacoes_compra.id'), nullable=False),
        sa.Column('fornecedor_id', sa.UUID(as_uuid=True), sa.ForeignKey('fornecedores.id'), nullable=False),
        sa.Column('status', sa.String(20), nullable=False, server_default='RASCUNHO'),
        sa.Column('valor_total', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('criado_em', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
    )
    op.create_table(
        'guias_itens',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True),
        sa.Column('guia_tiss_id', sa.UUID(as_uuid=True), sa.ForeignKey('guias_tiss.id'), nullable=False),
        sa.Column('laudo_id', sa.UUID(as_uuid=True), sa.ForeignKey('laudos.id'), nullable=False, unique=True),
        sa.Column('procedimento_id', sa.UUID(as_uuid=True), sa.ForeignKey('procedimentos.id'), nullable=False),
        sa.Column('valor_faturado', sa.Numeric(12, 2), nullable=False),
        sa.Column('status', sa.String(20), nullable=False, server_default='FATURADO'),
        sa.Column('criado_em', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
    )
    op.create_table(
        'glosas',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True),
        sa.Column('guia_item_id', sa.UUID(as_uuid=True), sa.ForeignKey('guias_itens.id'), nullable=False),
        sa.Column('motivo', sa.String(255), nullable=False),
        sa.Column('valor_glosado', sa.Numeric(12, 2), nullable=False),
        sa.Column('unidade_origem_id', sa.UUID(as_uuid=True), sa.ForeignKey('unidades.id'), nullable=False),
        sa.Column('criado_em', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
    )
    op.create_table(
        'titulos_receber',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True),
        sa.Column('lote_faturamento_id', sa.UUID(as_uuid=True), sa.ForeignKey('lotes_faturamento.id'), nullable=False),
        sa.Column('valor', sa.Numeric(12, 2), nullable=False),
        sa.Column('vencimento', sa.Date(), nullable=False),
        sa.Column('status', sa.String(20), nullable=False, server_default='PENDENTE'),
        sa.Column('criado_em', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
    )
    op.create_table(
        'titulos_pagar',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True),
        sa.Column('pedido_compra_id', sa.UUID(as_uuid=True), sa.ForeignKey('pedidos_compra.id'), nullable=False),
        sa.Column('valor', sa.Numeric(12, 2), nullable=False),
        sa.Column('vencimento', sa.Date(), nullable=False),
        sa.Column('status', sa.String(20), nullable=False, server_default='PENDENTE'),
        sa.Column('criado_em', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
    )
    op.create_table(
        'recebimentos_insumo',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True),
        sa.Column('pedido_compra_id', sa.UUID(as_uuid=True), sa.ForeignKey('pedidos_compra.id'), nullable=False),
        sa.Column('recebido_em', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('conferido', sa.Boolean(), nullable=False, server_default=sa.text('true')),
    )
    op.create_table(
        'pedidos_itens',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True),
        sa.Column('pedido_compra_id', sa.UUID(as_uuid=True), sa.ForeignKey('pedidos_compra.id'), nullable=False),
        sa.Column('insumo_material_id', sa.UUID(as_uuid=True), sa.ForeignKey('insumos_materiais.id'), nullable=False),
        sa.Column('quantidade', sa.Numeric(12, 3), nullable=False),
        sa.Column('valor_unitario', sa.Numeric(12, 2), nullable=False),
    )
    op.create_table(
        'estoque_movimentos',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True),
        sa.Column('insumo_material_id', sa.UUID(as_uuid=True), sa.ForeignKey('insumos_materiais.id'), nullable=False),
        sa.Column('tipo', sa.String(20), nullable=False),
        sa.Column('quantidade', sa.Numeric(12, 3), nullable=False),
        sa.Column('ocorrido_em', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('observacao', sa.String(255), nullable=True),
    )
    op.create_table(
        'movimentos_caixa',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True),
        sa.Column('titulo_receber_id', sa.UUID(as_uuid=True), sa.ForeignKey('titulos_receber.id'), nullable=True),
        sa.Column('titulo_pagar_id', sa.UUID(as_uuid=True), sa.ForeignKey('titulos_pagar.id'), nullable=True),
        sa.Column('tipo', sa.String(20), nullable=False),
        sa.Column('valor', sa.Numeric(12, 2), nullable=False),
        sa.Column('ocorrido_em', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('descricao', sa.String(255), nullable=True),
    )
    op.create_table(
        'conciliacoes_pagamento',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True),
        sa.Column('titulo_receber_id', sa.UUID(as_uuid=True), sa.ForeignKey('titulos_receber.id'), nullable=False),
        sa.Column('valor_recebido', sa.Numeric(12, 2), nullable=False),
        sa.Column('divergencia', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('conciliado_em', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('observacao', sa.String(255), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('conciliacoes_pagamento')
    op.drop_table('movimentos_caixa')
    op.drop_table('estoque_movimentos')
    op.drop_table('pedidos_itens')
    op.drop_table('recebimentos_insumo')
    op.drop_table('titulos_pagar')
    op.drop_table('titulos_receber')
    op.drop_table('glosas')
    op.drop_table('guias_itens')
    op.drop_table('pedidos_compra')
    op.drop_table('guias_tiss')
    op.drop_table('solicitacoes_compra')
    op.drop_table('lotes_faturamento')
    op.drop_table('insumos_materiais')
    op.drop_table('fornecedores')
