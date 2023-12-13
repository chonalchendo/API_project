from typing import Any, Generator

import httpx
from app.core.config import log
from tenacity import retry, stop_after_attempt, wait_fixed

from ..config import proxies


class AdidasDownloader:
    def __init__(self) -> None:
        self.proxy = proxies
        self.timeout = httpx.Timeout(100.0, connect=100.0)

    @retry(stop=stop_after_attempt(4), wait=wait_fixed(1))
    def download_json(self, url: str) -> Any:
        """
        Function that downloads data from the api and returns it in a json format

        Args:
            url: str - API url

        Return:
            Any - can return any type

        """
        try:
            with httpx.Client(
                proxies=self.proxy, timeout=self.timeout, verify=False
            ) as client:
                resp = client.get(url)
                resp.raise_for_status()
                return resp.json()
        except httpx.RequestError as req_err:
            log.error(f"HTTP Request Error: {req_err}")

    def unpack_product_json(self, url: str) -> Generator[dict[str, Any], None, None]:
        """
        Function that unpacks the product json data ready to be parsed using
        the Pydantic package

        Args:
            url: str - API url

        Returns: Generator[dict[str, Any], None, None] - generates each dictionary
        within the response list

        """
        try:
            json_data = self.download_json(url)
            items = json_data.get("raw", {}).get("itemList", {}).get("items", [])
            if not items:
                log.info("No items found in the JSON response.")
            for node in items:
                yield node
        except httpx.HTTPError as exc:
            log.info(f"HTTP Exception for {exc.request.url} - {exc}")

    def unpack_review_json(self, url: str) -> Generator[dict[str, Any], None, None]:
        """
        Function that unpacks the review json data ready to be parsed using
        the Pydantic package

        Args:
            url: str - API url

        Returns: Generator[dict[str, Any], None, None] - generates each dictionary
        within the response list

        """
        try:
            json_data = self.download_json(url)
            items = json_data.get("reviews", [])
            if not items:
                log.info("No items found in the JSON response.")
            for node in items:
                yield node
        except httpx.HTTPError as exc:
            log.info(f"HTTP Exception for {exc.request.url} - {exc}")
