from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.config import settings


# Настройка асинхронного движка и сессии SQLAlchemy
engine = create_async_engine(settings.DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()


# Dependency для получения сессии БД (используется в Depends)
async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session
