from datetime import datetime
from typing import Any
from unittest.mock import Mock

import pytest

from domain.clock import Clock
from domain.entities.review.dtos import ReviewData
from domain.entities.review.factories import ReviewFactory
from domain.entities.review.review import Review


class TestReviewFactory:
    @pytest.fixture(autouse=True)
    def setup(
        self,
        review_factory: ReviewFactory,
        valid_review_data_dto: ReviewData,
        mock_clock: Clock,
    ):
        self.factory = review_factory
        self.valid_data = valid_review_data_dto
        self.clock = mock_clock

    def test_create_with_valid_data_sets_correct_attributes(self):
        review = self.factory.create(self.valid_data)
        assert isinstance(review, Review)
        assert review.review_id is None
        assert review.recipe_id.value == self.valid_data.recipe_id
        assert review.user_id.value == self.valid_data.user_id
        assert review.rating == self.valid_data.rating
        assert review.text == self.valid_data.text.strip()
        assert review.created_at == self.clock.now()

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
        data = ReviewData(**valid_review_data | {field: value})
        with pytest.raises(AssertionError, match=error):
            self.factory.create(data)

    def test_create_uses_clock_for_created_at(self):
        self.clock.now = Mock(return_value=datetime(2025, 6, 16, 0, 0))
        review = self.factory.create(self.valid_data)
        self.clock.now.assert_called_once()
        assert review.created_at == datetime(2025, 6, 16, 0, 0)
