from datetime import datetime
from unittest.mock import Mock

import pytest

from application.dtos.recipe.recipe_dto import FullRecipeDTO
from application.usecases.recipe.get_recipe_by_id_usecase import (
    GetRecipeByIdUseCase,
)
from domain.entities.entity import Id
from domain.entities.recipe.recipe import Recipe
from domain.entities.recipe.value_objects import (
    RecipeContent,
    RecipeDetails,
    RecipeInstruction,
)
from domain.entities.review.review import AuthoredReview, Review
from domain.entities.user.role import RoleEnum
from domain.entities.user.user import User
from domain.entities.user.value_objects import FullName


class TestGetRecipeByIdUseCase:
    @pytest.fixture(autouse=True)
    def setup(
        self,
        mock_recipe_repository: Mock,
        mock_review_repository: Mock,
        mock_user_repository: Mock,
    ) -> None:
        self.mock_recipe_repository = mock_recipe_repository
        self.mock_review_repository = mock_review_repository
        self.mock_user_repository = mock_user_repository
        self.use_case = GetRecipeByIdUseCase(
            recipe_repository=self.mock_recipe_repository,
            review_repository=self.mock_review_repository,
            user_repository=mock_user_repository,
        )

    def setup_recipe_entity(
        self, *, recipe_id: int = 1, author_id: int = 1
    ) -> Recipe:
        recipe = Recipe(
            entity_id=Id(recipe_id),
            content=RecipeContent(title="Title", description="Description"),
            details=RecipeDetails(preparation_time=60, servings=4),
            instruction=RecipeInstruction(
                ingredients="Ingredients", steps="Steps"
            ),
            author_id=Id(author_id),
            images=[],
        )
        self.mock_recipe_repository.get_by_id.return_value = recipe
        return recipe

    def setup_review(self, *, recipe_id: int = 1, user_id: int = 1):
        review = Review(
            entity_id=Id(1),
            recipe_id=Id(recipe_id),
            user_id=Id(user_id),
            rating=4,
            text="Delicious recipe!",
            created_at=datetime(2025, 6, 16, 21, 51),
        )
        user = User(
            entity_id=Id(user_id),
            username="Reviewr",
            full_name=FullName(surname="Doe", name="Jane", patronymic=None),
            password_hash="hash",
            role=RoleEnum.USER.value,
        )
        entity = AuthoredReview(review, user)
        self.mock_review_repository.get_with_author_by_recipe_id.return_value = [
            entity
        ]
        return entity

    def setup_user_entity(
        self, *, user_id: int = 1, username: str = "user"
    ) -> User:
        user = User(
            entity_id=Id(1),
            username=username,
            full_name=FullName(surname="Doe", name="John", patronymic=None),
            password_hash="hash",
            role=RoleEnum.USER.value,
        )
        self.mock_user_repository.get_by_id.return_value = user
        return user

    def test_successful_retrieval(self) -> None:
        author = self.setup_user_entity(user_id=1)
        recipe = self.setup_recipe_entity(author_id=1)
        authored_review = self.setup_review(recipe_id=1)
        review = authored_review.review
        review_author = authored_review.author

        result = self.use_case.execute(recipe_id=1)

        assert isinstance(result, FullRecipeDTO)
        recipe_dto = result.recipe
        author_dto = result.author
        reviews_dto = result.reviews
        summary_dto = result.summary

        # Recipe
        assert recipe_dto.id == recipe.id_safe.value
        assert recipe_dto.title == recipe.content.title
        assert recipe_dto.description == recipe.content.description
        assert recipe_dto.ingredients == recipe.instruction.ingredients
        assert recipe_dto.steps == recipe.instruction.steps
        assert recipe_dto.author_id == recipe.author_id.value

        # Summary
        assert summary_dto.average_rating == float(review.rating)
        assert summary_dto.review_count == 1
        assert len(result.reviews) == 1

        # Author
        assert author_dto.id == author.id_safe.value

        # Reviews
        assert reviews_dto[0].review.rating == float(review.rating)
        assert reviews_dto[0].user.id == review_author.id_safe.value

        self.mock_user_repository.get_by_id.assert_called_once_with(
            author.id_safe.value
        )
        self.mock_recipe_repository.get_by_id.assert_called_once_with(
            recipe.id_safe.value
        )
        self.mock_review_repository.get_with_author_by_recipe_id.assert_called_once_with(
            recipe.id_safe.value
        )

    def test_retrieval_with_no_reviews(self) -> None:
        self.setup_recipe_entity()
        self.mock_review_repository.get_with_author_by_recipe_id.return_value = (
            []
        )
        result = self.use_case.execute(recipe_id=1)

        assert isinstance(result, FullRecipeDTO)

        assert result.summary.average_rating == 0
        assert result.summary.review_count == 0
        assert result.reviews == []
