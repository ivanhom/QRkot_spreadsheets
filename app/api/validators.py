from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import Messages
from app.crud import charity_project_crud
from app.models import CharityProject


async def check_name_duplicate(
        charity_project_name: str,
        session: AsyncSession
) -> None:
    """Проверка на уникальность вводимого имени благотворительного проекта."""
    charity_project_id = await charity_project_crud.get_by_attribute(
        attr_name='name', attr_value=charity_project_name, session=session
    )
    if charity_project_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=Messages.NAME_ALR_EXIST
        )


async def check_project_exist(
        project_id: int,
        session: AsyncSession
) -> CharityProject:
    """Проверяет, что благотворительный
    проект существует и возвращает его.
    """
    charity_project = await charity_project_crud.get_by_attribute(
        attr_name='id', attr_value=project_id, session=session)
    if not charity_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=Messages.PROJECT_NOT_FOUND
        )
    return charity_project


def check_project_have_not_invested_amount(
        charity_project: CharityProject
) -> None:
    """Проверяет, что удаляемый благотворительный
    проект не имеет инвестированных средств.
    """
    if charity_project.invested_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=Messages.PROJECT_ALR_INVESTED
        )


def check_project_not_closed(
        charity_project: CharityProject
) -> None:
    """Проверяет, что обновляемый
    благотворительный проект не закрыт.
    """
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=Messages.PROJECT_ALR_CLOSED
        )


def check_project_have_less_invested_amount(
        charity_project: CharityProject,
        new_full_amount: int
) -> None:
    """Проверяет, что новая общая сумма обновляемого
    благотворительного проекта больше уже инвестированных средств.
    """
    if new_full_amount < charity_project.invested_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=Messages.WRONG_FULL_AMOUNT
        )
