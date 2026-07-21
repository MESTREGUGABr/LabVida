from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from src.cadastro import models  # noqa: F401
from src.cadastro.convenio import models as convenio_models  # noqa: F401
from src.cadastro.medico import models as medico_models  # noqa: F401
from src.cadastro.procedimento import models as procedimento_models  # noqa: F401
from src.cadastro.unidade import models as unidade_models  # noqa: F401
from src.atendimento.amostra import models as amostra_models  # noqa: F401
from src.atendimento.autorizacao import models as autorizacao_models  # noqa: F401
from src.atendimento.ordem_servico import models as ordem_servico_models  # noqa: F401
from src.usuario import models as usuario_models  # noqa: F401
from src.laboratorial import models as laboratorial_models  # noqa: F401
from src.logistica.malote import models as malote_models  # noqa: F401
from src.logistica.recebimento import models as recebimento_models  # noqa: F401
from src.config import get_database_url
from src.db import Base

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    context.configure(
        url=get_database_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = get_database_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
