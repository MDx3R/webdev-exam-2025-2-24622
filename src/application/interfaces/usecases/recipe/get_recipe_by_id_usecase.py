from abc import ABC, abstractmethod

from application.dtos.recipe.recipe_dto import RecipeDTO


class IGetRecipeByIdUseCase(ABC):
    @abstractmethod
    def execute(self, recipe_id: int) -> RecipeDTO: ...
