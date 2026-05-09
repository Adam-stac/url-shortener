from pydantic_settings import BaseSettings

# pydantic-settings validates all config on startup.
# If DATABASE_URL is missing the app fails immediately with a clear error
# rather than crashing mid-request when the database is first accessed.
class Settings(BaseSettings):
    database_url: str
    redis_url: str = "redis://localhost:6379"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()