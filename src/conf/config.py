from pydantic import EmailStr
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # PostgreSQL database settings
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "contacts_db"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"

    # JWT settings
    JWT_SECRET: str = "current_jwt_secret"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_SECONDS: int = 3600

    # Email settings for FastAPI-Mail
    MAIL_USERNAME: EmailStr = "contactApp@meta.ua"
    MAIL_PASSWORD: str = "ContactApp0"
    MAIL_FROM: EmailStr = "contactApp@meta.ua"
    MAIL_PORT: int = 465
    MAIL_SERVER: str = "smtp.meta.ua"
    MAIL_FROM_NAME: str = "Rest API Service"
    MAIL_STARTTLS: bool = False
    MAIL_SSL_TLS: bool = True
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True

    # Cloudinary settings
    CLD_NAME: str = "dzglb1qlb"
    CLD_API_KEY: int = 277562143483385
    CLD_API_SECRET: str = "IedHZraTe0LtJG5ZTSjnb4aNeAw"

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

config = Settings()
