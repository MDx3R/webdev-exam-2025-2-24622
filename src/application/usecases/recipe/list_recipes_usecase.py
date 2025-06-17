from application.dtos.recipe.recipe_dto import RecipeSummaryDTO
from application.interfaces.usecases.recipe.list_recipes_usecase import (
    IListRecipesUseCase,
)
from domain.constants import MAX_PER_PAGE
from domain.repositories.recipe_repository import IRecipeRepository
from domain.repositories.review_repository import IReviewRepository


class ListRecipesUseCase(IListRecipesUseCase):
    def __init__(
        self,
        recipe_repository: IRecipeRepository,
        review_repository: IReviewRepository,
    ):
        self.recipe_repository = recipe_repository
        self.review_repository = review_repository

    def execute(self, page: int, per_page: int) -> list[RecipeSummaryDTO]:
        if page < 1 or per_page < 1 or per_page > MAX_PER_PAGE:
            raise ValueError("Invalid pagination parameters.")

        recipes = self.recipe_repository.get_all(page=page, per_page=per_page)

        result: list[RecipeSummaryDTO] = []
        for recipe in recipes:
            reviews = self.review_repository.get_by_recipe_id(
                recipe.id_safe.value
            )
            avg_rating = (
                sum(r.rating for r in reviews) / len(reviews) if reviews else 0
            )
            result.append(
                RecipeSummaryDTO.from_domain(recipe, avg_rating, len(reviews))
            )

        return result
