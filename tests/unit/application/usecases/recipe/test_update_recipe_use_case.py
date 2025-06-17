from unittest.mock import Mock
from xml.dom import NotFoundErr

import pytest

from application.commands.recipe.update_recipe_command import (
    UpdateRecipeCommand,
)
from application.dtos.recipe.recipe_dto import RecipeDTO
from application.dtos.user.user_descriptor import UserDescriptor
from application.usecases.recipe.update_recipe_usecase import (
    UpdateRecipeUseCase,
)
from domain.entities.entity import Id
from domain.entities.recipe.recipe import Recipe
from domain.entities.recipe.value_objects import (
    RecipeContent,
    RecipeDetails,
    RecipeInstruction,
)
from domain.entities.user.role import RoleEnum


class TestUpdateRecipeUseCase:
    @pytest.fixture(autouse=True)
    def setup(self, mock_recipe_repository: Mock):
        self.mock_recipe_repository = mock_recipe_repository
        self.use_case = UpdateRecipeUseCase(
            recipe_repository=self.mock_recipe_repository,
        )

    def setup_recipe_entity(
        self, *, recipe_id: int = 1, author_id: int = 1
    ) -> Recipe:
        recipe = Recipe(
            entity_id=Id(recipe_id),
            content=RecipeContent(
                title="Original title", description="Original description"
            ),
            details=RecipeDetails(preparation_time=60, servings=4),
            instruction=RecipeInstruction(
                ingredients="Original ingredients", steps="Original steps"
            ),
            author_id=Id(author_id),
            images=[],
        )
        self.setup_recipe_repository(recipe)
        return recipe

    def setup_recipe_repository(self, recipe: Recipe | None = None):
        if recipe:
            self.mock_recipe_repository.get_by_id.return_value = recipe
        else:
            self.mock_recipe_repository.get_by_id.side_effect = NotFoundErr

    def setup_command(self, recipe: Recipe | None) -> UpdateRecipeCommand:
        command = UpdateRecipeCommand(
            recipe_id=recipe.id_safe.value if recipe else 999,
            title="Updated title",
            description="Updated description",
            preparation_time=45,
            servings=3,
            ingredients="Updated ingredients",
            steps="Updated steps",
        )
        if recipe:
            self.mock_recipe_repository.save.return_value = Recipe(
                entity_id=Id(command.recipe_id),
                content=RecipeContent(
                    title=command.title, description=command.description
                ),
                details=RecipeDetails(
                    preparation_time=command.preparation_time,
                    servings=command.servings,
                ),
                instruction=RecipeInstruction(
                    ingredients=command.ingredients, steps=command.steps
                ),
                author_id=recipe.author_id,
                images=recipe.images,
            )
        return command

    def setup_user(self, user_id: int = 1) -> UserDescriptor:
        return UserDescriptor(
            user_id=user_id, username="User", role=RoleEnum.USER.value
        )

    def test_successful_update(self):
        recipe = self.setup_recipe_entity(author_id=1)
        command = self.setup_command(recipe)
        user = self.setup_user(user_id=1)

        result = self.use_case.execute(command=command, descriptor=user)

        assert isinstance(result, RecipeDTO)
        assert result.title == command.title
        assert result.description == command.description
        assert result.ingredients == command.ingredients
        assert result.steps == command.steps
        assert result.author_id == user.user_id

        self.mock_recipe_repository.get_by_id.assert_called_once_with(
            command.recipe_id
        )
        self.mock_recipe_repository.save.assert_called_once_with(recipe)

    def test_update_for_non_existent_recipe_raises_error(self):
        self.setup_recipe_repository(None)
        command = self.setup_command(None)
        user = self.setup_user(user_id=1)

        with pytest.raises(NotFoundErr):
            self.use_case.execute(command=command, descriptor=user)

        self.mock_recipe_repository.get_by_id.assert_called_once_with(
            command.recipe_id
        )
        self.mock_recipe_repository.save.assert_not_called()

    def test_update_by_another_user_raises_error(self):
        recipe = self.setup_recipe_entity(author_id=1)
        command = self.setup_command(recipe)
        user = self.setup_user(user_id=999)

        with pytest.raises(PermissionError):
            self.use_case.execute(command=command, descriptor=user)
