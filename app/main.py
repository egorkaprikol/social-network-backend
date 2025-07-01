from fastapi import FastAPI
from app.db import SessionLocal
from app.auth import service
from app.auth.router import router as auth_router

app = FastAPI(title="Social Network API", version="0.1.0")


# Роуты аутентификации и авторизации
app.include_router(auth_router, prefix="/auth")


# Инициализация дефолтной роли при старте
@app.on_event("startup")
async def init_defaults():
    async with SessionLocal() as db:
        app.state.default_role_id = await service.get_default_role_id(db)


@app.get("/")
def read_root():
    return {"Hello": "World"}
