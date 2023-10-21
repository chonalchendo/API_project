from fastapi import APIRouter

from app.models.adidas_model import Reviews, Sports
from app.utils.review_utils import ReviewServices

reviews_router = APIRouter()


@reviews_router.get(
    "/",
    summary="Get all product review information",
    response_model=list[Reviews],
)
async def read_reviews():
    return await ReviewServices.product_reviews(collection=Reviews)


@reviews_router.get(
    "/query/{model_id}",
    summary="Query reviews by modelId",
    # response_model=ReviewAIResponse,
)
async def query_by_parameter(model_id: str | None = None, question: str | None = None):
    response = await ReviewServices.review_ai_response(
        model_id=model_id, question=question, collection="reviews"
    )
    return response


@reviews_router.get(
    "/query/cache/{model_id}",
    summary="Query reviews by scraping data from website and using Redis as a cache",
)
async def query_cache(model_id: str | None = None, question: str | None = None):
    response = await ReviewServices.cached_scraped_ai_response(
        model_id=model_id, question=question
    )
    return response


@reviews_router.get(
    "/query/nlp/ai/",
    summary="Use NLP to label and filter database to return an AI response to user question on reviews",
)
async def query_nlp_ai(question: str):
    response = await ReviewServices.nlp_to_ai_response(
        collection="sports", query=question
    )
    return response


@reviews_router.get("/stats/{model}/", summary="Return the stats of a product")
async def get_product_stats(model: str):
    response = await ReviewServices.review_stats(model=model)
    return response


# -------------- Create a POST request to take in frontend query ------------- #


@reviews_router.post(
    "/sports/customer_query/{question}/{sort}",
    summary="Take in the frontend sports review query from the user and return the AI response",
)
async def frontend_query(question: str | None = None, sort: str | None = None):
    response = await ReviewServices.nlp_to_ai_response(
        collection="sports", query=question, sort=sort
    )
    return response


# ---------------- Create a put request to update the database --------------- #
