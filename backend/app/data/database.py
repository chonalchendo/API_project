from pymongo.mongo_client import MongoClient
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def local_connection(database: str) -> MongoClient:
    client = MongoClient("mongodb://localhost:27017/")
    db = client[database]
    return db


def atlas_connection(database: str) -> MongoClient:
    uri = "mongodb+srv://conalhenderson:Spartans97#@cluster0.u7w8ug3.mongodb.net/?retryWrites=true&w=majority"

    # Create a new client and connect to the server
    client = MongoClient(uri)

    # Send a ping to confirm a successful connection
    try:
        client.admin.command("ping")
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    return client[database]


def add_data(
    database: str, collection: str, data: list[dict], atlas: bool = True
) -> None:
    if atlas:
        db = atlas_connection(database)
    else:
        db = local_connection(database)
    db[collection].insert_many(data)


def delete_data(database: str, collection: str) -> None:
    db = local_connection(database)
    db[collection].delete_many({})


def update_data(database: str, collection: str, data: list[dict]) -> None:
    try:
        db = local_connection(database)
        db[collection].insert_many(data)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    print("Data has been uploaded/updated")


def get_collection(database: str, collection: str) -> MongoClient:
    db = local_connection(database)
    return db[collection]
