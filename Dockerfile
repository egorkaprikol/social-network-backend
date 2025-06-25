FROM python:3.12-slim

# Рабочая директория внутри контейнера
WORKDIR /app

# Копирование зависимостей
COPY requirements.txt .

# Установка пакетов: netcat, gcc и libpq-dev для psycopg2
RUN apt-get update && apt-get install -y netcat-openbsd gcc libpq-dev

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Права на скрипт
RUN chmod +x /app/entrypoint.sh

# Открытие порта, на случай если он закрыт
EXPOSE 8000

# Использование скрипта
ENTRYPOINT ["/app/entrypoint.sh"]