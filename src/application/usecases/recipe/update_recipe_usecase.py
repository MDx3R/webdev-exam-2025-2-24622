from application.commands.recipe.update_recipe_command import (
    UpdateRecipeCommand,
)
from application.dtos.recipe.recipe_dto import RecipeDTO
from application.dtos.user.user_descriptor import UserDescriptor
from application.interfaces.usecases.recipe.update_recipe_usecase import (
    IUpdateRecipeUseCase,
)
from application.transactions.transactional import transactional
from domain.entities.recipe.value_objects import (
    RecipeContent,
    RecipeDetails,
    RecipeInstruction,
)
from domain.repositories.recipe_repository import IRecipeRepository


class UpdateRecipeUseCase(IUpdateRecipeUseCase):
    def __init__(
        self,
        recipe_repository: IRecipeRepository,
    ):
        self.recipe_repository = recipe_repository

    @transactional
    def execute(
        self, command: UpdateRecipeCommand, descriptor: UserDescriptor
    ) -> RecipeDTO:
        recipe = self.recipe_repository.get_by_id(command.recipe_id)
        recipe.ensure_can_mutate(descriptor.user_id, descriptor.role)

        recipe.update(
            RecipeContent.create(command.title, command.description),
            RecipeDetails(command.preparation_time, command.servings),
            RecipeInstruction(command.ingredients, command.steps),
        )

        recipe = self.recipe_repository.save(recipe)
        return RecipeDTO.from_domain(recipe)
