from fastapi import APIRouter

from app.models.adidas_model import Sports
from app.schemas.adidas_schema import AdidasOut
from app.utils.product_utils import ApiServices

sports_router = APIRouter()


@sports_router.get(
    "/", summary="Return all sports product information", response_model=list[AdidasOut]
)
async def read_sports():
    return await ApiServices.list_products(collection=Sports)


@sports_router.get("/query", response_model=list[AdidasOut])
async def query_by_parameter(
    product: str | None = None,
    model: str | None = None,
    price: int | None = None,
    category: str | None = None,
    link: str | None = None,
    image: str | None = None,
    sport: str | None = None,
    division: str | None = None,
):
    return await ApiServices.parameter_query(
        collection=Sports,
        product=product,
        model=model,
        price=price,
        category=category,
        link=link,
        image=image,
        sport=sport,
        division=division,
    )


@sports_router.get("/query/nlp", response_model=list[AdidasOut])
async def query_by_nlp(question: str):
    return await ApiServices.nlp_query(collection=Sports, question=question)


# ---------------- PUT REQUEST --------------- #
