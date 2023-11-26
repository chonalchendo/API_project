from app.schemas.adidas.review_schema import (
    CustomQs,
    Dist,
    Insights,
    Rating,
    ReviewPhotos,
)
from beanie import Document


class Reviews(Document):
    modelId: str
    title: str
    text: str
    isRecommended: bool
    rating: int
    customQuestions: list[CustomQs]
    positiveFeedbackCount: int
    negativeFeedbackCount: int
    photos: list[ReviewPhotos]
    badges: list[str]
    locale: str
    color: str | None
    submissionTime: str
    added: str

    class Settings:
        name = "reviews"


class ReviewStats(Document):
    modelId: str
    overallRating: float
    reviewCount: int
    recommendationPercentage: int
    secondaryRatings: list[Rating]
    ratingDistribution: list[Dist]
    insightsFilters: list[Insights]

    class Settings:
        name = "review_stats"
