from dataclasses import dataclass
from datetime import datetime

from application.dtos.user.user_dto import UserDTO
from domain.entities.review.review import Review
from domain.entities.user.user import User


@dataclass
class ReviewDTO:
    review_id: int
    user_id: int
    rating: int
    text: str
    created_at: datetime

    @classmethod
    def from_domain(cls, review: Review) -> "ReviewDTO":
        return ReviewDTO(
            review_id=review.id_safe.value,
            user_id=review.user_id.value,
            rating=review.rating,
            text=review.text,
            created_at=review.created_at,
        )


@dataclass
class AuthoredReviewDTO:
    review: ReviewDTO
    user: UserDTO

    @classmethod
    def from_domain(cls, review: Review, user: User) -> "AuthoredReviewDTO":
        return cls(
            review=ReviewDTO.from_domain(review),
            user=UserDTO.from_domain(user),
        )
