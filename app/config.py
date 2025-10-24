from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    """
    Configuración general de la aplicación.
    Compatible con entornos locales (.env) y despliegues en Vercel.
    """

    OPENAI_API_KEY: str = ""
    ENVIRONMENT: str = "development"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
settings = Settings()

if not settings.OPENAI_API_KEY and "OPENAI_API_KEY" in os.environ:
    settings.OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
    settings.ENVIRONMENT = os.getenv("ENVIRONMENT", "production")
