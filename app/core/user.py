import logging
from typing import Optional, Union

from fastapi import Depends, Request
from fastapi_users import (BaseUserManager, FastAPIUsers, IntegerIDMixin,
                           InvalidPasswordException)
from fastapi_users.authentication import (AuthenticationBackend,
                                          BearerTransport, JWTStrategy)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import Messages
from app.core.config import settings
from app.core.db import get_async_session
from app.models.user import User
from app.schemas.user import UserCreate


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """Доступ к модели пользователя в БД через SQLAlchemy."""
    yield SQLAlchemyUserDatabase(session, User)


bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')


def get_jwt_strategy() -> JWTStrategy:
    """Определение стратегии хранения токена в виде JWT."""
    return JWTStrategy(
        secret=settings.secret, lifetime_seconds=settings.token_lifitime
    )


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """Регистрация и управление пользователями."""

    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User]
    ) -> None:
        """Условия валидации пароля."""
        if len(password) < settings.password_length:
            raise InvalidPasswordException(
                reason=Messages.PASSWORD_TO_SHORT
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason=Messages.PASSWORD_CONTAINS_EMAIL
            )

    async def on_after_register(
            self, user: User, request: Optional[Request] = None
    ):
        """Уведомление об успешной регистрации пользователя."""
        logging.info(Messages.USER_CREATED.format(user.email))


async def get_user_manager(user_db=Depends(get_user_db)):
    """Вызов объекта класса UserManager."""
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
