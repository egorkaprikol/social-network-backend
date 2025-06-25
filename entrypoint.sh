#!/bin/bash

# Ожидание, пока PostgreSQL поднимется
echo "Ожидаем доступность базы данных..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.5
done

echo "База данных доступна. Применяем миграции Alembic..."
alembic upgrade head

echo "Запуск приложения..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
