# shared/models.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# === 1. SQLAlchemy Base ===
Base = declarative_base()

# === 2. SQLAlchemy ORM Model (для БД) ===
class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    priority = Column(Integer, default=3, nullable=False)  # 1–5
    category = Column(String(100), default="Общее", nullable=False)
    is_adult = Column(Boolean, default=False, nullable=False)
    is_done = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(datetime.timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.now(datetime.timezone.utc), nullable=False)


class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    priority: int = Field(3, ge=1, le=5)
    category: str = Field(...)
    is_adult: bool = Field(...)

class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    priority: Optional[int] = Field(None, ge=1, le=5)
    category: Optional[str] = Field(None)
    is_adult: Optional[bool] = Field(None)
    is_done: Optional[bool] = Field(None)

class TodoRead(BaseModel):
    id: int
    title: str
    description: Optional[str]
    priority: int
    category: str
    is_adult: bool
    is_done: bool
    created_at: datetime

    class Config:
        orm_mode = True  #  важно для from_orm()