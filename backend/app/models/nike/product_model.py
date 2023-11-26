from beanie import Document


class Price(Document):
    currency: str
    currentPrice: float
    discounted: bool
    fullPrice: float


class Variant(Document):
    cloudProductId: str
    colorDescription: str
    price: Price
    inStock: bool
    isBestSeller: bool
    isNew: bool


class Shoe(Document):
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
