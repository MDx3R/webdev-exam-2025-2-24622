from abc import ABC, abstractmethod

from application.dtos.recipe.recipe_dto import FullRecipeDTO


class IGetRecipeByIdUseCase(ABC):
    @abstractmethod
    def execute(self, recipe_id: int) -> FullRecipeDTO: ...
