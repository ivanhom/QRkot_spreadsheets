from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.services.investment import investing
from app.api.validators import (check_name_duplicate, check_project_exist,
                                check_project_have_less_invested_amount,
                                check_project_have_not_invested_amount,
                                check_project_not_closed)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import charity_project_crud
from app.models import CharityProject
from app.models.donation import Donation
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def create_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)
) -> CharityProject:
    """Только для суперюзеров.
    Создаёт благотворительный проект.
    """
    await check_name_duplicate(charity_project.name, session)
    new_charity_project = await charity_project_crud.create(
        charity_project, session
    )
    await investing(new_charity_project, Donation, session)
    return new_charity_project


@router.get('/', response_model=list[CharityProjectDB])
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session)
) -> list[CharityProject]:
    """Возвращает список всех проектов."""
    return await charity_project_crud.get_multi(session)


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def delete_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> CharityProject:
    """Только для суперюзеров.
    Удаляет проект. Нельзя удалить проект, в который уже
    были инвестированы средства, его можно только закрыть.
    """
    project_to_delete = await check_project_exist(project_id, session)
    check_project_have_not_invested_amount(project_to_delete)
    return await charity_project_crud.remove(project_to_delete, session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session)
) -> CharityProject:
    """Только для суперюзеров.
    Закрытый проект нельзя редактировать; нельзя
    установить требуемую сумму меньше уже вложенной.
    """
    project_to_update = await check_project_exist(
        project_id, session
    )
    check_project_not_closed(project_to_update)

    if obj_in.name:
        await check_name_duplicate(obj_in.name, session)

    if obj_in.full_amount:
        check_project_have_less_invested_amount(
            project_to_update, obj_in.full_amount
        )

    return await charity_project_crud.update(
        db_obj=project_to_update,
        obj_in=obj_in,
        session=session,
    )
