from pydantic import BaseModel


class GoogleSpreadSheetURL(BaseModel):
    """Схема для вывода ссылки на созданный документ Google-таблицы."""
    spreadsheet_url: str
