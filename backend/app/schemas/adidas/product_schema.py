from datetime import datetime

from pydantic import BaseModel


class MetaData(BaseModel):
    canonical: str
    keywords: str
    page_title: str
    site_name: str


class AttributeList(BaseModel):
    sale: bool | None = None
    brand: str
    color: str
    gender: str
    sport: list[str] | None = None
    weight: str | None = None
    closure: list[str]
    surface: list[str]
    category: str
    foot_type: str | None = None
    sport_ids: list[str] | None = None
    sportSub: list[str] | None = None
    best_for_ids: list[str] | None = None
    productfit: list[str] | None = None
    base_material: list[str] | None = None
    productType: list[str] | None = None
    technologies: list[str] | None = None
    personalizable: bool
    customizable: bool
    toe_stack_height: str | None = None
    heel_stack_height: str | None = None
    is_orderable: bool
    isWaitingRoomProduct: bool
    isInPreview: bool
    specialLaunch: bool
    special_launch_type: str | None = None


class PricingInfo(BaseModel):
    currentPrice: int
    standard_price: int
    standard_price_no_vat: float
    sale_price: int | None = None
    sale_price_no_vat: float | None = None
    discount_text: str | None = None


class CareInstruc(BaseModel):
    code: str
    description: str


class WashInstruc(BaseModel):
    care_instructions: list[CareInstruc] | None = None
    extra_care_instructions: list[str] | None = None


class ProductDesc(BaseModel):
    title: str
    text: str
    subtitle: str
    usps: list[str]
    wash_care_instructions: WashInstruc


class Image(BaseModel):
    type: str
    image_url: str


class Product(BaseModel):
    id: str
    name: str
    model_number: str
    meta_data: MetaData
    attribute_list: AttributeList
    pricing_information: PricingInfo
    product_description: ProductDesc
    view_list: list[Image]
    updated: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
