# gateway/app.py
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from shared.session import get_db
from shared.models import TodoCreate, TodoUpdate, TodoRead
from todo.service import (
    get_all_todos,
    create_todo,
    get_todo_by_id,
    update_todo_by_id,
    delete_todo_by_id
)
from auth.router import router as auth_router
import asyncio

app = FastAPI(title="TaskFlow API Gateway")

# === Подключаем роутеры СРАЗУ после создания app ===
app.include_router(auth_router, prefix="/auth", tags=["Auth"])


# === Эндпоинты ===

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


@app.get("/todos", response_model=list[TodoRead])
def get_todos(
    is_done: bool | None = None,
    min_priority: int | None = None,
    db: Session = Depends(get_db),
):
    return get_all_todos(db, is_done, min_priority)


@app.post("/todos", response_model=TodoRead, status_code=status.HTTP_201_CREATED)
def create_todo_endpoint(
    todo: TodoCreate,
    db: Session = Depends(get_db),
):
    return create_todo(db, todo.model_dump())


@app.get("/todos/{todo_id}", response_model=TodoRead)
def get_todo(
    todo_id: int,
    db: Session = Depends(get_db),
):
    try:
        return get_todo_by_id(db, todo_id)
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")


@app.patch("/todos/{todo_id}", response_model=TodoRead)
def update_todo(
    todo_id: int,
    updates: TodoUpdate,
    db: Session = Depends(get_db),
):
    try:
        update_data = updates.model_dump(exclude_unset=True)
        return update_todo_by_id(db, todo_id, update_data)
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")


@app.delete("/todos/{todo_id}")
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
):
    try:
        delete_todo_by_id(db, todo_id)
        return {"message": "Todo deleted"}
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")


# === Полезный slow endpoint (для тестирования задержек) ===
@app.get("/slow")
async def slow_endpoint(ms: int = 300):
    await asyncio.sleep(ms / 1000)
    return {"slept_ms": ms}

