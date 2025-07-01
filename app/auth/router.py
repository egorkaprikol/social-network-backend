from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.db import get_db
from app.auth import schemas, service

router = APIRouter()


# Роут для регистрации пользователей
@router.post(
    "/register/",
    summary="Регистрация нового пользователя",
    description="Создает нового пользователя, проверяя уникальность email, username и номера телефона.",
    response_model=schemas.UserRead
)
async def register_user_endpoint(
    user: schemas.UserRegister,
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    new_user = await service.register_user(db=db, form_data=user, request=request)
    return new_user
