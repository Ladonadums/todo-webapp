"""
Бизнес-логика для работы с задачами (Todo).
Заменяет in-memory хранилище на PostgreSQL через SQLAlchemy.
Использует зависимость db: Session (Dependency Injection).
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from shared.models import Todo  # ORM модель из shared/models.py


def get_all_todos(
    db: Session,
    is_done: Optional[bool] = None,
    min_priority: Optional[int] = None
) -> List[Todo]:
    """
    Получить список задач с фильтрацией.
    :param db: SQLAlchemy session (передаётся через Depends)
    :param is_done: фильтр по статусу выполнения
    :param min_priority: минимальный приоритет (1–5)
    :return: список объектов Todo
    """
    query = db.query(Todo)

    if is_done is not None:
        query = query.filter(Todo.is_done == is_done)
    if min_priority is not None:
        query = query.filter(Todo.priority >= min_priority)

    return query.all()


def create_todo(db: Session, todo_data: dict) -> Todo:
    """
    Создать новую задачу в БД.
    :param db: сессия
    :param todo_data: словарь с данными (title, description, ...)
    :return: созданный объект Todo (с id, created_at и т.д.)
    """
    new_todo = Todo(**todo_data)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)  # чтобы получить автоинкрементный id и timestamps из БД
    return new_todo


def get_todo_by_id(db: Session, todo_id: int) -> Todo:
    """
    Найти задачу по ID.
    :param db: сессия
    :param todo_id: идентификатор
    :return: объект Todo
    :raises KeyError: если не найдено
    """
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise KeyError("Дело не найдено")
    return todo


def update_todo_by_id(db: Session, todo_id: int, updates: dict) -> Todo:
    """
    Обновить задачу по ID.
    :param db: сессия
    :param todo_id: ID задачи
    :param updates: словарь полей для обновления (например: {"is_done": True})
    :return: обновлённый объект Todo
    """
    todo = get_todo_by_id(db, todo_id)
    for key, value in updates.items():
        if hasattr(todo, key):
            setattr(todo, key, value)
    db.commit()
    db.refresh(todo)
    return todo


def delete_todo_by_id(db: Session, todo_id: int) -> dict:
    """
    Удалить задачу по ID.
    :param db: сессия
    :param todo_id: ID задачи
    :return: {"status": "deleted", "id": int}
    """
    todo = get_todo_by_id(db, todo_id)
    db.delete(todo)
    db.commit()
    return {"status": "deleted", "id": todo_id}