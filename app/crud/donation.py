from app.crud.base import CRUDBase
from app.models import Donation


class CRUDDonation(CRUDBase):
    """Класс для расширения стандартных
    CRUD операций с БД для модели Donation.
    """
    pass


donation_crud = CRUDDonation(Donation)
