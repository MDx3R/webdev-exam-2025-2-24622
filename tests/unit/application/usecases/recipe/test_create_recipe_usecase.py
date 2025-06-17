from io import BytesIO
from typing import Any
from unittest.mock import Mock
from uuid import uuid4

import pytest

from application.commands.recipe.create_recipe_command import (
    CreateRecipeCommand,
)
from application.commands.recipe.upload_image_command import UploadImageCommand
from application.dtos.recipe.recipe_dto import RecipeDTO
from application.dtos.user.user_descriptor import UserDescriptor
from application.usecases.recipe.create_recipe_usecase import (
    CreateRecipeUseCase,
)
from domain.entities.entity import Id
from domain.entities.recipe.dtos import RecipeData
from domain.entities.recipe.image import RecipeImage
from domain.entities.recipe.recipe import Recipe
from domain.entities.recipe.value_objects import (
    RecipeContent,
    RecipeDetails,
    RecipeInstruction,
)
from domain.entities.user.role import RoleEnum


class TestCreateRecipeUseCase:
    @pytest.fixture(autouse=True)
    def setup(
        self,
        mock_recipe_repository: Mock,
        mock_recipe_factory: Mock,
        mock_recipe_image_factory: Mock,
    ) -> None:
        self.mock_recipe_repository = mock_recipe_repository
        self.mock_recipe_factory = mock_recipe_factory
        self.mock_recipe_image_factory = mock_recipe_image_factory
        self.use_case = CreateRecipeUseCase(
            recipe_factory=self.mock_recipe_factory,
            image_factory=mock_recipe_image_factory,
            recipe_repository=self.mock_recipe_repository,
        )
        self.image = UploadImageCommand(
            mime_type="image/jpeg", content=BytesIO()
        )

    def setup_recipe_entity(
        self,
        *,
        recipe_id: int = 1,
        author_id: int = 1,
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
        self.mock_recipe_factory.create.return_value = recipe
        self.mock_recipe_repository.save.return_value = recipe
        return recipe

    def setup_command(
        self, recipe: Recipe, add_images: bool = False
    ) -> CreateRecipeCommand:
        data: dict[str, Any] = {
            "title": recipe.content.title,
            "description": recipe.content.description,
            "preparation_time": recipe.details.preparation_time,
            "servings": recipe.details.servings,
            "ingredients": recipe.instruction.ingredients,
            "steps": recipe.instruction.steps,
            "images": (
                [UploadImageCommand(mime_type="image/jpeg", content=BytesIO())]
                if add_images
                else []
            ),
        }
        command = CreateRecipeCommand(**data)
        if add_images:
            self.mock_recipe_image_factory.create.return_value = RecipeImage(
                entity_id=Id(999),
                filename=str(uuid4()),
                mime_type="image/jpeg",
                recipe_id=recipe.id_safe,
            )
        return command

    def setup_user(self, user_id: int = 1) -> UserDescriptor:
        return UserDescriptor(
            user_id=user_id, username="john_doe", role=RoleEnum.USER.value
        )

    def test_successful_creation(self) -> None:
        recipe = self.setup_recipe_entity()
        command = self.setup_command(recipe)
        user = self.setup_user()

        result = self.use_case.execute(command=command, descriptor=user)

        assert isinstance(result, RecipeDTO)
        assert result.title == command.title
        assert result.description == command.description
        assert result.ingredients == command.ingredients
        assert result.steps == command.steps
        assert result.author_id == user.user_id

        self.mock_recipe_factory.create.assert_called_once_with(
            RecipeData(
                title=command.title,
                description=command.description,
                preparation_time=command.preparation_time,
                servings=command.servings,
                ingredients=command.ingredients,
                steps=command.steps,
                author_id=user.user_id,
            )
        )
        self.mock_recipe_repository.save.assert_called_once_with(recipe)

    def test_successful_creation_with_images(self) -> None:
        recipe = self.setup_recipe_entity(recipe_id=1)
        command = self.setup_command(recipe, add_images=True)
        user = self.setup_user()

        result = self.use_case.execute(command=command, descriptor=user)

        assert isinstance(result, RecipeDTO)
        assert len(result.images) == 1

        self.mock_recipe_factory.create.assert_called_once_with(
            RecipeData(
                title=command.title,
                description=command.description,
                preparation_time=command.preparation_time,
                servings=command.servings,
                ingredients=command.ingredients,
                steps=command.steps,
                author_id=user.user_id,
            )
        )
        assert (
            self.mock_recipe_repository.save.call_count == 2  # noqa: PLR2004
        )
