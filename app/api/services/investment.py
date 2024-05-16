from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject, Donation


async def investing(
    new_object: Union[CharityProject, Donation],
    investing_model: Union[CharityProject, Donation],
    session: AsyncSession
) -> Union[CharityProject, Donation]:
    """Получение списка объектов, которые не до конца
    инвестированы и поочередное взаимное инвестирование
    их средств с новым поступившим объектом.
    """
    investing_sources = await CRUDBase(investing_model).get_by_attribute(
        attr_name='fully_invested', attr_value=False,
        session=session, multi=True
    )

    for investing_source in investing_sources:
        if new_object.fully_invested:
            break
        new_object, investing_source = compare_invested_amounts(
            new_object, investing_source
        )
        session.add(new_object)
        session.add(investing_source)

    await session.commit()
    await session.refresh(new_object)
    return new_object


def compare_invested_amounts(
    new_obj: Union[CharityProject, Donation],
    invest_src: Union[CharityProject, Donation]
) -> Union[CharityProject, Donation]:
    """Сравнение инвестированных сумм и вызов процесса
    закрытия полностью проинвестированного объекта.
    """
    new_obj_need_invst = new_obj.full_amount - new_obj.invested_amount
    invest_src_can_invst = invest_src.full_amount - invest_src.invested_amount

    if new_obj_need_invst < invest_src_can_invst:
        invest_src.invested_amount += new_obj_need_invst
        CRUDBase(new_obj).close_obj()
    elif new_obj_need_invst > invest_src_can_invst:
        new_obj.invested_amount += invest_src_can_invst
        CRUDBase(invest_src).close_obj()
    else:
        CRUDBase(new_obj).close_obj()
        CRUDBase(invest_src).close_obj()

    return new_obj, invest_src
