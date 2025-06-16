from dataclasses import dataclass


@dataclass(frozen=True)
class ReviewData:
    recipe_id: int
    user_id: int
    rating: int
    text: str
