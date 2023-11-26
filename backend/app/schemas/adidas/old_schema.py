from datetime import datetime
from typing import Optional

from pydantic import BaseModel

# --------------------------- Data scraping schema --------------------------- #


class AdidasImage(BaseModel):
    src: str


class AdidasShoe(BaseModel):
    displayName: str
    productId: str
    modelId: str
    price: float
    salePrice: float
    salePercentage: str
    division: str
    category: str
    sport: str
    colorVariations: list[str]
    link: str
    unisex: bool
    altText: str
    sustainability: list[str]
    surface: list[str]
    ecomTechnologies: list[str]
    weight: Optional[str] = None
    rating: Optional[float]
    ratingCount: Optional[int]
    image: AdidasImage
    secondImage: Optional[AdidasImage] = None
    updated: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class AdidasOut(BaseModel):
    altText: str
    price: float
    salePrice: float
    salePercentage: str
    link: str
    rating: Optional[float]
    ratingCount: Optional[int]
    image: AdidasImage


class ReviewsOut(BaseModel):
    title: str
    text: str


class ReviewAIResponse(BaseModel):
    response: str


class ModelView(BaseModel):
    modelId: str
