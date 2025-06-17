from application.dtos.user.user_descriptor import UserDescriptor
from application.interfaces.usecases.recipe.delete_recipe_usecase import (
    IDeleteRecipeUseCase,
)
from application.transactions.transactional import transactional
from domain.repositories.recipe_repository import IRecipeRepository


class DeleteRecipeUseCase(IDeleteRecipeUseCase):
    def __init__(
        self,
        recipe_repository: IRecipeRepository,
    ):
        self.recipe_repository = recipe_repository

    @transactional
    def execute(self, recipe_id: int, descriptor: UserDescriptor) -> None:
        recipe = self.recipe_repository.get_by_id(recipe_id)
        recipe.ensure_can_mutate(descriptor.user_id, descriptor.role)
        self.recipe_repository.remove(recipe)
