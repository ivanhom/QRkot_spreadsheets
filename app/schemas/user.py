from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Схема для чтения модели User."""
    pass


class UserCreate(schemas.BaseUserCreate):
    """Схема для создания модели User."""
    pass


class UserUpdate(schemas.BaseUserUpdate):
    """Схема для обновления модели User."""
    pass
