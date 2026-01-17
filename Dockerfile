# Используем официальный образ Python
FROM python:3.13-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости (без кэша — чтобы образ был меньше)
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код проекта
COPY . .

# Открываем порт 8000
EXPOSE 8000

# Запускаем API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]