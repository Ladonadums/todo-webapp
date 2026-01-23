import sqlite3
from datetime import datetime

# Подключение к базе данных
DB_PATH = "schul.db"
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Включаем поддержку внешних ключей
cur.execute("PRAGMA foreign_keys = ON;")

# Создание таблиц (если не существуют)
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER,
    registered_at TEXT
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    level TEXT NOT NULL
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS enrollments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    enrolled_at TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
);
""")

print("Таблицы созданы.")

# Очистка данных (опционально)
cur.execute("DELETE FROM enrollments")
cur.execute("DELETE FROM courses")
cur.execute("DELETE FROM users")
print("🧹 Данные очищены.")

# Вставка пользователей
users_data = [
    ("Анна Иванова", "anna@example.com", 28),
    ("Борис Петров", "boris@example.com", 35),
    ("Светлана Сидорова", "sveta@example.com", 22),
    ("Виктория", "victoria@rubius.com", 34),
    ("Павел", "pavel@rubius.com", 38),
    ("Юлия", "yulia@rubius.com", 23),
    ("Алексей", "alexey@rubius.com", 32),
    ("Наталья", "natalya@rubius.com", 28),
]

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
cur.executemany(
    "INSERT INTO users (name, email, age, registered_at) VALUES (?, ?, ?, ?)",
    [(name, email, age, now) for name, email, age in users_data]
)
print(f"Добавлено {len(users_data)} пользователей.")

# Вставка курсов
courses_data = [
    ("Введение в Python", "beginner"),
    ("Продвинутый SQL", "middle"),
    ("Машинное обучение с нуля", "advanced"),
    ("Web-разработка на Flask", "beginner"),
    ("Базы данных для начинающих", "beginner"),
]

cur.executemany(
    "INSERT INTO courses (title, level) VALUES (?, ?)",
    courses_data
)
print(f"Добавлено {len(courses_data)} курсов.")

# Вставка записей на курсы — БЕЗОПАСНО
# Получаем реальные ID из базы
cur.execute("SELECT id FROM users LIMIT 5")      # первые 5 пользователей
user_ids = [row[0] for row in cur.fetchall()]

cur.execute("SELECT id FROM courses LIMIT 2")    # первые 2 курса
course_ids = [row[0] for row in cur.fetchall()]

enrollments_data = []
for user_id in user_ids:
    for course_id in course_ids:
        enrollments_data.append((user_id, course_id, now))

cur.executemany(
    "INSERT INTO enrollments (user_id, course_id, enrolled_at) VALUES (?, ?, ?)",
    enrollments_data
)
print(f"Добавлено {len(enrollments_data)} записей на курсы.")

# Сохраняем изменения
conn.commit()

# Часть 4: Вывод ВСЕХ данных через SELECT *
print("\n" + "="*50)
print("РЕЗУЛЬТАТ: SELECT * FROM ...")
print("="*50)

print("\nusers:")
cur.execute("SELECT * FROM users")
for row in cur.fetchall():
    print(row)

print("\ncourses:")
cur.execute("SELECT * FROM courses")
for row in cur.fetchall():
    print(row)

print("\nenrollments:")
cur.execute("SELECT * FROM enrollments")
for row in cur.fetchall():
    print(row)

# Закрываем соединение
conn.close()
print("\nСкрипт завершён успешно!")