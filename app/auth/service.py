from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from app.auth import schemas, models
from fastapi import Request, HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Функция для хеширования пароля
def get_password_hash(password):
    """
    Хэширует пароль.

    Аргументы:
    - password: Пароль, введённый пользователем.

    Возвращает:
    - hashed_password: Хэшированный пароль.
    """
    return pwd_context.hash(password)


# Функция для получения дефолтной роли
async def get_default_role_id(db: AsyncSession) -> int:
    """
    Получает дефолтную роль при старте сервера.

    Аргументы:
    - db (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой.

    Возвращает:
    - role_id: Идентификатор дефолтной роли(user) из базы данных.

    Исключения:
    - ValueError: Если дефолтной роли(user) не существует.
    """
    result = await db.execute(select(models.Role.id).where(models.Role.name == 'user'))
    role_id = result.scalar_one_or_none()
    if not role_id:
        raise ValueError("Default role 'user' not found in database!")
    return role_id


# Функция для регистрации пользователей
async def register_user(db: AsyncSession, form_data: schemas.UserRegister, request: Request):
    """
    Регистрирует нового пользователя в системе.

    При регистрации происходит:
    - Проверка, что email, username и phone_number ещё не заняты.
    - Хеширование пароля.
    - Присвоение дефолтной роли пользователю.
    - Добавление пользователя в базу и коммит транзакции.

    Аргументы:
    - db (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой.
    - form_data (schemas.UserRegister): Данные, введённые пользователем при регистрации.
    - request (Request): Объект запроса FastAPI, используется для доступа к состоянию приложения.

    Возвращает:
    - models.User: Объект пользователя, созданный и сохранённый в базе.

    Исключения:
    - HTTPException: Если пользователь с такими email, username или phone_number уже существует (400),
                       или если произошла другая непредвиденная ошибка при регистрации (500).
    """
    default_role_id = request.app.state.default_role_id

    # Проверка существующих данных
    # Реализовано для более дружелюбного ответа пользователю (не хочется ждать IntegrityError от БД)
    existing_user = await db.execute(
        select(models.User).where(
            (models.User.email == form_data.email) |
            (models.User.username == form_data.username) |
            (models.User.phone_number == form_data.phone_number)
        )
    )
    user = existing_user.scalar_one_or_none()
    if user:
        # Уточнение, какое именно поле занято
        if user.email == form_data.email:
            raise HTTPException(
                status_code=400, detail="Email is already registered")
        if user.username == form_data.username:
            raise HTTPException(
                status_code=400, detail="Username is already taken")
        if user.phone_number == form_data.phone_number:
            raise HTTPException(
                status_code=400, detail="Phone number is already registered")
        raise HTTPException(
            status_code=400, detail="User with same data already exists")
    
    new_user = models.User(
        username=form_data.username,
        email=form_data.email,
        phone_number=form_data.phone_number,
        # Хеширование пароля перед сохранением
        hashed_password=get_password_hash(form_data.password),
        role_id=default_role_id
    )
    try:
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user
    # Защита от race condition, на случай, если что-то изменилось между проверкой и вставкой
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400, detail="User with same email/username/phone already exists")
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500, detail="Unexpected error during registration")
