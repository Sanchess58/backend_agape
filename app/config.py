import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    JWT_SECRET_KEY: str
    ALGORITHM: str
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    BUCKET_NAME: str
    S3_URL: str
    S3_REGION: str
    ADMIN_SECRET: str

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.getcwd()), ".env")
    )

settings = Settings()


def get_db_url() -> str:
    return (f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
            f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
