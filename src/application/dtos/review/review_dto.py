from dataclasses import dataclass
from datetime import datetime


@dataclass
class ReviewDTO:
    user_id: int
    rating: int
    text: str
    created_at: datetime
