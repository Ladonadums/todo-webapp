from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse
from jose import jwt
from typing import Optional
from datetime import datetime
import asyncio

# === НОВЫЙ ИМПОРТ: для работы с БД ===
from sqlalchemy.orm import Session
from shared.session import get_db  #  зависимость для получения сессии

# Импорты моделей и сервисов (без изменений)
from shared.models import TodoCreate, TodoUpdate, TodoRead
from todo.service import (
    get_all_todos,
    create_todo,
    get_todo_by_id,
    update_todo_by_id,
    delete_todo_by_id
)

# === Настройки JWT (временно) ===
SECRET_KEY = "supersecret"  #  позже заменить на os.getenv("JWT_SECRET")
ALGORITHM = "HS256"

app = FastAPI(title="TaskFlow API Gateway")


# === Middleware: проверка JWT (без изменений) ===
@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    if request.url.path.startswith(("/auth", "/docs", "/health", "/")):
        return await call_next(request)

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")

    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        request.state.user_id = payload.get("sub")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    return await call_next(request)


# === Эндпоинты: корень и healthcheck (без изменений) ===
@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <html>
    <head><title>TaskFlow API</title></head>
    <body>
        <h1>TaskFlow API</h1>
        <p><a href="/docs">Swagger UI</a></p>
    </body>
    </html>
    """

@app.get("/health")
def health():
    return {"status": "OK"}


# === КЛЮЧЕВОЕ ИЗМЕНЕНИЕ: все эндпоинты получают db через Depends(get_db) ===

@app.get("/todos", response_model=list[TodoRead])
def get_todos(
    is_done: Optional[bool] = None,
    min_priority: Optional[int] = None,
    db: Session = Depends(get_db),  #  ДОБАВЛЕНО: сессия из shared/session.py
    request: Request = None
):
    # Передаём db в service-функцию
    return get_all_todos(db, is_done, min_priority)  #  ИЗМЕНЕНО: добавлен параметр db


@app.post("/todos", response_model=TodoRead, status_code=201)
def create_todo_endpoint(
    todo: TodoCreate,
    db: Session = Depends(get_db),  # ДОБАВЛЕНО
    request: Request = None
):
    todo_dict = todo.model_dump()
    return create_todo(db, todo_dict)  #  ИЗМЕНЕНО: добавлен db


@app.get("/todos/{todo_id}", response_model=TodoRead)
def get_todo(
    todo_id: int,
    db: Session = Depends(get_db),  #  ДОБАВЛЕНО
    request: Request = None
):
    try:
        return get_todo_by_id(db, todo_id)  #  ИЗМЕНЕНО: добавлен db
    except KeyError:
        raise HTTPException(status_code=404, detail="Дело не найдено")


@app.patch("/todos/{todo_id}", response_model=TodoRead)
def update_todo(
    todo_id: int,
    updates: TodoUpdate,
    db: Session = Depends(get_db),  #  ДОБАВЛЕНО
    request: Request = None
):
    try:
        update_data = updates.model_dump(exclude_unset=True)
        return update_todo_by_id(db, todo_id, update_data)  #  ИЗМЕНЕНО: добавлен db
    except KeyError:
        raise HTTPException(status_code=404, detail="Дело не найдено")


@app.delete("/todos/{todo_id}")
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),  #  ДОБАВЛЕНО
    request: Request = None
):
    try:
        return delete_todo_by_id(db, todo_id)  #  ИЗМЕНЕНО: добавлен db
    except KeyError:
        raise HTTPException(status_code=404, detail="Дело не найдено")


# === Slow endpoint (без изменений — не работает с БД) ===
@app.get("/slow")
async def slow_endpoint(ms: int = 300):
    await asyncio.sleep(ms / 1000)
    return {"slept_ms": ms}