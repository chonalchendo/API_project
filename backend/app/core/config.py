from decouple import config
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Blue Ribbon 2"
    MONGO_CONNECTION_STRING: str = config("MONGO_CONNECTION_STRING", cast=str)
    OPENAI_API_KEY: str = config("OPENAI_API_KEY", cast=str)
    # REDIS_CONNECTION: Redis = Redis(host="localhost", port=6379, db=0)
    ORIGINS: list = [
        "http://localhost",
        "http://localhost:8501",
        "http://192.168.0.56",
        "http://192.168.0.56:8501",
    ]

    class Config:
        case_sensitive = True


settings = Settings()
