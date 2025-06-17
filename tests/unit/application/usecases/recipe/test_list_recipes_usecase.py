from datetime import datetime
from unittest.mock import Mock

import pytest

from application.dtos.recipe.recipe_dto import RecipeSummaryDTO
from application.usecases.recipe.list_recipes_usecase import ListRecipesUseCase
from domain.constants import MAX_PER_PAGE
from domain.entities.entity import Id
from domain.entities.recipe.recipe import Recipe
from domain.entities.recipe.value_objects import (
    RecipeContent,
    RecipeDetails,
    RecipeInstruction,
)


class TestListRecipesUseCase:
    @pytest.fixture(autouse=True)
    def setup(
        self, mock_recipe_repository: Mock, mock_review_repository: Mock
    ) -> None:
        self.mock_recipe_repository = mock_recipe_repository
        self.mock_review_repository = mock_review_repository
        self.use_case = ListRecipesUseCase(
            recipe_repository=self.mock_recipe_repository,
            review_repository=self.mock_review_repository,
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
        self.mock_recipe_repository.get_all.return_value = [recipe]
        return recipe

    def setup_review(self, *, user_id: int = 1):
        from domain.entities.review.review import Review

        review = Review(
            entity_id=Id(1),
            recipe_id=Id(1),
            user_id=Id(user_id),
            rating=4,
            text="Delicious recipe!",
            created_at=datetime(2025, 6, 16, 21, 51),
        )
        self.mock_review_repository.get_by_recipe_id.return_value = [review]
        return review

    def test_successful_list(self) -> None:
        self.setup_recipe_entity()
        self.setup_review()
        result = self.use_case.execute(page=1, per_page=10)
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], RecipeSummaryDTO)
        assert result[0].id == 1

        self.mock_recipe_repository.get_all.assert_called_once_with(
            page=1, per_page=10
        )
        self.mock_review_repository.get_by_recipe_id.assert_called_once_with(1)

    @pytest.mark.parametrize(
        "page,per_page",
        [
            (0, 10),
            (-1, 10),
            (1, 0),
            (1, -1),
            (1, MAX_PER_PAGE + 1),
        ],
    )
    def test_invalid_pagination_raises_error(
        self, page: int, per_page: int
    ) -> None:
        with pytest.raises(ValueError, match="Invalid pagination parameters"):
            self.use_case.execute(page=page, per_page=per_page)
        self.mock_recipe_repository.get_all.assert_not_called()
        self.mock_review_repository.get_by_recipe_id.assert_not_called()
