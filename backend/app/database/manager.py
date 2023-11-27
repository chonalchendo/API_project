from app.core.config import settings

from .handler import Handler

# adidas database
adidas_db = Handler(
    connection_string=settings.MONGO_CONNECTION_STRING, database="adidas"
)
