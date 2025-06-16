from abc import ABC, abstractmethod
from collections.abc import Sequence

from domain.entities.review.review import Review


class IReviewRepository(ABC):
    """
    Interface for Review aggregate repository.
    """

    @abstractmethod
    def get_by_id(self, review_id: int) -> Review: ...
    @abstractmethod
    def get_by_recipe_id(self, recipe_id: int) -> Sequence[Review]: ...
    @abstractmethod
    def save(self, review: Review) -> None: ...
    @abstractmethod
    def exists_for_user_and_recipe(
        self, user_id: int, recipe_id: int
    ) -> bool: ...
