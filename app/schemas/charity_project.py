from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, NonNegativeInt, PositiveInt

from app.constants import FieldExamples


class CharityProjectBase(BaseModel):
    """Базовая схема для модели CharityProject."""
    name: str = Field(..., max_length=100, example=FieldExamples.NAME_1)
    description: str = Field(..., example=FieldExamples.DESCRIPTION_1)
    full_amount: PositiveInt = Field(..., example=FieldExamples.FULL_AMOUNT_1)

    class Config:
        extra = Extra.forbid
        min_anystr_length = 1
        orm_mode = True


class CharityProjectCreate(CharityProjectBase):
    """Схема для создания модели CharityProject."""
    pass


class CharityProjectUpdate(CharityProjectBase):
    """Схема для обновления модели CharityProject."""
    name: Optional[str] = Field(
        None, max_length=100, example=FieldExamples.NAME_2
    )
    description: Optional[str] = Field(
        None, example=FieldExamples.DESCRIPTION_2
    )
    full_amount: Optional[PositiveInt] = Field(
        None, example=FieldExamples.FULL_AMOUNT_2
    )


class CharityProjectDB(CharityProjectBase):
    """Схема модели CharityProject для работы с БД."""
    id: int = Field(..., example=FieldExamples.ID_1)
    invested_amount: NonNegativeInt = Field(0)
    fully_invested: bool = Field(False)
    create_date: datetime
    close_date: Optional[datetime]
