from dataclasses import replace
from typing import Any

import pytest

from domain.entities.entity import Id
from domain.entities.recipe.image import RecipeImage
from domain.entities.recipe.recipe import Recipe
from domain.entities.recipe.value_objects import (
    RecipeContent,
    RecipeDetails,
    RecipeInstruction,
)


@pytest.fixture
def valid_recipe_content_data() -> dict[str, str]:
    return {
        "title": "Borscht",
        "description": "Classic beet soup.",
    }


@pytest.fixture
def valid_recipe_instruction_data() -> dict[str, str]:
    return {
        "ingredients": "Beetroot, potato, carrot, onion, beef",
        "steps": "1. Prep\n2. Cook\n3. Serve",
    }


@pytest.fixture
def valid_recipe_details_data() -> dict[str, int]:
    return {
        "preparation_time": 60,
        "servings": 4,
    }


@pytest.fixture
def valid_recipe_data(
    valid_recipe_content_data: dict[str, str],
    valid_recipe_instruction_data: dict[str, str],
    valid_recipe_details_data: dict[str, int],
) -> dict[str, Any]:
    return {
        "content": RecipeContent.create(**valid_recipe_content_data),
        "instruction": RecipeInstruction.create(
            **valid_recipe_instruction_data
        ),
        "details": RecipeDetails.create(**valid_recipe_details_data),
        "author_id": 10,
        "images": [],
    }


@pytest.fixture
def valid_recipe(valid_recipe_data: dict[str, Any]) -> Recipe:
    return Recipe.create(**valid_recipe_data)


class TestRecipeContent:
    def test_create_with_valid_data_sets_correct_attributes(
        self, valid_recipe_content_data: dict[str, str]
    ):
        content = RecipeContent.create(**valid_recipe_content_data)
        assert content.title == valid_recipe_content_data["title"].strip()
        assert (
            content.description
            == valid_recipe_content_data["description"].strip()
        )

    @pytest.mark.parametrize(
        "field,value,error",
        [
            ("title", "", "Title is required."),
            ("title", "   ", "Title is required."),
            ("description", "", "Description is required."),
            ("description", "   ", "Description is required."),
        ],
    )
    def test_create_with_invalid_data_raises_assertion(
        self,
        valid_recipe_content_data: dict[str, str],
        field: str,
        value: str,
        error: str,
    ):
        data = valid_recipe_content_data | {field: value}
        with pytest.raises(AssertionError, match=error):
            RecipeContent.create(**data)


class TestRecipeInstruction:
    def test_create_with_valid_data_sets_correct_attributes(
        self, valid_recipe_instruction_data: dict[str, str]
    ):
        instruction = RecipeInstruction.create(**valid_recipe_instruction_data)
        assert (
            instruction.ingredients
            == valid_recipe_instruction_data["ingredients"].strip()
        )
        assert (
            instruction.steps == valid_recipe_instruction_data["steps"].strip()
        )

    @pytest.mark.parametrize(
        "field,value,error",
        [
            ("ingredients", "", "Ingredients are required."),
            ("ingredients", "   ", "Ingredients are required."),
            ("steps", "", "Steps are required."),
            ("steps", "   ", "Steps are required."),
        ],
    )
    def test_create_with_invalid_data_raises_assertion(
        self,
        valid_recipe_instruction_data: dict[str, str],
        field: str,
        value: str,
        error: str,
    ):
        data = valid_recipe_instruction_data | {field: value}
        with pytest.raises(AssertionError, match=error):
            RecipeInstruction.create(**data)


class TestRecipeDetails:
    def test_create_with_valid_data_sets_correct_attributes(
        self, valid_recipe_details_data: dict[str, int]
    ):
        details = RecipeDetails.create(**valid_recipe_details_data)
        assert (
            details.preparation_time
            == valid_recipe_details_data["preparation_time"]
        )
        assert details.servings == valid_recipe_details_data["servings"]

    @pytest.mark.parametrize(
        "field,value,error",
        [
            ("preparation_time", 0, "Preparation time must be positive."),
            ("preparation_time", -1, "Preparation time must be positive."),
            ("servings", 0, "Servings must be positive."),
            ("servings", -1, "Servings must be positive."),
        ],
    )
    def test_create_with_invalid_data_raises_assertion(
        self,
        valid_recipe_details_data: dict[str, int],
        field: str,
        value: int,
        error: str,
    ):
        data = valid_recipe_details_data | {field: value}
        with pytest.raises(AssertionError, match=error):
            RecipeDetails.create(**data)


class TestRecipe:
    @pytest.fixture(autouse=True)
    def setup(self, valid_recipe: Recipe):
        self.recipe = valid_recipe

    def test_create_with_valid_data_sets_correct_attributes(
        self, valid_recipe_data: dict[str, Any]
    ):
        recipe = Recipe.create(**valid_recipe_data)
        assert recipe.recipe_id is None
        assert recipe.content == valid_recipe_data["content"]
        assert recipe.details == valid_recipe_data["details"]
        assert recipe.instruction == valid_recipe_data["instruction"]
        assert recipe.author_id.value == valid_recipe_data["author_id"]
        assert recipe.images == valid_recipe_data["images"]

    def test_create_with_author_id_none_raises_assertion(
        self, valid_recipe_data: dict[str, Any]
    ):
        data = valid_recipe_data | {"author_id": None}
        with pytest.raises(AssertionError, match="Author ID is required."):
            Recipe(entity_id=None, **data)

    def test_add_image_appends_correctly(self):
        image = RecipeImage.create(
            filename="img.jpg",
            mime_type="image/jpeg",
            recipe_id=1,
        )
        self.recipe.add_image(image)
        assert self.recipe.images == [image]

    def test_add_multiple_images_appends_in_order(self):
        image1 = RecipeImage.create(
            filename="img1.jpg",
            mime_type="image/jpeg",
            recipe_id=1,
        )
        image2 = RecipeImage.create(
            filename="img2.jpg",
            mime_type="image/jpeg",
            recipe_id=1,
        )
        self.recipe.add_image(image1)
        self.recipe.add_image(image2)
        assert self.recipe.images == [image1, image2]

    def test_remove_image_by_id_removes_correctly(self):
        image1 = RecipeImage(
            entity_id=Id(1),
            filename="img1.jpg",
            mime_type="image/jpeg",
            recipe_id=Id(1),
        )
        image2 = RecipeImage(
            entity_id=Id(2),
            filename="img2.jpg",
            mime_type="image/jpeg",
            recipe_id=Id(1),
        )
        self.recipe = replace(self.recipe, images=[image1, image2])
        self.recipe.remove_image(image1.id_safe.value)
        assert self.recipe.images == [image2]

    def test_remove_nonexistent_image_does_nothing(self):
        image = RecipeImage.create(
            filename="img.jpg",
            mime_type="image/jpeg",
            recipe_id=1,
        )
        self.recipe = replace(self.recipe, images=[image])
        assert self.recipe.images
        self.recipe.remove_image(999)  # Non-existent ID
        assert self.recipe.images == [image]
