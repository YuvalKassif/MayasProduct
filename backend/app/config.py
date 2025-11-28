from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="APP_")

    app_name: str = "secondhand-clothing-api"
    environment: str = "local"
    log_level: str = "INFO"
    cors_origins: str | None = None  # comma-separated list

    # Database
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@db:5432/app",
        validation_alias=AliasChoices("DATABASE_URL", "APP_DATABASE_URL"),
    )

    # Security/JWT
    jwt_secret: str = Field(
        default="dev-secret-change-me",
        validation_alias=AliasChoices("JWT_SECRET", "APP_JWT_SECRET"),
    )
    jwt_access_minutes: int = 15
    jwt_refresh_days: int = 7
    cookie_domain: str | None = None


settings = Settings()
