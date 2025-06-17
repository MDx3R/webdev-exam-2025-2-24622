from unittest.mock import Mock

import pytest

from application.dtos.user.user_descriptor import UserDescriptor
from application.usecases.recipe.delete_recipe_usecase import (
    DeleteRecipeUseCase,
)
from domain.entities.entity import Id
from domain.entities.recipe.recipe import Recipe
from domain.entities.recipe.value_objects import (
    RecipeContent,
    RecipeDetails,
    RecipeInstruction,
)
from domain.entities.user.role import RoleEnum


class TestDeleteRecipeUseCase:
    @pytest.fixture(autouse=True)
    def setup(self, mock_recipe_repository: Mock) -> None:
        self.mock_recipe_repository = mock_recipe_repository
        self.use_case = DeleteRecipeUseCase(
            recipe_repository=self.mock_recipe_repository,
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

    def setup_user(self, user_id: int = 1) -> UserDescriptor:
        return UserDescriptor(
            user_id=user_id, username="john_doe", role=RoleEnum.USER.value
        )

    def test_successful_deletion(self) -> None:
        recipe = self.setup_recipe_entity(author_id=10)
        user = self.setup_user(user_id=10)

        self.use_case.execute(recipe_id=1, descriptor=user)

        self.mock_recipe_repository.get_by_id.assert_called_once_with(1)
        self.mock_recipe_repository.remove.assert_called_once_with(recipe)

    def test_forbidden_deletion_by_another_user(self) -> None:
        self.setup_recipe_entity(author_id=10)
        user = self.setup_user(user_id=999)

        with pytest.raises(PermissionError):
            self.use_case.execute(recipe_id=1, descriptor=user)

        self.mock_recipe_repository.get_by_id.assert_called_once_with(1)
        self.mock_recipe_repository.remove.assert_not_called()
