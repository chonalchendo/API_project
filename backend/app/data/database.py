from typing import Any

from app.core.config import log, settings
from pymongo.mongo_client import MongoClient


def local_connection(database: str) -> MongoClient:
    client = MongoClient(settings.MONGO_CONNECTION_STRING)
    return client[database]


def atlas_connection(database: str) -> MongoClient:
    # Create a new client and connect to the server
    client = MongoClient(settings.ATLAS_CONNECTION_STRING)

    # Send a ping to confirm a successful connection
    try:
        client.admin.command("ping")
        log.info("Pinged your deployment. You successfully connected to MongoDB!")
        return client[database]
    except Exception as e:
        log.error(e)


def delete_data(database: str, collection: str) -> None:
    db = local_connection(database)
    db[collection].delete_many({})


def upload_data(database: str, collection: str, data: Any) -> None:
    try:
        db = local_connection(database)
        db[collection].insert_many(data)
    except Exception as e:
        log.error(f"An error occurred: {e}")
    log.info(f"Data has been uploaded to {collection}")


def change_field_name(database: str, collection: str, rename: dict[str, str]) -> None:
    try:
        db = local_connection(database)
        db[collection].update_many({}, {"$rename": rename})
    except Exception as e:
        log.error(f"Database field has not been updated. Error - {e}")
    finally:
        log.info("Field name has been updated")


def get_collection(database: str, collection: str) -> MongoClient:
    db = local_connection(database)
    return db[collection]


if __name__ == "__main__":
    change_field_name(
        database="adidas", collection="product_detailed", rename={"id": "product_id"}
    )
