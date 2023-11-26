from app.utils.errors import handle_errors
from beanie import Document, PydanticObjectId


class DataBaseServices:
    """
    Class that handles all Database related queries for the FastAPI framework.
    """

    @staticmethod
    async def list_products(collection: Document) -> list[Document] | None:
        """
        Method that retrieves all the documents from a specified collection in
        MongoDB

        Args:
            collection: Document - MongoDB collection

        Returns:
           list[Document] - list of documents from a collection
        """
        try:
            product = await collection.find_all().to_list()
            if not product:
                handle_errors.error_404(detail="Products not found")
            return product

        except Exception as e:
            handle_errors.error_500(detail="Internal server error", error=e)

    @staticmethod
    async def retrieve_object(
        collection: Document, object_id: PydanticObjectId
    ) -> Document | None:
        """
        Method that retrieves one document based on ObjectId.

        Args:
            collection: Document - MongoDB collection

        Returns:
            Document - document from MongoDB
        """
        try:
            product = await collection.get(object_id)
            if not product:
                handle_errors.error_404(detail=f"Product {object_id} not found")
            return product

        except Exception as e:
            handle_errors.error_500(detail="Internal server error", error=e)

    @staticmethod
    async def parameter_query(
        collection: Document,
        product: str | None = None,
        model: str | None = None,
        price: int | None = None,
        category: str | None = None,
        division: str | None = None,
        sport: str | None = None,
    ) -> list[Document] | None:
        """
        Method that allows the User to query the a MongoDB collection based on
        document keys.

        Args:
            collection: Document - MongoDB collection
            product: str | None - product id (defaults to None)
            model: str | None - model id (defaults to None)
            price: str | None - product price (defaults to None)
            category: str | None - product category (defaults to None)
            division: str | None - product division (defaults to None)
            sport: str | None - product sport (defaults to None)

        Returns:
            list[Document] | None - list of MongoDB documents or None
        """
        query = {}
        if product:
            query["product_id"] = product
        if model:
            query["model_number"] = model
        if price:
            query["price"] = price
        if category:
            query["category"] = category
        if division:
            if "terrex" in division.lower():
                division = division.upper()
            else:
                division = division.capitalize()
            query["division"] = division
        if sport:
            query["sport"] = sport.capitalize()

        try:
            items = await collection.find(query).to_list()
            if not items:
                handle_errors.error_404(detail="Query did not return a result")
            return items

        except Exception as e:
            handle_errors.error_500(detail="Internal server error", error=e)


product_db = DataBaseServices()
