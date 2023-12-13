from random import randint

import requests
from app.core.config import settings

# api key for fake headers
SCRAPEOPS_API_KEY = settings.SCRAPEOPS_API_KEY

# proxy set up
PROXY = settings.ZENROWS_API_KEY_2
proxies = {"http://": PROXY, "https://": PROXY}


def get_headers_list(num_headers: int) -> list[dict[str, str]]:
    """Function that gets a specified number of browser headers.

    Args:
        num_headers: int - number of headers to generate

    Returns:
        list[dict[str, str]] - list of dictionaries

    """
    response = requests.get(
        "http://headers.scrapeops.io/v1/browser-headers",
        params={"api_key": SCRAPEOPS_API_KEY, "num_headers": num_headers},
    )
    json_response = response.json()
    return json_response.get("result", [])


def get_random_header(header_list: list[dict[str, str]]) -> dict[str, str]:
    """Function that gets a random browser header from the list of random
    headers generated using the get_headers_list function.

    Args:
        header_list: list[dict[str, str]] - list of broswer headers

    Returns:
        dict[str, str] - dictionary

    """
    random_index = randint(0, len(header_list) - 1)
    return header_list[random_index]
