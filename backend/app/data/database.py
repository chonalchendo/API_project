import logging
import os
from typing import Any

from app.core.config import log
from dotenv import load_dotenv
from pymongo import database
from pymongo.mongo_client import MongoClient

load_dotenv()

mongodb_conn_string = os.getenv("MONGO_CONNECTION_STRING")
atlas_conn_string = os.getenv("ATLAS_CONNECTION_STRING")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def local_connection(database: str) -> MongoClient:
    client = MongoClient(mongodb_conn_string)
    db = client[database]
    return db


def atlas_connection(database: str) -> MongoClient:
    uri = atlas_conn_string

    # Create a new client and connect to the server
    client = MongoClient(uri)

    # Send a ping to confirm a successful connection
    try:
        client.admin.command("ping")
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    return client[database]


def delete_data(database: str, collection: str) -> None:
    db = local_connection(database)
    db[collection].delete_many({})


def upload_data(database: str, collection: str, data: Any) -> None:
    try:
        db = local_connection(database)
        db[collection].insert_many(data)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    logger.info(f"Data has been uploaded to {collection}")


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
