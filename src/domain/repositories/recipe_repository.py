from abc import ABC, abstractmethod
from collections.abc import Sequence

from domain.entities.entity import Id
from domain.entities.recipe.recipe import Recipe


class IRecipeRepository(ABC):
    """
    Interface for Recipe aggregate repository.
    """

    @abstractmethod
    def get_by_id(self, recipe_id: Id) -> Recipe: ...
    @abstractmethod
    def get_all(self, page: int, per_page: int) -> Sequence[Recipe]: ...
    @abstractmethod
    def save(self, recipe: Recipe) -> Recipe: ...
    @abstractmethod
    def remove(self, recipe: Recipe) -> None: ...
