# Используем официальный образ Python
FROM python:3.13-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY pyproject.toml poetry.lock ./

# Устанавливаем Poetry
RUN pip install poetry

# Устанавливаем зависимости проекта
RUN poetry install --no-root

# Копируем исходный код
COPY . .

# Запускаем бота
CMD ["poetry", "run", "python", "bot/main.py"]