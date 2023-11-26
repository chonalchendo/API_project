from datetime import datetime

from pydantic import BaseModel


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
