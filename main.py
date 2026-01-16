from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import asyncio

# =============== МОДЕЛИ (Pydantic v2) ===============
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

# =============== ПРИЛОЖЕНИЕ ===============
app = FastAPI()

# =============== ХРАНИЛИЩЕ ===============
todos = [
    {
        "id": 0,
        "title": "Список срочных дел",
        "description": "Если запустить сервер то это...uvicorn",
        "priority": 3,
        "category": "Программисты",
        "is_adult": False,
        "is_done": False,
        "created_at": datetime.now()
    }
]
# =============== HTML ЭНДПОИНТ ===============
@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <html>
    <head>
        <title>API Дел программиста</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 40px;
                background-color: #f9f9f9;
                color: #333;
                line-height: 1.6;
            }
            h1 {
                color: #2c3e50;
                border-bottom: 2px solid #3498db;
                padding-bottom: 5px;
            }
            p {
                color: #555;
            }
            ul {
                padding-left: 20px;
            }
            li {
                margin: 8px 0;
                color: #27ae60;
            }
            code {
                background-color: #eee;
                padding: 2px 6px;
                border-radius: 4px;
                font-family: Consolas, Monaco, monospace;
                font-size: 0.9em;
            }
        </style>
    </head>
    <body>
        <h1>API Дел программиста</h1>
        <p>Доступные эндпоинты:</p>
        <ul>
            <li><code>GET /todos</code> — Получить все дела (фильтры: ?is_done=true&amp;min_priority=3)</li>
            <li><code>POST /todos</code> — Добавить дело</li>
            <li><code>GET /todos/{id}</code> — Получить дело по id</li>
            <li><code>PATCH /todos/{id}</code> — Частично обновить дело</li>
            <li><code>DELETE /todos/{id}</code> — Удалить дело</li>
            <li><code>GET /slow?ms=500</code> — Учебная задержка</li>
        </ul>
        <p><a href="/docs">Открыть Swagger UI &rarr;</a></p>
    </body>
    </html>
    """
# =============== ЭНДПОИНТЫ ===============
@app.get("/todos", response_model=list[TodoRead])
def get_todos(
    is_done: Optional[bool] = Query(None),
    min_priority: Optional[int] = Query(None)
):
    result = todos
    if is_done is not None:
        result = [t for t in result if t["is_done"] == is_done]
    if min_priority is not None:
        result = [t for t in result if t["priority"] >= min_priority]
    return result

@app.post("/todos", response_model=TodoRead, status_code=201)
async def create_todo(todo: TodoCreate):
    new_id = max((t["id"] for t in todos), default=-1) + 1
    todo_dict = todo.model_dump()  # ← Pydantic v2
    todo_dict["id"] = new_id
    todo_dict["is_done"] = False
    todo_dict["created_at"] = datetime.now()
    todos.append(todo_dict)
    return todo_dict

@app.get("/todos/{todo_id}", response_model=TodoRead)
def get_todo(todo_id: int):
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Дело не найдено")

@app.patch("/todos/{todo_id}", response_model=TodoRead)
def update_todo(todo_id: int, updates: TodoUpdate):
    for todo in todos:
        if todo["id"] == todo_id:
            update_data = updates.model_dump(exclude_unset=True)  # ← Pydantic v2
            todo.update(update_data)
            return todo
    raise HTTPException(status_code=404, detail="Дело не найдено")

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for i, todo in enumerate(todos):
        if todo["id"] == todo_id:
            todos.pop(i)
            return {"status": "deleted", "id": todo_id}
    raise HTTPException(status_code=404, detail="Дело не найдено")

@app.get("/slow")
async def slow_endpoint(ms: int = 300):
    await asyncio.sleep(ms / 1000)
    return {"slept_ms": ms}



