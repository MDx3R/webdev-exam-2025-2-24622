from application.dtos.recipe.recipe_dto import (
    FullRecipeDTO,
    RecipeDTO,
    RecipeSummaryDTO,
)
from application.dtos.review.review_dto import (
    AuthoredReviewDTO,
)
from application.dtos.user.user_dto import UserDTO
from application.interfaces.usecases.recipe.get_recipe_by_id_usecase import (
    IGetRecipeByIdUseCase,
)
from domain.repositories.recipe_repository import IRecipeRepository
from domain.repositories.review_repository import IReviewRepository
from domain.repositories.user_repository import IUserRepository


class GetRecipeByIdUseCase(IGetRecipeByIdUseCase):
    def __init__(
        self,
        recipe_repository: IRecipeRepository,
        review_repository: IReviewRepository,
        user_repository: IUserRepository,
    ):
        self.recipe_repository = recipe_repository
        self.review_repository = review_repository
        self.user_repository = user_repository

    def execute(self, recipe_id: int) -> FullRecipeDTO:
        recipe = self.recipe_repository.get_by_id(recipe_id)
        author = self.user_repository.get_by_id(recipe.author_id.value)
        reviews = self.review_repository.get_with_author_by_recipe_id(
            recipe_id
        )
        print(reviews)
        avg_rating = (
            (sum(i.review.rating for i in reviews) / len(reviews))
            if reviews
            else 0
        )

        return FullRecipeDTO.create(
            RecipeDTO.from_domain(recipe),
            UserDTO.from_domain(author),
            reviews=[
                AuthoredReviewDTO.from_domain(r.review, r.author)
                for r in reviews
            ],
            summary=RecipeSummaryDTO.from_domain(
                recipe, avg_rating, len(reviews)
            ),
        )
