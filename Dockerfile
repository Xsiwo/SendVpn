FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование файлов проекта
COPY . .

# Создание необходимых директорий
RUN mkdir -p data logs

# Переменные окружения
ENV PYTHONUNBUFFERED=1

# Запуск бота
CMD ["python", "bot/main.py"]
