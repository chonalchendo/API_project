import json
import logging

from app.cache.manager import cache_instance
from app.data.database import get_collection
from app.llm.model import model
from app.nlp.scripts.model import NLPModel
from app.schemas.adidas_schema import list_serial
from app.utils.errors import handle_errors
from app.utils.scrape import scrape_adidas_reviews, scrape_review_stats
from beanie import Document

logging.basicConfig(level=logging.INFO)


class ReviewServices:
    @staticmethod
    async def product_reviews(collection: Document) -> list[Document]:
        try:
            product = await collection.find_all().to_list()
            if not product:
                handle_errors.error_404(detail="No review found")
            return product

        except Exception as e:
            handle_errors.error_500(error=e)

    @staticmethod
    async def review_stats(model: str) -> dict:
        try:
            stats = scrape_review_stats(model=model)
            if not stats:
                handle_errors.error_404(detail="No review stats found")
            return stats

        except Exception as e:
            handle_errors.error_500(detail="Internal Server Error", error=e)

    @staticmethod
    async def review_ai_response(
        collection: str, model_id: str | None = None, question: str | None = None
    ) -> dict[str, str]:
        coll = get_collection(database="adidas", collection=collection)
        query = {}
        try:
            if model_id:
                query["modelId"] = model_id

            reviews = list_serial(coll.find(query))
            if reviews is None:
                handle_errors.error_404(detail="No review found")

            concatenated_text = " ".join(
                [item["title"] + item["text"] for item in reviews]
            )
            if concatenated_text is None:
                handle_errors.error_404(detail="No string detected")

            ai_response = model(text=concatenated_text, query=question)
            if ai_response is None:
                handle_errors.error_404(detail="Model has not loaded")

            return {"response": ai_response["result"]}

        except Exception as e:
            handle_errors.error_500(error=e)

    @staticmethod
    async def cached_scraped_ai_response(
        model_id: str, question: str
    ) -> dict[str, str]:
        try:
            # load in scraper model with URL to put model_id in
            cache = cache_instance.get(model_id)
            if cache:
                data = json.loads(cache)
            else:
                print("scraping data")
                data = scrape_adidas_reviews(model_id=model_id)
                if data is None:
                    handle_errors.error_404(detail="Data not found")

            cache_instance.set(model_id, json.dumps(data))

            reviews = list_serial(data)
            concatenated_text = " ".join(
                [item["title"] + item["text"] for item in reviews]
            )

            ai_response = model(text=concatenated_text, query=question)
            return {"response": ai_response["result"]}

        except Exception as e:
            handle_errors.error_500(error=e)

    @staticmethod
    async def nlp_to_ai_response(collection: str, query: str, sort: str | None = None):
        coll = get_collection(database="adidas", collection=collection)
        # take in the users query
        logging.info("--- processing nlp model ---")
        filter = NLPModel.model(query=query)
        # use the labels to filter the database and the review type
        logging.info("--- getting filter key value pairs ---")
        filters = {key: value for key, value in filter.items()}
        if "displayName" in filters.keys():
            filter = {}
            filter["displayName"] = filters["displayName"]

            # get the model_id to filter the api request
            data = list(coll.find(filter))
            model_id = [
                {key: value}
                for d in data
                for key, value in d.items()
                if key == "modelId"
            ][0]

        if sort:
            sort_filter = filters["sort"]

        # scrape the data and prepare for ai_model
        logging.info("--- scraping data ---")
        data = scrape_adidas_reviews(model_id=model_id["modelId"], sort=sort_filter)

        reviews = list_serial(data)

        concatenated_text = " ".join(
            [
                item["title"] + item["text"]
                for item in reviews
                if item["title"] is not None and item["text"] is not None
            ]
        )

        logging.info("--- generating AI response ---")
        ai_response = model(text=concatenated_text, query=query)
        # return model response
        return {"response": ai_response["result"]}
