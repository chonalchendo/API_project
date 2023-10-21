import json

import httpx
from fake_useragent import UserAgent
from seleniumwire import webdriver
from seleniumwire.utils import decode as decodesw

from app.schemas.adidas_schema import AdidasShoe, Product, Reviews, ReviewStats
from app.schemas.nike_schema import Shoe


def get_user_agent():
    return UserAgent(verify_ssl=False).random


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


class AdidasScraper:
    def __init__(self) -> None:
        self.proxy = "http://94c37dc021d4b6378a7f067a026622613b5389d5:autoparse=true@proxy.zenrows.com:8001"
        self.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        }
        self.timeout = httpx.Timeout(10.0, connect=60.0)

    def download_json(self, url: str) -> json:
        try:
            with httpx.Client(headers=self.headers, timeout=self.timeout) as client:
                resp = client.get(url)
                resp.raise_for_status()
                return resp.json()
        except httpx.RequestError as req_err:
            print(f"HTTP Request Error: {req_err}")

    def unpack_product_json(self, url: str):
        try:
            json_data = self.download_json(url)
            items = json_data.get("raw", {}).get("itemList", {}).get("items", [])
            if not items:
                print("No items found in the JSON response.")
            for node in items:
                yield node
        except httpx.HTTPError as exc:
            print(f"HTTP Exception for {exc.request.url} - {exc}")

    def get_product_data(self, tag: str, page: int) -> list[AdidasShoe]:
        api_url = (
            f"https://www.adidas.co.uk/api/plp/content-engine?query={tag}&start={page}"
        )
        data_list = []
        data = self.unpack_product_json(api_url)
        for product in data:
            item = AdidasShoe(**product)
            data_list.append(item)
        return data_list

    def unpack_review_json(self, url: str):
        try:
            json_data = self.download_json(url)
            items = json_data.get("reviews", [])
            if not items:
                print("No items found in the JSON response.")
            for node in items:
                yield node
        except httpx.HTTPError as exc:
            print(f"HTTP Exception for {exc.request.url} - {exc}")

    def get_product_reviews(
        self, offset: int, model_id: str, sort: str
    ) -> list[Reviews]:
        review_list = []
        review_api = f"https://www.adidas.co.uk/api/models/{model_id}/reviews?bazaarVoiceLocale=en_GB&feature&includeLocales=en%2A&limit=10&offset={offset}&sort={sort}"
        data = self.unpack_review_json(review_api)
        for review in data:
            item = Reviews(**review)
            item.modelId = model_id
            review_list.append(item)
        return review_list

    def review_stats(self, model: str) -> ReviewStats:
        api = f"https://www.adidas.co.uk/api/models/{model}/ratings?bazaarVoiceLocale=en_GB&includeLocales=en*"
        stats = self.download_json(api)
        data = ReviewStats(**stats)
        data.modelId = model
        return data

    def get_single_product(self, product: str) -> Product:
        api = f"https://www.adidas.co.uk/api/products/{product}"
        product = self.download_json(api)
        data = Product(**product)
        return data


adidas_scraper = AdidasScraper()


class UrlDriver:
    def __init__(self) -> None:
        self.driver = webdriver.Chrome(seleniumwire_options={"disable_encoding": True})

    def show_request_urls(self, target_url) -> list[dict[str, str]]:
        self.driver.get(target_url)
        urls = []
        for request in self.driver.requests:
            urls.append({"url": request.url})
        return urls

    def show_response(self, target_url) -> list:
        self.driver.get(target_url)
        resps = []
        for request in self.driver.requests:
            try:
                data = decodesw(
                    request.response.body,
                    request.response.headers.get("Content-Encoding", "identity"),
                )
                resp = json.loads(data.decode("utf-8"))
                resps.append(resp)
            except:
                pass
        return resps

    def get_urls(self, url: str) -> list:
        keywords = ["api", "v2", "v1"]
        urls = self.show_request_urls(url)
        filtered_urls = [
            url for url in urls if any(kw in url["url"] for kw in keywords)
        ]
        return filtered_urls

    def close(self) -> None:
        self.driver.close()
