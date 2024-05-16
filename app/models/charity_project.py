from sqlalchemy import Column, String, Text

from app.models.base_model import BaseCharityProjectDonation


class CharityProject(BaseCharityProjectDonation):
    """Модель БД для благотворительных проектов."""
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
