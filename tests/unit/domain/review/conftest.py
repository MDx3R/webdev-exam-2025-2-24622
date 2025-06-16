from datetime import datetime
from typing import Any

import pytest

from domain.clock import Clock, FixedClock
from domain.entities.review.dtos import ReviewData
from domain.entities.review.factories import ReviewFactory


@pytest.fixture
def mock_clock() -> Clock:
    mock = FixedClock(datetime(2025, 6, 16, 0, 0))
    return mock


@pytest.fixture
def valid_review_data() -> dict[str, Any]:
    return {
        "recipe_id": 1,
        "user_id": 10,
        "rating": 4,
        "text": "Delicious recipe!",
    }


@pytest.fixture
def valid_review_data_dto(valid_review_data: dict[str, Any]) -> ReviewData:
    return ReviewData(**valid_review_data)


@pytest.fixture
def review_factory(mock_clock: Clock) -> ReviewFactory:
    return ReviewFactory(clock=mock_clock)
