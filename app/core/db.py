from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from app.core.config import settings


class PreBase:
    """Базовый шаблон создаваемой модели в БД"""

    @declared_attr
    def __tablename__(cls):
        """Изменение имени создаваемой таблицы в БД."""
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.database_url)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    """Генератор асинхронной сессии для доступа
    к модели БД через SQLAlchemy.
    """
    async with AsyncSessionLocal() as async_session:
        yield async_session
