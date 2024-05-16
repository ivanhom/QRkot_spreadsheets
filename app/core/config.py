from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    """Настройка переменных окружения проекта."""
    app_title: str = 'Название проекта'
    app_description: str = 'О проекте'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    password_length = 3
    secret: str = 'SECRET'
    time_format: str = '%Y/%m/%d %H:%M:%S'
    token_lifitime = 3600

    # Переменные для Google API
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()
