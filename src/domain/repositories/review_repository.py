from abc import ABC, abstractmethod
from collections.abc import Sequence

from domain.entities.entity import Id
from domain.entities.review.review import Review


class IReviewRepository(ABC):
    """
    Interface for Review aggregate repository.
    """

    @abstractmethod
    def get_by_id(self, review_id: Id) -> Review: ...
    @abstractmethod
    def get_by_recipe_id(self, recipe_id: Id) -> Sequence[Review]: ...
    @abstractmethod
    def save(self, review: Review) -> None: ...
    @abstractmethod
    def exists_for_user_and_recipe(
        self, user_id: Id, recipe_id: Id
    ) -> bool: ...
