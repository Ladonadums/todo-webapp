# shared/models.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

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