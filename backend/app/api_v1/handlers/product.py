from app.models.adidas.product_model import Product
from app.services.adidas.products.database_services import product_db
from fastapi import APIRouter

product_router = APIRouter()


@product_router.get(
    "/", summary="Query MongoDB product collection for products based on user queries"
)
async def get_product(
    product: str | None = None,
    model: str | None = None,
    price: int | None = None,
    category: str | None = None,
    division: str | None = None,
    sport: str | None = None,
):
    product = await product_db.parameter_query(
        collection=Product,
        product=product,
        model=model,
        price=price,
        category=category,
        division=division,
        sport=sport,
    )
    return product
