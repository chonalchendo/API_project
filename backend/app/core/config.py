import logging

from decouple import config
from pydantic_settings import BaseSettings
from rich.logging import RichHandler


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Blue Ribbon 2"
    MONGO_CONNECTION_STRING: str = config("MONGO_CONNECTION_STRING", cast=str)
    ATLAS_CONNECTION_STRING: str = config("ATLAS_CONNECTION_STRING", cast=str)
    OPENAI_API_KEY: str = config("OPENAI_API_KEY", cast=str)
    SCRAPEOPS_API_KEY: str = config("SCRAPEOPS_API_KEY", cast=str)
    ZENROWS_API_KEY: str = config("ZENROWS_API", cast=str)
    ZENROWS_API_KEY_2: str = config("ZENROWS_API_2", cast=str)
    IPROYAL_API_KEY: str = config("IPROYAL_API", cast=str)
    ORIGINS: list = [
        "http://localhost",
        "http://localhost:8501",
        "http://192.168.0.56",
        "http://192.168.0.56:8501",
    ]

    class Config:
        case_sensitive = True


# logging set up
logging.basicConfig(
    level="INFO",
    format="%(levelname)s [%(asctime)s] %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[RichHandler(rich_tracebacks=True)],
)

# load config variables
log = logging.getLogger("rich")
settings = Settings()
