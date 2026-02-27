"""
SQLAlchemy session factory для всего проекта.
Используется в:
  - services/todo/service.py
  - services/auth/service.py
  - gateway/app.py (опционально)
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
import os
from dotenv import load_dotenv

# === Загрузка .env из корня проекта ===
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    raise RuntimeError(f".env file not found at {env_path}. Please create it in the project root.")

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set in .env. "
        "Expected format: postgresql+psycopg2://user:pass@host:port/db\n"
        "For Docker Compose: use 'postgres' as host (not localhost)."
    )

engine = create_engine(
    DATABASE_URL,
    echo=False,
    poolclass=NullPool,
    future=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#  НОВАЯ ФУНКЦИЯ ДЛЯ ALEMBIC
def get_engine():
    return engine