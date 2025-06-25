# Social Network Backend

Бэкенд социальной сети, написанный на Python с использованием FastAPI. Запуск и конфигурация осуществляется через Docker.

## 📦 Стек технологий

- Python 3.12
- FastAPI
- Uvicorn
- Docker & Docker Compose

## 🔧 Установка и запуск

### 1. Клонируйте репозиторий

git clone https://github.com/egorkaprikol/social-network-backend.git

cd social-network-backend

### 2. Подготовьте .env файл с базой данных

#### Создайте файл .env в корне проекта по шаблону:

PROJECT_NAME=social-network-backend
DEBUG=True

#### Подключение к бд

POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=social_network
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

#### Если необходимо измените внешний порт в файле docker-compose.yml

### 3. Соберите и запустите проект через Docker Compose

docker-compose up --build

#### После запуска приложение будет доступно по адресу:

http://localhost:8000

### 4. API документация

FastAPI автоматически генерирует документацию:

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

### 5. Полезные команды Docker:

#### Остановить контейнеры
docker-compose down

#### Пересобрать контейнеры
docker-compose up --build

#### Просмотреть логи
docker-compose logs -f

### 6. Миграции базы данных:

Для управления схемой базы данных используется Alembic — инструмент миграций SQLAlchemy.
Миграции — это способ поэтапного изменения структуры базы (создание таблиц, добавление колонок и т.п.) без потери данных.

#### Как работать с миграциями:

При старте контейнера backend миграции,которые уже находятся в проекте применяются автоматически.

Если вы внесли изменения в модели SQLAlchemy и хотите их применить к базе, необходимо:

#### Создать миграцию:

docker exec -it social-network-backend alembic revision --autogenerate -m "Описание миграции"

#### Применить миграцию к базе данных:

docker exec -it social-network-backend alembic upgrade head