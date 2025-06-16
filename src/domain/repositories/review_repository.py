from abc import ABC, abstractmethod
from collections.abc import Sequence

from domain.entities.review.review import Review


class ReviewRepository(ABC):
    """
    Interface for Review aggregate repository.
    """

    @abstractmethod
    async def get_by_id(self, review_id: int) -> Review: ...
    @abstractmethod
    async def get_by_recipe_id(self, recipe_id: int) -> Sequence[Review]: ...
    @abstractmethod
    async def save(self, review: Review) -> None: ...
    @abstractmethod
    async def exists_for_user_and_recipe(
        self, user_id: int, recipe_id: int
    ) -> bool: ...
