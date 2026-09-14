from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Local-pilot configuration. Values are read from apps/api/.env — see
    .env.example in this folder. Never commit real secrets here."""

    environment: str = "local"
    database_url: str = (
        "postgresql+psycopg://sklos:sklos_local_password@localhost:5432/sklos_local"
    )
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"

    class Config:
        env_file = ".env"


settings = Settings()
