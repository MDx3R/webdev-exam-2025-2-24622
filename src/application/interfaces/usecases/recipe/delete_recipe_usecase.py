from abc import ABC, abstractmethod

from application.dtos.user.user_descriptor import UserDescriptor


class IDeleteRecipeUseCase(ABC):
    @abstractmethod
    def execute(self, recipe_id: int, descriptor: UserDescriptor) -> None: ...
