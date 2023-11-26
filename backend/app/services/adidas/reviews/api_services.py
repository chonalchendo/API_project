import json
from typing import Any

from app.cache.manager import cache_instance
from app.scraper.adidas.run import review_scraper
from app.utils.errors import handle_errors


class APIServices:
    """
    Class that deals with getting review information directly from Adidas API
    """

    @staticmethod
    async def get_review_stats(model: str) -> list[dict[str, Any]]:
        """
        Method that returns all reviews for a specified model. Uses Redis
        as a cache to improve response time.

        Args:
            model: str - model id

        Returns:
            list[dict] - list of stats dictionaries
        """
        try:
            cache = cache_instance.get(key=model)
            if cache:
                data = json.loads(cache)
                if not data:
                    handle_errors.error_404(detail="No review stats found")
                if "reviewStats" not in data[0]:
                    data[0]["reviewStats"] = review_scraper.scrape_review_stats(
                        model=model
                    )
                    cache_instance.set(model, json.dumps(data))
            else:
                data = {}
                data["reviewStats"] = review_scraper.scrape_review_stats(model=model)
                if not data:
                    handle_errors.error_404(detail="No review stats found")
                cache_instance.set(key=model, value=json.dumps(data))
            return data[0]["reviewStats"]

        except Exception as e:
            handle_errors.error_500(detail="Server Error - Review Stats", error=e)
