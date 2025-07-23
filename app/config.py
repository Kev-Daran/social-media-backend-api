from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    database_username : str
    database_hostname : str
    database_password : str
    database_port : str
    database_name : str
    secret_key : str
    algorithm : str
    access_token_expire_minutes : int

    class Config:
        env_file = Path(__file__).parent / ".env"          # IMPORTANT: NOT HAVING EXACT FILE LOCATION WILL MESS UP ALEMBIC MIGRATIONS


settings = Settings()