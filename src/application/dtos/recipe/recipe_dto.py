from dataclasses import dataclass

from application.dtos.image.image_dto import ImageDTO
from application.dtos.review.review_dto import AuthoredReviewDTO
from application.dtos.user.user_dto import UserDTO
from domain.entities.recipe.recipe import Recipe


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

    @classmethod
    def from_domain(cls, recipe: Recipe) -> "RecipeDTO":
        return cls(
            id=recipe.id_safe.value,
            title=recipe.content.title,
            description=recipe.content.description,
            preparation_time=recipe.details.preparation_time,
            servings=recipe.details.servings,
            ingredients=recipe.instruction.ingredients,
            steps=recipe.instruction.steps,
            author_id=recipe.author_id.value,
            images=[ImageDTO.from_domain(img) for img in recipe.images],
        )


@dataclass
class RecipeSummaryDTO:
    id: int
    title: str
    preparation_time: int
    servings: int
    average_rating: float
    review_count: int
    author_id: int
    images: list[ImageDTO]

    @classmethod
    def from_domain(
        cls,
        recipe: Recipe,
        average_rating: float,
        review_count: int,
    ) -> "RecipeSummaryDTO":
        return cls(
            id=recipe.id_safe.value,
            title=recipe.content.title,
            preparation_time=recipe.details.preparation_time,
            servings=recipe.details.servings,
            average_rating=average_rating,
            review_count=review_count,
            author_id=recipe.author_id.value,
            images=[ImageDTO.from_domain(img) for img in recipe.images],
        )


@dataclass
class FullRecipeDTO:
    recipe: RecipeDTO
    author: UserDTO
    reviews: list[AuthoredReviewDTO]
    summary: RecipeSummaryDTO

    @classmethod
    def create(
        cls,
        recipe: RecipeDTO,
        author: UserDTO,
        reviews: list[AuthoredReviewDTO],
        summary: RecipeSummaryDTO,
    ) -> "FullRecipeDTO":
        return cls(
            recipe=recipe, author=author, reviews=reviews, summary=summary
        )
