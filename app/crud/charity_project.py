from typing import Union

from sqlalchemy import asc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):
    """Класс для расширения стандартных
    CRUD операций с БД для модели CharityProject.
    """

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ) -> Union[None, list]:
        """Сортирует список со всеми закрытыми проектами по
        количеству времени, которое понадобилось на сбор
        средств, — от меньшего к большему.
        """
        top_projects = await session.execute(
            select(
                [CharityProject.name,
                 (
                     func.julianday(CharityProject.close_date) -
                     func.julianday(CharityProject.create_date)
                 ).label('duration'),
                 CharityProject.description]
            ).where(CharityProject.fully_invested).order_by(asc('duration'))
        )
        top_projects = top_projects.all()
        return top_projects


charity_project_crud = CRUDCharityProject(CharityProject)
