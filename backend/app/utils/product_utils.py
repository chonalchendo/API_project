from app.data.database import get_collection
from app.llm.model import model
from app.nlp.scripts.model import NLPModel
from app.utils.api_helpers import (convert_dict_to_string,
                                   convert_mongodb_doc_to_json)
from app.utils.errors import handle_errors
from app.utils.scrape import (get_product_from_api, scrape_adidas,
                              scrape_adidas_reviews)
from beanie import Document, PydanticObjectId
from fastapi.encoders import jsonable_encoder


class ApiServices:
    @staticmethod
    async def list_products(collection: Document):
        try:
            product = await collection.find_all().to_list()
            if not product:
                handle_errors.error_404(detail="Products not found")
            return product

        except Exception as e:
            handle_errors.error_500(detail="Internal server error", error=e)

    @staticmethod
    async def retrieve_object(collection: Document, product_id: PydanticObjectId):
        try:
            product = await collection.get(product_id)
            if not product:
                handle_errors.error_404(detail=f"Product {product_id} not found")
            return product

        except Exception as e:
            handle_errors.error_500(detail="Internal server error", error=e)

    @staticmethod
    async def retrieve_product_api(product_id: str):
        try:
            product = get_product_from_api(product=product_id)
            if not product:
                handle_errors.error_404(detail=f"Product ID {product_id} not found")
            return product

        except Exception as e:
            handle_errors.error_500(detail="Internal Server Error", error=e)

    @staticmethod
    async def parameter_query(
        collection: Document,
        product: str | None = None,
        model: str | None = None,
        price: int | None = None,
        category: str | None = None,
        link: str | None = None,
        image: str | None = None,
        division: str | None = None,
        sport: str | None = None,
    ):
        query = {}
        if product:
            query["productId"] = product
        if model:
            query["modelId"] = model
        if price is not None:
            query["price"] = price
        if category:
            query["category"] = category
        if link:
            query["link"] = link
        if image:
            query["image"] = image
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

    @staticmethod
    async def ai_query(collection: str, product: str, question: str | None = None):
        coll = get_collection(database="adidas", collection=collection)
        query = {}
        if product:
            query["productId"] = product
        try:
            doc = coll.find_one(query)
            if not doc:
                handle_errors.error_404(detail="Product not found")

            # Convert the MongoDB document to JSON-serializable data using the custom function
            json_data = convert_mongodb_doc_to_json(doc)
            # Use jsonable_encoder to handle the rest of the serialization
            serialized_data = jsonable_encoder(json_data)
            string_data = convert_dict_to_string(serialized_data)

            ai_response = model(text=string_data, query=question)
            return {"response": ai_response["result"]}

        except Exception as e:
            handle_errors.error_500(detail="Internal server error", error=e)

    @staticmethod
    async def nlp_query(collection: Document, question: str):
        query = NLPModel.model(query=question)
        query = {key: value.capitalize() for key, value in query.items()}
        items = await collection.find(query).to_list()

        try:
            if not items:
                handle_errors.error_404(detail="Product not found")
            return items

        except Exception as e:
            handle_errors.error_500(detail="Internal server error", error=e)

    @staticmethod
    async def product_from_api(product: str):
        """Function that returns the specific product a user wants from the
        Adidas API
        """
        return scrape_adidas(product=product)
