"""Seeder de RBAC — perfis e permissões (Stack D).

Princípios de segurança aplicados:
- Privilégio mínimo: cada perfil recebe só o que precisa
- Segregação de funções: compras separa solicitante, aprovador e almoxarife
- Read/Write separados: cadastros têm permissões de leitura e escrita distintas
- Acesso plano (ADR 0002): usuário sem perfil vê menu completo

Popula 11 perfis e 34 permissões com vínculos N:N, mais a equipe operacional
(um usuário por função, com o perfil correspondente).
Idempotente **linha a linha**: permissão, perfil e vínculo são conferidos um a um,
então uma base já semeada recebe o que for adicionado depois; usuários são
conferidos por e-mail.
"""

from src.db import session_scope
from src.rbac import repository
from src.rbac.models import Perfil, PerfilPermissao, Permissao
from src.seeder.catalogo import USUARIOS
from src.usuario import repository as usuario_repository

_PERMISSOES = [
    # --- Cadastro: leitura (read-only) ---
    ("cadastro:pacientes:ler", "Listar e buscar pacientes"),
    ("cadastro:convenios:ler", "Listar convênios"),
    ("cadastro:medicos:ler", "Listar médicos"),
    ("cadastro:procedimentos:ler", "Listar procedimentos e valores"),
    ("cadastro:unidades:ler", "Listar unidades e setores"),
    # --- Cadastro: escrita ---
    ("cadastro:pacientes:escrever", "Criar, editar e inativar pacientes"),
    ("cadastro:convenios:escrever", "Criar e editar convênios"),
    ("cadastro:medicos:escrever", "Criar e editar médicos"),
    ("cadastro:procedimentos:escrever", "Criar e editar procedimentos e valores"),
    ("cadastro:unidades:escrever", "Criar e editar unidades e setores"),
    # --- Atendimento e Coleta ---
    ("atendimento:visualizar_os", "Visualizar Ordens de Serviço"),
    ("atendimento:abrir_os", "Abrir Ordem de Serviço"),
    ("atendimento:coletar", "Registrar coleta de amostra"),
    ("atendimento:cancelar_os", "Cancelar itens e Ordens de Serviço"),
    # --- Logística ---
    ("logistica:visualizar_malotes", "Visualizar malotes e protocolos"),
    ("logistica:despachar_malote", "Criar e despachar malotes"),
    ("logistica:receber_malote", "Registrar protocolo de recebimento"),
    # --- Laboratorial ---
    ("laboratorial:registrar_resultado", "Registrar e editar resultados de exames"),
    ("laboratorial:liberar_laudo", "Liberar laudo (exige responsável técnico)"),
    # --- Faturamento ---
    ("faturamento:visualizar_lotes", "Visualizar lotes e guias TISS"),
    ("faturamento:gerenciar_lotes", "Criar e fechar lotes de faturamento"),
    ("faturamento:registrar_glosa", "Registrar glosa em guia"),
    ("faturamento:valor_excecao", "Cobrar valor diferente da tabela de precos"),
    # --- Financeiro ---
    ("financeiro:visualizar_titulos", "Visualizar títulos a receber e pagar"),
    ("financeiro:baixar_titulo", "Baixar títulos a receber e a pagar"),
    ("financeiro:conciliar", "Registrar conciliação de pagamento"),
    # --- Compras: segregação de funções ---
    ("compras:visualizar_estoque", "Visualizar estoque e movimentações"),
    ("compras:solicitar", "Criar solicitação de compra"),
    ("compras:aprovar", "Aprovar pedido de compra"),
    ("compras:receber", "Dar entrada em insumo e atualizar estoque"),
    ("compras:gerenciar_fornecedores", "Criar e editar fornecedores"),
    # --- BI ---
    ("bi:visualizar", "Acessar dashboards de BI"),
    # --- Administração ---
    ("admin:gerenciar_usuarios", "Gerenciar perfis e permissões de usuários"),
    ("admin:visualizar_auditoria", "Visualizar logs de auditoria"),
]

_ADMIN = [
    "cadastro:pacientes:ler", "cadastro:pacientes:escrever",
    "cadastro:convenios:ler", "cadastro:convenios:escrever",
    "cadastro:medicos:ler", "cadastro:medicos:escrever",
    "cadastro:procedimentos:ler", "cadastro:procedimentos:escrever",
    "cadastro:unidades:ler", "cadastro:unidades:escrever",
    "atendimento:visualizar_os", "atendimento:abrir_os", "atendimento:coletar",
    "atendimento:cancelar_os",
    "logistica:visualizar_malotes", "logistica:despachar_malote", "logistica:receber_malote",
    "laboratorial:registrar_resultado", "laboratorial:liberar_laudo",
    "faturamento:visualizar_lotes", "faturamento:gerenciar_lotes", "faturamento:registrar_glosa",
    "faturamento:valor_excecao",
    "financeiro:visualizar_titulos", "financeiro:baixar_titulo", "financeiro:conciliar",
    "compras:visualizar_estoque", "compras:solicitar", "compras:aprovar", "compras:receber",
    "compras:gerenciar_fornecedores",
    "bi:visualizar",
    "admin:gerenciar_usuarios", "admin:visualizar_auditoria",
]

_CADASTRO_LEITURA = [
    "cadastro:pacientes:ler", "cadastro:convenios:ler",
    "cadastro:medicos:ler", "cadastro:procedimentos:ler", "cadastro:unidades:ler",
]

_PERFIS = {
    "admin": _ADMIN,

    "atendente": _CADASTRO_LEITURA + [
        "cadastro:pacientes:escrever",
        "atendimento:visualizar_os", "atendimento:abrir_os",
    ],

    "coletador": [
        "cadastro:pacientes:ler",
        "atendimento:visualizar_os", "atendimento:coletar",
    ],

    "tecnico_laboratorio": [
        "cadastro:pacientes:ler",
        "laboratorial:registrar_resultado",
    ],

    "responsavel_tecnico": [
        "cadastro:pacientes:ler",
        "cadastro:medicos:ler", "cadastro:medicos:escrever",
        "laboratorial:registrar_resultado", "laboratorial:liberar_laudo",
    ],

    "faturista": [
        "cadastro:pacientes:ler", "cadastro:convenios:ler", "cadastro:procedimentos:ler",
        "faturamento:visualizar_lotes", "faturamento:gerenciar_lotes", "faturamento:registrar_glosa",
        "faturamento:valor_excecao",
        "financeiro:visualizar_titulos",
    ],

    "financeiro": [
        "cadastro:pacientes:ler",
        "faturamento:visualizar_lotes",
        "financeiro:visualizar_titulos", "financeiro:baixar_titulo", "financeiro:conciliar",
    ],

    "requisitante_compras": [
        "compras:visualizar_estoque", "compras:solicitar",
    ],

    "aprovador_compras": [
        "compras:visualizar_estoque", "compras:aprovar",
    ],

    "almoxarife": [
        "compras:visualizar_estoque", "compras:receber", "compras:gerenciar_fornecedores",
    ],

    "visualizador": _CADASTRO_LEITURA + [
        "atendimento:visualizar_os",
        "logistica:visualizar_malotes",
        "faturamento:visualizar_lotes",
        "financeiro:visualizar_titulos",
        "compras:visualizar_estoque",
        "bi:visualizar",
    ],
}


def executar_seeder_rbac() -> dict[str, int]:
    contagem = {"perfis": 0, "permissoes": 0, "usuarios": 0}

    with session_scope() as session:
        contagem["perfis"], contagem["permissoes"] = _seed_perfis(session)
        contagem["usuarios"] = _seed_usuarios(session)

    return contagem


def _seed_perfis(session) -> tuple[int, int]:
    """Upsert linha a linha de permissões, perfis e vínculos.

    Antes havia um early-return (`if listar_permissoes(session): return 0, 0`) que
    congelava toda base já semeada na primeira versão do RBAC: permissão nova
    nunca chegava, e a tela que dependesse dela ficava inacessível para todo mundo
    — inclusive admin. Como as fases seguintes acrescentam 8 permissões, isso
    precisava cair antes.

    Retorna quantos perfis e permissões foram **criados nesta execução** (0 e 0
    quando a base já está em dia).
    """
    permissoes_criadas = 0
    permissoes_map: dict[str, Permissao] = {}

    for codigo, descricao in _PERMISSOES:
        permissao = repository.obter_permissao_por_codigo(session, codigo)
        if permissao is None:
            permissao = Permissao(codigo=codigo, descricao=descricao)
            repository.salvar_permissao(session, permissao)
            permissoes_criadas += 1
        elif permissao.descricao != descricao:
            permissao.descricao = descricao
        permissoes_map[codigo] = permissao

    session.flush()

    perfis_criados = 0
    for nome_perfil, codigos_permissoes in _PERFIS.items():
        perfil = repository.obter_perfil_por_nome(session, nome_perfil)
        if perfil is None:
            perfil = Perfil(nome=nome_perfil, descricao=f"Perfil {nome_perfil}")
            repository.salvar_perfil(session, perfil)
            perfis_criados += 1
            session.flush()

        ja_vinculadas = {
            p.codigo for p in repository.listar_permissoes_por_perfil(session, perfil.id)
        }
        for codigo in codigos_permissoes:
            if codigo in ja_vinculadas:
                continue
            repository.vincular_permissao(
                session,
                PerfilPermissao(perfil_id=perfil.id, permissao_id=permissoes_map[codigo].id),
            )

    session.commit()
    return perfis_criados, permissoes_criadas


def _seed_usuarios(session) -> int:
    """Cria a equipe operacional, cada um com o perfil mínimo da sua função.

    O resto do seeder depende disso: coleta, compras e baixa de título passam
    pelo gate de RBAC e só funcionam com um usuário que tenha a permissão.
    """
    from src.usuario.models import Usuario

    criados = 0
    for email, nome, nome_perfil in USUARIOS:
        if usuario_repository.obter_por_email(session, email) is not None:
            continue
        perfil = repository.obter_perfil_por_nome(session, nome_perfil)
        session.add(
            Usuario(email=email, nome=nome, ativo=True, perfil_id=perfil.id if perfil else None)
        )
        criados += 1

    session.commit()
    return criados


def main() -> None:
    contagem = executar_seeder_rbac()
    print("Seed RBAC finalizado")
    for chave, valor in contagem.items():
        print(f"{chave}: {valor}")


if __name__ == "__main__":
    main()
