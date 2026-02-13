FROM python:3.11-slim

WORKDIR /app

# Установка Python зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование проекта
COPY . /app

# Указываем переменные окружения (можно переопределить при запуске)
ENV PYTHONUNBUFFERED=1

# Команда запуска
CMD ["python3", "-u", "-m", "src.main"]
