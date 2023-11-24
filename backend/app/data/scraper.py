import json

import httpx
from app.data.scraper_file.config import get_headers_list
from app.schemas.nike_schema import Shoe
from seleniumwire import webdriver
from seleniumwire.utils import decode as decodesw


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
