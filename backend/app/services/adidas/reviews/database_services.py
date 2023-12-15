from app.schemas.adidas.review_schema import Reviews
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
    async def get_model_reviews(
        collection: Document,
        model: str,
        recommended: bool | None = None,
        rating: int | None = None,
    ) -> list[Document] | None:
        """
        Method that returns all the review information for a specified model from
        MongoDB.
        The collection can be changed so that the review_stats collection can be
        queried too.

        Args:
            collection: Document - The MongoDB collection to query
            model: str - The model id to be queried

        Returns:
            list[Document] - return a list of MongoDB documents

        """
        query = {}
        if model:
            query["modelId"] = model
        if recommended:
            query["isRocommended"] = recommended
        if rating:
            query["rating"] = rating

        try:
            reviews = await collection.find(query).to_list()

            if not reviews:
                handle_errors.error_404(
                    detail=f"Query did not return reviews for {model}"
                )
            return reviews
        except Exception as e:
            handle_errors.error_500(
                detail=f"Internal Server Error - error when querying model {model}",
                error=e,
            )


review_db_service = DataBaseServices()
