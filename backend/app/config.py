from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "secondhand-clothing-api"
    environment: str = "local"
    log_level: str = "INFO"
    cors_origins: str | None = None  # comma-separated list
    database_url: str = (
        "postgresql+asyncpg://postgres:postgres@db:5432/app"
    )  # env override via DATABASE_URL

    class Config:
        env_file = ".env"
        env_prefix = "APP_"
        fields = {"database_url": {"env": ["DATABASE_URL", "APP_DATABASE_URL"]}}


settings = Settings()
