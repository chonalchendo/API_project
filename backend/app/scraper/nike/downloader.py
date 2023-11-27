import httpx
from app.schemas.nike.product_schema import Shoe


class NikeScraper:
    def download_json(self, url: str):
        resp = httpx.get(url)
        for node in resp.json()["data"]["products"]["products"]:
            yield node

    def get_data(self, url: str) -> list[Shoe]:
        data_list = []
        for shoe in self.download_json(url):
            product = Shoe(**shoe)
            data_list.append(product)
        return data_list
