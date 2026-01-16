import pytest
from fastapi.testclient import TestClient
from main import app

# Создаём тестовый клиент
client = TestClient(app)

# Фикстура для очистки списка задач перед каждым тестом
@pytest.fixture(autouse=True)
def clear_todos():
    from main import todos
    # Очищаем список и добавляем начальную задачу
    todos.clear()
    todos.append({
        "id": 0,
        "title": "Список срочных дел",
        "description": "Если запустить сервер то это...uvicorn",
        "priority": 3,
        "category": "Программисты",
        "is_adult": False,
        "is_done": False,
        "created_at": "2026-01-13T12:00:00"
    })

# 1. Создание задачи
def test_create_todo():
    response = client.post("/todos", json={
        "title": "Новая задача",
        "description": "Описание",
        "priority": 2,
        "category": "Тест",
        "is_adult": False
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Новая задача"
    assert data["priority"] == 2
    assert data["is_done"] == False
    assert "id" in data
    assert "created_at" in data

# 2. Получение списка задач
def test_get_todos():
    response = client.get("/todos")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

# 3. Получение одной задачи
def test_get_todo_by_id():
    # Существующий id
    response = client.get("/todos/0")
    assert response.status_code == 200
    assert response.json()["id"] == 0
    # Несуществующий id
    response = client.get("/todos/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Дело не найдено"

# 4. Ошибка валидации
def test_validation_error():
    # Пустой title
    response = client.post("/todos", json={
        "title": "",
        "description": "Описание",
        "priority": 2,
        "category": "Тест",
        "is_adult": False
    })
    assert response.status_code == 422

 # Слишком длинный title
    response = client.post("/todos", json={
        "title": "A" * 101,
        "description": "Описание",
        "priority": 2,
        "category": "Тест",
        "is_adult": False
    })
    assert response.status_code == 422

# 5. Удаление задачи
def test_delete_todo():
    # Удаление существующей
    response = client.delete("/todos/0")
    assert response.status_code == 200
    assert response.json() == {"status": "deleted", "id": 0}

    # Повторное удаление → 404
    response = client.delete("/todos/0")
    assert response.status_code == 404