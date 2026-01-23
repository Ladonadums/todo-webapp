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

## Docker Usage

### Build the image
```bash
docker build -t my-api .

Run the container

docker run --rm -p 8000:8000 my-api
Check the API
Open http://localhost:8000/docs

API запускается внутри контейнера на базе Linux 
(образ python:3.13-slim основан на Debian)
Docker изначально создан для Linux
где контейнеризация работает на уровне ядра
на Windows Docker использует небольшую виртуальную 
машину с Linux под капотом

SQLite
Скрипт автоматически создаёт SQLite-базу данных schul.db
8 пользователей
5 курсов
10 записей на курсы
Все таблицы связаны через внешние ключи, 
обеспечивая целостность данных.

Как запустить?

Убедитесь, что установлен Python 3.
Откройте терминал в папке проекта:
cd C:\Users\Unknown\PycharmProjects\todo-webapp
Запустите скрипт: python seed.py

Создаваемые таблицы

users — пользователи (id, name, email, age, registered_at)
courses — курсы (id, title, level)
enrollments — записи на курсы (id, user_id, course_id, enrolled_at)
→ Связи: user_id - users.id, course_id - courses.id

Вывод в консоль:

Подтверждение создания и заполнения таблиц
Полное содержимое всех трёх таблиц через SELECT * FROM ...
(все строки, без ограничений)
