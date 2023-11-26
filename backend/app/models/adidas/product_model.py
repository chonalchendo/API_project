from app.schemas.adidas.product_schema import (
    AttributeList,
    Image,
    MetaData,
    PricingInfo,
    ProductDesc,
)
from beanie import Document


class Product(Document):
    product_id: str
    name: str
    model_number: str
    meta_data: MetaData
    attribute_list: AttributeList
    pricing_information: PricingInfo
    product_description: ProductDesc
    view_list: list[Image]
    updated: str

    class Settings:
        name = "product_detailed"
