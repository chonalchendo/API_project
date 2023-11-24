import logging
import os
from random import randint

import requests
from dotenv import load_dotenv
from rich.logging import RichHandler

load_dotenv()

# api key for fake headers
SCRAPEOPS_API_KEY = os.getenv("SCRAPEOPS_API_KEY")

# proxy set up
PROXY = os.getenv("ZENROWS_API")
proxies = {"http://": PROXY, "https://": PROXY}


# logging set up
logging.basicConfig(
    level="NOTSET",
    format="%(levelname)s [%(asctime)s] %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[RichHandler(rich_tracebacks=True)],
)

log = logging.getLogger("rich")


def get_headers_list(num_headers: int) -> list[dict[str, str]]:
    response = requests.get(
        "http://headers.scrapeops.io/v1/browser-headers",
        params={"api_key": SCRAPEOPS_API_KEY, "num_headers": num_headers},
    )
    json_response = response.json()
    return json_response.get("result", [])


def get_random_header(header_list):
    random_index = randint(0, len(header_list) - 1)
    return header_list[random_index]
