from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from jose import jwt
from typing import Optional
from datetime import datetime
import asyncio

# Импорты из других модулей
from shared.models import TodoCreate, TodoUpdate, TodoRead
from todo.service import (
    get_all_todos,
    create_todo,
    get_todo_by_id,
    update_todo_by_id,
    delete_todo_by_id
)

# === Настройки ===
SECRET_KEY = "supersecret"  # → взять из .env позже
ALGORITHM = "HS256"

app = FastAPI(title="TaskFlow API Gateway")

# === Middleware: проверка JWT для защищённых эндпоинтов ===
@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    # Пропускаем /auth/* и / (HTML), /docs, /health
    if request.url.path.startswith(("/auth", "/docs", "/health", "/")):
        return await call_next(request)

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")

    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        request.state.user_id = payload.get("sub")  # сохраняем user_id для downstream
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    return await call_next(request)

# === Эндпоинт: корень (HTML) ===
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

# === Healthcheck ===
@app.get("/health")
def health():
    return {"status": "OK"}

# === Эндпоинты, которые проходят через middleware (защищённые) ===
@app.get("/todos", response_model=list[TodoRead])
def get_todos(
    is_done: Optional[bool] = None,
    min_priority: Optional[int] = None,
    request: Request = None  # ← явная типизация + значение по умолчанию
):
    return get_all_todos(is_done, min_priority)

@app.post("/todos", response_model=TodoRead, status_code=201)
def create_todo_endpoint(todo: TodoCreate, request: Request):
    todo_dict = todo.model_dump()
    return create_todo(todo_dict)

@app.get("/todos/{todo_id}", response_model=TodoRead)
def get_todo(todo_id: int, request: Request):
    try:
        return get_todo_by_id(todo_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Дело не найдено")

@app.patch("/todos/{todo_id}", response_model=TodoRead)
def update_todo(todo_id: int, updates: TodoUpdate, request: Request):
    try:
        update_data = updates.model_dump(exclude_unset=True)
        return update_todo_by_id(todo_id, update_data)
    except KeyError:
        raise HTTPException(status_code=404, detail="Дело не найдено")

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, request: Request):
    try:
        return delete_todo_by_id(todo_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Дело не найдено")

@app.get("/slow")
async def slow_endpoint(ms: int = 300):
    await asyncio.sleep(ms / 1000)
    return {"slept_ms": ms}