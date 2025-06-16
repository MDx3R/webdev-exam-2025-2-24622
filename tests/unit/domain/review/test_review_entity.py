from typing import Any

import pytest

from domain.clock import Clock
from domain.entities.entity import Id
from domain.entities.review.review import Review


@pytest.fixture
def valid_review_data(mock_clock: Clock) -> dict[str, Any]:
    return {
        "recipe_id": 1,
        "user_id": 10,
        "rating": 4,
        "text": "Delicious recipe!",
        "created_at": mock_clock.now(),
    }


@pytest.fixture
def valid_review(valid_review_data: dict[str, Any]) -> Review:
    return Review.create(**valid_review_data)


class TestReview:
    @pytest.fixture(autouse=True)
    def setup(self, valid_review: Review):
        self.review = valid_review

    def test_create_with_valid_data_sets_correct_attributes(
        self, valid_review_data: dict[str, Any]
    ):
        review = Review.create(**valid_review_data)
        assert review.review_id is None
        assert review.recipe_id == Id(valid_review_data["recipe_id"])
        assert review.user_id == Id(valid_review_data["user_id"])
        assert review.rating == valid_review_data["rating"]
        assert review.text == valid_review_data["text"].strip()
        assert review.created_at == valid_review_data["created_at"]

    @pytest.mark.parametrize(
        "field,value,error",
        [
            ("recipe_id", 0, "ID must be positive"),
            ("recipe_id", -1, "ID must be positive"),
            ("user_id", 0, "ID must be positive"),
            ("user_id", -1, "ID must be positive"),
            ("rating", -1, "Rating must be between 0 and 5"),
            ("rating", 6, "Rating must be between 0 and 5"),
            ("text", "", "Review text is required"),
            ("text", "   ", "Review text is required"),
        ],
    )
    def test_create_with_invalid_data_raises_assertion(
        self,
        valid_review_data: dict[str, Any],
        field: str,
        value: Any,
        error: str,
    ):
        data = valid_review_data | {field: value}
        with pytest.raises(AssertionError, match=error):
            Review.create(**data)
