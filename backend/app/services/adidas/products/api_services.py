import json
from typing import Any

from app.cache.manager import cache_instance
from app.scraper.adidas.run import product_scraper
from app.utils.errors import handle_errors


class APIServices:
    """
    Class that handles all calls to directly retrieve a product from the Adidas API.
    """

    @staticmethod
    async def retrieve_product_api(
        product_id: str,
    ) -> (Any | list[dict[str, Any]] | None):
        """
        Method that retrieves a single product directly from the Adidas API.

        Args:
            product_id: str - product id

        Returns: (Any | List[dict[str, Any]] | None) - returns from the cache,
        or the API, or None

        """
        try:
            cache = cache_instance.get(key=product_id)
            if cache:
                product = json.loads(cache)
            else:
                product = product_scraper.scrape_detail_product(product=product_id)
                if not product:
                    handle_errors.error_404(detail=f"Product ID {product_id} rot found")
                cache_instance.set(key=product_id, value=json.dumps(product))
            return product

        except Exception as e:
            handle_errors.error_500(detail="Internal Server Error", error=e)
