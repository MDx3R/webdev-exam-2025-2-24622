from typing import Any

import pytest

from domain.entities.recipe.dtos import RecipeData, RecipeImageData
from domain.entities.recipe.factories import RecipeFactory, RecipeImageFactory


@pytest.fixture
def valid_recipe_image_data() -> dict[str, Any]:
    return {
        "filename": "img.jpg",
        "mime_type": "image/jpeg",
        "recipe_id": 1,
    }


@pytest.fixture
def valid_recipe_data() -> dict[str, Any]:
    return {
        "title": "Borscht",
        "description": "Classic beet soup.",
        "preparation_time": 60,
        "servings": 4,
        "ingredients": "Beetroot, potato, carrot, onion, beef",
        "steps": "1. Prep\n2. Cook\n3. Serve",
        "author_id": 10,
    }


@pytest.fixture
def valid_recipe_image_data_dto(
    valid_recipe_image_data: dict[str, Any],
) -> RecipeImageData:
    return RecipeImageData(**valid_recipe_image_data)


@pytest.fixture
def valid_recipe_data_dto(valid_recipe_data: dict[str, Any]) -> RecipeData:
    return RecipeData(**valid_recipe_data)


@pytest.fixture
def recipe_image_factory() -> RecipeImageFactory:
    return RecipeImageFactory()


@pytest.fixture
def recipe_factory() -> RecipeFactory:
    return RecipeFactory()
