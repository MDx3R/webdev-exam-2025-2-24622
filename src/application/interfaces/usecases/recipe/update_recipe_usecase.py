from abc import ABC, abstractmethod

from application.commands.recipe.update_recipe_command import (
    UpdateRecipeCommand,
)
from application.dtos.user.user_descriptor import UserDescriptor


class IUpdateRecipeUseCase(ABC):
    @abstractmethod
    def execute(
        self, command: UpdateRecipeCommand, descriptor: UserDescriptor
    ) -> None: ...
