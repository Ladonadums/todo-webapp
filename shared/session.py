# shared/session.py
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

# Чтение URL из окружения (через .env или docker-compose)
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set. "
        "Expected format: postgresql+psycopg2://user:pass@host:port/db"
    )

# Создаём engine — один на всё приложение
engine = create_engine(
    DATABASE_URL,
    echo=False,           # True для отладки SQL
    poolclass=NullPool,   # Для тестов / без пула (в продакшене — QueuePool)
    future=True,          # SQLAlchemy 2.0.46 API
)

# Фабрика сессий
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Зависимость для FastAPI (если используется в роутах)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()