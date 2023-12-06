from typing import Any

from app.core.config import log
from pymongo.errors import OperationFailure

from .connection import Connector


class Handler(Connector):
    """
    Class that deals with database operations.
    """

    def __init__(self, connection_string: str, database: str) -> None:
        super().__init__(connection_string)
        self.database = database

    def upload_data(self, collection: str, data: Any) -> None:
        """
        Method that deals with uploading data to a MongoDB collection.

        Args:
            collection: str - MongoDB collection name
            data: Any - data to be uploaded

        Returns:
           NoneType
        """
        try:
            db = self.db_connection(self.database)
            db[collection].insert_many(data)
            log.info(
                f"Data added to the '{collection}' collection in the '{self.database}' database."
            )
        except OperationFailure as e:
            log.error(f"An error has occurred: {e}")

    def delete_data(self, collection: str) -> None:
        """
        Method that deals with deleting data from a MongoDB collection.

        Args:
            collection: str - MongoDB collection name

        Returns:
            NoneType
        """
        try:
            db = self.db_connection(self.database)
            db[collection].delete_many({})
            log.info(
                f"Data has been deleted from the {collection} in the '{self.database}' database."
            )
        except OperationFailure as e:
            log.error(f"An error has occurred: {e}")

    def fetch_data(
        self,
        collection: str,
        query: dict[Any, Any] | None = None,
        filter: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Method that deals with retrieving all data from a collection.

        Args:
            collection: str - MongoDB collection name
            query: dict[Any, Any] | None - query MongoDB collection (defaults to None).
            filter: dict[str, Any] | None - filter the MongoDB collection (defaults to None).

        Returns:
            list[dict[str, Any]] - list of BSON dictionaries
        """
        try:
            db = self.db_connection(self.database)
            data = list(db[collection].find(query, filter))
            log.info(
                f"Data has been successfully queried from the {collection} in the '{self.database}' database."
            )
            return data
        except OperationFailure as e:
            log.error(f"An error has occurred: {e}")

    def change_field_name(self, collection: str, rename: dict[str, str]) -> None:
        """
        Method that deals with changing the name of a field in MongoDB.

        Args:
            collection: str - MongoDB collection name
            rename: dict[str, str] - dictionary containing field name to change and
            what to change it to.

        Returns:
            NoneType
        """
        try:
            db = self.db_connection(self.database)
            db[collection].update_many({}, {"$rename": rename})
            log.info(
                f"Field name '{rename.keys()}' has been updated to '{rename.values()}'"
            )
        except Exception as e:
            log.error(f"Database field has not been updated. Error - {e}")
