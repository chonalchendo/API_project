from fastapi import APIRouter

from app.utils.product_utils import ApiServices

product_router = APIRouter()


@product_router.get(
    "/{product}", summary="Retrieve a product directly from the Adidas API"
)
async def get_product(product: str):
    product = await ApiServices.retrieve_product_api(product_id=product)
    return product
