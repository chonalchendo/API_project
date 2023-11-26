from app.utils.errors import handle_errors
from beanie import Document


class DataBaseServices:
    @staticmethod
    async def all_product_reviews(collection: Document) -> list[Document] | None:
        """
        Method to return all the reviews from the reviews collection.

        Args:
            collection: Document - MongoDB collection

        Returns:
            list[Document] - list of documents
        """
        try:
            product = await collection.find_all().to_list()
            if not product:
                handle_errors.error_404(detail="No review found")
            return product

        except Exception as e:
            handle_errors.error_500(error=e)

    @staticmethod
    async def get_model_reviews_db(
        collection: Document, model: str
    ) -> list[Document] | None:
        """
        Method that returns all the review information for a specified model from
        MongoDB.

        args:
            collection: Document - The MongoDB collection to query
            model: str - The model id to be queried

        return: list[Document] - return a list of MongoDB documents

        """
        if model:
            query = {"modelId": model}
        try:
            reviews = await collection.find(query).to_list()
            if not reviews:
                handle_errors.error_404(
                    detail=f"Query did not return reviews for {model}"
                )
            return reviews
        except Exception as e:
            handle_errors.error_500(detail="Internal Server Error", error=e)
