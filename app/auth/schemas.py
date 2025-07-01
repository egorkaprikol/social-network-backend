import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, validator
import re


# Pydantic-схемы для валидации входных данных
# Базовый класс пользователя(User)
class UserBase(BaseModel):
    username: str
    email: EmailStr
    phone_number: str


# Регистрация пользователя
class UserRegister(UserBase):
    password: str

    @validator('username')
    def username_must_be_alphanumeric(cls, v):
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError(
                'Username must contain only letters, numbers and underscores')
        if len(v) < 3 or len(v) > 30:
            raise ValueError('Username must be between 3 and 30 characters')
        return v

    @validator('phone_number')
    def phone_number_must_be_valid(cls, v):
        if not re.match(r'^\+?\d{10,15}$', v):
            raise ValueError(
                'Phone number must be at least 10 digits, may start with +')
        return v

    @validator('password')
    def password_must_be_valid(cls, v):
        errors = []
        if len(v) < 10:
            errors.append('at least 10 characters')
        if not re.search(r'[A-Z]', v):
            errors.append('at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            errors.append('at least one lowercase letter')
        if not re.search(r'\d', v):
            errors.append('at least one digit')
        if not re.match(r'^[A-Za-z0-9!@#$%^&*()_+=\-{}\[\]:;"\'<>,.?/]+$', v):
            errors.append('only special characters are allowed')
        if errors:
            raise ValueError(f'Password must have: {", ".join(errors)}')
        return v


# Получить пользователя
class UserRead(UserBase):
    created_at: datetime.datetime

    # Класс для работы с ORM-моделями (SQLAlchemy)
    class Config:
        orm_mode = True


# Обновить пользователя
class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    phone_number: Optional[str]
    password: Optional[str]
