from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = "postgresql+asyncpg://user:password@db:5432/wallet_db"
    echo: bool = True


settings = Settings()
