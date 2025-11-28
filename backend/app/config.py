from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "secondhand-clothing-api"
    environment: str = "local"
    log_level: str = "INFO"
    cors_origins: str | None = None  # comma-separated list

    class Config:
        env_file = ".env"
        env_prefix = "APP_"


settings = Settings()

