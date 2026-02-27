# auth/service.py
import hashlib
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from shared.models import User
from sqlalchemy.orm import Session
import os

SECRET_KEY = os.environ["JWT_SECRET"] # хранится в .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Временно: сравниваем хэш SHA256 (для демонстрации)
    return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password

def get_password_hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # Подпись

def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, email: str, password: str) -> User:
    hashed = get_password_hash(password)
    user = User(email=email, hashed_password=hashed) # создёт объект ORM
    db.add(user)                                     # добавление в сессию
    db.commit()                                      # фиксация транзакции
    db.refresh(user)                                 # обновляет объект(id например)
    return user