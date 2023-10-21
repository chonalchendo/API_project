import time
from typing import Literal

from fastapi.encoders import jsonable_encoder
from rich import print

from app.data.database import update_data
from app.data.scraper import adidas_scraper


def num_convert(num: int):
    return num * 48


def scrape_adidas(product: str) -> list[dict]:
    all_data = []
    page = 0
    while True:
        data = adidas_scraper.get_product_data(tag=product, page=num_convert(page))
        if not data:
            break
        all_data.extend(data)
        print(f"Parsed page number {page}")
        page += 1
        time.sleep(10)
    final_data = jsonable_encoder(all_data)
    print("Data has been encoded")
    return final_data


def scrape_adidas_reviews(model_id: str, sort: str = "newest") -> list[dict]:
    review_data = []
    page = 0
    while True:
        data = adidas_scraper.get_product_reviews(
            offset=page, model_id=model_id, sort=sort
        )
        if not data or page > 50:
            break
        review_data.extend(data)
        print(f"Parsed offset number {page}")
        page += 10
        time.sleep(10)
    final_data = jsonable_encoder(review_data)
    print("Data has been encoded")
    return final_data


def scrape_review_stats(model: str) -> list[dict]:
    data = adidas_scraper.review_stats(model=model)
    final_data = jsonable_encoder(data)
    return [final_data]


def get_product_from_api(product: str) -> list[dict]:
    data = adidas_scraper.get_single_product(product=product)
    final_data = jsonable_encoder(data)
    return [final_data]


def scrape_to_db(
    model: str, collection: Literal["brands", "sports", "reviews"]
) -> None:
    data = scrape_adidas_reviews(model_id=model)
    update_data(database="adidas", collection=collection, data=data)
