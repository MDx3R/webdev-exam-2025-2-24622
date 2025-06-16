from dataclasses import replace
from typing import Any
from unittest.mock import Mock

import pytest

from domain.entities.recipe.dtos import RecipeData, RecipeImageData
from domain.entities.recipe.factories import RecipeFactory, RecipeImageFactory
from domain.entities.recipe.image import RecipeImage
from domain.entities.recipe.recipe import Recipe


class TestRecipeImageFactory:
    @pytest.fixture(autouse=True)
    def setup(
        self,
        recipe_image_factory: RecipeImageFactory,
        valid_recipe_image_data_dto: RecipeImageData,
    ):
        self.image_factory = recipe_image_factory
        self.valid_image_data = valid_recipe_image_data_dto

    def test_create_with_valid_data_sets_correct_attributes(self):
        image = self.image_factory.create(self.valid_image_data)
        assert isinstance(image, RecipeImage)
        assert image.image_id is None
        assert image.filename == self.valid_image_data.filename
        assert image.mime_type == self.valid_image_data.mime_type
        assert image.recipe_id.value == self.valid_image_data.recipe_id

    @pytest.mark.parametrize(
        "field,value,error",
        [
            ("filename", "", "Filename is required"),
            ("filename", "   ", "Filename is required"),
            ("mime_type", "", "MIME type is required"),
            ("mime_type", "   ", "MIME type is required"),
            (
                "mime_type",
                "text/plain",
                r"Invalid MIME type. Valid values: \{.*?\}",
            ),
            ("recipe_id", 0, "ID must be positive"),
            ("recipe_id", -1, "ID must be positive"),
        ],
    )
    def test_create_with_invalid_data_raises_assertion(
        self,
        valid_recipe_image_data: dict[str, Any],
        field: str,
        value: Any,
        error: str,
    ):
        data = valid_recipe_image_data | {field: value}
        with pytest.raises(AssertionError, match=error):
            self.image_factory.create(RecipeImageData(**data))


class TestRecipeFactory:
    @pytest.fixture(autouse=True)
    def setup(
        self,
        recipe_factory: RecipeFactory,
        recipe_image_factory: RecipeImageFactory,
        valid_recipe_data_dto: RecipeData,
        valid_recipe_image_data_dto: RecipeImageData,
    ):
        self.recipe_factory = recipe_factory
        self.image_factory = recipe_image_factory
        self.valid_data = valid_recipe_data_dto
        self.valid_image_data = valid_recipe_image_data_dto

    def test_create_with_valid_data_sets_correct_attributes(self):
        recipe = self.recipe_factory.create(self.valid_data)
        assert isinstance(recipe, Recipe)
        assert recipe.recipe_id is None
        assert recipe.content.title == self.valid_data.title.strip()
        assert (
            recipe.content.description == self.valid_data.description.strip()
        )
        assert (
            recipe.details.preparation_time == self.valid_data.preparation_time
        )
        assert recipe.details.servings == self.valid_data.servings
        assert (
            recipe.instruction.ingredients
            == self.valid_data.ingredients.strip()
        )
        assert recipe.instruction.steps == self.valid_data.steps.strip()
        assert recipe.author_id.value == self.valid_data.author_id
        assert recipe.images == []

    def test_create_with_images_calls_image_factory(self):
        mock_image = RecipeImage.create(
            filename=self.valid_image_data.filename,
            mime_type=self.valid_image_data.mime_type,
            recipe_id=self.valid_image_data.recipe_id,
        )
        self.image_factory.create = Mock(return_value=mock_image)
        data = replace(self.valid_data, images=[self.valid_image_data])
        recipe = self.recipe_factory.create(data)
        self.image_factory.create.assert_called_once_with(
            self.valid_image_data
        )
        assert len(recipe.images) == 1
        assert recipe.images[0].filename == self.valid_image_data.filename

    @pytest.mark.parametrize(
        "field,value,error",
        [
            ("title", "", "Title is required"),
            ("title", "   ", "Title is required"),
            ("description", "", "Description is required"),
            ("description", "   ", "Description is required"),
            ("preparation_time", 0, "Preparation time must be positive"),
            ("preparation_time", -1, "Preparation time must be positive"),
            ("servings", 0, "Servings must be positive"),
            ("servings", -1, "Servings must be positive"),
            ("ingredients", "", "Ingredients are required"),
            ("ingredients", "   ", "Ingredients are required"),
            ("steps", "", "Steps are required"),
            ("steps", "   ", "Steps are required"),
            ("author_id", None, "ID is not set"),
            ("author_id", -1, "ID must be positive"),
        ],
    )
    def test_create_with_invalid_fields_raises_assertion(
        self,
        valid_recipe_data: dict[str, Any],
        field: str,
        value: Any,
        error: str,
    ):
        data = RecipeData(**valid_recipe_data | {field: value})
        with pytest.raises(AssertionError, match=error):
            self.recipe_factory.create(data)
