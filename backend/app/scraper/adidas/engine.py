from app.schemas.adidas.old_schema import AdidasShoe
from app.schemas.adidas.product_schema import Product
from app.schemas.adidas.review_schema import Reviews, ReviewStats

from .downloader import AdidasDownloader


class ProductScraper(AdidasDownloader):
    def get_product_data(self, tag: str, page: int) -> list[AdidasShoe]:
        """
        Function that takes the data from the product API, validate the data using
        Pydantic and returns to a list

        Args:
            tag: str - product range i.e. Originals
            page: int - api page

        Returns:
            list[AdidasShoe]: Pydantic.BaseModel - list of pydantic data models
        """
        api_url = (
            f"https://www.adidas.co.uk/api/plp/content-engine?query={tag}&start={page}"
        )
        data_list = []
        data = self.unpack_product_json(api_url)
        for product in data:
            item = AdidasShoe(**product)
            data_list.append(item)
        return data_list

    def get_single_product(self, product: str) -> Product:
        """
        Function that returns data on a specific product which is specified using the
        product id

        Args:
            product: str - product id

        Returns:
            Product: Pydantic.BaseModel - Pydantic model of product information
        """
        api = f"https://www.adidas.co.uk/api/products/{product}"
        prod_info = self.download_json(url=api)
        data = Product(**prod_info)
        return data


class ReviewScraper(AdidasDownloader):
    def get_product_reviews(
        self, offset: int, model_id: str, sort: str
    ) -> list[Reviews]:
        """
        Function that returns the product reviews, validates the data using Pydantic
        then returns the model to a list

        Args:
            offset: int - essentially the page which increments in 10s
            model_id: str - model id
            sort: str - sort reviews by 'newest', 'helpful', etc.

        Returns:
            list[Reviews]: list[Pydantic.BaseModel] - list of review models defined using pydantic
        """
        review_list = []
        review_api = f"https://www.adidas.co.uk/api/models/{model_id}/reviews?bazaarVoiceLocale=en_GB&feature&includeLocales=en%2A&limit=10&offset={offset}&sort={sort}"
        data = self.unpack_review_json(review_api)
        for review in data:
            item = Reviews(**review)
            item.modelId = model_id
            review_list.append(item)
        return review_list

    def get_review_stats(self, model: str) -> ReviewStats:
        """
        Function that returns all the stats on a model.

        Args:
            model: str - model id

        Returns:
            ReviewStats: Pydantic.BaseModel - Pydantic model of model review stats
        """
        api = f"https://www.adidas.co.uk/api/models/{model}/ratings?bazaarVoiceLocale=en_GB&includeLocales=en*"
        stats = self.download_json(api)
        data = ReviewStats(**stats)
        data.modelId = model
        return data
