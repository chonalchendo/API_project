from app.core.config import settings

from .handler import Handler

# adidas database
adidas_db = Handler(
    connection_string=settings.MONGO_CONNECTION_STRING, database="adidas"
)


if __name__ == "__main__":
    rename = {"id": "product_id"}
    adidas_db.change_field_name(collection="product_detailed", rename=rename)
