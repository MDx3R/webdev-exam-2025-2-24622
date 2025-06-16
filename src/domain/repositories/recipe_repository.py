from abc import ABC, abstractmethod
from collections.abc import Sequence

from domain.entities.recipe.recipe import Recipe


class IRecipeRepository(ABC):
    """
    Interface for Recipe aggregate repository.
    """

    @abstractmethod
    async def get_by_id(self, recipe_id: int) -> Recipe: ...
    @abstractmethod
    async def get_all(self, page: int, per_page: int) -> Sequence[Recipe]: ...
    @abstractmethod
    async def save(self, recipe: Recipe) -> Recipe: ...
    @abstractmethod
    async def remove(self, recipe: Recipe) -> None: ...
