from dataclasses import dataclass

from application.dtos.image.image_dto import ImageDTO
from application.dtos.review.review_dto import ReviewDTO


@dataclass
class RecipeDTO:
    id: int
    title: str
    description: str
    preparation_time: int
    servings: int
    ingredients: str
    steps: str
    author_id: int
    images: list[ImageDTO]
    reviews: list[ReviewDTO]
    average_rating: float
    review_count: int


@dataclass
class RecipeSummaryDTO:
    id: int
    title: str
    preparation_time: int
    servings: int
    average_rating: float
    review_count: int
