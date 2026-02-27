# alembic/env.py
import os
import sys
from logging.config import fileConfig

#  КЛЮЧЕВАЯ СТРОКА: добавляем /app в PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import engine_from_config, pool
from alembic import context
from shared.models import Base  # ← теперь будет работать

config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata

def run_migrations_offline():
    raise NotImplementedError("Offline mode not supported")

def run_migrations_online():
    from shared.session import get_engine
    connectable = get_engine()
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()









