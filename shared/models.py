# shared/models.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

# === Pydantic models (DTO) ===
class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    priority: int = Field(3, ge=1, le=5)
    category: str = Field("Общее", max_length=100)
    is_adult: bool = False

class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    priority: Optional[int] = Field(None, ge=1, le=5)
    category: Optional[str] = Field(None, max_length=100)
    is_adult: Optional[bool] = None
    is_done: Optional[bool] = None

class TodoRead(BaseModel):
    id: int
    title: str
    description: Optional[str]
    priority: int
    category: str
    is_adult: bool
    is_done: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# === SQLAlchemy ORM model ===
Base = declarative_base()

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    priority = Column(Integer, default=3, nullable=False)
    category = Column(String(100), default="Общее", nullable=False)
    is_adult = Column(Boolean, default=False, nullable=False)
    is_done = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)