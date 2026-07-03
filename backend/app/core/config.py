from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Database
    database_url: str = "postgresql+asyncpg://coffeans:coffeans@localhost:5432/coffeans"

    # Auth
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7  # 1 week

    # External APIs
    anthropic_api_key: str = ""
    google_places_api_key: str = ""

    # App
    environment: str = "development"
    cors_origins: list[str] = ["http://localhost:5173"]


settings = Settings()
