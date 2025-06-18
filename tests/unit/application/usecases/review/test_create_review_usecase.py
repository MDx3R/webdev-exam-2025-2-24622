from datetime import datetime
from unittest.mock import Mock

import pytest

from application.commands.review.create_review_command import (
    CreateReviewCommand,
)
from application.dtos.user.user_descriptor import UserDescriptor
from application.usecases.review.create_review_usecase import (
    CreateReviewUseCase,
)
from domain.entities.entity import Id
from domain.entities.review.dtos import ReviewData
from domain.entities.review.review import Review
from domain.entities.user.role import RoleEnum


class TestCreateReviewUseCase:
    @pytest.fixture(autouse=True)
    def setup(
        self, mock_review_repository: Mock, mock_review_factory: Mock
    ) -> None:
        self.mock_review_repository = mock_review_repository
        self.mock_review_factory = mock_review_factory
        self.use_case = CreateReviewUseCase(
            review_factory=self.mock_review_factory,
            recipe_repository=Mock(),
            review_repository=self.mock_review_repository,
        )

    def setup_review_entity(
        self, *, review_id: int = 1, user_id: int = 10
    ) -> Review:
        review = Review(
            entity_id=Id(review_id),
            recipe_id=Id(1),
            user_id=Id(user_id),
            rating=4,
            text="Delicious recipe!",
            created_at=datetime(2025, 6, 16, 21, 51),
        )
        self.mock_review_factory.create.return_value = review
        self.mock_review_repository.save.return_value = review
        self.mock_review_repository.exists_for_user_and_recipe.return_value = (
            False
        )
        return review

    def setup_command(self) -> CreateReviewCommand:
        return CreateReviewCommand(
            recipe_id=1,
            user_id=10,
            rating=4,
            text="Delicious recipe!",
        )

    def setup_user(self, user_id: int = 10) -> UserDescriptor:
        return UserDescriptor(
            user_id=user_id, username="john_doe", role=RoleEnum.USER.value
        )

    def test_successful_creation(self) -> None:
        review = self.setup_review_entity(user_id=10)
        command = self.setup_command()
        user = self.setup_user(user_id=10)

        result = self.use_case.execute(command=command, descriptor=user)

        # assert isinstance(result, ReviewDTO) # TODO: ReviewDTO
        # assert result.rating == command.rating
        # assert result.text == command.text
        assert result

        self.mock_review_factory.create.assert_called_once_with(
            ReviewData(
                recipe_id=command.recipe_id,
                user_id=command.user_id,
                rating=command.rating,
                text=command.text,
            )
        )
        self.mock_review_repository.save.assert_called_once_with(review)
        self.mock_review_repository.exists_for_user_and_recipe.assert_called_once_with(
            command.user_id, command.recipe_id
        )

    def test_existing_review_raises_error(self) -> None:
        command = self.setup_command()
        user = self.setup_user()
        self.mock_review_repository.exists_for_user_and_recipe.return_value = (
            True
        )
        with pytest.raises(
            ValueError, match="User has already reviewed this recipe"
        ):
            self.use_case.execute(command=command, descriptor=user)

        self.mock_review_factory.create.assert_not_called()
        self.mock_review_repository.save.assert_not_called()
        self.mock_review_repository.exists_for_user_and_recipe.assert_called_once_with(
            command.user_id, command.recipe_id
        )

    def test_unauthorized_role_raises_error(self) -> None:
        command = self.setup_command()
        user = UserDescriptor(
            user_id=10, username="john_doe", role="Non-existent Role"  # type: ignore
        )
        with pytest.raises(
            PermissionError, match="User cannot create reviews"
        ):
            self.use_case.execute(command=command, descriptor=user)

        self.mock_review_factory.create.assert_not_called()
        self.mock_review_repository.save.assert_not_called()
        self.mock_review_repository.exists_for_user_and_recipe.assert_not_called()
