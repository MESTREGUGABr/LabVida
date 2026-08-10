# Substituir login Google (Auth0/OIDC) por autenticação local com email e senha

Status: accepted

## Contexto

O [ADR 0002](0002-autenticacao-google-usuario-rbac-minimo.md) fixou o login via Google OAuth (através do Auth0) como requisito de autenticação do projeto, justificado por rastreabilidade acadêmica: associar cada ação a uma identidade conhecida sem montar um sistema de gestão de acessos mais pesado que o necessário para a demo.

**Na apresentação mais recente do projeto ao professor (09/08/2026), ele pediu explicitamente a correção desse ponto**: substituir a autenticação por Google por um login local tradicional, com **email e senha**. Diferente dos apontamentos catalogados em [plano-evolucao-erp.md](../plano-evolucao-erp.md) §1 (que vieram de uma apresentação anterior), este é um pedido novo, registrado nesta sessão de planejamento.

## Decisão

Substituir o fluxo OIDC/Auth0 (`src/auth.py`) por autenticação local:

- Tabela `usuarios` ganha coluna de senha com hash (bcrypt/argon2 — decidir no detalhamento da fase), nunca texto plano.
- Tela de login própria (email + senha) no lugar do redirect para Auth0.
- Fluxo de criação de conta / definição de senha inicial para o usuário (self-service ou por admin — decidir no detalhamento).
- Rastreabilidade por usuário autenticado é preservada — é o mesmo requisito do ADR 0002, só muda o mecanismo de prova de identidade.
- `AuthConfig`/`PKCE`/`code_verifier` deixam de existir; os achados N15/N16 do [plano-evolucao-erp.md](../plano-evolucao-erp.md) §7.3 (JWT nunca validado, `state` carregando o `code_verifier` em claro) ficam **resolvidos por remoção da superfície**, não por correção — o fluxo que os continha some.

## Consequências

- **Supersede o [ADR 0002](0002-autenticacao-google-usuario-rbac-minimo.md)** na parte de mecanismo de login. O bootstrap de perfil também muda de regra: **todo cadastro novo recebe `admin` diretamente**, não só o primeiro — decisão consciente, aceitável só porque o projeto é acadêmico e não vai a produção real; facilita testes (qualquer conta criada já administra o sistema). Promoção/rebaixamento manual de perfil continua disponível em *Administração → Usuários*.
- F14 (Segurança) do roadmap deixa de precisar corrigir JWT/JWKS/`state` do fluxo Google — esse fluxo é removido, não corrigido. F14 permanece para os itens que não dependem do mecanismo de login: auditoria de leitura de PII e salt no `cpf_hash`.
- Precisa de nova migration para a coluna de senha e de política de complexidade/expiração a definir.
- Sem Auth0, cai a dependência de um provedor externo — simplifica o deploy, mas o projeto passa a ser responsável por armazenamento seguro de credenciais (hash, nunca log, nunca no `auditoria_log`).
