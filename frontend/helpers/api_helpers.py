from typing import Any

import httpx
import pandas as pd
import streamlit as st
from rich import print


def response_handler(response: httpx.get) -> Any:
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        st.error(f"Error: {response.status_code} - {response.text}")


def return_product_info(
    product: str | None = None, model: str | None = None
) -> dict[Any, Any]:
    if product:
        api = f"http://localhost:8000/api/v1/product/{product}"
    if model:
        api = f"http://localhost:8000/api/v1/reviews/stats/{model}/"
    response = httpx.get(api, timeout=100)
    data = response_handler(response).pop(0)
    return data


def return_model_info(model: str | None = None) -> dict[Any, Any]:
    api = f"http://localhost:8000/api/v1/reviews/stats/{model}/"
    response = httpx.get(api, timeout=100)
    data = response_handler(response)
    return data


def return_reviews_db(model: str) -> list[dict[str, Any]]:
    """
    Function that deals with the API call to return all the review information
    contained within the MongoDB database

    args:
        model: str - model id
    return: list[dict[str, Any]] - return data from database
    """
    api = f"http://127.0.0.1:8000/api/v1/reviews/review_info/?model={model}"
    response = httpx.get(api, timeout=100)
    data = response_handler(response)
    return data


def handle_llm_response(
    model_id: str | None = None, question: str | None = None, sort: str | None = None
) -> str:
    llm_api = f"http://localhost:8000/api/v1/reviews/query/?model_id={model_id}&question={question}&sort={sort}"
    response = httpx.get(llm_api, timeout=100)
    data = response_handler(response)
    return data["response"]


if __name__ == "__main__":
    resp = return_reviews_db(model="KGO51")
    print(resp)
    df = pd.DataFrame(resp)
    print(df)
