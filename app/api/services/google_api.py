from datetime import datetime, timedelta

from aiogoogle import Aiogoogle

from app.constants import GoogleAPIConfig
from app.core.config import settings


async def spreadsheets_create(wrapper_services: Aiogoogle) -> tuple[str, str]:
    """Создание документа Goggle-таблицы."""
    now_date_time = datetime.now().strftime(settings.time_format)
    service = await wrapper_services.discover(
        GoogleAPIConfig.SHEETS_API, GoogleAPIConfig.SHEETS_API_VER
    )
    spreadsheet_body = {
        'properties': {'title': f'Отчёт на {now_date_time}',
                       'locale': 'ru_RU'},
        'sheets': GoogleAPIConfig.SHEETS_CONF
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheetid = response['spreadsheetId']
    spreadsheet_url = GoogleAPIConfig.SHEETS_URL_TEMPLATE + spreadsheetid
    return spreadsheetid, spreadsheet_url


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    """Предоставление прав доступа вашему личному
    Google-аккаунту к созданному документу.
    """
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover(
        GoogleAPIConfig.DRIVE_API, GoogleAPIConfig.DRIVE_API_VER
    )
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields='id'
        ))


async def spreadsheets_update_value(
        spreadsheetid: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    """Запись полученной из базы данных информации в документ с таблицами."""
    now_date_time = datetime.now().strftime(settings.time_format)
    service = await wrapper_services.discover(
        GoogleAPIConfig.SHEETS_API, GoogleAPIConfig.SHEETS_API_VER
    )
    table_values = [
        ['Отчёт от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Нназвание проекта', 'Время сбора', 'Описание']
    ]
    for item in projects:
        new_row = [
            item['name'],
            str(timedelta(item['duration'])),
            item['description']
        ]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
