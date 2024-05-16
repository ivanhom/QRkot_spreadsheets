from datetime import datetime
from typing import Any, Optional

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class CRUDBase:
    """Базовый класс для стандартных CRUD операций с БД."""

    def __init__(self, model) -> None:
        """Привязка модели к объекту класса."""
        self.model = model

    async def get_by_attribute(
            self,
            attr_name: str,
            attr_value: Any,
            session: AsyncSession,
            multi: bool = False
    ):
        """Получение объекта модели по его атрибуту.
        Если параметр 'multi' будет равен 'True', то
        функция вернёт список объектов."""
        attr = getattr(self.model, attr_name)
        db_obj = await session.execute(
            select(self.model).where(attr == attr_value)
        )
        if multi:
            return db_obj.scalars().all()
        return db_obj.scalars().first()

    async def get_multi(
            self,
            session: AsyncSession
    ):
        """Получение списка объектов модели."""
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in: BaseModel,
            session: AsyncSession,
            user: Optional[User] = None
    ):
        """Создание объекта модели."""
        obj_in_data = obj_in.dict()
        if user:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db_obj,
            obj_in: BaseModel,
            session: AsyncSession
    ):
        """Обновление объекта модели."""
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        if (
            update_data.get('full_amount') and
            obj_data['invested_amount'] == update_data['full_amount']
        ):
            update_data['fully_invested'] = True
            update_data['close_date'] = datetime.now()

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj,
            session: AsyncSession
    ):
        """Удаление объекта модели."""
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    def close_obj(self):
        """Процесс закрытия полностью проинвестированного объекта."""
        self.model.invested_amount = self.model.full_amount
        self.model.fully_invested = True
        self.model.close_date = datetime.now()
        return self.model
