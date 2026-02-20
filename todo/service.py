from typing import List, Optional
from datetime import datetime
from shared.models import TodoCreate, TodoUpdate, TodoRead




# Хранилище (временно — потом будет PostgreSQL)
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

def get_all_todos(is_done: Optional[bool] = None, min_priority: Optional[int] = None) -> List[dict]:
    result = todos
    if is_done is not None:
        result = [t for t in result if t["is_done"] == is_done]
    if min_priority is not None:
        result = [t for t in result if t["priority"] >= min_priority]
    return result

def create_todo(todo_data: dict) -> dict:
    new_id = max((t["id"] for t in todos), default=-1) + 1
    todo_dict = todo_data.copy()
    todo_dict["id"] = new_id
    todo_dict["is_done"] = False
    todo_dict["created_at"] = datetime.now()
    todos.append(todo_dict)
    return todo_dict

def get_todo_by_id(todo_id: int) -> dict:
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
    raise KeyError("Дело не найдено")

def update_todo_by_id(todo_id: int, updates: dict) -> dict:
    for todo in todos:
        if todo["id"] == todo_id:
            todo.update(updates)
            return todo
    raise KeyError("Дело не найдено")

def delete_todo_by_id(todo_id: int) -> dict:
    for i, todo in enumerate(todos):
        if todo["id"] == todo_id:
            todos.pop(i)
            return {"status": "deleted", "id": todo_id}
    raise KeyError("Дело не найдено")