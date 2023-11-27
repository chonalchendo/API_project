from app.database.manager import adidas_db
from icecream import ic

from .run import product_scraper, review_scraper


def upload_multi_prods(range: str) -> None:
    """
    Function that scrapes all the specified product information from the Adidas API
    and uploads it to the products collection in the MongoDB database.

    Args:
        range: str - product range to scrape

    Return: None
    """
    data = product_scraper.scrape_multi_prods(fashion_line=range)
    adidas_db.upload_data(collection="product", data=data)


def upload_detailed_prod(product: str) -> None:
    """
    Function that scrapes the specified detailed product information from the Adidas
    API and uploads it to the products? collection in MongoDB

    Args:
        product: str - product id

    Return: None
    """
    data = product_scraper.scrape_detail_product(product=product)
    ic(data)
    adidas_db.upload_data(collection="product_detailed", data=data)


def upload_model_reviews(model: str) -> None:
    """
    Function that scrapes model reviews and uploads them to the reviews
    collection in MongoDB

    Args:
        model: str - model id

    Return: None
    """
    data = review_scraper.scrape_model_reviews(model=model)
    adidas_db.upload_data(collection="reviews", data=data)


def upload_review_stats(model: str) -> None:
    """
    Function that scrapes model review stats and uploads them to the review_stats
    collection in MongoDB

    Args:
        model: str - model id

    Return: None
    """
    data = review_scraper.scrape_review_stats(model=model)
    ic(data)
    adidas_db.upload_data(collection="review_stats", data=data)
