# Deploy & Hardening — LabVida

Guia prático para colocar o LabVida em produção. É **agnóstico de provedor**: assume
um host capaz de rodar contêiner (VM com Docker, Fly.io, Render, Railway, Cloud Run…)
e um **PostgreSQL gerenciado**. A execução do deploy depende de um alvo e de credenciais
definidos pelo time.

## 1. Pré-requisitos

- PostgreSQL 16 (de preferência gerenciado, com backup automático).
- Um tenant Auth0 com uma aplicação **Regular Web Application**.
- Runtime de contêiner (Docker) no alvo, ou um PaaS que builda o `Dockerfile`.

## 2. Variáveis de ambiente

Copie `.env.production.example` para o gestor de segredos do alvo (**nunca** commite o
`.env` real). Variáveis:

| Variável | Descrição |
|---|---|
| `DATABASE_URL` | `postgresql+psycopg://user:senha@host:5432/db` do Postgres gerenciado |
| `AUTH0_DOMAIN` / `AUTH0_CLIENT_ID` / `AUTH0_CLIENT_SECRET` | Credenciais da app Auth0 |
| `APP_BASE_URL` | URL pública (ex.: `https://labvida.example.com`) — precisa bater com o callback do Auth0 |
| `LGPD_ENCRYPTION_KEY` | Chave Fernet (32 bytes base64 url-safe) que criptografa o CPF |
| `PORT` | Porta do Streamlit (default 8501) |

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
> **acesso plano** (todo logado vê tudo). Com os perfis semeados, o **primeiro** usuário
> que logar vira `admin` (bootstrap) e os demais entram como `visualizador` até serem
> promovidos em *Administração → Usuários e Perfis*.

## 4. Hardening (revisar antes de expor)

- [ ] **Segredos fora do git**: `.env` no `.gitignore`; `AUTH0_CLIENT_SECRET` e
      `LGPD_ENCRYPTION_KEY` apenas no gestor de segredos do alvo.
- [ ] **Auth0 — Breached/Leaked Password Detection** ligado (Security → Attack Protection).
- [ ] **Auth0 — Bot Detection / Brute-force protection** ligados.
- [ ] **Auth0 — Allowed Callback/Logout URLs** restritos ao `APP_BASE_URL` de produção.
- [ ] **Signup público**: desabilitar se o acesso for só para a equipe do laboratório.
- [ ] **HTTPS** obrigatório (o `APP_BASE_URL` deve ser `https://`).
- [ ] **Postgres**: acesso restrito por rede/VPC, TLS, backups automáticos.
- [ ] **Promover o admin correto** logo após o primeiro login (bootstrap) e revisar perfis.
- [ ] **Auditoria**: garantir retenção do `auditoria_log` (append-only) conforme a política.

## 5. Rotina de release

1. `alembic upgrade head` (as migrations são versionadas; head atual descrita na resenha).
2. Deploy da nova imagem.
3. Smoke test: login, abrir OS, registrar coleta, liberar laudo, fechar lote.

> Integrações externas (TISS real, HL7/ASTM) permanecem **fora do escopo** do protótipo.
