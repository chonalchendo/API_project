import uvicorn
from beanie import init_beanie
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

from app.api_v1.router import router
from app.core.config import settings
from app.models.adidas.old_model import Brands, Sports
from app.models.adidas.product_model import Product
from app.models.adidas.review_model import Reviews, ReviewStats

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def app_init():
    """
    Initialise crucial application services.
    """
    db_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING).adidas

    await init_beanie(
        database=db_client,
        document_models=[Brands, Sports, Reviews, ReviewStats, Product],
    )


app.include_router(router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

