# Deploy & Hardening — LabVida

Guia prático para colocar o LabVida em produção. É **agnóstico de provedor**: assume
um host capaz de rodar contêiner (VM com Docker, Fly.io, Render, Railway, Cloud Run…)
e um **PostgreSQL gerenciado**. A execução do deploy depende de um alvo e de credenciais
definidos pelo time.

## 1. Pré-requisitos

- PostgreSQL 16 (de preferência gerenciado, com backup automático).
- Runtime de contêiner (Docker) no alvo, ou um PaaS que builda o `Dockerfile`.

Não há provedor de autenticação externo a provisionar: desde a fase F15, o login é local
(e-mail e senha, hash bcrypt) — ver [ADR 0010](docs/adr/0010-substituir-login-google-por-email-senha.md).

## 2. Variáveis de ambiente

Copie `.env.production.example` para o gestor de segredos do alvo (**nunca** commite o
`.env` real). Variáveis:

| Variável | Descrição |
|---|---|
| `DATABASE_URL` | `postgresql+psycopg://user:senha@host:5432/db` do Postgres gerenciado |
| `APP_BASE_URL` | URL pública (ex.: `https://labvida.example.com`) |
| `LGPD_ENCRYPTION_KEY` | Chave Fernet (32 bytes base64 url-safe) que criptografa o CPF — o único segredo real que este projeto exige |
| `PORT` | Porta do Streamlit (default 8501) |

> `SENHA_PADRAO_SEED` (usada só por `python -m src.seeder`) **não deve ser definida em
> produção** — o seeder de demonstração não deve rodar fora de ambiente de desenvolvimento/teste.

Gere a chave LGPD:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

> ⚠️ **A chave LGPD é permanente.** Trocá-la sem re-criptografar torna ilegíveis os CPFs já gravados.
> Para rotacionar com segurança, defina a **nova** chave no ambiente e rode o utilitário informando a
> **antiga** (ele descriptografa com a antiga e regrava com a nova; o `cpf_hash` não muda):
>
> ```bash
> LGPD_ENCRYPTION_KEY=<chave_nova> python -m src.lgpd.rotacao <chave_antiga>
> ```
>
> Faça isso em janela de manutenção, com backup do banco antes.

## 3. Subir a aplicação

O `Dockerfile` já roda como usuário não-root. Em produção **não** use o bind-mount de
código do `docker-compose.yml` (aquele compose é para desenvolvimento). Fluxo:

```bash
# 1. Aplicar migrations (uma vez por release)
alembic upgrade head

# 2. Semear RBAC + dados de referência (primeira vez / ambiente novo)
python -m src.seeder        # inclui os perfis de RBAC (obrigatório p/ o gate valer)

# 3. Servir
streamlit run app.py --server.address=0.0.0.0 --server.port=$PORT
```

> **RBAC:** sem `python -m src.seeder` os perfis não existem e o sistema cai no
> **acesso plano** (todo logado vê tudo). Com os perfis semeados, **todo usuário que se
> cadastrar** (aba "Criar conta" da tela de login) vira `admin` diretamente — decisão do
> projeto acadêmico (ver [ADR 0010](docs/adr/0010-substituir-login-google-por-email-senha.md)),
> **inadequada para produção real** sem revisão (ver item de hardening abaixo).

## 4. Hardening (revisar antes de expor)

- [ ] **Segredos fora do git**: `.env` no `.gitignore`; `LGPD_ENCRYPTION_KEY` apenas no
      gestor de segredos do alvo.
- [ ] **`SENHA_PADRAO_SEED` não definida** e seeder de demonstração **não executado** em produção.
- [ ] **Cadastro local sempre aberto E todo cadastro vira admin** (`app.py` /
      `_atribuir_perfil_inicial`): qualquer visitante que preencha a aba "Criar conta" ganha
      acesso total ao sistema, sem aprovação nem promoção manual. **Isso é aceitável só em
      ambiente acadêmico/demo — antes de qualquer exposição real, reverta a regra para
      "primeiro usuário vira admin, demais entram como `visualizador`"** (ou algo mais
      restrito) e/ou bloqueie a rota por rede (VPN/allowlist de IP).
- [ ] **Sem rate limiting / bloqueio por tentativas** no login local (limitação conhecida,
      ver ADR 0010) — considerar um proxy/WAF com rate limiting na frente se exposto à internet.
- [ ] **HTTPS** obrigatório (o `APP_BASE_URL` deve ser `https://`).
- [ ] **Postgres**: acesso restrito por rede/VPC, TLS, backups automáticos.
- [ ] **Promover o admin correto** logo após o primeiro cadastro (bootstrap) e revisar perfis.
- [ ] **Auditoria**: garantir retenção do `auditoria_log` (append-only) conforme a política.

## 5. Rotina de release

1. `alembic upgrade head` (as migrations são versionadas; head atual descrita na resenha).
2. Deploy da nova imagem.
3. Smoke test: login, abrir OS, registrar coleta, liberar laudo, fechar lote.

> Integrações externas (TISS real, HL7/ASTM) permanecem **fora do escopo** do protótipo.
