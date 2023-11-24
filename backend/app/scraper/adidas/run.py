import time
from typing import Any

from fastapi.encoders import jsonable_encoder

from ..config import log
from .engine import ProductScraper, ReviewScraper


class ProdScrapeRun(ProductScraper):
    def scrape_multi_prods(self, fashion_line: str) -> list[dict]:
        """
        Function that returns all the products for a specified fashion range
        within Adidas. For example, the 'Originals' line. All basic product data
        is returned, for more in-depth data use the scrape_detail_product()
        function

        Args:
            fashion_line: str - 'Originals', 'TERREX', 'Sports'

        Returns:
            list[dict] - list of dictionaries
        """
        all_data = []
        page = 0
        while True:
            data = self.get_product_data(tag=fashion_line, page=page * 48)
            if not data:
                break
            all_data.extend(data)
            log.info(f"Parsed page number {page}")
            page += 1
            time.sleep(10)
        final_data = jsonable_encoder(all_data)
        log.info("Data has been encoded")
        return final_data

    def scrape_detail_product(self, product: str) -> list[dict[str, Any]]:
        """
        Function that scrapes an individual product with more in-depth
        information on the product such as description etc.

        Args:
            product: str - product id

        Returns:
            list[dict] - list of dictionaries
        """
        data = self.get_single_product(product=product)
        final_data = jsonable_encoder(data)
        log.info(f"Product {product} has been parsed and encoded")
        return [final_data]


class ReviewScrapeRun(ReviewScraper):
    def scrape_model_reviews(
        self, model: str, sort: str = "newest"
    ) -> list[dict[str, Any]]:
        """
        Function that scrapes all the reviews for a model and returns as a list
        of dictionaries.

        Args:
            model: str - model id
            sort: str (defualts to 'newest') - 'newest', 'helpful', etc.

        Returns:
            list[dict] - list of dictionaries
        """
        review_data = []
        page = 0
        while True:
            data = self.get_product_reviews(offset=page, model_id=model, sort=sort)
            if not data:
                break
            review_data.extend(data)
            log.info(f"Parsed offset number {page}")
            page += 10
            # time.sleep(10)
        final_data = jsonable_encoder(review_data)
        log.info(f"ALL reviews for model {model} parsed and encoded")
        return final_data

    def scrape_review_stats(self, model: str) -> list[dict[str, Any]]:
        """
        Function that scrapes the review stats for each model and returns as a
        list of dictionaries.

        Args:
            model: str - model id

        Returns:
            list[dict] - list of dictionaries
        """
        data = self.get_review_stats(model=model)
        final_data = jsonable_encoder(data)
        log.info(f"Reviews for model {model} have been parsed and encoded")
        return [final_data]


product_scraper = ProdScrapeRun()
review_scraper = ReviewScrapeRun()
