"""
Configuração centralizada da aplicação.
Carrega variáveis de ambiente (incluindo .env) e expõe valores tipados.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações da aplicação a partir de variáveis de ambiente."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Banco de dados
    DATABASE_URL: str = (
        "postgresql+psycopg2://postgres:postgres@db:5432/stock_db"
    )


settings = Settings()
