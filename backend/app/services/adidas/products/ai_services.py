from typing import Any

from app.core.config import log
from app.data.database import get_collection
from app.llm.model import model
from app.nlp.scripts.model import NLPModel
from app.utils.api_helpers import convert_dict_to_string, convert_mongodb_doc_to_json
from app.utils.errors import handle_errors
from beanie import Document
from fastapi.encoders import jsonable_encoder


class ProdAIServices:
    """
    Class that deals with product AI functionality of the API
    """

    @staticmethod
    async def ai_query(
        collection: str, product: str, question: str
    ) -> (dict[str, Any] | None):
        """
        Method that returns an OpenAI Chat model reponse to a question by a
        user on a specific product queried from MongoDB. The product information
        ran as an input into the model, therefore, the user can ask chatgpt anything
        about the product that is contained within the dataset.

        Args:
            collection: str - MongoDB collection
            product: str - product id
            question: str - user question about the product

        Return:
            (dict[str, Any] | None) - Returns the response as a dictionary or Nonetype
        """
        coll = get_collection(database="adidas", collection=collection)
        if product:
            query = {"productId": product}
            try:
                doc = coll.find_one(query)
                if not doc:
                    handle_errors.error_404(detail="Product not found")

                # Convert the MongoDB document to JSON-serialised
                json_data = convert_mongodb_doc_to_json(doc)
                serialized_data = jsonable_encoder(json_data)
                string_data = convert_dict_to_string(serialized_data)

                ai_response = model(text=string_data, query=question)
                log.info("Model response has been generated")
                return {"response": ai_response["result"]}

            except Exception as e:
                handle_errors.error_500(detail="Internal server error", error=e)
        else:
            log.error("No product selected")

    @staticmethod
    async def nlp_query(collection: Document, question: str) -> (list[Document] | None):
        """
        Method that uses NLP to query the database and returns the a list products as
        MongoDB documents associated with the NLP search.

        Args:
            collection: str - MongoDB collection
            question: str - user query

        Returns:
            (list[Document] | None): list of MongoDB documents or None
        """
        query = NLPModel.model(query=question)
        query = {key: value.capitalize() for key, value in query.items()}
        items = await collection.find(query).to_list()

        try:
            if not items:
                handle_errors.error_404(detail="Product not found")
            log.info("Items have been returned")
            return items

        except Exception as e:
            handle_errors.error_500(detail="Internal server error", error=e)
