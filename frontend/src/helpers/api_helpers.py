from typing import Any

import httpx
from httpx import Response
from rich import print
from settings import API_URL


def response_creator(
    endpoint: str,
    base_url: str = API_URL,
    timeout: float = 30.0,
    params: dict[str, Any] | None = None,
) -> Response:
    """
    Function that deals with making the call to the API and returning the http response.

    Args:
        endpoint: str - API endpoint to query
        base_url: str - base API url (defaults to API_URL)
        params: dict[str, Any] | None - API query parameters

    Returns:
        Response: http response
    """
    # with httpx.Client(base_url=base_url, timeout=100) as client:
    #     return client.get(endpoint, params=params)
    resp = httpx.get(f"{base_url}/{endpoint}", params=params, timeout=timeout)
    return resp


def response_handler(response: Response) -> Any:
    """
    Function that deals with the httpx response and returns it in json format.

    Args:
        response: Response - API request

    Returns:
        Any
    """
    if response.status_code == 200:
        data = response.json()
        print(response.status_code)
        return data
    else:
        # st.error(f"Error: {response.status_code} - {response.text}")
        print(f"Response error: {response.status_code}")


def get_reviews_by_model(
    data: list[dict[str, Any]], model_id: str
) -> list[dict[str, Any]]:
    """
    Function that extracts dictionaries from the provided data based on the model ID.

    Args:
        data: list[dict[str, Any]] - list of dictionaries containing review data
        model_id: str - model ID to filter the data

    Returns:
        list[dict[str, Any]] - list of dictionaries for the specified model ID
    """
    return [review for review in data if review.get("modelId") == model_id]


def get_all_products() -> Any:
    """
    Function that returns all products from the product API.

    Returns:
        Any
    """
    api = response_creator(endpoint="products/all")
    return response_handler(api)


def product_api_query(
    endpoint: str = "products",
    product: str | None = None,
    name: str | None = None,    
    model: str | None = None,
    price: int | None = None,
    category: str | None = None,
    division: str | None = None,
    sport: str | None = None,
) -> Any:
    """
    Function that handles all calls to the product API.
    Includes returning one product or querying the entire product collection
    in MongoDB.

    Args:
        endpoint: str - define the api endpoint (defualts to 'products')
        product: str | None - product id (defaults to None)
        model: str | None - model id (defaults to None)
        price: str | None - product price (defaults to None)
        category: str | None - product category (defaults to None)
        division: str | None - product division (defaults to None)
        sport: str | None - product sports (defaults to None)

    Returns:
       Any
    """
    params = {}
    if model:
        params["model"] = model
    if name:
        params["name"] = name
    if price:
        params["price"] = price
    if category:
        params["category"] = category
    if division:
        params["division"] = division
    if sport:
        params["sport"] = sport

    if product:
        # return a single product
        api = response_creator(endpoint=f"{endpoint}/{product}")
    else:
        # query the products database
        api = response_creator(endpoint=f"{endpoint}/", params=params)
    return response_handler(api)[0]


def reviews_api_query(
    model: str,
    endpoint: str = "reviews",
    rating: int | None = None,
    recommended: bool | None = None,
) -> Any:
    """
    Function to query the reviews API. The API can be queried
    by returning all review information for single product, or
    queried by rating and whether it was recommended.

    Args:
        model: str - model id
        endpoint: str | None - review collection endpoint (defaults to None)
        rating: int | None - review rating (defaults to None)
        recommended: bool | None - user recommendation (defaults to None)

    Returns:
        Any
    """
    params = {}
    if rating:
        params["rating"] = rating
    if recommended:
        params["recommended"] = recommended

    api = response_creator(endpoint=f"{endpoint}/{model}", params=params)
    return response_handler(api)


def review_stats_query(
    model: str,
    endpoint: str = "reviews/stats",
    # rating: float | none = none,
    # review_count: int | none = none,
) -> Any:
    """
    function that handles queries to the review stats api.
    the api can be filtered based on model, overall rating,
    or review count.

    args:
        endpoint: str - review stats endpoint (defaults to 'reviews/stats')
        model: str | none - model id (defaults to none)
        rating: float | none - overall rating of model (defaults to none)
        review_count: int | none - number of reviews made (defaults to none)

    returns:
        any
    """
    # params = {}
    # if rating:
    #     params["rating"] = rating
    # if review_count:
    #     params["review_count"] = review_count
    # if model:
    endpoint_url = f"{API_URL}/{endpoint}/{model.rstrip('/')}"
    # api = response_creator(endpoint=endpoint_url)
    api = httpx.get(endpoint_url)
    resp = response_handler(api)
    return resp[0]


def handle_llm_response(
    endpoint: str = "reviews/query",
    model: str | None = None,
    question: str | None = None,
) -> str:
    """Function that handles the response from the LLM API.

    Args:
        endpoint (str, optional): LLM API endpoint. Defaults to "reviews/query".
        model (str | None, optional): model id. Defaults to None.
        question (str | None, optional): user question. Defaults to None.

    Returns:
        str: response from LLM API
    """
    params = {}
    if question:
        params["question"] = question

    resp = response_creator(
        endpoint=f"{endpoint}/{model}", timeout=100.0, params=params
    )
    data = response_handler(resp)
    return data["response"]
