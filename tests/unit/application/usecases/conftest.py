from datetime import datetime
from unittest.mock import MagicMock, Mock, create_autospec

import pytest

from application.interfaces.services.password_hash_service import (
    IPasswordHasher,
)
from application.transactions.configuration import CurrentTransactionManager
from application.transactions.transaction_manager import ITransactionManager
from domain.clock import Clock, FixedClock
from domain.entities.recipe.factories import (
    IRecipeFactory,
    IRecipeImageFactory,
)
from domain.repositories.recipe_repository import IRecipeRepository
from domain.repositories.review_repository import IReviewRepository
from domain.repositories.user_repository import IUserRepository


@pytest.fixture
def mock_clock() -> Clock:
    mock = FixedClock(datetime(2025, 6, 16, 0, 0))
    return mock


@pytest.fixture
def mock_review_factory(mock_clock: Clock):
    return create_autospec(IRecipeImageFactory, instance=True)


@pytest.fixture
def mock_recipe_image_factory():
    return create_autospec(IRecipeImageFactory, instance=True)


@pytest.fixture
def mock_recipe_factory():
    return create_autospec(IRecipeFactory, instance=True)


@pytest.fixture
def mock_user_repository():
    return create_autospec(IUserRepository, instance=True)


@pytest.fixture
def mock_recipe_repository():
    return create_autospec(IRecipeRepository, instance=True)


@pytest.fixture
def mock_review_repository():
    return create_autospec(IReviewRepository, instance=True)


@pytest.fixture
def mock_password_hasher():
    return create_autospec(IPasswordHasher, instance=True)


@pytest.fixture(autouse=True)
def mock_transaction_manager():
    mock_manager = Mock(ITransactionManager)
    mock_context = Mock()
    mock_manager.__enter__ = MagicMock(return_value=mock_context)
    mock_manager.__exit__ = MagicMock(return_value=None)

    CurrentTransactionManager.set(mock_manager)
