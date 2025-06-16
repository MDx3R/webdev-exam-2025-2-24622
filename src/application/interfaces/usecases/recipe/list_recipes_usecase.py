from abc import ABC, abstractmethod

from application.dtos.recipe.recipe_dto import RecipeSummaryDTO


class IListRecipesUseCase(ABC):
    @abstractmethod
    def execute(self, page: int, per_page: int) -> list[RecipeSummaryDTO]: ...
