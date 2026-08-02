"""Conjuntos de tabelas truncadas entre testes.

Antes, cada pacote de teste carregava sua propria tupla `_TABELAS` — seis listas
com o mesmo nucleo de 18 tabelas, divergindo so nas bordas. Toda tabela nova
exigia lembrar de seis arquivos, e esquecer um vazava estado entre testes.

Aqui os conjuntos sao nomeados por dominio e compostos por soma. `TRUNCATE ...
CASCADE` ja derruba as dependentes, entao a ordem e irrelevante; os conjuntos
existem para deixar explicito o escopo que cada pacote considera seu.

Cada conftest continua declarando o proprio escopo — a composicao preserva
exatamente o comportamento anterior. Em especial, `laboratorial` e `logistica`
NAO truncam RBAC: com a tabela `perfis` vazia o gate entra em modo bootstrap e
libera tudo, o que mudaria o que esses testes exercitam.
"""

from sqlalchemy import text
from sqlalchemy.orm import Session

# Cadastro + atendimento + logistica: o esqueleto que todo teste precisa zerar.
NUCLEO = (
    "protocolos_recebimento",
    "amostras_movimentacoes",
    "malotes_amostras",
    "malotes",
    "coletas",
    "amostras",
    "autorizacoes_convenio",
    "os_status_historico",
    "os_itens",
    "ordens_servico",
    "procedimento_valores",
    "medicos",
    "procedimentos",
    "convenios",
    "setores",
    "unidades",
    "usuarios",
    "pacientes",
)

LABORATORIAL = (
    "resultados_auditoria",
    "laudos",
    "resultados",
    "valores_referencia",
    "equipamentos",
)

FATURAMENTO = (
    "glosas",
    "guias_itens",
    "guias_tiss",
    "lotes_faturamento",
)

FINANCEIRO = (
    "conciliacoes_pagamento",
    "movimentos_caixa",
    "titulos_pagar",
    "titulos_receber",
)

COMPRAS = (
    "estoque_movimentos",
    "pedidos_itens",
    "recebimentos_insumo",
    "pedidos_compra",
    "solicitacoes_compra",
    "insumos_materiais",
    "fornecedores",
)

RBAC = (
    "perfil_permissao",
    "permissoes",
    "perfis",
)

AUDITORIA = ("auditoria_log",)

# Escopo do fluxo completo: da OS ao recebimento do titulo.
CICLO_COMPLETO = NUCLEO + LABORATORIAL + FATURAMENTO + FINANCEIRO + COMPRAS


def limpar(session: Session, tabelas: tuple[str, ...]) -> None:
    session.execute(text("TRUNCATE " + ", ".join(tabelas) + " RESTART IDENTITY CASCADE"))
    session.commit()
