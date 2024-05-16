from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, NonNegativeInt, PositiveInt

from app.constants import FieldExamples


class DonationBase(BaseModel):
    """Базовая схема для модели Donation."""
    full_amount: PositiveInt = Field(..., example=FieldExamples.FULL_AMOUNT_3)
    comment: Optional[str] = Field(None, example=FieldExamples.COMMENT)

    class Config:
        extra = Extra.forbid
        orm_mode = True


class DonationCreate(DonationBase):
    """Схема для создания модели Donation."""
    pass


class DonationGet(DonationBase):
    """Схема для чтения модели Donation."""
    id: int = Field(..., example=FieldExamples.ID_1)
    create_date: datetime


class DonationDB(DonationGet):
    """Схема модели Donation для работы с БД."""
    user_id: int = Field(..., example=FieldExamples.ID_2)
    invested_amount: NonNegativeInt = Field(0)
    fully_invested: bool = Field(False)
    close_date: Optional[datetime]
