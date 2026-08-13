from sqlalchemy import engine_from_config, pool
from alembic import context

# Імпортуємо Base та всі моделі через абсолютні імпорти
from backend.database import Base
from backend.models.accounts import Account
from backend.models.journal import Journal
from backend.models.finance import Finance
from backend.models.inventory import Inventory
from backend.models.purchases import Purchase
from backend.models.sales import Sale
from backend.models.legal import Legal

# Alembic Config object
config = context.config

# Тут вже є всі таблиці через Base.metadata
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
