from pydantic import BaseModel


class Price(BaseModel):
    currency: str
    currentPrice: float
    discounted: bool
    fullPrice: float


class Variant(BaseModel):
    cloudProductId: str
    colorDescription: str
    price: Price
    inStock: bool
    isBestSeller: bool
    isNew: bool


class Shoe(BaseModel):
    url: str
    cloudProductId: str
    title: str
    subtitle: str
    salesChannel: list[str]
    productType: str
    price: Price
    inStock: bool
    isBestSeller: bool
    isNBA: bool
    isNFL: bool
    isSustainable: bool
    colorways: list[Variant]
