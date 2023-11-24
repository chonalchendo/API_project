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


# adidas review schemas


class CustomQs(BaseModel):
    value: str | None = None
    id: str | None = None
    valueLabel: str | None = None
    dimensionLabel: str | None = None


class ReviewPhotos(BaseModel):
    normalUrl: str | None = None


class Reviews(BaseModel):
    id: str
    modelId: str | None = None
    title: str | None = None
    text: str | None = None
    isRecommended: bool
    rating: int
    customQuestions: list[CustomQs] | None = None
    positiveFeedbackCount: int | None = None
    negativeFeedbackCount: int | None = None
    photos: list[ReviewPhotos] | None = None
    badges: list[str] | None = None
    locale: str | None = None
    color: str | None = None
    submissionTime: str | None = None
    added: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class RatingLabel(BaseModel):
    value: str | None = None


class Rating(BaseModel):
    name: str
    averageRating: float
    minLabel: RatingLabel | None = None
    midLabel: RatingLabel | None = None
    maxLabel: RatingLabel | None = None


class Dist(BaseModel):
    rating: int
    count: int


class InsightValues(BaseModel):
    reviewCount: int | None = None
    answerId: str | None = None
    answerLabel: str | None = None


class Insights(BaseModel):
    questionId: str | None = None
    label: str | None = None
    values: list[InsightValues] | None = None


class ReviewStats(BaseModel):
    modelId: str | None = None
    overallRating: float | None = None
    reviewCount: int | None = None
    recommendationPercentage: int | None = None
    secondaryRatings: list[Rating] | None = None
    ratingDistribution: list[Dist] | None = None
    insightsFilters: list[Insights] | None = None


# ------------------------- Database retrival schemas ------------------------ #


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


def individual_serial(review: str) -> dict:
    return {"title": review["title"], "text": review["text"]}


def list_serial(reviews: str) -> list:
    return [individual_serial(review) for review in reviews]
