# Todo RestApi на FastAPI

 REST API для управления задачами (TODO).  
Сделан на платформе FastAPI.

#Установка зависимостей

```bash
pip install -r requirements.txt
```
# Запуск сервера
```bash
uvicorn main:app --reload
```
Сервер будет доступен по адресу:  
**http://127.0.0.1:8000**

# URL для проверки
 `GET /` | Главная HTML-страница с описанием API |
| `GET /docs` | Интерактивная документация (Swagger UI) — **основной инструмент для тестирования** |
| `GET /openapi.json` | Спецификация API в формате OpenAPI |
| `POST /todos` | Создать новую задачу |
| `GET /todos` | Получить список всех задач (поддерживает фильтры: `?is_done=true&min_priority=3`) |
| `GET /todos/{id}` | Получить задачу по id |
| `PATCH /todos/{id}` | Частично обновить задачу |
| `DELETE /todos/{id}` | Удалить задачу |
| `GET /slow?ms=500` | Учебный эндпоинт с задержкой (для демонстрации async) |
