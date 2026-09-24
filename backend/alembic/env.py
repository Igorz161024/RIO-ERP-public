import sys
import os
from sqlalchemy import engine_from_config, pool
from alembic import context

# Додаємо шлях до кореня проєкту (RIO-ERP), щоб імпорти backend працювали
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Імпортуємо Base та всі моделі
from backend.database import Base
from backend.models.accounts import Account
from backend.models.journal import Journal
from backend.models.finance import Finance
from backend.models.inventory import Inventory
from backend.models.purchases import Purchase
from backend.models.sales import Sale
from backend.models.legal import Legal
from backend.models.user import User   # 👈 правильний імпорт (файл users.py)

# Alembic Config object
config = context.config

# Метадані для міграцій
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Запуск міграцій у 'offline' режимі."""
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
    """Запуск міграцій у 'online' режимі."""
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
