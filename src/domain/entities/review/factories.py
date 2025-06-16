from abc import ABC, abstractmethod

from domain.clock import Clock
from domain.entities.review.dtos import ReviewData
from domain.entities.review.review import Review


class IReviewFactory(ABC):
    @abstractmethod
    def create(self, data: ReviewData) -> Review: ...


class ReviewFactory(IReviewFactory):
    def __init__(self, clock: Clock) -> None:
        self.clock = clock

    def create(self, data: ReviewData) -> Review:
        return Review.create(
            recipe_id=data.recipe_id,
            user_id=data.user_id,
            rating=data.rating,
            text=data.text,
            created_at=self.clock.now(),
        )
