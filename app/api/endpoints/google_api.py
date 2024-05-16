from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.services.google_api import (set_user_permissions,
                                         spreadsheets_create,
                                         spreadsheets_update_value)
from app.core.db import get_async_session
from app.core.google_client import get_service
from app.crud.charity_project import charity_project_crud
from app.schemas.google_api import GoogleSpreadSheetURL


router = APIRouter()


@router.get('/')
async def get_report(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service)
) -> GoogleSpreadSheetURL:
    """Только для суперюзеров.
    Формирование отчёта в Google-таблице о закрытых проектах,
    отсортированных по скорости сбора средств.
    """
    projects = await charity_project_crud.get_projects_by_completion_rate(
        session
    )
    spreadsheetid, spreadsheet_url = await spreadsheets_create(
        wrapper_services
    )
    await set_user_permissions(spreadsheetid, wrapper_services)
    await spreadsheets_update_value(spreadsheetid,
                                    projects,
                                    wrapper_services)
    return {'spreadsheet_url': spreadsheet_url}
