from app.core.config import log
from pymongo.database import Database
from pymongo.errors import ConnectionFailure
from pymongo.mongo_client import MongoClient


class Connector:
    """
    Class that deals with connecting to the database.
    Responsible for establishing a connection to the MongoDB server.
    """

    def __init__(self, connection_string: str) -> None:
        self.connection_string = connection_string

    def db_connection(self, database: str) -> Database:
        """
        Method that returns a MongoDB database.

        Args:
            database: str - database name

        Returns:
            MongoClient - MongoDB database
        """
        client = MongoClient(self.connection_string)
        try:
            client.admin.command("ping")
            log.info("Pinged your deployment. Successful connection to MongoDB.")
            return client[database]
        except ConnectionFailure as e:
            log.error(e)
            
    
