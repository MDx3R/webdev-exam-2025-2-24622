from dataclasses import dataclass
from datetime import datetime

from domain.constants import MAX_RATING, MIN_RATING
from domain.entities.entity import Entity, Id
from domain.entities.user.user import User


@dataclass
class Review(Entity):
    """
    Aggregate root for Review.
    """

    recipe_id: Id
    user_id: Id
    rating: int
    text: str
    created_at: datetime

    def __post_init__(self):
        assert (
            MIN_RATING <= self.rating <= MAX_RATING
        ), "Rating must be between 0 and 5."
        assert self.text.strip(), "Review text is required."
        assert self.recipe_id, "Recipe ID is required."
        assert self.user_id, "User ID is required."

    @property
    def review_id(self) -> Id | None:
        return self.id

    @classmethod
    def create(
        cls,
        recipe_id: int,
        user_id: int,
        rating: int,
        text: str,
        created_at: datetime,
    ) -> "Review":
        return cls(
            entity_id=None,
            recipe_id=Id(recipe_id),
            user_id=Id(user_id),
            rating=rating,
            text=text,
            created_at=created_at,
        )


@dataclass(frozen=True)
class AuthoredReview:
    review: Review
    author: User
