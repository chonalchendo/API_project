from fastapi import APIRouter

from app.api_v1.handlers import brands, product, reviews, sports

router = APIRouter()

router.include_router(brands.brands_router, prefix="/brands", tags=["Adidas"])
router.include_router(sports.sports_router, prefix="/sports", tags=["Adidas"])
router.include_router(reviews.reviews_router, prefix="/reviews", tags=["Adidas"])
router.include_router(product.product_router, prefix="/product", tags=["Adidas"])
