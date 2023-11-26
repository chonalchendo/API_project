import json
from typing import Any

from app.cache.manager import cache_instance
from app.core.config import log
from app.data.database import get_collection
from app.llm.model import model
from app.nlp.scripts.model import NLPModel
from app.schemas.adidas_schema import list_serial
from app.scraper.adidas.run import review_scraper
from app.utils.errors import handle_errors


class ReviewAIServices:
    """
    Class that deals with AI responses for product reviews
    """

    @staticmethod
    async def review_ai_response(
        collection: str, model_id: str, question: str
    ) -> dict[str, str] | None:
        """
        Method that returns an AI response, using GPT-4, based on the
        titles and bodies of all the reviews for a specified model.

        Args:
            collection: str - MongoDB collection
            model_id: str - model id
            question: str - user question
        """
        coll = get_collection(database="adidas", collection=collection)
        try:
            if model_id:
                query = {"modelId": model_id}

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
        model_id: str, question: str, sort: str
    ) -> dict[str, str] | None:
        """
        Method that retrieves the review text for a model from Redis. If
        the model does not exit in the cache, then it will scrape directly
        from the Adidas API. The text is then run through the OpenAI model
        and the LLM response is returned.

        Args:
            model_id: str - model id
            question: str - use question
            sort: str - sort reviews

        Returns:
            dict[str, str] | None - return a dictionary
        """
        try:
            # load in scraper model with URL to put model_id in
            cache = cache_instance.get(model_id)
            if cache:
                data = json.loads(cache)
                if not data:
                    handle_errors.error_404(
                        detail=f"No Review data for model {model_id}"
                    )
                if "reviewText" not in data[0]:
                    data[0]["reviewText"] = review_scraper.scrape_model_reviews(
                        model=model_id, sort=sort
                    )
                cache_instance.set(model_id, json.dumps(data))

            else:
                data = {}
                log.info("--- scraping data ---")
                data["reviewText"] = review_scraper.scrape_model_reviews(
                    model=model_id, sort=sort
                )
                if not data:
                    handle_errors.error_404(detail="Data not found")
                cache_instance.set(model_id, json.dumps(data))

            if data:
                reviews = list_serial(data[0]["reviewText"])
                concatenated_text = " ".join(
                    [item["title"] + item["text"] for item in reviews]
                )

                ai_response = model(text=concatenated_text, query=question)
                return {"response": ai_response["result"]}

        except Exception as e:
            handle_errors.error_500(error=e, detail="Server Error - LLM response")

    @staticmethod
    async def nlp_to_ai_response(
        collection: str, query: str, sort: str | None = None
    ) -> dict[str, Any]:
        """
        Method that returns the OpenAI LLM response from text data retrieved from
        MongoDB based on the user query which labels the model id and queries the
        reviews collection with the label.

        Args:
            collection: str - MongoDB collection
            query: str - user question
            sort: str | None - sort reviews (defualts to None)

        Returns:
            dict[str, Any] - dictionary with str key and any value
        """
        coll = get_collection(database="adidas", collection=collection)
        # take in the users query
        log.info("--- processing nlp model ---")
        filter = NLPModel.model(query=query)
        # use the labels to filter the database and the review type
        log.info("--- getting filter key value pairs ---")
        filters = {key: value for key, value in filter.items()}
        if "displayName" in filters.keys():
            filter = {"diplayName": filters["displayName"]}

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
        log.info("--- scraping data ---")
        data = review_scraper.scrape_model_reviews(
            model=model_id["modelId"], sort=sort_filter
        )

        reviews = list_serial(data)

        concatenated_text = " ".join(
            [
                item["title"] + item["text"]
                for item in reviews
                if item["title"] is not None and item["text"] is not None
            ]
        )
        log.info("--- generating AI response ---")
        ai_response = model(text=concatenated_text, query=query)
        return {"response": ai_response["result"]}
