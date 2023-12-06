from app.models.adidas.product_model import Product
from app.services.adidas.products.database_services import product_db
from fastapi import APIRouter

product_router = APIRouter()


@product_router.get(
    "/",
    summary="Query MongoDB product collection for products based on user queries",
    status_code=200,
)
async def query_products(
    model: str | None = None,
    price: int | None = None,
    category: str | None = None,
    division: str | None = None,
    sport: str | None = None,
):
    return await product_db.parameter_query(
        collection=Product,
        model=model,
        price=price,
        category=category,
        division=division,
        sport=sport,
    )


@product_router.get(
    "/{product}", summary="Return a single product from MongoDB", status_code=200
)
async def return_product(product: str):
    return await product_db.parameter_query(collection=Product, product=product)
