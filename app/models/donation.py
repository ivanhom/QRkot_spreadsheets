from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base_model import BaseCharityProjectDonation


class Donation(BaseCharityProjectDonation):
    """Модель БД для пожертвований."""
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
