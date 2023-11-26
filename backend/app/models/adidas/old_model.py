from typing import Optional

from beanie import Document
from pydantic import BaseModel


class AdidasImage(BaseModel):
    src: str


class Brands(Document):
    # id: PydanticObjectId = Field(default_factory=uuid4, unique=True)
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
    updated: str

    class Settings:
        name = "brands"


class Sports(Document):
    # id: PydanticObjectId = Field(default_factory=uuid4, unique=True)
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
    updated: str

    class Settings:
        name = "sports"
