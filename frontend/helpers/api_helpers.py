import json

import httpx
import streamlit as st


def response_handler(response: httpx.get) -> json:
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        st.error(f"Error: {response.status_code} - {response.text}")


def return_product_info(product: str | None = None, model: str | None = None):
    if product:
        api = f"http://localhost:8000/api/v1/product/{product}"
    if model:
        api = f"http://localhost:8000/api/v1/reviews/stats/{model}/"
    response = httpx.get(api, timeout=100)
    data = response_handler(response).pop(0)
    return data
