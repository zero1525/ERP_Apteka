# Используем легковесный образ Python
FROM python:3.12-slim

# Устанавливаем системные зависимости, нужные для сборки psycopg2 (драйвера Postgres)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Настраиваем рабочую директорию внутри контейнера
WORKDIR /app

# Отключаем буферизацию логов Python (чтобы сразу видеть ошибки в консоли Docker)
ENV PYTHONUNBUFFERED=1

# Копируем и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . .

# Открываем порт, на котором обычно крутится Django в Docker
EXPOSE 8000

# Команда для запуска (gunicorn или обычный runserver для тестов)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]