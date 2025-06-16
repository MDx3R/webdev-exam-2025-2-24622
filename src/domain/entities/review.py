from dataclasses import dataclass
from datetime import datetime

from domain.constants import MAX_RATING, MIN_RATING


@dataclass
class Review:
    """
    Aggregate root for Review.
    """

    review_id: int
    recipe_id: int
    user_id: int
    rating: int
    text: str
    created_at: datetime

    def __post_init__(self):
        assert (
            MIN_RATING <= self.rating <= MAX_RATING
        ), "Rating must be between 0 and 5."
        assert self.text, "Review text is required."
