from abc import ABC, abstractmethod

from domain.entities.recipe.dtos import RecipeData, RecipeImageData
from domain.entities.recipe.image import RecipeImage
from domain.entities.recipe.recipe import Recipe
from domain.entities.recipe.value_objects import (
    RecipeContent,
    RecipeDetails,
    RecipeInstruction,
)


class IRecipeImageFactory(ABC):
    @abstractmethod
    def create(self, data: RecipeImageData) -> RecipeImage: ...


class RecipeImageFactory(IRecipeImageFactory):
    def create(self, data: RecipeImageData) -> RecipeImage:
        return RecipeImage.create(
            data.filename, data.mime_type, data.recipe_id
        )


class IRecipeFactory(ABC):
    @abstractmethod
    def create(self, data: RecipeData) -> Recipe: ...


class RecipeFactory(IRecipeFactory):
    def create(self, data: RecipeData) -> Recipe:
        content = RecipeContent.create(
            title=data.title, description=data.description
        )
        details = RecipeDetails.create(
            preparation_time=data.preparation_time, servings=data.servings
        )
        instruction = RecipeInstruction(
            ingredients=data.ingredients, steps=data.steps
        )

        return Recipe.create(
            content=content,
            details=details,
            instruction=instruction,
            author_id=data.author_id,
            images=[],
        )
