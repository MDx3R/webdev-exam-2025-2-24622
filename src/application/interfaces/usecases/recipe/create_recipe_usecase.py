from abc import ABC, abstractmethod

from application.commands.recipe.create_recipe_command import (
    CreateRecipeCommand,
)
from application.dtos.recipe.recipe_dto import RecipeDTO
from application.dtos.user.user_descriptor import UserDescriptor


class ICreateRecipeUseCase(ABC):
    @abstractmethod
    def execute(
        self, command: CreateRecipeCommand, descriptor: UserDescriptor
    ) -> RecipeDTO: ...
