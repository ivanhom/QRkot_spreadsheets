from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.services.investment import investing
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import donation_crud
from app.models import CharityProject, Donation, User
from app.schemas.donation import DonationCreate, DonationDB, DonationGet

router = APIRouter()


@router.post('/', response_model=DonationGet)
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
) -> Donation:
    """Сделать пожертвование."""
    new_donation = await donation_crud.create(donation, session, user)
    await investing(new_donation, CharityProject, session)
    return new_donation


@router.get('/', response_model=list[DonationDB])
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_superuser)
) -> list[Donation]:
    """Только для суперюзеров.
    Возвращает список всех пожертвований.
    """
    return await donation_crud.get_multi(session)


@router.get('/my', response_model=list[DonationGet])
async def get_user_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
) -> list[Donation]:
    """Вернуть список пожертвований пользователя, выполняющего запрос."""
    return await donation_crud.get_by_attribute(
        attr_name='user_id', attr_value=user.id, session=session, multi=True)
