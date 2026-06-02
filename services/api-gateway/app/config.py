from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://church_user:church_pass_2024@localhost:5433/churchdb"
    REDIS_URL: str = "redis://localhost:6380/0"
    SECRET_KEY: str = "church_secret_key_change_in_production_2024"
    ENVIRONMENT: str = "development"
    KEYCLOAK_URL: str = "http://localhost:8082"

    class Config:
        env_file = ".env"

settings = Settings()
