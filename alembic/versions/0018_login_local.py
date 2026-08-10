"""Login local (email e senha) — Fase F15

Correcao pedida pelo professor na apresentacao de 09/08/2026: substituir o
login Google/Auth0 por autenticacao local. Ver ADR 0010, que supera o ADR 0002
no mecanismo de login. A regra de bootstrap tambem mudou depois: hoje todo
cadastro novo vira `admin` direto, nao so o primeiro (`_atribuir_perfil_inicial`
em `src/usuario/service.py`) — decisao aceitavel so por nao ir a producao real.

DUAS COLUNAS, AMBAS NULLABLE

`senha_hash` e `senha_definida_em` nascem nullable porque os usuarios ja
existentes (criados via Google, ou pelo seeder antes desta fase) nunca tiveram
senha. Nao ha backfill de DML nesta migration.

A alternativa seria um NOT NULL com um hash generico igual para todo mundo —
pior do que nao ter senha, porque criaria uma credencial conhecida valida para
contas as quais nenhum humano escolheu senha. A regra de negocio (aplicada em
`src/usuario/senha.py` e `src/usuario/service.autenticar`) e:

    senha_hash IS NULL  =>  login SEMPRE recusado.

Nunca "aceita qualquer senha", nunca "cria a senha no primeiro login digitado".
Contas legadas precisam de uma senha definida por um admin (`admin_usuarios.py`)
ou pelo seeder (`SENHA_PADRAO_SEED`) para voltarem a logar.

`String(255)` e nao `String(60)` (tamanho tipico de hash bcrypt) para nao
travar uma eventual troca futura de algoritmo de hash (ex. argon2, ~97 chars).

Revision ID: 0018_login_local
Revises: 0017_competencias
Create Date: 2026-08-09

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0018_login_local"
down_revision: Union[str, Sequence[str], None] = "0017_competencias"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("usuarios", sa.Column("senha_hash", sa.String(255), nullable=True))
    op.add_column(
        "usuarios",
        sa.Column("senha_definida_em", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    # Lossy: quem tiver senha definida perde a credencial ao reverter.
    op.drop_column("usuarios", "senha_definida_em")
    op.drop_column("usuarios", "senha_hash")
